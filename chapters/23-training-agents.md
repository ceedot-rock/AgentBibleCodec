# Chapter 23 — Training Agents

## Principle

When configuration and prompting reach their measured ceiling, the remaining lever is the weights. Training an agent means teaching behavior from *evidence*: demonstrations and trajectories whose correctness was established by execution. The governing principle is provenance — every training example asserts "this behavior was right," and that assertion must carry the same executed proof demanded of any other claim (Chapter 21).

## Substance

**Supervised fine-tuning (SFT)** trains on (input, desired output) pairs by gradient descent on the model's own loss — teaching format, style, procedure, and, with enough verified substance, capability. **LoRA** (after Hu et al., 2021) makes this cheap: freeze the base weights, train low-rank adapter matrices on selected projections; adapters are small, swappable, and composable (different adapters for different roles — a coder, an analyzer — over one base).

**STaR and rejection sampling** (after Zelikman et al., 2022) solve the demonstrations problem: let the current model attempt tasks, keep only attempts that *verifiably succeed* (the target tests pass under independent execution), fine-tune on those, and iterate — each round's better sampler yields better data. The oracle variant builds trajectories from known-good solutions (e.g., human gold patches) and admits them only when the solution verifies and the trajectory's observations are *real* — replayed against the actual environment at the actual state, so every tool result in the record is genuine output. Synthesized observations (plausible reconstructions of what tools "would have" returned) teach the model a fictional world; the honest gates reject them or label them permanently.

**Dataset hygiene is a border checkpoint:** reject benchmark items and holdout items (by id *and* by content collision — same repo at the same commit), reject records failing the evidence gate, reject over-length records rather than truncating them into nonsense, deduplicate by solution fingerprint, cap per-task counts so one easy task can't dominate. A manifest records exactly what was admitted and why the rest was not; the dataset's claims about itself must be checkable.

**The numerics of training are part of training.** Gradient descent updates weights by amounts on the order of the learning rate (10⁻⁵–10⁻⁴). In float16, the representable spacing near a weight of magnitude ~1 is ~10⁻³ — *larger than the update* — so updates round back to the identical stored value, and the optimizer's second-moment estimates underflow below the subnormal floor. A model trained in pure fp16 at small learning rates can be *incapable of changing*, while its loss curve prints normally and its logs look like a training run. The standard cure is mixed precision done correctly: master weights and optimizer state in fp32, forward/backward compute in bf16/fp16 autocast, gradient checkpointing when memory binds. And the standard *verification*: a one-step census — take one optimizer step and count how many weights actually changed (in fp32, expect ~all; in broken fp16, a small fraction) — run *before* the expensive run, not after the puzzling flat result. Training failures are quiet: leakage inflates every later metric, wrong precision produces a perfect log of a frozen model, and a launcher that reports success for a crashed subprocess will happily confirm all of it. Verify artifacts (weights moved, adapter loads, eval delta exists), never wrappers.

## Worked example

A fine-tune completes 5 epochs; evaluation shows *exactly* chance performance, identical across epochs — the signature not of weak learning but of *no* learning. The differential diagnosis is short: (1) label alignment (are targets permuted? — check end-to-end with one hand-traced example); (2) gradient flow (does every parameter receive gradient? — one backward pass with per-module norms); (3) update survival (one optimizer step, then a census of changed weights in the training precision). Cause (3) convicts silently and is the one nobody checks first, because "the loss printed" feels like training. The census takes minutes and settles it.

## Failure mode

Training on the benchmark; training on unverified or synthesized trajectories while claiming verified data; silent precision pathologies; evaluating the trained model on data adjacent to its training set and calling the gap "capability"; and selecting the final checkpoint by vibes instead of a frozen-bench delta against the untrained control under an identical configuration hash.

## Rule

> **Rule.** A training run is reported only with three artifacts: a dataset manifest proving zero benchmark/holdout contamination and the evidence status of every admitted record; a pre-flight check that the optimizer measurably changes weights in the training precision; and a post-training delta against the untrained control on the frozen bench under identical configuration. Missing any one, the run is *unverified* — whatever its logs say.
