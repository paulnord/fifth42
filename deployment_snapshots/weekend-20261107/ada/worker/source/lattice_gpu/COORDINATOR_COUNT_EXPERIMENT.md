# CPU-local coordinator count prototype

Status: implementation and five focused protocol tests complete. No native-engine
integration or performance trials were run. This is not a validated speed result
and must not be used as production coverage evidence. No ADA, GPU, remote write,
or overnight launcher was touched. Existing source was not edited.

The standalone script retains the requested selected window
[3751385984,3751387008), denominator shell [100000000001,200000000000], width 8,
222 bits, cap 42 and fixed 256-patch commit boundaries. It compares a local 1x4
and 2x2 CPU analog, not ADA 1x16 / 2x8. The broker owns one persistent CPU
engine with one native thread. Both layouts share the same four allowed CPUs;
the two-coordinator layout gives each coordinator and its pool a disjoint pair.
The native process shares the four-CPU allocation rather than getting extra CPUs.

Leaf initialization calls the existing arithmetic initializer without its CPU
argument to preserve dependency pins and parent-lifetime checks, then pins using
the final multiprocessing identity component. Startup checks observe all leaf
workers and demand exactly one per assigned CPU. Requests/replies include trial,
coordinator, full window and batch identity. The broker rejects stale or reordered
requests; coordinators reject stale replies. Each coordinator holds only one
chunk, submits one batch and waits for its response before proceeding. Existing
assembly, packet, task and point guards remain; the 8 MiB prepared-chunk bound
is retained. Independent journals advance only after all batch output is decoded
and verified. The parent combines and checks the complete ordered union.

The opt-in CLI supports counterbalanced repeats with a 120-second global bound,
but repeated trials are **not being run** because the user's objective changed.
Timing fields separate startup, steady work and total elapsed time, plus broker
process CPU time (including transport, packet guards and native RPC handling)
and native RPC wall time. Steady time includes coordinator journal commits and
receipt of completion records. Total time includes process shutdown. No inferred
speedup is reported.

Focused checks:
- Exact same 256-patch chunk boundaries under the 1-way and 2-way split.
- Stale trial/coordinator/window/batch and bool-for-int identity rejection.
- Duplicate and reordered requests and changing batch counts rejected.
- Nested worker affinity uses identity[-1] while invoking original guards.
- Stale replies fail before advancing the client batch index.

## Future integration status

The parent task owns the distinct-region exploration harness and exact-region
union ledger. This unbenchmarked coordinator prototype is only a possible future
backend. Before integration it needs a small native-engine correctness control,
independent review of failure cleanup and affinity observations, and comparison
against original reference certificates/packets. Its current identical-window
CLI does not implement new-region selection or exact region-union accounting.
No distinct-region runner or competing planner is supplied here.
