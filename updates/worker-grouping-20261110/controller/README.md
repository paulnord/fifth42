# Cabbage controller final-report gate

This is a derived replacement for the archived controller at
`deployment_snapshots/overnight-20261110/cabbage/handoff/source/controller.py`.
The archive is unchanged.

The old controller indexed `sup['worker_exit_code']` as soon as the systemd
service was no longer `active`. That is not evidence that the supervisor has
published its terminal cleanup report. This version waits at most 120 seconds
for the terminal report, preserving the absolute deadline and stop signal.
Missing/null exit code is **pending**, never success. Explicit errors, nonzero
or wrongly typed exit codes, and mismatched frozen configuration identity fail
closed. Completion requires terminal worker/supervisor states, exact integer
exit 0, explicit no-error fields, leases released, and owned-process exit
evidence. It then retains the existing verified-replica and seal checks before
any continuation decision. An explicit supervisor stop trigger also prevents
rollover, including when the cursor happens to equal the endpoint.

Run `python3 -B test_completion.py`. Twenty-one tests cover delayed/missing report,
timeout, stop/deadline, errors, wrong types, wrong identity, cleanup evidence and
existing stop/rotation decisions. These are isolated tests with service actions
stubbed to fail; they are **not** live systemd/NFS restart validation.

Do not run this copied controller from the update directory or overwrite a
live frozen controller. Reconcile Cabbage's actual current code against the
archived base first. Stage the change in a fresh release, update the controller
manifest through its existing freeze workflow, preserve current checkpoint and
claim identity, and test terminal-report delay + graceful stop + replica sealing
on a fresh TEST_ONLY run before any authorized production restart. Do not
extend the fixed deadline or automatically recover unknown exits. For an
already stopped run, use its audited checkpoint/replica as the parent of a fresh
continuation; this fix does not repair data or resume the old journal.
