# Red Team Review: crescent_city (2026-05-15)

## Scope

This review stress-tests the local `crescent_city` project as a
reproducible research artifact. It asks what can still go wrong when the
pipeline, tests, figures, citations, and render path are working.

Local baseline refreshed on 18 May 2026:

- `output/pipeline_report.json`: 5/5 checks passed, 59,086 words, 370
  unique citations, average FKGL 17.40, citation density 6.26, and 24
  generated figures.
- `docs/project_overview.md`: 58 analyzed Markdown source files, 24 PNG
  plus 24 SVG figures, and 20 checked-in data inputs.
- `data/historical_events.json`: rows from 2024 onward are expected to
  carry `checked_current_source`, `checked_as_of`, `source_tier`, and
  `refresh_trigger` metadata.
- `docs/claim_ledger.md`: the active control point for current-event
  refreshes, modeled hazards, sensitive evidence boundaries, and reserve
  bibliography policy.

## Core Thesis Under Review

The manuscript uses Space, Time, People, and Ideas to make Crescent City
and Del Norte County inspectable as one nested coastal system. The project
claims that readers can audit this synthesis through checked-in sources,
data, code, figures, bibliography, rendered outputs, and tests.

The strongest version of the thesis is not "the pipeline proves every
sentence." The stronger and more defensible claim is: the pipeline makes
the research object rebuildable and exposes enough structure for focused
source review.

## Main Risk

The project is strong at proving structural reproducibility. It is weaker
at proving ongoing factual freshness. A critic does not need to break the
build; they need to find one stale current-status paragraph, one
overconfident modeled-hazard statement, one unsupported local civic
detail, or one source whose evidence class is presented too strongly.

That is the central red-team finding.

## Evidence-Surface Assessment

| Surface | Strength | Risk | Control |
|---|---|---|---|
| Manuscript structure | Stable 58-file organization with section anchors | Broad synthesis can hide semantic dependencies | `tests/test_manuscript.py`, `manuscript/SYNTAX.md` |
| Bibliography | 370 cited keys and explicit reserve-key policy | Citation presence does not prove source-to-claim fit | `tests/test_citations.py`, `docs/claim_ledger.md` |
| Figures | 24 registered figures with PNG and SVG outputs | Mixed evidence classes can look visually equivalent | `src/figures.py`, figure captions, `tests/test_figures.py` |
| Current events | Recent rows carry audit metadata | Public records can change after `checked_as_of` | `docs/source_refresh_workflow.md` |
| Indigenous and archaeology material | Public-source and generalized-location boundary | Public availability is not the same as community consent | `data/README.md`, manuscript language, claim ledger |
| Rendering | PDF, HTML, slides, and validation are reproducible | Render validity is not truth validation | `docs/rendering_and_outputs.md` |
| Documentation | Docs are now task-oriented and test-linked | Counts and commands can drift after code changes | `tests/test_documentation.py` |

## Atomic Claims To Pressure Test

| ID | Claim | Red-team question |
|---|---|---|
| C01 | The Space-Time-People-Ideas frame organizes the manuscript without distorting chronology. | Do chapter transitions preserve chronology where chronology matters? |
| C02 | The 1964 tsunami is a legitimate hinge for the whole history. | Does the manuscript avoid making one disaster explain unrelated phenomena? |
| C03 | Evidence classes are distinguished. | Are measurements, models, estimates, reconstructions, and current statuses labeled consistently? |
| C04 | Indigenous and archaeological material respects public-source boundaries. | Are any protected locations, restricted practices, or over-specific site details exposed? |
| C05 | Local journalism is used only where appropriate. | Has any technical, legal, or scientific claim depended on journalism when an official source exists? |
| C06 | The bibliography supports cited claims. | Does each citation support the exact sentence it is attached to? |
| C07 | Reserve bibliography entries are intentional. | Does every uncited source have a current reason to remain? |
| C08 | Figure captions preserve source basis and limitation. | Does any figure imply more precision than the source supports? |
| C09 | Current events are dated snapshots. | Are scheduled, proposed, pending, and completed statuses kept separate? |
| C10 | Tests catch meaningful drift. | Which truth claims remain outside the test surface? |
| C11 | Manuscript variables keep numeric claims connected to pipeline outputs. | Are injected values used instead of hand-authored numbers where appropriate? |
| C12 | Documentation is part of reproducibility. | Can a maintainer follow docs without inferring hidden workflow steps? |

## High-Value Attack Paths

| Attack path | Why it matters | Defensive response |
|---|---|---|
| Recheck every 2024 onward event after its `checked_as_of` date | Stale public status is the fastest way for a green build to be wrong | Follow `source_refresh_workflow.md` before public render |
| Compare citations against exact claims, not just key presence | Citation resolution can hide weak support | Prioritize high-risk paragraphs and figure captions |
| Inspect figures that mix models, measurements, and estimates | Visual marks can flatten evidence classes | Keep captions and legends explicit about encoding |
| Audit reserve bibliography keys | Working libraries can accumulate unused material | Keep reserve-key reasons current in `claim_ledger.md` |
| Inspect Indigenous-history and archaeology prose for over-disclosure | Ethical harm can occur even with a working build | Keep locations generalized and use public/authorized sources |
| Review rendered PDF, not only Markdown | Pandoc/LaTeX can change cross-reference presentation | Use `rendering_and_outputs.md` and spot-check PDF sections |

## Steelman

The project is unusually inspectable for a local history manuscript. It
does not hide its machinery: source Markdown, data, plotting code,
bibliography, figure registry, tests, PDF render path, and publication
metadata are all present. The nested-systems frame gives the manuscript a
stable architecture without requiring the reader to treat geology,
settlement, sovereignty, industry, disaster, and civic memory as the same
kind of evidence. The best defense of the artifact is that it is honest
about what reproducibility can and cannot prove.

## Counter-Argument

Reproducibility can faithfully rebuild an obsolete or overconfident claim.
Citation density can reward source presence even when source fit is weak.
Current events can change faster than documentation and test cycles.
Local journalism is sometimes necessary, but it is a fragile basis for
scholarship when official records later appear. The artifact therefore
needs source-refresh discipline as much as it needs passing tests.

## Operating Guidance

Use this review as a checklist before public renders:

1. Treat current-event freshness as the highest-risk surface.
2. Upgrade local-journalism-backed claims to official sources whenever
   those sources become available.
3. Preserve "modeled," "projected," "estimated," "scheduled," and
   "proposed" language where those words match the evidence.
4. Keep Indigenous and archaeological material public, generalized, and
   ethically bounded.
5. Do not use generated outputs as source truth.
6. Run project tests, strict pipeline, render validation, and copy-out
   before handoff.

## Bottom Line

The artifact is technically strong. Its main residual risk is not build
failure; it is overreading a green build as complete truth validation.
The right maintenance posture is therefore: keep the pipeline green, and
refresh high-risk claims deliberately before publication.
