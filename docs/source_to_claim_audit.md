# Source-To-Claim Audit

This audit checks whether each manuscript section has an appropriate
source posture for the kind of claims it makes. It complements citation
resolution: a resolved citation key proves only that the key exists, not
that the cited source is the right authority for the sentence.

Review date: 2026-05-18. External source-risk guidance was checked with
Perplexity for official-source preference, current-event wording,
housing-pipeline status, rural healthcare access, cultural-resource
confidentiality, hazard language, and infrastructure-estimate risk.
A follow-up housing/transport query warned against treating HCD,
Prohousing, voucher, RHNA, Battery Point, and Last Chance Grade claims
as settled without primary sources; the local audit then checked the
official City housing update, HCD Prohousing release mirrored by the
City, Caltrans selection release, and Caltrans Alternative F project
page before retaining dated project-status language.
A hazard follow-up checked the Crescent City Harbor District AB 691
Sea-Level Rise Assessment and tightened the harbor-infrastructure
wording so it names flooding, saltwater intrusion, impaired function,
and adaptation need without asserting a one-foot structural-failure
threshold.
A healthcare follow-up confirmed the HCAI/Sutter 49-licensed-bed claim
but found no primary source for a hard "only hospital within ninety
miles" radius; manuscript language now uses local acute-care anchor
wording and keeps distance/travel burden in the transfer-pathway
discussion.

## Audit Rules

| Claim class | Source-to-claim rule |
|---|---|
| Current public status | Prefer city, county, tribal, agency, court, election, district, or official program records; use local journalism only as dated status or context. |
| Housing pipeline | Distinguish planned units, committed vouchers, funding awards, construction, lease-up, and delivered inventory. |
| Healthcare and social services | Distinguish facility presence, licensed capacity, service availability, transfer pathway, staffing, adequacy, and outcomes. |
| Indigenous and archaeology | Use public or authorized material only; avoid protected locations, identifiers, parcel detail, point coordinates, or restricted cultural knowledge. |
| Hazards and sea level | Preserve measured, modeled, projected, scenario, and planning-estimate language. |
| Infrastructure cost and schedule | Treat planning estimates as volatile unless an adopted capital source makes them final. |

## High-Risk Claim-Fit Notes

| Area | Current fit | Required next action |
|---|---|---|
| `10_housing.md` | Captions and prose now describe pipeline status rather than delivered inventory. City/HCD Prohousing and Housing Element claims are tied to the official City update and HCD release, while Western City/RHNA wording remains production/capacity-specific. | Recheck city, HCD, housing-provider, and funding records before publication; update `data/housing_pipeline_projects.csv` first. |
| `52_healthcare_social_services.md` | The network figure is framed as service-pathway mapping, not measured adequacy. Sutter Coast wording uses the HCAI-supported 49 licensed beds and local acute-care anchor status rather than an unsupported hard-radius exclusivity claim. | Recheck HCAI, provider pages, county services, IHS/UIHS, Tolowa public programs, and 2-1-1 style directories before claiming current service availability, staffing, or exact regional coverage. |
| `21_archaeology.md` | Section uses public evidence classes and generalized language. Sensitive chronology rows leave `lat`/`lon` blank. | Do not add protected coordinates, site identifiers, parcel references, or consultation detail beyond public summaries. |
| `41_indigenous.md` and `42_nee_dash.md` | Tribal and ethnographic material is public-facing and culturally bounded. | Prefer Tolowa Dee-ni' Nation public sources when available; do not infer private ceremonial detail. |
| `35_currents.md` and `71_timeline.md` | Current-event rows carry `checked_as_of`, source tier, and refresh trigger metadata. | Follow `current_events_refresh.md` before any public render after a trigger date or agency correction. |
| `05_sea_level_rise.md`, `04_cascadia.md`, `31_tsunami.md` | Hazard language distinguishes measured, modeled, projected, reconstructed, and planning-assessment evidence. Sea-level infrastructure language now cites the Harbor District AB 691 assessment without turning impaired-function risk into a structural-failure finding. | Recheck NOAA, USGS, OPC, FEMA, Cal OES, Harbor District, and local hazard documents if any scenario value or infrastructure status changes. |
| `11_transportation.md` | Last Chance Grade language is planning-estimate and selected-alternative language. | Recheck Caltrans project pages and environmental documents before repeating cost, schedule, or selected-alternative claims. |
| `09_seawall_engineering.md` | Harbor chronology is framed as event timeline, not complete inventory. | Recheck Harbor District or city records before claiming current engineering status or completed construction. |

