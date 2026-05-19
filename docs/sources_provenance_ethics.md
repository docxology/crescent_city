# Sources, Provenance, And Ethics

This guide defines how Crescent City source material is selected,
recorded, refreshed, and bounded ethically. It sits between the working
data files, the claim ledger, and the manuscript. Use it before adding a
new source-backed claim, revising current-event rows, or expanding
Indigenous, archaeological, legal, medical, or civic material.

## Source Policy

The project prefers sources that are stable, attributable, and
appropriate to the claim type.

| Claim type | Preferred source | Rule |
|---|---|---|
| Official status | City, county, tribal, state, federal, court, school, harbor, or agency records | Date the status claim and cite the responsible public body. |
| Scientific measurement | NOAA, USGS, NPS, CDFW, Caltrans, HCAI, peer-reviewed papers, or government technical reports | Preserve the instrument, model, date range, and uncertainty language. |
| Local civic detail | Official records first; local journalism only when no stable public record is available yet | Use journalism as dated public-status evidence, not as technical proof. |
| Indigenous public history | Tribal publications, tribally authorized public material, law, public ethnography, and archive records | Do not publish restricted knowledge, protected site detail, or community-private material. |
| Archaeology | Public reports, public summaries, law, and high-level evidence classes | Keep site locations generalized and avoid coordinates, parcel detail, or identifiers. |
| Markets and tourism | Named public data instruments or commercial publications | Keep the source instrument visible and avoid converting rankings into civic facts. |

Local memory, oral recollection, and unpublished notes may guide
research questions, but they are not enough for a public manuscript claim
unless the material has been cleared for this publication context and
given an auditable citation path.

## Current-Event Source Tiers

`data/historical_events.json` uses the exact `source_tier` labels below.
They are enforced by `tests/test_data.py`; do not invent alternate tier
names in prose or data.

| Tier | Meaning | Use |
|---|---|---|
| `official_primary` | Direct record from the responsible agency, court, tribe, public body, or data portal | Preferred for status, legal, scientific, and technical claims. |
| `official_plus_local_journalism` | Official record plus local reporting for context, timeline detail, or local interpretation | Use when the official source carries the fact and journalism helps explain public context. |
| `official_plus_reference` | Official record plus a stable reference source, background source, or election/agency reference page | Use for public schedules, ballots, reference summaries, or official-status rows needing context. |
| `local_journalism_current_status` | Local reporting describes a current public status while formal records are unavailable or incomplete | Use only as dated current status and schedule a re-audit. |
| `local_journalism_pending_official_record` | Local reporting describes a legal or public-safety event that should later be checked against court, sheriff, district-attorney, or agency records | Treat as provisional and re-audit when official records appear. |
| `commercial_publication` | Commercial list, ranking, tourism publication, or non-government cultural publication | Use for cultural or tourism status, not legal, scientific, or technical facts. |
| `tribal_press_release_republished` | Tribal public statement or press release republished by another outlet | Preserve tribal framing and check the original tribal source when possible. |

When a better source becomes available, update the data row first, then
the BibTeX key, manuscript prose, figure caption, and
[claim_ledger.md](claim_ledger.md).

## Provenance Fields

Every data-backed claim should expose enough context for a reviewer to
trace it without reverse-engineering the figure code.

| Field or record | Required use |
|---|---|
| `source_keys` | BibTeX keys in `manuscript/references.bib`; use a list in JSON and semicolon-delimited keys in CSV. |
| `evidence_type` / `evidence_class` | State whether the row is measured, projected, modeled, schematic, estimated, scheduled, or current public status. |
| `checked_as_of` | Use ISO dates for recent public-status rows and any source whose status can change. |
| `refresh_trigger` | Name the event or source change that requires another audit. |
| `notes` | Record the row-level caveat, instrument boundary, or reason a value is rounded. |
| Stable IDs | Treat `event_id`, `point_id`, `metric_id`, `node_id`, and related IDs as audit anchors. |
| Location fields | `lat` and `lon` may be blank together when location precision would expose Indigenous, archaeology-adjacent, massacre, or protected-resource detail. |

Generated files under `../output/` may show the current result, but they
are not provenance records. The source record lives in `../data/`,
`../manuscript/references.bib`, the manuscript text, or a checked-in doc.

## Sensitive Material Boundaries

The project is public-facing. It should not publish material merely
because it can be found.

| Area | Boundary |
|---|---|
| Indigenous history | Use public, tribally authorized, legal, archival, and scholarly sources. Do not infer ceremonial detail or publish community-private material. |
| Archaeology and Indigenous place history | Use evidence classes and public historical framing. Do not add protected site coordinates, parcel-level locations, identifiers, or point locations in source data. |
| Legal and public-safety events | Keep allegations, charges, and dispositions tied to dated official or journalism-backed records. Do not imply outcomes before records support them. |
| Healthcare and social services | Distinguish licensed capacity, staffing, access, transfers, and service availability. Do not infer care quality from a capacity number alone. |
| Private people | Avoid addresses, personal contact details, and unnecessary identifying detail for living people unless already central to a public official record. |

When a claim can be accurate but harmful, either generalize it, cite only
the public aggregate, or leave it out.

## Reuse And Licensing

The manuscript and rendered scholarly artifacts use the license declared
in `../manuscript/config.yaml`. Code and data have separate licensing
realities described in the root [README.md](../README.md).

Reuse rules:

- Cite the original public source, not just this project, when reusing a
  factual data point.
- Preserve agency, tribal, journalistic, and archive attribution.
- Do not imply that a source endorses this manuscript.
- Keep generated figures connected to their source keys and figure-catalog
  entries.
- Remove or revise material if the public source is corrected,
  withdrawn, or superseded.

## Refresh Responsibilities

Use this sequence for source maintenance:

1. Check [claim_ledger.md](claim_ledger.md) for volatile areas and
   source-tier policy.
2. Follow [source_refresh_workflow.md](source_refresh_workflow.md) for
   current events and high-risk claims.
3. Update [data_dictionary.md](data_dictionary.md) if a data file,
   provenance field, or update risk changes.
4. Update [manuscript_authoring.md](manuscript_authoring.md) if the
   evidence-language rule changes.
5. Run the targeted tests listed in
   [testing_and_quality.md](testing_and_quality.md).

Do not leave a source upgrade only in prose. If a figure, timeline, or
pipeline output depends on the claim, update the data and generated
artifacts through the normal pipeline.
