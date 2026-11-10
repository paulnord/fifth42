"""Read-only, stdlib audit of captured grouped coverage and GMP evidence."""
from fractions import Fraction
import argparse,hashlib,json,re
from pathlib import Path

def require(ok,message):
    if not ok:raise RuntimeError(message)
def stable(row):return json.dumps(row,sort_keys=True,separators=(',',':')).encode()
def digest(raw):return hashlib.sha256(raw).hexdigest()
def read_json(path):return json.loads(Path(path).read_bytes())

def audit_suffix(run, baseline, checkpoint, mode, audit_period=None):
    """Audit every captured new receipt; never call the mutating recovery API."""
    parent = baseline['checkpoint']
    audit_period = audit_period or baseline['config']['gmp_audit_period']
    append = mode == 'append'
    cursor = parent['next_patch']
    sequence = parent['chunks'] if append else 0
    points = parent['points'] if append else 0
    patches = parent['patches'] if append else 0
    hits = set(map(tuple, parent['hits'])) if append else set()
    previous = parent['journal_sha256'] if append else '0' * 64
    offset = parent['journal_offset'] if append else 0
    chunks = audited = 0
    limit = checkpoint['journal_offset']
    require(type(limit) is int and offset <= limit <= (run/'coverage.jsonl').stat().st_size,
            'Invalid committed journal byte offset')
    with (run/'coverage.jsonl').open('rb') as stream:
        stream.seek(offset)
        while stream.tell() < limit:
            raw = stream.readline(min(limit - stream.tell(), 8 * 1024**2))
            require(raw.endswith(b'\n'), 'Partial or oversized committed receipt')
            row = json.loads(raw)
            row_hash = row.pop('sha256')
            require(digest(stable(row)) == row_hash, 'New receipt hash mismatch')
            require(row['sequence'] == sequence + 1 and row['previous_sha256'] == previous,
                    'New receipt hash chain or sequence mismatch')
            window = row['window']
            require(type(window['first']) is int and type(window['last']) is int and
                    window['first'] == cursor and
                    cursor < window['last'] <= checkpoint['window']['last'],
                    'New receipts contain a gap, duplicate or reordered chunk')
            require(window['last'] - cursor == min(256, checkpoint['window']['last'] - cursor),
                    'Unexpected new chunk length')
            require(all(window[k] == checkpoint['window'][k] for k in
                        ('lo', 'hi', 'width', 'bits', 'cap', 'geometry_policy')),
                    'New receipt geometry changed')
            rows = row['patches']
            require(row.get('coverage_schema')=='logical-width8-physical-groups-v1' and row['group_limit']==baseline['config']['group_limit'],'Grouped schema/policy changed')
            spans=row['logical_spans'];specs=row['physical_specifications']
            require(len(rows)==len(spans)==len(specs)>0,'Missing physical specifications')
            fine=cursor
            count=(9*window['lo']+79)//80
            for p,span,spec in zip(rows,spans,specs):
                first,last=span
                require(type(first) is int and type(last) is int and first==fine and 0<last-first<=row['group_limit'] and last<=window['last'],'Gap or overlap within grouped interval')
                require(p[0]==spec[0]==first and spec[1:3]==[window['lo'],window['hi']] and spec[5]==window['cap'],'Physical specification changed identity or shell')
                require(Fraction(*spec[3])==Fraction(9*first,10*count) and Fraction(*spec[4])==Fraction(9*last,10*count),'Physical edges do not cover original reservation cells')
                require(isinstance(p[1],str) and re.fullmatch('[0-9a-f]{64}',p[1]) and type(p[2]) is int and p[2]>0,'Invalid physical patch manifest')
                fine=last
            require(fine==window['last'],'Grouped interval is incomplete')
            require([p[1] for p in row['precision_bits']]==[spec[6] for spec in specs],'Physical precision differs from specification')
            precision = row['precision_bits']
            require([p[0] for p in precision] == [p[0] for p in rows] and
                    all(len(p) == 2 and type(p[0]) is int and type(p[1]) is int and
                        48 <= p[1] <= window['bits']
                        for p in precision), 'Adaptive precision receipts changed')
            require(row['complete'] is True and type(row['points']) is int and
                    row['points'] == sum(p[2] for p in rows), 'Incomplete new receipt')
            batches = row['batches']
            require([p for b in batches for p in b['patch_ids']] == [p[0] for p in rows] and
                    sum(b['points'] for b in batches) == row['points'],
                    'Executed batch coverage mismatch')
            require([count for b in batches for count in b['native_counts']] ==
                    [[p[0], p[2], p[2]] for p in rows], 'Native visits are incomplete')
            require(all(len(count) == 3 and all(type(value) is int for value in count)
                        for batch in batches for count in batch['native_counts']),
                    'Malformed native count types')
            require(row['independent_gmp_audited'] is (sequence % audit_period == 0),
                    'Independent audit cadence changed')
            for index, batch in enumerate(batches):
                identity = batch['identity']
                require(batch['backend'] == 'gpu' and identity['window'] == window and
                        identity['trial'] == checkpoint['identity']['trial'] and
                        identity['batch'] == index, 'Stale native batch identity')
                if row['independent_gmp_audited']:
                    reference = read_json(run/'independent-audits'/f'{sequence+1:08d}-{index}.json')
                    ids = batch['patch_ids']
                    require(reference['box_complete'] is True and
                            [c['id'] for c in reference['counts']] == list(range(len(ids))),
                            'Malformed independent GMP counts')
                    counts = [[ids[c['id']], c['expected'], c['visited']]
                              for c in reference['counts']]
                    records = sorted([ids[h['task']], h['linear'], h['a'], h['b'], h['c']]
                                     for h in reference['hits'])
                    require(counts == batch['native_counts'] and
                            reference['points_visited'] == batch['points'] and
                            records == batch['native_hit_records'],
                            'Independent GMP/native mismatch')
            sequence += 1
            chunks += 1
            audited += row['independent_gmp_audited']
            patches += window['last']-window['first']
            points += row['points']
            hits.update(map(tuple, row['hits']))
            cursor, previous = window['last'], row_hash
    require((sequence, patches, points, cursor, previous, sorted(hits)) ==
            (checkpoint['chunks'], checkpoint['patches'], checkpoint['points'],
             checkpoint['next_patch'], checkpoint['journal_sha256'], checkpoint['hits']),
            'New committed prefix does not match checkpoint totals')
    require(chunks > 0, 'No new complete receipt was committed')
    return dict(new_chunks=chunks, new_patches=cursor-parent['next_patch'],
                new_gmp_audited_chunks=audited, next_patch=cursor)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--run',type=Path,required=True);parser.add_argument('--config',type=Path,required=True)
    args=parser.parse_args();config=read_json(args.config);cp=read_json(args.run/'checkpoint.json')
    result=audit_suffix(args.run,dict(checkpoint=dict(next_patch=config['initial_patch']),config=config),cp,'fresh',config['gmp_audit_period'])
    result.update(status='passed',checkpoint_sha256=digest((args.run/'checkpoint.json').read_bytes()),committed_bytes=cp['journal_offset'],journal_sha256=cp['journal_sha256'])
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
