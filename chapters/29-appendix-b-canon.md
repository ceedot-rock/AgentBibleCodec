# Appendix B — The Canon: Definitive Sources by Domain

No single book contains the craft. This appendix is the map: for each domain, the public works an agent (or its trainer) should treat as ground truth — the texts against which claims in this Bible, and anywhere else, are checked. Listing is by the part of this book they ground.

## Part I — Foundations

- **Computation & computability** — Turing, *On Computable Numbers* (1936); Sipser, *Introduction to the Theory of Computation*; Hopcroft & Ullman, *Introduction to Automata Theory, Languages, and Computation*.
- **Information theory** — Shannon, *A Mathematical Theory of Communication* (1948); Cover & Thomas, *Elements of Information Theory*.
- **Algorithms & complexity** — Cormen, Leiserson, Rivest & Stein, *Introduction to Algorithms* (CLRS); Knuth, *The Art of Computer Programming* (TAOCP); Garey & Johnson, *Computers and Intractability* (NP-completeness).
- **Data structures** — CLRS (above); Knuth, TAOCP vols. 1 & 3; Sedgewick & Wayne, *Algorithms*.
- **Programming languages & paradigms** — Abelson & Sussman, *Structure and Interpretation of Computer Programs* (SICP); Pierce, *Types and Programming Languages*; Friedman & Wand, *Essentials of Programming Languages*.
- **Types & semantics** — Pierce (above); Winskel, *The Formal Semantics of Programming Languages*; Hoare, *An Axiomatic Basis for Computer Programming* (1969).
- **Operating systems** — Tanenbaum & Bos, *Modern Operating Systems*; Arpaci-Dusseau & Arpaci-Dusseau, *Operating Systems: Three Easy Pieces* (OSTEP); Bryant & O'Hallaron, *Computer Systems: A Programmer's Perspective* (CS:APP).
- **Networking & distributed systems** — Tanenbaum & Wetherall, *Computer Networks*; Kleppmann, *Designing Data-Intensive Applications*; Brewer, *CAP Theorem* (2000) and Gilbert & Lynch's proof (2002); Lamport, *Time, Clocks, and the Ordering of Events* (1978).
- **Databases** — Codd, *A Relational Model of Data for Large Shared Data Banks* (1970); Garcia-Molina, Ullman & Widom, *Database Systems: The Complete Book*; Kleppmann (above) for the modern storage landscape.
- **Compilers** — Aho, Lam, Sethi & Ullman, *Compilers: Principles, Techniques, and Tools* (the Dragon Book); Appel, *Modern Compiler Implementation*; Cooper & Torczon, *Engineering a Compiler*.

## Part II — The Craft

- **Design & architecture** — Gamma, Helm, Johnson & Vlissides, *Design Patterns* (1994); Evans, *Domain-Driven Design*; Martin, *Clean Architecture*; McConnell, *Code Complete*; Brooks, *The Mythical Man-Month*.
- **Testing & verification** — Claessen & Hughes, *QuickCheck* (2000) for property-based testing; Zeller, *Why Programs Fail* (also the debugging canon); the fuzzing literature via AFL (Zalewski) and its successors.
- **Debugging** — Zeller (above); Kernighan & Pike, *The Practice of Programming*; Agans, *Debugging: The 9 Indispensable Rules*.
- **Security** — OWASP Top 10 and ASVS; Anderson, *Security Engineering*; Schneier, *Applied Cryptography* (concepts) with Ferguson, Schneier & Kohno, *Cryptography Engineering* (practice); Microsoft's STRIDE threat-modeling literature.
- **Performance** — Amdahl (1967); Hennessy & Patterson, *Computer Architecture: A Quantitative Approach*; Gregg, *Systems Performance*; the `perf`/profiling literature of the relevant platform.
- **Concurrency** — Herlihy & Shavit, *The Art of Multiprocessor Programming*; the Java and C++ memory-model specifications (JLS §17; ISO C++ [atomics]); Go's concurrency writings (Pike, *Go Proverbs*; the Go memory model document).
- **Collaboration & version control** — the Git book (Chacon & Straub, *Pro Git*); Humble & Farley, *Continuous Delivery*.
- **Readability & documentation** — Kernighan & Pike (above); McConnell (above); Google's engineering practices documentation (public) for review culture.

## Part III — The Agentic Layer

- **Agent loops** — Yao et al., *ReAct* (2022); Shinn et al., *Reflexion* (2023); Yao et al., *Tree of Thoughts* (2023).
- **Coding agents & benchmarks** — Jimenez et al., *SWE-bench* (2024); Yang et al., *SWE-agent* (2024); the SWE-bench family of follow-on benchmarks.
- **Context** — Liu et al., *Lost in the Middle* (2023); Anthropic's public engineering writings on context engineering and tool design for agents.
- **Training** — Hu et al., *LoRA* (2021); Zelikman et al., *STaR* (2022); the rejection-sampling/fine-tuning literature descended from them; Micikevicius et al., *Mixed Precision Training* (2018) for the numerics.
- **Accountability** — Schneier & Kelsey, *Secure Audit Logs* (1999); RFC 6962 (Certificate Transparency) for transparency logs; RFC 7519 (JWT) for signed credentials; the capability-security literature (Miller, *Robust Composition*, 2006) for mandates and least authority.

*Currency note.* The foundations canon is stable across decades. The agentic layer is young and moving; its entries are the founding works as of this writing (2026), and a serious reader re-derives the frontier from the current literature rather than trusting any frozen list — including this one.
