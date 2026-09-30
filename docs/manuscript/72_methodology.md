## How This History Was Built: Methods, Sources, and Editorial Practice {#sec:methodology}

### Research Design for a Reproducible Local History

This study combines archival analysis, secondary-source synthesis, and
quantitative data analysis. Its method is historical, but its workflow
is reproducible: the data, code, figure scripts, and rendered outputs
are kept in the project repository [@peng2011reproducible].

The manuscript uses a four-lens nested-systems structure rather than a
single strict chronology. Space, Time, People, and Ideas each gather
chapters where that lens explains the interaction most clearly. The
Space part moves from Earth systems toward the built townsite. The Time
part supplies the long chronology, from archaeology through contact,
extraction, disaster, and recent events. The People part follows tribal
nations, immigrant communities, public institutions, education,
religion, healthcare, and social services. The Ideas part treats
planning, preparedness, dam removal, political imagination, tourism,
folklore, methods, and reproducibility as forces that shape action.

The structure is meant to be navigable in two ways. Readers can follow
the manuscript in order, moving from scale to sequence to institutions
to interpretation. They can also use cross-references and the timeline
in [@sec:timeline] as a chronological anchor when a topic reappears in
more than one part [@oneill1986hierarchical; @liu2007chans;
@ostrom2009ses; @tuan1977space_place; @massey2005for_space].

### Primary Sources and Public-Record Evidence

Key primary sources include:

- Federal and state records: Census data [@uscb2020census],
  Bureau of Indian Affairs reports, and California state legislative
  documents
- Newspaper archives: Local newspaper coverage spanning 1854–present,
  maintained by the Del Norte County Historical Society
- Ethnographic records: Edward Sapir's fieldwork on the Tolowa
  language and culture [@sapir1930], and ethnographic surveys by
  A.L. Kroeber and colleagues
- Archival collections: The Del Norte County Historical Society
  maintains photographs, maps, and manuscript collections relevant to
  this study [@nortoni1971]
- Geological and seismological data: Paleoseismic trenching results
  and tide gauge records from the National Oceanic and Atmospheric
  Administration [@noaanthropogenic; @usgs2015tsunami]

### Secondary Sources and Interpretive Literature

The bibliography combines peer-reviewed scholarship, government and
tribal primary documents, court records, local archives, and carefully
attributed contemporary civic journalism. Core secondary literatures
include ethnography [@gould1978; @native_encyclopedia], ecology
[@stephens2018; @marine; @redwood_parks], geology [@goldfinger2012],
policy analysis [@yaffee1994], and disaster science [@borrero2017].
Where possible, popular or journalistic accounts are used only for
dated contemporary events, institutional announcements, or local facts
not yet represented in peer-reviewed literature.

### Evidence and Claim Confidence

The manuscript distinguishes among evidence classes in prose and
captions wherever the distinction changes interpretation. Census and
Department of Finance values are named as counts or estimates; tide-
gauge trends are measured relative-sea-level records; Cascadia
probabilities, sea-level projections, and tsunami scenarios are model
outputs; twentieth-century disaster damages are post-event
reconstructions; and 2024--2026 civic items are public-status claims
checked against official records before local journalism is used. This
claim-confidence practice is meant to keep a reader from treating a
licensed hospital bed count, a Caltrans planning estimate, a Realtor.com
listing snapshot, a turbidite recurrence model, and an eyewitness
massacre memory as the same kind of fact [@wilkinson2016fair;
@sandve2013reproducible].

### How to Read the Evidence

Four recurring evidence boundaries should be kept visible while reading
the manuscript. First, Indigenous history is cited only through public,
published, or tribally authorized materials; restricted ceremonial
knowledge, sensitive site locations, and internal community protocols
are not treated as extractable data. Second, hazard claims distinguish
measured records from modeled scenarios: a tide-gauge observation, a
tsunami-inundation model, a Cascadia recurrence probability, and a
planning exercise casualty estimate are different kinds of evidence.
Third, demographic and economic figures combine instruments when the
local record requires it — decennial census counts, ACS estimates,
Department of Finance estimates, QCEW employment, and modeled visitor-
spending effects — so captions name the instrument rather than implying
a single continuous series. Fourth, current-event passages are dated
status claims. They anchor decisions to official agendas, agency
releases, court records, or public notices when available, and use local
journalism only for civic details not yet preserved in stable official
records [@wilkinson2016fair; @sandve2013reproducible; @style].

