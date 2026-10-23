# Chapter 24 — Mandates, Receipts, and Accountability Patterns

## Principle

Agents act in the world — they spend, edit, send, and delete — and someone is answerable for those acts. Accountability is an engineering pattern, not a policy document: before the act, a *mandate* bounds what the agent may do; during the act, *receipts* record what it did; after the act, a third party can *verify* the record against the mandate without trusting the agent or its operator. Identity, authorization, and audit — designed before the incident, not reconstructed after it.

## Substance

**Identity.** The agent carries a short-lived, signed credential binding it to a principal and a configuration (model, prompt hash, tool set). Short lifetimes bound the value of theft; signatures make the credential unforgeable by the agent itself; the identity record makes any later artifact attributable: *this* agent, in *this* configuration, did this.

**Mandates.** A mandate is a signed, expiring authorization with explicit bounds — the generalization of capability and spend-limit patterns across computing: allowed tools and action classes; allowed scope (paths, hosts, accounts); numeric caps (calls, tokens, money, wall-clock); expiry. Enforcement is *fail-closed and at the point of action*: a call outside the mandate is denied by the enforcing layer (Chapter 19's Level 2 — a mandate checked by the agent's own goodwill is a wish), and an exhausted or expired mandate denies by default. Mandates compose with least privilege (Chapter 13): the agent that drafts does not hold the send permission; drafting and sending are different grants, and the distance between them is the distance between a suggestion and a commitment.

**Receipts.** Every action appends a receipt to a hash-chained ledger (after Schneier & Kelsey's tamper-evident logging, 1999; the transparency-log family, RFC 6962, is the public-scale relative): each receipt commits to its predecessor's hash and records the action, its arguments hash, its result hash, resources consumed, and its mandate. At completion the final artifact (the patch, the purchase) is *sealed*: a closing record binds the artifact's hash to the ledger head and the mandate — so the artifact provably came from the run the ledger describes.

**What verification proves — and what it does not.** A checker validates: chain integrity (no receipt altered, deleted, or reordered without detection), seal binding (this artifact ↔ this ledger), and mandate compliance (every receipt inside the bounds). State the limits with equal precision: an *unsigned* chain proves internal consistency, not authenticity — an attacker who can rewrite the whole ledger can recompute the whole chain and seal, and no check on the record alone detects it. Authenticity requires a signature the agent cannot forge or an external anchor the attacker cannot rewrite (periodically publishing the ledger head to an independent medium — a public transparency log, a timestamping service, a blockchain — so history-rewriting becomes publicly evident). A second limit: receipts record what the *recording layer* saw; a compromised recorder can lie at the source. Coverage is a property of placement (harness-observed recording beats agent-self-reported recording — Chapter 19 again), and honest systems say which placement they use.

## Worked example

A purchasing agent holds a mandate: vendor allow-list, $500 cap, 20 calls, 1 hour. It buys in 14 calls and $412; each call's receipt chains to the last; the invoice is sealed against the ledger head. An auditor — trusting neither the agent nor its operator — replays the chain, checks the seal, and sums the receipts against the mandate: attribution, conduct, and integrity each answered from the record alone. Now tamper with it: edit one receipt's amount and the chain breaks at the next link; delete a receipt and the sequence gaps; truncate the tail and the seal's head mismatches. Rewrite *everything* consistently and the unsigned chain accepts it — which is exactly why the operator also anchors the head externally each hour: the rewrite would now contradict a public record. Each guarantee is stated with its attacker model; that is what makes it a guarantee rather than a slogan.

## Failure mode

Audit theater: logs the audited party can edit, receipts recorded by the agent itself with no independent observation, mandates enforced by prompt text, seals computed over artifacts that are later modified (a seal binds a hash — hash the final artifact, after final edits, or it binds a draft), and valid-but-wrong-mode credentials (a demo/test credential is cryptographically *valid*; validity checks alone do not exclude it — mode must be checked explicitly, a classic).

## Rule

> **Rule.** Every accountability claim names its placement and its attacker: who records, who can rewrite, what detects rewriting, and what the record cannot prove. A claim that a log "proves" an agent's conduct is falsified by exhibiting one undetectable rewrite the design permits — and every design must either close that rewrite or publish it as its stated limit.
