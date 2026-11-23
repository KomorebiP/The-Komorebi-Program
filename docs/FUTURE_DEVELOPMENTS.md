# Future Developments

My next research priorities are Hilbert's 12th and 24th problems, the Strong
Artin conjecture, and the Langlands program. I also plan to extend my work on
machine learning and reasoning, strengthen the existing mathematics and
software, and make the website and GitHub repositories easier to use.

These priorities may change as new research and tools become available,
including work released by OpenAI and other research groups.

Editorially revised 21 November 2026. The linked records document progress,
supporting evidence, and outstanding requirements for each area of work.
Their individual research dates and verification statuses remain unchanged.

## Main research directions

### Hilbert's 12th problem

The next steps are to develop the existing arithmetic constructions and address
the analytic comparisons and realization steps still required for the full
problem. The linked studies distinguish established finite results from
unresolved analytic and global obligations.

[Ambient dual slice](works/hilbert12-ambient-dual-slice.md) ·
[Analytic Fourier branch](works/hilbert12-analytic-fourier.md) ·
[Cubic divisor development](works/hilbert12-cubic-divisor.md)

### Hilbert's 24th problem

Proof Path Theory studies how proofs are recorded, interpreted, validated, and
compared. Further work will examine criteria for proof comparison and
simplicity, with the aim of making proofs easier to explain and check.

[Proof Path Theory](works/proof-path-theory.md)

### Strong Artin

Work on the Strong Artin conjecture will focus on the unresolved global
automorphic attachment and fresh, reproducible checks of the existing formal
developments. The general conjecture remains open.

[Strong Artin: current work and evidence](works/strong-artin-reader.md)

### Langlands program

Papers XI and XII provide starting points for studying connections among
arithmetic realizations, Hecke data, and automorphic constructions. The linked
records identify the missing arithmetic inputs and distinguish conditional
comparisons from established results.

[Paper XI: arithmetic realization](works/paper-xi.md) ·
[Paper XII: conditional automorphic completion](works/paper-xii.md)

### Machine learning and reasoning

The current research includes the Large Signal Model, Machine Native Reasoning,
and Machine Understanding. Next steps include refining the mathematical models,
clarifying the connections between theory and implementation, and evaluating
empirical claims through reproducible tests.

[Large Signal Model](works/monographs-large-signal-model.md) ·
[Machine Native Reasoning](works/monographs-machine-native-reasoning.md) ·
[Machine Understanding](works/research-machine-understanding.md)

## Refining the current work

Ongoing work includes correcting manuscripts, checking proofs, expanding
examples, and extending selected formal developments. Each new edition will
remain linked to its sources, claim map, and reproducibility records so readers
can trace the mathematical statements and the evidence supporting them.

[Current evidence by work](STATUS_CATALOG.md) ·
[Detailed development queue](FINALIZATION_QUEUE.md)

## Reading editions and visual guides

The twelve core papers have online reading editions and visual guides.
The [Large Signal Model](works/monographs-large-signal-model.md) also has an
online edition connecting its statements, written proofs, and formal
correspondence records.

Plans for the reading library include more guided routes, additional books,
and closer connections between explanations and worked examples. A 97-chapter
edition of Machine Native Reasoning has been reconstructed and published with
editable TeX sources and recorded source and build checks. Its statements still
need to be reconciled with the accepted core, and the broader claims require
separate review.

[Read online](https://KomorebiP.github.io/The-Komorebi-Program/read/index.html) ·
[Explore visual guides](https://KomorebiP.github.io/The-Komorebi-Program/read/visual-guides.html) ·
[Read the expanded book](https://KomorebiP.github.io/The-Komorebi-Program/read/research-machine-native-reasoning-wider/reconstructed-edition.html) ·
[Expanded-book review requirements](FINALIZATION_QUEUE.md#f03)

## Lean and reproducible checks

Development of the browser-based Lean environment will focus on loading
libraries, maintaining compiler compatibility, and reliably checking larger
dependency chains. Another priority is making more retained formal sources
available for inspection, particularly the newer Special Functions developments.
Reproduction instructions must remain consistent with the published editions.

Further formalization will use explicit maps between manuscript claims and Lean
declarations. For editions supported only by retained compilation records,
fresh replays of the pinned sources and dependencies remain necessary.

[Try browser Lean](https://KomorebiP.github.io/The-Komorebi-Program/lean/browser/index.html) ·
[Browser development plan](LEAN_BROWSER.md#route-to-broader-browser-support) ·
[Reproduction guide](LEAN_EXECUTION.md) ·
[Formal replay requirements](FINALIZATION_QUEUE.md#f05)

## Interactive mathematics

Further work on the Signal, Recovery, and J-Space laboratories will connect
experiments more clearly to the mathematics they illustrate. Priorities include
guided demonstrations, meaningful comparisons, and results that readers can
inspect and reproduce.

New examples will identify their assumptions, explain which results are exact
and which are numerical, and link to the relevant sources. Evidence for the
Large Signal Model's mathematical edition will remain separate from evidence
about its software implementation and empirical performance.

[Open interactive tools](https://KomorebiP.github.io/The-Komorebi-Program/interactive.html) ·
[Current laboratory features](READER_SITE.md) ·
[Large Signal Model software and limits](works/large-signal-model.md)

## Website and repository usability and accessibility

Improving navigation and accessibility across the website and GitHub
repositories remains a priority. Planned improvements include clearer entry
points, better search, stronger cross-references, simpler setup instructions,
more useful downloads, and easier ways to report errors.

Accessibility reviews will cover keyboard navigation, screen-reader access,
mobile reading, reading order for mathematical expressions, descriptions of
diagrams, and the original PDF files.

[Reading and accessibility options](ACCESSIBILITY.md) ·
[Using and contributing to the repositories](../CONTRIBUTING.md)

[Research directions](PROJECT_MAP.md) ·
[Detailed development queue](FINALIZATION_QUEUE.md) ·
[Incubator and return criteria](INCUBATOR.md)
