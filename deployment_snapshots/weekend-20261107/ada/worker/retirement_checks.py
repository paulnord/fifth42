"""Additional evidence required to accept one independently verified, owner-authorized retired service."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

SERVICE = 'fifth-lattice-overnight-20261105.service'
RUN = Path('/home/pnord/fifth-lattice-gpu/overnight-runs/20261105T231850Z-bxr6mn4c')
PUBLISHED = Path('/home/pnord/fifth-lattice-gpu/github-status-checkout/ada_validation/overnight-20261105/status.json')
_journal_identity = None


def require(value, message):
    if not value:
        raise RuntimeError('Retired-service evidence rejected: '+message)


def sha(path):
    result = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024*1024), b''):
            result.update(block)
    return result.hexdigest()


def identity(path):
    stat = path.stat()
    return stat.st_dev, stat.st_ino, stat.st_size, stat.st_mtime_ns, stat.st_ctime_ns


def verify_retirement(service, record_path):
    global _journal_identity
    record = json.loads(Path(record_path).read_text())
    require(service == SERVICE and record.get('service') == SERVICE, 'unexpected service')
    require(record.get('owner_authorized_conditional_proceed') is True and
            record.get('service_retirement_independently_verified') is True, 'conditional owner authorization or independent evidence is missing')
    require(isinstance(record.get('owner_response'), str) and record['owner_response'].strip(),
            'original owner response is missing')
    require(record.get('scope') == 'bounded scratch tests only', 'unexpected scope')
    inspection_path = Path(record['inspection_path'])
    require(sha(inspection_path) == record['inspection_sha256'], 'runtime inspection changed')
    inspection = json.loads(inspection_path.read_text())
    require(inspection.get('status') == 'clear_for_bounded_tests' and
            inspection.get('old_service_retired') is True and
            inspection.get('active_related_services') == [] and
            inspection.get('related_processes') == [] and
            inspection.get('all_inspected_leases_free') is True, 'runtime inspection was not clear')
    audit_path = Path(record['audit_path'])
    require(sha(audit_path) == record['audit_sha256'], 'audit file changed')
    audit = json.loads(audit_path.read_text())
    require(audit.get('status') == 'passed' and audit.get('run') == str(RUN), 'audit did not pass')
    age = (datetime.now(timezone.utc)-datetime.fromisoformat(audit['updated_utc'])).total_seconds()
    require(0 <= age <= 1800, 'read-only audit must be less than 30 minutes old')
    require(audit.get('uncommitted_trailing_bytes') == 0 and
            audit.get('run_files_unchanged_during_audit') is True and
            audit.get('published_checkpoint_equal') is True and
            audit.get('worker_exit_code') == 0 and audit.get('lattice_source_preserved') is True,
            'completion/preservation evidence is incomplete')
    require(audit.get('search_publisher_process_matches') == [] and
            audit.get('all_inspected_leases_free') is True, 'audit found active work')
    for filename in ('checkpoint.json', 'preservation.json'):
        require(sha(RUN/filename) == audit['files_before'][filename]['sha256'], filename+' changed')
    journal = RUN/'coverage.jsonl'
    now = identity(journal)
    if _journal_identity is None:
        require(sha(journal) == audit['files_before']['coverage.jsonl']['sha256'], 'journal changed')
        require(identity(journal) == now, 'journal changed while checked')
        _journal_identity = now
    require(now == _journal_identity, 'journal identity or timestamps changed')
    checkpoint = json.loads((RUN/'checkpoint.json').read_text())
    require(checkpoint.get('status') == 'stopped' and checkpoint.get('completed_bound') is None and
            checkpoint.get('journal_offset') == now[2] and
            checkpoint.get('journal_sha256') == audit['committed_chain_sha256'],
            'checkpoint is not the verified terminal checkpoint')
    publication = json.loads(PUBLISHED.read_text())
    require(publication.get('phase') == 'stopped' and publication.get('checkpoint') == checkpoint,
            'terminal publication changed')
    publisher_log = RUN.parent.parent/'overnight-publisher.log'
    last = [json.loads(line) for line in publisher_log.read_text().splitlines() if line.startswith('{')][-1]
    require(last == audit['final_publisher_result'] and last.get('status') == 'published' and
            last.get('phase') == 'stopped', 'final publisher record changed')
    for query in ('list-units', 'list-unit-files'):
        command = ['systemctl', '--user', query, '--type=service', '--no-legend']
        if query == 'list-units':
            command.insert(3, '--all')
        result = subprocess.run(command, capture_output=True, text=True, timeout=5, check=True)
        require(not any(line.split()[0].startswith('fifth') for line in result.stdout.splitlines()
                        if line.strip()), 'a fifth service is loaded or installed')