## Section Coverage

| Manuscript file | Dominant claim class | Fit status | Maintenance note |
|---|---|---|---|
| `00_abstract.md` | Synthesis and metrics | Fit with generated variables | Re-render after pipeline metrics change. |
| `01_introduction.md` | Framing and method | Fit with systems and reproducibility sources | Keep thesis language sourced but not overclaimed. |
| `02_space.md` | Geographic framing | Fit with public geographic context | Avoid adding unsourced local precision. |
| `03_environment.md` | Climate and setting | Fit with NOAA and ecological sources | Keep airport normals distinct from microclimate claims. |
| `04_cascadia.md` | Geologic hazard | High-risk fit controlled | Preserve model and recurrence uncertainty. |
| `05_sea_level_rise.md` | Coastal hazard | High-risk fit controlled | Distinguish tide gauge, projection, scenario, and subsidence. |
| `06_smith_river_ecology.md` | Protected river ecology | Fit with official and conservation sources | Recheck designation values if agency records change. |
| `07_redwood_parks.md` | Conservation history | Fit with NPS and conservation sources | Keep acreage values as rounded estimates. |
| `08_oil_spill.md` | Marine hazard | Fit with agency and historical records | Keep risk language conditional and source dated. |
| `09_seawall_engineering.md` | Harbor infrastructure | High-risk fit controlled | Do not imply complete infrastructure inventory. |
| `10_housing.md` | Current housing pipeline | High-risk fit controlled | Recheck before publication; planned is not delivered. |
| `11_transportation.md` | Highway and Last Chance Grade | High-risk fit controlled | Treat cost and schedule as planning estimates. |
| `20_time.md` | Chronological framing | Fit with methodology sources | Keep as interpretive bridge. |
| `21_archaeology.md` | Archaeology and cultural resources | High-risk fit controlled | Preserve confidentiality boundaries. |
| `22_contact.md` | Contact-era history | Fit with historical and ethnographic sources | Avoid totalizing contact-era claims. |
| `23_early_settlement.md` | Early American settlement | Fit with historical sources | Keep violence and dispossession sourced. |
| `24_gold_rush.md` | Gold Rush context | Fit with historical sources | Avoid unsupported regional generalization. |
| `25_lumber.md` | Timber economy | Fit with historical and economic sources | Keep estimates labeled. |
| `26_lumber_technology.md` | Industrial technology | Fit with historical sources | Distinguish local examples from industry-wide claims. |
| `27_fishing.md` | Fishing economy | Fit with fishery and history sources | Recheck current salmon claims through fishery agencies. |
| `28_railroad.md` | Transport history | Fit with historical sources | Avoid speculative counterfactuals. |
| `29_economic_history.md` | Economic transition | Fit with mixed public estimates | Keep sector comparisons instrument-aware. |
| `30_agriculture.md` | Agriculture and lilies | Fit with agricultural and local sources | Keep market estimates sourced and bounded. |
| `31_tsunami.md` | 1964 and later tsunami impact | High-risk fit controlled | Preserve measured versus reconstructed values. |
| `32_tsunami_context.md` | Comparative tsunami context | Fit with hazard literature | Avoid implying identical mechanisms across events. |
| `33_tohoku.md` | 2011 Tohoku effects | Fit with tsunami and harbor records | Keep harbor-current damage distinct from run-up height. |
| `34_wildfire.md` | Fire and regional hazard | Fit with agency and local records | Keep exposure language conditional. |
| `35_currents.md` | 2024-2026 current events | High-risk fit controlled | Follow current refresh protocol. |
| `40_people.md` | Social framing | Fit with synthesis sources | Keep as orientation. |
| `41_indigenous.md` | Tolowa Dee-ni' history | High-risk fit controlled | Prefer public tribal sources and authorized framing. |
| `42_nee_dash.md` | Cultural practice | High-risk fit controlled | Do not add private ceremonial detail. |
| `43_neighboring_tribes.md` | Regional tribal context | Fit with public tribal and scholarly sources | Preserve distinct nations and territories. |
| `44_immigrant_communities.md` | Migration and communities | Fit with demographic and historical sources | Avoid flattening distinct migration histories. |
| `45_governance.md` | Civic governance | Fit with legal and civic records | Use official records for public-body claims. |
| `46_del_norte.md` | County institutions | Fit with county and historical sources | Keep institution status dated. |
| `47_military.md` | Military history | Fit with public historical sources | Avoid unsupported strategic claims. |
| `48_world_war_ii.md` | WWII home-front history | Fit with public historical sources | Keep local examples tied to sources. |
| `49_education.md` | Education institutions | Fit with public institutional sources | Recheck current institutional status if updated. |
| `50_religion.md` | Religious history | Fit with local and historical sources | Avoid doctrinal claims beyond sources. |
| `51_demographics.md` | Population composition | Fit with Census, ACS, and DOF sources | Keep estimate instruments distinct. |
| `52_healthcare_social_services.md` | Healthcare and service access | High-risk fit controlled | Do not infer adequacy or outcomes from network presence. |
| `60_ideas.md` | Interpretive framing | Fit with cited theory | Keep as synthesis rather than new empirical claim. |
| `61_zoning.md` | Land-use governance | Fit with official and legal sources | Distinguish adopted rules from proposed changes. |
| `62_resilience.md` | Resilience planning | Fit with hazard and planning sources | Avoid certainty about future hazard response. |
| `63_klamath_dam_removal.md` | Klamath restoration | Fit with official restoration records | Recheck post-removal monitoring updates before release. |
| `64_jefferson.md` | State of Jefferson history | Fit with historical and political sources | Preserve movement framing and avoid legal overstatement. |
| `65_modern.md` | Modern economy and civic status | Fit with mixed current records | Recheck volatile public-status claims. |
| `66_culture.md` | Cultural institutions | Fit with public cultural sources | Keep current status dated. |
| `67_arts.md` | Arts and public culture | Fit with public cultural sources | Avoid promotional language. |
| `68_tourism.md` | Tourism and identity | Fit with public and commercial sources | Do not treat rankings as civic facts. |
| `69_klamath_knot.md` | Ecological and cultural synthesis | Fit with cited scholarship | Keep ecological synthesis tied to sources. |
| `70_conclusion.md` | Synthesis and implications | Fit after compression | Do not add new claims in conclusion. |
| `71_timeline.md` | Chronology | High-risk fit controlled | Keep scheduled rows scheduled until records update. |
| `72_methodology.md` | Method and reproducibility | Fit with reproducibility literature | Keep commands current with tests. |
| `73_reproducibility.md` | Reproduction contract | Fit with project outputs | Refresh metrics after pipeline changes. |
| `99_references.md` | Bibliography section | Fit with generated bibliography | Citation tests remain source of truth. |
| `A1_figure_catalogue.md` | Figure provenance | Fit with registry and `figure_provenance.csv` | Keep every entry synced with the manifest contract. |
| `A2_glossary.md` | Term definitions | Fit with manuscript terminology | Avoid adding unsourced substantive claims. |

## Completion Standard

Before a public release, rerun the current-event refresh protocol, then
run the strict pipeline, render, and validation commands in
`publication_checklist.md`. A green build is necessary, but claim-fit
review remains a separate editorial gate.
