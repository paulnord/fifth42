# Verified search coverage

The largest completed box is **[-35,000,000,35,000,000]^3**, with no solutions
to x^5+y^5+z^5=42. All sign combinations are covered using the proved modulo-11
role assignment and ordering a<=b. This does not rule out larger solutions.

| Backend | Inclusive box bound | Completed canonical rows | Exact steps | Solutions |
| --- | ---: | ---: | ---: | ---: |
| CPU | 10,000 | 1,819 | 16,536,529 | 0 |
| CPU | 100,000 | 18,181 | 1,652,834,710 | 0 |
| GPU | 100,000 | 18,181 | 1,652,834,710 | 0 |
| GPU | 1,000,000 | 181,819 | 165,290,016,529 | 0 |
| GPU | 10,000,000 | 1,818,181 | 16,528,919,834,710 | 0 |
| GPU | 35,000,000 | 6,363,637 | 202,479,360,247,934 | 0 |

The last run committed 98 chunks. Its z rows cover -34,999,998 through +34,999,998
in steps of 11; the other two variables span the full configured bound in all
admissible residue classes. Search time was 2,749.48181 seconds and engine wall
time 2,856.43546 seconds. The outer one-hour timeout was not reached.

Every original checkpoint's row continuity, metadata, candidates and fingerprints
were checked. The committed [compact results](results/coverage.json) retain the
source/binary hashes, exact counts and timing, while raw checkpoints, binaries
and local machine identifiers remain untracked. Test-only alternate targets,
CPU emulation and benchmark samples do not confer additional full-box coverage.

The GPU proof of concept was executed on Ada's RTX 3080 Ti with CUDA 12.8 and
g++-13. The restricted agent session could inspect files and compile but could
not access device nodes; GPU execution took place in the user's normal terminal.
No BNL resources were used.
