#!/usr/bin/env python3
"""Check the Git index for generated/binary files, large files and secret patterns.

This is a focused hygiene check, not a claim to detect every possible secret.
It reports only paths/rule names, never matched credential text.
"""
import re
import subprocess
import sys

RULES={
    'private-key':rb'-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----',
    'github-token':rb'\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b',
    'aws-access-key':rb'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b',
}

def main():
    paths=subprocess.check_output(['git','ls-files','-z']).decode().split('\0')
    failures=[];count=0;size=0
    for path in filter(None,paths):
        parts=path.split('/')
        if (any(p in ('bin','archive','.ssh','.aws','.codex') for p in parts) or
                ('runs' in parts and parts[-1]!='.gitkeep')):
            failures.append((path,'generated-or-private-path'))
        if '/compat/bits/' in '/'+path:failures.append((path,'generated-system-header'))
        data=subprocess.check_output(['git','show',':'+path]);count+=1;size+=len(data)
        if len(data)>256*1024:failures.append((path,'file-over-256-KiB'))
        if b'\0' in data:failures.append((path,'binary-content'))
        for name,pattern in RULES.items():
            if re.search(pattern,data):failures.append((path,name))
    for path,rule in failures:print(f'REJECT {path}: {rule}',file=sys.stderr)
    if failures:raise SystemExit(1)
    print(f'Index reviewed: {count} text files, {size:,} bytes; no prohibited paths, binaries, bulky files or known credential patterns.')

if __name__=='__main__':main()
