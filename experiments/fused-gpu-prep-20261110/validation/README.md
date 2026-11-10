Local validation (no NVIDIA GPU is exposed here):
- CUDA13.2.78 compile/link succeeded for CGBN and cuPQC at TPI8 and16, architecture sm86. Empty compiler logs are retained. TPI4/32 builds were not completed and are not offered by the runner.
-10 malformed-input prelaunch rejection tests per compiled backend/configuration.
-190 exact patch geometry comparisons against archived production reference,53 corrupted/invalid input rejections.
-190 executions of the actual shared CUDA arithmetic algorithm using GMP host numbers checked for4096-bit overflow at every operation; all match.
-12 CPU region/group cases,8patches each, exact geometry/LLL/bounds smoke checks passed. Their timing values are local smoke data, not Cabbage performance.
- Shell syntax and Python byte compilation pass.

No GPU arithmetic correctness or performance has been measured. Local binaries and SDK are not committed. Cabbage must run device correctness gates before timing conclusions.
