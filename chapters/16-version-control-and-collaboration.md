# Chapter 16 — Version Control and Collaboration

## Principle

Version control is the team's shared memory and time machine: every change recorded with its author, its moment, and — if the team writes them — its reasons. For an agent, version control is also the primary *safety instrument*: work happens in increments that can be inspected, compared, and reversed. A change that cannot be described as a diff cannot be reviewed; a change that cannot be reverted cannot be risked.

## Substance

**The model that matters** (Git, the dominant instance): commits are snapshots in a directed acyclic graph; branches are movable pointers; merging reconciles lines of development; the working tree, the index, and HEAD are three distinct states (most beginner confusion is conflating them). History is a designed artifact: atomic commits (one logical change each) make review, bisection (`git bisect`, Chapter 12), and reversion mechanical; tangled commits make all three archaeology.

**The collaboration protocol:** work on branches; propose changes as reviewable units (pull/merge requests) with a description that states intent, evidence, and risk; review is a verification activity (Chapter 11), not a style tribunal — the reviewer's questions are "is this correct, is this tested, is this the right boundary, can this be reverted"; continuous integration runs the suite on every proposal so "green" is a property of the change, not of someone's machine.

**Hygiene with teeth:** commit messages that say *why* (the what is in the diff); never commit secrets (Chapter 13 — history remembers what working trees forget, and rotation, not deletion, is the remedy); small changes over large ones (review quality collapses with size — a 1,000-line change gets a 1,000-line skim); and protected files discipline — configuration and test infrastructure changes ride in their own commits, visibly, because they alter what "passing" means for everyone.

## Worked example

A regression appears somewhere in 400 commits since the last release. `git bisect` with an automated test performs a binary search over history: ~9 test runs localize the exact introducing commit, whose diff — being atomic — shows the precise mechanism. The same hunt without atomic history is a week of suspicion. Bisectability is not a luxury feature; it is the debugging method's infrastructure, and it is purchased entirely by commit discipline exercised months earlier.

## Failure mode

The mega-commit (a feature, two fixes, and a refactor in one — unreviewable, unrevertable, unbisectable); committing generated artifacts and editor noise until the diff lies about the change; force-pushing shared history (rewriting the team's memory under their feet); and review theater — approvals without reading, which convert the safety instrument into a signature formality.

## Rule

> **Rule.** Every commit is one logical change with a message stating its reason, small enough to be reviewed in full and reverted without collateral. Any change a reviewer cannot fully read is, by definition, too large — split it before asking for review.
