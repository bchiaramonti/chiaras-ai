# Skill Authoring Best Practices

## Contents
- Core principles
- Naming conventions
- Writing descriptions
- Progressive disclosure patterns
- Workflows and feedback loops
- Content guidelines
- Common patterns
- Executable scripts
- Anti-patterns to avoid
- Checklist

## Core Principles

### 1. Concise is Key

The context window is a shared resource. Only add context Claude doesn't already have.

Challenge each piece: "Does Claude really need this?" / "Can I assume Claude knows this?"

**Good** (~50 tokens):
```markdown
Use pdfplumber for text extraction:
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

**Bad** (~150 tokens): Explaining what PDFs are before showing code.

### 2. Set Appropriate Degrees of Freedom

Match specificity to task fragility:

- **High freedom** (text instructions): Multiple valid approaches, context-dependent
- **Medium freedom** (pseudocode/scripts with params): Preferred pattern with variation
- **Low freedom** (exact scripts): Fragile, error-prone, consistency-critical operations

### 3. Test with All Target Models

- **Haiku**: Does the Skill provide enough guidance?
- **Sonnet**: Is it clear and efficient?
- **Opus**: Does it avoid over-explaining?

## Naming Conventions

Use **gerund form** (verb + -ing):
- `processing-pdfs`, `analyzing-spreadsheets`, `managing-databases`

Avoid: vague names (`helper`, `utils`), overly generic (`documents`, `data`), reserved words.

## Writing Descriptions

- Always **third person** ("Processes files..." not "I process files")
- Include **what** + **when**: "Extracts text from PDFs. Use when working with PDF files."
- Include key terms for discovery
- Max 1024 characters

## Progressive Disclosure Patterns

### Pattern 1: High-level guide with references
```markdown
# Skill Title
## Quick start
[Minimal example]
## Advanced features
See [FORMS.md](FORMS.md) for form filling
See [REFERENCE.md](REFERENCE.md) for API details
```

### Pattern 2: Domain-specific organization
```
skill/
├── SKILL.md (overview + navigation)
└── reference/
    ├── finance.md
    ├── sales.md
    └── product.md
```

### Pattern 3: Conditional details
```markdown
## Basic usage
[Default instructions]
**For tracked changes**: See [REDLINING.md](REDLINING.md)
**For OOXML details**: See [OOXML.md](OOXML.md)
```

**Rule:** Keep references 1 level deep from SKILL.md. No nested chains.

## Workflows and Feedback Loops

### Workflow Pattern
Break complex operations into clear sequential steps with a checklist:
```
Task Progress:
- [ ] Step 1: Analyze input
- [ ] Step 2: Generate plan
- [ ] Step 3: Validate plan
- [ ] Step 4: Execute
- [ ] Step 5: Verify output
```

### Feedback Loop Pattern
Run validator -> fix errors -> repeat:
1. Make changes
2. **Validate immediately** (run script or check rules)
3. If fails: fix + validate again
4. **Only proceed when validation passes**

## Content Guidelines

- **No time-sensitive info**: Use "old patterns" section for deprecated approaches
- **Consistent terminology**: Pick one term, use it everywhere
- **Unix-style paths only**: Forward slashes everywhere

## Common Patterns

### Template Pattern
Provide output templates matching strictness to requirements.

### Examples Pattern
Input/output pairs showing expected format and style.

### Conditional Workflow Pattern
Decision points guiding Claude to the right workflow branch.

## Executable Scripts

- **Handle errors explicitly** (don't punt to Claude)
- **Document magic numbers** (justify all constants)
- **Prefer execution over reading** (output is cheaper than code in context)
- **Make execution intent clear**: "Run `script.py`" vs "See `script.py` for the algorithm"

## Skill Categories (Skills 2.0)

Anthropic's Skill Creator framework distinguishes two types:

1. **Capability Uplift Skills**: Extend model functionality (PDF forms, PPTX generation). Have limited lifespans with "retirement dates" as native model capabilities improve.
2. **Workflow/Preference Skills**: Automate specific workflows and enforce compliance. Longer-term value for repetitive tasks (NDA checklists, code review, data overviews).

### Evaluation-Driven Development

Create evaluations **before** writing extensive documentation:

1. **Identify gaps**: Run Claude on representative tasks without a skill. Document failures.
2. **Create evaluations**: Build 3+ test scenarios that test those gaps.
3. **Establish baseline**: Measure performance without the skill.
4. **Write minimal instructions**: Just enough to address the gaps.
5. **Iterate**: Execute evals, compare against baseline, refine.

### MCP Tool References

If your skill uses MCP tools, always use fully qualified names: `ServerName:tool_name`

```markdown
Use the BigQuery:bigquery_schema tool to retrieve table schemas.
Use the GitHub:create_issue tool to create issues.
```

### Table of Contents for Long Files

For reference files longer than 100 lines, include a TOC at the top so Claude sees the full scope even when previewing.

## Anti-Patterns to Avoid

- Windows-style paths (`\` instead of `/`)
- Too many options without a default recommendation
- Deeply nested file references
- Verbose explanations of things Claude already knows
- Time-sensitive instructions

## Iterative Development: Claude A/B Method

1. Work through a task with Claude A (no skill) — note what context you provide
2. Ask Claude A to create a skill capturing the reusable pattern
3. Review for conciseness — remove what Claude already knows
4. Test with Claude B (fresh instance with skill loaded)
5. Observe Claude B's behavior, bring insights back to Claude A
6. Iterate based on real usage, not assumptions

## Quality Checklist

### Core
- [ ] Description: specific, third person, includes key terms
- [ ] SKILL.md: under 500 lines
- [ ] Progressive disclosure used
- [ ] No time-sensitive information
- [ ] Consistent terminology
- [ ] References 1 level deep
- [ ] Workflows have clear steps

### Code/Scripts
- [ ] Errors handled explicitly
- [ ] No magic numbers
- [ ] Dependencies listed
- [ ] Unix-style paths only
- [ ] Validation/feedback loops for critical ops

### Testing
- [ ] At least 3 evaluation scenarios
- [ ] Tested with target models
- [ ] Tested with real usage
