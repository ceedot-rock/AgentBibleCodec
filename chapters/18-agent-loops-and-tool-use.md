# Chapter 18 — Agent Loops and Tool Use

## Principle

An agent is a loop, not a model: perceive through tools, decide, act through tools, observe the result, repeat under a budget until a stopping rule fires (this generalizes Chapter 1's foundations to the working agent). The model supplies decisions; the loop supplies everything that makes decisions *consequential and checkable* — observations, state, tools, budget, termination. When an agent fails, the failure belongs to a named loop component before it belongs to "the model."

## Substance

**The canonical loop is ReAct** (after Yao et al., 2022): reasoning and acting interleaved, each action conditioned on the observations previous actions returned. Refinements build on it: **Reflexion** (after Shinn et al., 2023) adds verbal self-feedback stored across attempts — the agent writes down what it concludes from a failure and carries the note into the next try; **plan-and-execute** separates a planner that decomposes the task from executors that run the steps (cheaper per step, weaker at recovery when the plan meets reality); **tree/search-based** agents (Tree of Thoughts, after Yao et al., 2023) explore multiple candidate paths with explicit evaluation — paying compute for decision quality where decisions are expensive to reverse.

**Tool use is an interface discipline.** Tools are functions with names, typed arguments, and structured results. What makes them usable by a model: small, composable surfaces (a read tool, an edit tool, a run tool — not forty flags on one mega-tool); results that are complete but bounded (truncated with the truncation *announced*); errors returned as structured observations the model can act on, not as crashes that end the run; and idempotency where the world allows it, because agents retry. The agent–computer interface (after SWE-agent, Yang et al., 2024) is measured to matter as much as the model: how files are presented, how edit confirmations read, how output windows are sized — these are agent-quality decisions.

**State** is what the loop remembers outside the model's head: working notes, enumerated target lists, checkpoints (a known-good state to retreat to), and the trace itself — the complete record of calls and observations, which is both the debugging instrument and, in accountable systems (Chapter 24), the audit artifact.

**Budgets are part of the architecture,** not an operational afterthought: call budgets, token budgets, wall-clock budgets — with defined behavior at exhaustion (submit the best verified state; never leave the run's product unextracted). An agent without an exhaustion behavior has a failure mode shaped like a cliff.

## Worked example

A coding agent fixing a failing test, loop by loop: observe (the test failure output, quoted exactly) → hypothesize (three ranked root-cause candidates, written down) → act (read the implicated function, not the whole file) → observe (the code contradicts hypothesis #1) → act (write a failing reproduction; run it; it fails as predicted — the hypothesis now has evidence) → edit → run the target tests → the repro passes, one neighboring test regresses → diagnose (the fix was too broad) → narrow the edit → all green → submit. Every step's observation changed the next decision; nothing was believed without a tool returning it. That trace, read afterward, is the difference between an agent and a text generator with permissions.

## Failure mode

The open-loop failure: long sequences of actions taken from the initial plan without intermediate observation (the agent "executes" a script in its head and discovers reality only at the end). Tool misuse follows: calls with hallucinated names or arguments (a symptom of a surface the model couldn't internalize), retrying a failed call verbatim (the definition of loop-thrash), and silent tool failure — treating an error result as a success observation and building on it.

## Rule

> **Rule.** Every action in an agent run must be preceded by an observation that justifies it and followed by an observation that judges it. A run whose trace contains long action sequences with no intervening observations is operating open-loop, and its outputs are unverified by construction — whatever they look like.