For 2024--2026 current-event rows, the source hierarchy is explicit in
`data/historical_events.json` rather than implied by prose order:

| Source tier | Use in this manuscript | Revision rule |
|---|---|---|
| Official primary | City, county, tribal, state, federal, court, regulatory, or instrument record | Treat as the anchor source and refresh when the issuing body changes the record. |
| Tribal public source | Tribal publication, authorized public statement, or tribally controlled cultural/governance material | Treat as primary for tribal self-description; do not replace it with outside synthesis. |
| Official plus local journalism | Official record establishes the action; local reporting supplies context, quotations, or local sequence | Keep the official record in the citation cluster and re-audit both sources after status changes. |
| Local journalism pending official record | Civic incident or local transition not yet preserved in a stable public record | Word as a dated report and replace or supplement it when court, agency, or meeting records appear. |
| Commercial publication or listing | Recognition, market listing, ranking, or snapshot outside the public-record system | Treat as a dated external claim, not as a durable civic fact. |

### Documentation as Historical Method

The project-facing documentation is treated as part of the method, not
as packaging added after the fact. `README.md` gives a reader the public
quick start, `AGENTS.md` records the working contracts for future
editorial and technical agents, and the `docs/` directory preserves the
project overview, architecture map, command sequence, claim ledger, and
reserve-source audit. Keeping those files synchronized with the figure
registry, bibliography, and current Space-Time-People-Ideas table of
contents supports Sandve et al.'s
reproducibility rule that textual claims must remain connected to the
underlying results, and it also makes the manuscript easier to treat as
a FAIR research object rather than as a static PDF
[@sandve2013reproducible; @wilkinson2016fair].

### Data Analysis, Figure Generation, and QA Checks

Demographic and economic data were analyzed using Python. The systems
map in [@fig:nested_systems_map] documents the manuscript's conceptual
architecture; [@fig:section_word_counts], [@fig:readability_metrics], and
[@fig:citation_density] document the manuscript's own quantitative
properties. Census data
were extracted at the census-tract level and aggregated to the Del
Norte County level [@uscb2020census]. Readability analysis of the
manuscript was performed using the Flesch-Kincaid framework, computing
Flesch Reading Ease and Flesch-Kincaid Grade Level [@fkgl;
@flesch1948new]. Citation density was computed as citations per
1,000 words to ensure adequate scholarly grounding [@style].

![Word count per manuscript chapter and appendix source, computed from the Markdown source tree with folder documentation, syntax notes, preamble files, and references excluded. Source basis: manuscript source files and `output/manuscript_report.json`. The evidence class is automated editorial metric. Green bars mark sections above the mean section length; part-grouped panels show the Space, Time, People, Ideas, and appendix groupings without changing the section-level calculation. The limitation is interpretive: the figure is an editorial-load diagnostic, not a claim about historical importance. The interpretive claim is maintenance-oriented: long sections usually indicate dense archival, technical, or current-event synthesis that future editors should re-check after major source updates.](output/figures/section_word_counts.png){#fig:section_word_counts width=82%}

![Readability metrics for the manuscript, computed per source section under the Flesch-Kincaid framework and grouped visually by manuscript part. Source basis: manuscript source files and automated readability formulas. Cyan bars report Flesch Reading Ease; the orange line reports Flesch-Kincaid Grade Level in the lower panel. The evidence class is automated prose-surface measurement, not scholarly evaluation: the formulas cannot see source quality, narrative judgment, tribal-cultural nuance, or whether a technical term is necessary. The limitation is therefore conceptual as well as statistical. The interpretive claim is editorial triage: the plot helps find sections where sentence splitting or topic-sentence work may help readers without diluting precision.](output/figures/readability_metrics.png){#fig:readability_metrics width=100%}

![Citation density per source section, counted as Pandoc-style citation tokens per 1,000 words and grouped by manuscript part. Source basis: manuscript source files, Pandoc-style citation tokens, and the configured citation-density floor in `src/pipeline.py`. The evidence class is automated citation-coverage metric. The dashed red line marks the configured floor. This is a conservative coverage signal rather than an accuracy score: multi-source citation clusters are counted by bracket, lower-density methodology sections may synthesize previously cited evidence, and a high-density chapter can still contain a claim that needs rechecking. The interpretive claim is procedural: the project uses citation density to find review targets, not to certify truth.](output/figures/citation_density.png){#fig:citation_density width=100%}
