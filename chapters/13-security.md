# Chapter 13 — Security

## Principle

Security is the property that a system behaves as intended *in the presence of an adversary* — an intelligent opponent who reads the code, chooses inputs maliciously, and profits from the difference between what the author assumed and what the system permits. Correctness reasoning assumes a indifferent universe; security reasoning assumes a hostile one. This changes everything about how code must be written and reviewed.

## Substance

**The foundational habits:** validate and encode at boundaries — injection (SQL, command, template) exists wherever untrusted data is concatenated into a language, and is killed by parameterization/escaping, never by blocklists; authentication (who are you) is not authorization (what may you do) — check both, server-side, on every request; least privilege (each component, token, and account gets the minimum it needs — the blast radius principle); secrets are credentials, not data — never in code, never in logs, never in version control, rotated and scoped; cryptography is used, never invented — vetted libraries, standard constructions, and paranoia about the surrounding protocol, where real-world failures actually live.

**The standard taxonomies** give the field its checklist: the OWASP Top 10 for web applications (broken access control, cryptographic failures, injection, insecure design, misconfiguration, vulnerable components, auth failures, integrity failures, logging failures, SSRF); STRIDE for threat modeling (spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege); CWE for weakness classes. Use them as coverage instruments — a design review that walks STRIDE per component finds what ad-hoc worry misses.

**The deep principles:** defense in depth (no single control is load-bearing); fail closed (on error, deny — the default that matters is the one taken when the check itself crashes); complete mediation (check every access, not every session); the trusted computing base is everything whose compromise breaks the guarantee — keep it small and audited; and attackers think in graphs while defenders think in lists (after John Lambert): the defender patches entries, the attacker chains them.

**Supply chain** is the modern surface: dependencies are code you run with your privileges — pin them, audit them, watch their advisories; the build pipeline is part of the trusted base (reproducible builds, signed artifacts, provenance attestations are the accountability patterns of Chapter 24 applied to software itself).

## Worked example

A search feature builds a query by string concatenation: `"... WHERE name = '" + input + "'"`. Input `' OR '1'='1` returns every row; input with a UNION exfiltrates other tables. The fix is not filtering quotes (attackers encode around filters forever) but *parameterized queries*, which separate code from data structurally — the driver sends the query shape and the values on different channels, so no input can ever become syntax. The generalization: injection is a category, not an instance — SQL, shell commands, HTML (XSS), LDAP, template engines — and in every case the cure is the same shape: never let data cross into code without a structural boundary.

## Failure mode

Security by obscurity (secret URLs, hidden fields — discovered, not protected); client-side enforcement (checks in JavaScript the attacker doesn't run); rolling your own crypto or auth; logs full of credentials; and the philosophical failure — reviewing for bugs but not for abuse cases: "what would I do with this feature if I were hostile?" is a different question from "does this feature work?"

## Rule

> **Rule.** For every input boundary, name the language the data could enter (SQL, shell, HTML, path, query) and the structural mechanism that prevents it from becoming code there. For every privileged action, name the server-side authorization check. A review that finds neither named is a review that did not cover security, whatever else it covered.
