"""Audit captured committed receipts without importing search or recovery code."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import time


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def stable(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def sha(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def audit(release, destination, extend=None, require_stopped=False):
    config_raw = (release / 'config.json').read_bytes()
    config = json.loads(config_raw)
    run = Path(config['output'])
    captured_at = datetime.now(timezone.utc).isoformat()
    checkpoint_raw = (run / 'checkpoint.json').read_bytes()
    checkpoint = json.loads(checkpoint_raw)
    capture = destination / (config['run_id'] + '-captured-checkpoint.json')
    with capture.open('xb') as stream:
        stream.write(checkpoint_raw)
    terminal = None
    if require_stopped:
        terminal = json.loads((run / 'status.json').read_bytes())
        require(terminal['status'] == 'stopped' and terminal['error'] is None,
                'Final audit requires a clean terminal worker status')
        require((run / 'coverage.jsonl').stat().st_size == checkpoint['journal_offset'],
                'Final journal has an uncommitted suffix requiring separate reconciliation')
    require(sha(Path(config['manifest'])) == config['manifest_sha256'], 'Manifest changed')
    manifest = json.loads(Path(config['manifest']).read_bytes())
    for name, expected in manifest['files'].items():
        require(sha(release / name) == expected, 'Frozen release changed: ' + name)
    for name, expected in manifest.get('external_files', {}).items():
        require(sha(Path(name)) == expected, 'External source changed: ' + name)
    fingerprint = hashlib.sha256(stable(dict(manifest_sha256=config['manifest_sha256'],
                                             config=config))).hexdigest()
    require(checkpoint['identity'] == dict(trial=config['run_id'], source_identity=fingerprint),
            'Checkpoint source/configuration identity mismatch')
    window = checkpoint['window']
    require(window['first'] == config['initial_patch'], 'Starting cursor changed')
    for name in ('lo', 'hi', 'width', 'bits', 'cap'):
        setting = {'lo': 'shell_lo', 'hi': 'shell_hi'}.get(name, name)
        require(window[name] == config[setting], 'Window setting changed: ' + name)
    limit = checkpoint['journal_offset']
    require(type(limit) is int and 0 <= limit <= (run / 'coverage.jsonl').stat().st_size,
            'Invalid committed byte offset')
    cursor = window['first']
    chunks = patches = points = audits = 0
    previous = '0' * 64
    hits = set()
    raw_digest = hashlib.sha256()
    started = last_notice = time.monotonic()
    inherited = None
    with (run / 'coverage.jsonl').open('rb') as stream:
        if extend is not None:
            prior = json.loads(extend.read_bytes())
            prior_raw = Path(prior['captured_checkpoint']).read_bytes()
            prior_checkpoint = json.loads(prior_raw)
            require(prior['status'] == 'passed' and prior['source_identity'] == fingerprint and
                    prior['captured_checkpoint_sha256'] == hashlib.sha256(prior_raw).hexdigest() and
                    prior_checkpoint['identity'] == checkpoint['identity'] and
                    prior_checkpoint['window'] == window and
                    prior['committed_bytes'] == prior_checkpoint['journal_offset'] <= limit,
                    'Prior audited checkpoint cannot extend this committed prefix')
            left = prior_checkpoint['journal_offset']
            while left:
                block = stream.read(min(left, 1024 * 1024))
                require(block, 'Prior committed prefix was truncated')
                raw_digest.update(block)
                left -= len(block)
            require(raw_digest.hexdigest() == prior['committed_raw_sha256'],
                    'Previously audited committed bytes changed')
            chunks = prior_checkpoint['chunks']
            patches = prior_checkpoint['patches']
            points = prior_checkpoint['points']
            cursor = prior_checkpoint['next_patch']
            previous = prior_checkpoint['journal_sha256']
            hits = set(map(tuple, prior_checkpoint['hits']))
            audits = prior['independent_gmp_audited_chunks']
            inherited = dict(report=str(extend), report_sha256=sha(extend),
                             rehashed_unchanged_committed_bytes=stream.tell(),
                             chunks=chunks, patches=patches)
        while stream.tell() < limit:
            raw = stream.readline(limit - stream.tell())
            require(raw.endswith(b'\n'), 'Truncated committed record')
            raw_digest.update(raw)
            row = json.loads(raw)
            digest = row.pop('sha256')
            require(row['sequence'] == chunks + 1 and row['previous_sha256'] == previous,
                    'Broken receipt sequence/hash link')
            require(hashlib.sha256(stable(row)).hexdigest() == digest, 'Receipt digest mismatch')
            item = row['window']
            require(all(item[key] == window[key] for key in window if key not in ('first', 'last')),
                    'Receipt window changed')
            require(item['first'] == cursor and cursor < item['last'] <= window['last'],
                    'Missing, duplicate, stale or reordered patches')
            require(item['last'] - cursor == min(config['chunk_patches'], window['last'] - cursor),
                    'Unexpected chunk length')
            require(row.get('complete') is True, 'Incomplete receipt')
            rows = row['patches']
            require([p[0] for p in rows] == list(range(cursor, item['last'])),
                    'Patch manifest has gaps or duplicates')
            require(all(type(p[0]) is int and type(p[2]) is int and p[2] > 0 and
                        isinstance(p[1], str) and re.fullmatch('[0-9a-f]{64}', p[1])
                        for p in rows), 'Malformed patch manifest')
            if window.get('geometry_policy') == 'adaptive':
                precision = row.get('precision_bits', [])
                require([p[0] for p in precision] == [p[0] for p in rows] and
                        all(len(p) == 2 and type(p[1]) is int and 48 <= p[1] <= window['bits']
                            for p in precision), 'Adaptive precision manifest mismatch')
            require(type(row['points']) is int and row['points'] == sum(p[2] for p in rows),
                    'Manifest point total mismatch')
            batches = row['batches']
            require(sum(b['points'] for b in batches) == row['points'], 'Batch point total mismatch')
            require([p for b in batches for p in b['patch_ids']] == [p[0] for p in rows],
                    'Executed batch manifest mismatch')
            expected_counts = [[p[0], p[2], p[2]] for p in rows]
            require([p for b in batches for p in b['native_counts']] == expected_counts,
                    'Coefficient visits disagree with patch manifests')
            audited = chunks % config['gmp_audit_period'] == 0
            require(row.get('independent_gmp_audited') is audited, 'Independent audit cadence changed')
            for index, batch in enumerate(batches):
                identity = batch['identity']
                require(identity['window'] == item and identity['trial'] == config['run_id'] and
                        identity['batch'] == index and identity['coordinator'] == 0 and
                        batch['backend'] == 'gpu', 'Batch identity changed')
                if audited:
                    reference = json.loads((run / 'independent-audits' /
                                            f'{chunks + 1:08d}-{index}.json').read_bytes())
                    counts = reference['counts']
                    require(reference['box_complete'] is True and
                            [c['id'] for c in counts] == list(range(len(batch['patch_ids']))),
                            'Malformed independent GMP receipt')
                    normalized = sorted([batch['patch_ids'][i], c['expected'], c['visited']]
                                        for i, c in enumerate(counts))
                    require(normalized == batch['native_counts'] and
                            reference['points_visited'] == batch['points'],
                            'Independent GMP coefficient counts differ')
                    native_hits = sorted([batch['patch_ids'][h['task']], h['linear'],
                                          h['a'], h['b'], h['c']] for h in reference['hits'])
                    require(native_hits == batch['native_hit_records'], 'Independent GMP hits differ')
            chunks += 1
            patches += len(rows)
            points += row['points']
            audits += audited
            hits.update(map(tuple, row['hits']))
            cursor, previous = item['last'], digest
            if time.monotonic() - last_notice >= 10:
                print(json.dumps(dict(run=config['run_id'], audited_chunks=chunks,
                                      total_chunks=checkpoint['chunks'])), flush=True)
                last_notice = time.monotonic()
        require(stream.tell() == limit, 'Committed byte prefix mismatch')
    require((chunks, patches, points, cursor, previous, sorted(hits)) ==
            (checkpoint['chunks'], checkpoint['patches'], checkpoint['points'],
             checkpoint['next_patch'], checkpoint['journal_sha256'], checkpoint['hits']),
            'Checkpoint totals disagree with committed receipts')
    require(patches == cursor - window['first'] and checkpoint['completed_bound'] is None,
            'Selected coverage/bound mismatch')
    require((release / 'config.json').read_bytes() == config_raw, 'Configuration changed during audit')
    if require_stopped:
        require((run / 'checkpoint.json').read_bytes() == checkpoint_raw and
                json.loads((run / 'status.json').read_bytes()) == terminal and
                (run / 'coverage.jsonl').stat().st_size == limit,
                'Terminal artifacts changed during final audit')
    result = dict(status='passed', release=str(release), captured_utc=captured_at,
                  read_only=True, captured_checkpoint=str(capture),
                  captured_checkpoint_sha256=hashlib.sha256(checkpoint_raw).hexdigest(),
                  committed_bytes=limit, committed_raw_sha256=raw_digest.hexdigest(),
                  committed_chain_sha256=previous, chunks=chunks, patches=patches,
                  coefficient_points=points, independent_gmp_audited_chunks=audits,
                  selected_interval=[window['first'], cursor], hits=sorted(hits),
                  gaps_within_selected_interval=[], duplicates_within_selected_interval=[],
                  frozen_sources_match=True, source_identity=fingerprint,
                  final_checkpoint=require_stopped, inherited_verified_prefix=inherited,
                  uncommitted_trailing_bytes=((run / 'coverage.jsonl').stat().st_size - limit
                                             if require_stopped else None),
                  bytes_after_captured_prefix=(run / 'coverage.jsonl').stat().st_size - limit,
                  seconds=time.monotonic() - started,
                  limitation=('Verified final committed receipts; coefficients are not recomputed. '
                              'Selected coverage only; no full-box bound.' if require_stopped else
                              'Captured committed receipts; coefficients are not recomputed. '
                              'A live run may have advanced. No final handoff checkpoint or full-box bound.'))
    report_path = destination / (config['run_id'] + '-prefix-audit.json')
    with report_path.open('x') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print(json.dumps(result), flush=True)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--release', required=True, type=Path)
    parser.add_argument('--output-dir', required=True, type=Path)
    parser.add_argument('--extend', type=Path)
    parser.add_argument('--require-stopped', action='store_true')
    arguments = parser.parse_args()
    arguments.output_dir.mkdir(exist_ok=True)
    audit(arguments.release.resolve(), arguments.output_dir.resolve(),
          arguments.extend, arguments.require_stopped)
