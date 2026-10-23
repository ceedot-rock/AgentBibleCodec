# Chapter 10 — Software Design and Architecture

## Principle

Architecture is the set of decisions that are expensive to change: module boundaries, data ownership, dependency direction, the seams where parts can be replaced. Good architecture is not the absence of structure nor its maximization — it is structure placed exactly where change is expected, bought with complexity paid only there.

## Substance

**Cohesion and coupling** are the twin measures (after Constantine; popularized by *Code Complete*, McConnell): a module should do one thing completely (high cohesion), and modules should know as little about each other as possible (low coupling). Nearly every design smell is one of these failing: the god-object (cohesion collapsed), the shotgun change (coupling so high one fix touches twelve files).

**The durable patterns of structure:** layered architectures (dependencies point one way; the domain doesn't import the database), ports-and-adapters / hexagonal design (the core speaks interfaces; infrastructure implements them — the same instinct as Chapter 8's "invariants belong in storage"), dependency inversion (high-level policy must not depend on low-level detail), and the Gang of Four vocabulary (*Design Patterns*, 1994) for object-level recurring shapes. SOLID is the widely-taught mnemonic for five of these ideas; treat it as a checklist of questions, not commandments.

**Boundaries and APIs.** A system's real architecture is its boundaries: API contracts, data schemas, module interfaces. Design them for the consumer, version them deliberately, and assume every published contract becomes permanent (Hyrum's Law: with enough users, every observable behavior — including bugs — becomes depended upon). Conway's Law completes the picture: systems mirror the communication structure of the organizations that build them, so boundaries between teams become boundaries between components whether planned or not.

**Trade-off literacy.** Architecture is the management of quality attributes that fight each other: consistency vs availability (Chapter 7), coupling vs duplication (a little duplication is cheaper than the wrong abstraction — after Sandi Metz's formulation), generality vs simplicity, build vs buy. The senior skill is naming the trade-off being made *in the decision record*, so the future reader knows what was knowingly spent.

## Worked example

A reporting feature needs user data. Options: (a) query the user service's database directly — fastest to write, couples reporting to the user schema forever, breaks when the user team migrates; ( (b) call the user service's API — a boundary, versioned, slower per call, and the reporting feature survives the migration. The architectural content is not the code (both are a dozen lines) but which future changes each option makes cheap or expensive. Architecture reviews exist to price exactly this.

## Failure mode

Resume-driven design (architectures chosen for novelty), premature abstraction (generalizing from one example — wait for the third occurrence; the rule of three), the distributed monolith (microservice boundaries with monolith coupling — both costs, neither benefit), and architecture astronautics: layers that exist to display structure while the actual data flow sneaks around them.

## Rule

> **Rule.** For every new boundary or abstraction, write down which anticipated change it makes cheaper and what it costs today. If no anticipated change can be named, build the simple thing; the abstraction can be extracted when the second concrete case exists — and not before the third demands it.
