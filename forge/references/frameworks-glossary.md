# Frameworks Glossary

Quick reference for every framework, methodology, and standard used across the Forge pipeline. Each entry provides context for why the framework matters and how it's applied.

---

## Problem Statement Canvas (IDEO)

A structured template for defining problems before jumping to solutions. Forces teams to articulate the problem, affected audience, current pain points, and success criteria independently from any proposed solution. In Forge, the `problem-framing` skill uses this canvas to transform raw ideas into analytical documents.

**Source:** IDEO Human-Centered Design Toolkit — https://www.ideo.com/tools

---

## Jobs To Be Done — JTBD (Clayton Christensen)

A demand-side innovation framework that focuses on the "job" a customer hires a product to do. The canonical format is: "When [situation], I want [motivation], so that [outcome]." JTBD shifts focus from demographics to causality — what circumstances push someone to seek a solution. In Forge, every problem statement must include at least one JTBD statement.

**Source:** Christensen, C. M. et al. — *Competing Against Luck* (2016) — https://www.christenseninstitute.org/jobs-to-be-done/

---

## Double Diamond (Design Council UK)

A design process model with four phases arranged as two diamonds: Discover (diverge) → Define (converge) → Develop (diverge) → Deliver (converge). The first diamond ensures you're solving the right problem; the second ensures you're solving it the right way. Forge's Discovery + Product phases mirror the first diamond, while Design + Architecture mirror the second.

**Source:** Design Council UK — https://www.designcouncil.org.uk/our-resources/the-double-diamond/

---

## Shape Up — Appetite + Pitch (Ryan Singer / Basecamp)

A product development methodology that replaces time estimates with "appetite" — the maximum time worth investing in a feature. Work is shaped into pitches with fixed time, variable scope. Rabbit holes (hidden complexity) are identified upfront and eliminated. In Forge, the `scope-shaper` agent applies Shape Up principles to negotiate MVP scope.

**Source:** Singer, R. — *Shape Up: Stop Running in Circles and Ship Work that Matters* (2019) — https://basecamp.com/shapeup

---

## User Story Mapping (Jeff Patton)

A technique for organizing user stories into a two-dimensional map: activities along the horizontal backbone, and story detail levels vertically. The top row represents the big picture; lower rows add detail. A horizontal line cuts the MVP from future releases. In Forge, the `product-definition` skill generates a user story map to visualize scope and release planning.

**Source:** Patton, J. — *User Story Mapping* (2014) — https://www.jpattonassociates.com/user-story-mapping/

---

## MoSCoW Prioritization (Dai Clegg)

A prioritization technique that classifies requirements into four categories: **Must** have (non-negotiable for launch), **Should** have (important but not blocking), **Could** have (nice-to-have), **Won't** have (explicitly out of scope for this release). In Forge, every user story in the PRD receives a MoSCoW classification, and only "Must" stories enter the MVP.

**Source:** Clegg, D. & Barker, R. — *Case Method Fast-Track: A RAD Approach* (1994) — https://www.agilebusiness.org/dsdm-project-framework/moscow-prioririsation.html

---

## Atomic Design (Brad Frost)

A methodology for building design systems from the smallest pieces up: Atoms (inputs, labels) → Molecules (search bar) → Organisms (header) → Templates (page layout) → Pages (instances). In Forge, the `design-system-bootstrap` skill organizes components following Atomic Design levels, ensuring systematic reuse.

**Source:** Frost, B. — *Atomic Design* (2016) — https://atomicdesign.bradfrost.com/

---

## C4 Model (Simon Brown)

A hierarchical approach to software architecture visualization at four levels: **Context** (system + actors + external systems), **Containers** (deployable units), **Components** (modules within a container), **Code** (classes/functions). In Forge, the `architecture-design` skill generates C4 diagrams at levels 1-3 using Mermaid.

**Source:** Brown, S. — *The C4 Model for Visualising Software Architecture* — https://c4model.com/

---

## ADR — Architecture Decision Records (Michael Nygard)

A lightweight format for documenting significant architectural decisions. Each ADR captures: Context (why the decision is needed), Decision (what was decided), Alternatives (what was considered), and Consequences (positive and negative). ADRs are numbered, immutable after approval, and can only be superseded by new ADRs. In Forge, the `adr-writer` skill generates ADRs whenever the `architecture-design` skill makes significant choices.

