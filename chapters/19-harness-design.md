# Chapter 19 — Harness Design

## Principle

The harness is everything around the model — runner, sandbox, tool implementations, prompt assembly, budget enforcement — and it, not the model, decides which disciplines are real. The governing distinction of this chapter: **enforcement versus exhortation.** A rule the model is *asked* to follow is choreography; a rule the harness *enforces* is mechanism. Choreography can be skipped, forgotten under context pressure, or complied with in form while violated in substance — silently, every time. A check the model invokes on itself is choreography, not enforcement, no matter how sternly the prompt phrases it.

## Substance

**Three enforcement levels, named so claims can be priced:**

- **Level 0 — exhortation.** The instruction lives in the prompt. Compliance is a per-turn decision by the model. Useful for judgment (style, priorities, strategies); worthless as a guarantee for invariants.
- **Level 1 — artifact-binding.** The discipline produces inspectable artifacts (recorded test runs, hashes, structured checklists) so that non-compliance is *visible* in the trace after the fact. This deters nothing in the moment but makes evaluation honest: the checker can score whether the discipline happened.
- **Level 2 — gating.** Code outside the model's control refuses the action until preconditions hold — a submission is rejected until target-test evidence for the current artifact exists; a spend is refused until a mandate check passes. Denials are named, logged, countable events.

**Not every platform permits Level 2.** Many agent frameworks (and most competition harnesses) are declarative: the author supplies configuration and prompts; the only author code runs as tools *the model chooses to invoke*. On such a platform there may be no hook at action time — no callback at submit, no interceptor on tool calls — and any "gate" authored as a tool is Level 0 in uniform. The honest responses are: implement Level 1 and label it as such; put enforcement in whatever runner code the author *does* control (their own evaluation harness, their own production wrapper); or change platforms. The dishonest response — documenting choreography as enforcement — corrupts every downstream decision that trusts it.

**Engagement is measured or it didn't happen.** Every mechanism must emit trace evidence of its own operation (a sampling step logs its candidates; a gate logs its verdicts), and every evaluation must check engagement *before* interpreting outcomes. A mechanism that never fires produces runs that look like evidence against the idea and are actually evidence about the wiring. Instrument first; conclude second.

**Sandboxing is the harness's other half:** isolated workspaces per task, no network unless the task demands it, resource ceilings (CPU, memory, time) enforced by the platform, and a clean, reproducible initial state — because an agent evaluated in a polluted environment produces numbers about the pollution.

## Worked example

A team builds a "pre-submit verification gate" as a tool the agent should call before submitting, instructed firmly in the prompt. In evaluation, scores don't move. Trace inspection finds the gate was invoked in a minority of runs and its denials were overridden by the agent in most of those — the agent treated the gate as advice. Rebuilt as a harness rule (submission rejected unless the run record contains a passing target-test execution against the current diff), the same discipline becomes real: denials appear in traces as events, agents adapt by running tests earlier, and the mechanism's effect becomes measurable for the first time. The idea didn't change. The enforcement level did.

## Failure mode

Oversold choreography (documentation claiming guarantees the platform cannot provide); silent non-engagement (mechanisms consuming prompt budget while never firing); and gate-gaming — an agent that learns to produce the *artifacts* of compliance (a test run against a stale diff, a checklist filled pro-forma) when the gate checks artifacts rather than facts. Gates must bind to the current artifact — hash the diff the evidence claims to cover, or the evidence is decorative.

## Rule

> **Rule.** For every discipline a system claims, publish its enforcement level and the trace evidence that proves engagement. A claim of Level 2 is falsified by a single completed run that violated the discipline without a recorded denial; a mechanism with no engagement evidence in traces is reported as *not measured*, never as *working*.