**Source:** Nygard, M. — "Documenting Architecture Decisions" (2011) — https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions

---

## Google Design Docs (Google Engineering)

A structured template for technical specifications used internally at Google. Includes: Context, Goals/Non-Goals, Design (proposed solution with diagrams), Alternatives Considered, Cross-cutting Concerns (security, privacy, testing). In Forge, the `tech-spec-writer` skill adapts this format for feature-level specifications.

**Source:** Google Engineering Practices — https://google.github.io/eng-practices/

---

## Test Pyramid (Mike Cohn)

A testing strategy that recommends many fast unit tests at the base, fewer integration tests in the middle, and minimal end-to-end tests at the top. The pyramid shape ensures fast feedback loops and cost-effective test suites. In Forge, the `test-strategy` skill uses the pyramid to allocate testing effort across layers.

**Source:** Cohn, M. — *Succeeding with Agile* (2009) — https://www.mountaingoatsoftware.com/blog/the-forgotten-layer-of-the-test-automation-pyramid

---

## Testing Trophy (Kent C. Dodds)

An alternative to the Test Pyramid that places integration tests as the largest layer, arguing they give the best confidence-to-cost ratio. The trophy shape (from bottom): Static Analysis → Unit → Integration (largest) → E2E (smallest). In Forge, the `test-strategy` skill references both models and recommends the appropriate one based on project type.

**Source:** Dodds, K. C. — "The Testing Trophy and Testing Classifications" (2019) — https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications

---

## Conventional Commits (conventionalcommits.org)

A specification for structured commit messages: `type(scope): description`. Types include `feat`, `fix`, `docs`, `refactor`, `test`, `chore`. Enables automated changelog generation and semantic versioning. In Forge, the `code-standards` skill mandates Conventional Commits for all projects.

**Source:** Conventional Commits v1.0.0 — https://www.conventionalcommits.org/

---

## Semantic Versioning (semver.org)

A versioning scheme `MAJOR.MINOR.PATCH` where MAJOR = breaking changes, MINOR = new features (backwards-compatible), PATCH = bug fixes. In Forge, the `changelog-manager` skill uses SemVer to version project releases.

**Source:** Semantic Versioning 2.0.0 — https://semver.org/

---

## Keep a Changelog (keepachangelog.com)

A convention for maintaining human-readable changelogs. Entries are grouped by version under categories: Added, Changed, Deprecated, Removed, Fixed, Security. An `[Unreleased]` section accumulates changes until the next release. In Forge, the `changelog-manager` skill maintains `CHANGELOG.md` in this format.

**Source:** Keep a Changelog v1.1.0 — https://keepachangelog.com/

---

## OWASP Top 10 (OWASP Foundation)

The ten most critical web application security risks, updated periodically. Categories include Broken Access Control, Cryptographic Failures, Injection, Insecure Design, Security Misconfiguration, Vulnerable Components, Authentication Failures, Data Integrity Failures, Logging Failures, and SSRF. In Forge, the `security-baseline` skill maps each category to the project's specific context.

**Source:** OWASP Top 10 (2021) — https://owasp.org/www-project-top-ten/

---

## WCAG 2.1 (W3C)

Web Content Accessibility Guidelines define how to make web content accessible to people with disabilities. Organized around four principles: Perceivable, Operable, Understandable, Robust (POUR). Three conformance levels: A (minimum), AA (standard target), AAA (enhanced). In Forge, design tokens and wireframes should consider WCAG AA contrast ratios, and the QA checklist includes accessibility verification.

**Source:** W3C WCAG 2.1 — https://www.w3.org/TR/WCAG21/

---

## Clean Architecture (Robert C. Martin)

An architectural pattern that organizes code in concentric layers with dependencies pointing inward: Entities (core business rules) → Use Cases (application rules) → Interface Adapters → Frameworks/Drivers. The key principle is the Dependency Rule — inner layers never depend on outer layers. In Forge, the `architecture-design` skill may recommend Clean Architecture when the project requires strong separation of concerns.

**Source:** Martin, R. C. — *Clean Architecture: A Craftsman's Guide to Software Structure and Design* (2017)
