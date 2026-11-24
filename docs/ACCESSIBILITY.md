# Accessibility and reading options

The [Komorebi website](https://KomorebiP.github.io/The-Komorebi-Program/)
provides HTML reading editions, original PDFs, and links to manuscript and
software source files. Maintained Markdown guides are also available on
GitHub. This guide explains how to choose a format, navigate by keyboard,
adjust the reading view, and find statements, proofs, and source material.

## Choose a reading format

<table>
<caption>Choose a reading format or tool</caption>
<thead><tr><th scope="col">What you want to do</th><th scope="col">Where to begin</th></tr></thead>
<tbody>
<tr><th scope="row">Read a paper or book in HTML</th><td><a href="https://KomorebiP.github.io/The-Komorebi-Program/read/index.html">Reading library</a></td></tr>
<tr><th scope="row">Read diagrams and worked visual guides</th><td><a href="https://KomorebiP.github.io/The-Komorebi-Program/read/visual-guides.html">Visual guides</a></td></tr>
<tr><th scope="row">Keep two documents open together</th><td><a href="https://KomorebiP.github.io/The-Komorebi-Program/side-by-side.html">Read side by side</a></td></tr>
<tr><th scope="row">Find a passage or term</th><td><a href="https://KomorebiP.github.io/The-Komorebi-Program/search.html">Site search</a> or the <a href="GLOSSARY.md">glossary</a></td></tr>
<tr><th scope="row">Open or download an original PDF</th><td><a href="https://KomorebiP.github.io/The-Komorebi-Program/documents.html">Papers and PDFs</a></td></tr>
</tbody>
</table>

### Before you begin

**Start with HTML when possible.** The core-paper HTML chapters provide
headings, section links, text settings, and navigation between chapters,
statements, proofs, and references. The visual guides offer HTML versions of
the illustrated material.

**Formats differ in accessibility.** Some original PDFs may lack semantic
tags, a reliable reading order, or descriptions of equations. Markdown and
source text are alternatives when a reading edition is not usable, but TeX
source is not the same as rendered mathematics.

**Testing is not complete.** Representative pages have undergone keyboard
and narrow-screen checks. A complete screen-reader review has not been
performed, and the site does not claim WCAG conformance. See
[known limitations](#accessibility-limitations) or
[report an access problem](#accessibility-help).

### Features that need JavaScript

Ordinary reading pages, chapter links, static glossary entries, and source
links remain available without JavaScript. Site search, interactive filters,
reference previews, text settings, saved reading, and the side-by-side reader
require JavaScript. Saved places, reading sessions, and preferences also
depend on browser storage.

If these features are unavailable, use the ordinary document links, your
browser's Find command, and separate tabs for comparing documents.

## Navigate and read

### Keyboard controls

Use **Tab** and **Shift+Tab** to move between controls. Press **Enter** to
follow links or activate buttons. Use **Space** or **Enter** to open and close
disclosures.
The site provides **Skip to main content**, named navigation regions, visible
keyboard focus, and layouts that reflow on narrow screens. Wide tables, code
blocks, and displayed equations have keyboard-scrollable areas. Focus a wide
block, then use the arrow keys to scroll it.

### Find sections and chapters

The site header provides **Read**, **Collection**, **Glossary**, **About**,
and **Search**. **Browse** groups additional links under **Read**, **Look up**,
and **Use**. Press **Escape** while the Browse menu is open to close it and
return keyboard focus to the **Browse** button. Without JavaScript, those grouped links remain visible.

Long guides include an **On this page** list. In reading chapters, the
section sidebar and **On this page** links help you move within the text.
Following an in-page link moves keyboard focus to its destination and opens
any enclosing contents disclosure. Direct passage links and the browser's
Back and Forward controls return you to the linked passage, unless you have
since moved focus to another control.

Chapter pages provide **Previous**, **Next**, and **Chapters** controls,
with destination titles shown. The sidebar also links to **Work overview**
and **Full contents**. Visual guides use **Atlas plates** for navigation,
except for Paper IX, which uses **Visual sections**.

Open **Reading tools** to access **Reading library**, **Switch work**, and
other controls. **Find a chapter** filters the contents by title or reading-page
number. **Escape** clears the search and then closes its menu. Complete
chapter lists remain available without JavaScript.

### Adjust text and simplify the page

In a reading chapter, open **Reading tools**, then **Text settings**, to choose
standard, large, or extra-large text and a sans-serif or serif typeface for
prose. These settings apply across reading chapters and are saved in the
browser when local storage is available. **Reset text settings** restores
the defaults. You can also use your browser's zoom controls.

Open **Resources & source** for PDFs and related resources. Its **Show source
and reference links** option reveals each passage's permalink, source line,
claim record, and related resources. The choice is remembered when browser
storage is available. Proof links, atlas links, and chapter navigation remain
available in either view. **Skip contents and start reading** moves directly
to the text. Without JavaScript, passage links remain visible.

### Follow statements, proofs, and references

When a chapter contains statement records, open **Statements and proofs** in
its contents. **Find a statement** searches titles, printed numbers, statement
types, and source labels. Number searches require an exact match. Include a statement type, such as
**Theorem 12.6**, to distinguish records with the same number. Greek letter
names such as **rho** also match their symbols. The **Proof links only** filter shows
entries with a recorded **Read proof** link. Following a statement or proof
link moves keyboard focus to the passage. **Escape** clears the filters, then
closes the list. The full list and links also work without JavaScript.

Use **Find statements** in **Reading tools** to search across a core paper.
Results remain grouped by chapter. The query and filters are stored in the
page URL, so reloading, using the browser's Back control, or sharing the link
restores them. Changing filters does not add browser-history steps.

Use **Find a reference** in bibliographies to search by author, title, year,
or citation key. Clearing it restores every entry. A direct reference link
reveals its entry even if a filter has hidden it. The **Cited in this paper**
link leads to the HTML passages that cite the entry. Original citation
numbers and bibliography order are preserved.

Reference and citation links in the twelve core papers also offer a separate
**Preview** button. It opens a labeled dialog without changing your reading
position. **Tab** and **Shift+Tab** move within the dialog. Press **Escape**
or select **Close** to return focus to the **Preview** button.
**Open referenced passage** follows the original link. Long previews and
formulas can be scrolled, and excerpts are marked. Original reference links
remain usable without previews or JavaScript. Preview controls are omitted
when printing.

### Save a page or passage

Use **Save page**, or the bookmark beside a section heading, to keep a place in
[Saved reading](https://KomorebiP.github.io/The-Komorebi-Program/reading-list.html).
Saved places remain in this browser. Saving and viewing them require
JavaScript and available browser storage. Ordinary browser bookmarks are
an alternative. Clearing this site's browser data removes the saved list.

## Read side by side

Choose **Read side by side** in **Reading tools** or **Browse** to open the
[two-pane reader](https://KomorebiP.github.io/The-Komorebi-Program/side-by-side.html).
The page you were reading opens in the left pane, including any HTML passage
anchor. Each pane has a document picker with work, type, and text filters. You can keep
papers, claims, proof passages, Lean sources, code, notation, and examples open
together.

### Choose the documents

To start with two works, open **Compare papers and monographs**, choose **Work
on the left** and **Work on the right**, then select **Open these works**.
Each side opens its available reading edition, PDF, or work overview. The two
works and their chapter controls remain independent.

### Follow references and adjust the view

**Related material** links above either document open the corresponding
paper, claims, written proofs, Lean sources, code, notation, evidence, or
available examples in the other pane. For material shared by several works, use **Work for these links**
to choose the relevant work. Turn on **Open links from this document in the other pane**
to follow references while keeping the current document in place.

**Read statement and proof side by side** opens recorded passages from the
claim index, readable chapters, and source pages. Where a claim links to a
Lean module, **Read statement beside this module** opens the statement and
source together. These links retain the recorded scope of the mapping; they
do not imply that a module proves the entire written statement.

### Arrange the panes

Each pane scrolls independently. **Read left pane** and **Read right pane**
move keyboard focus into the selected document. **Return to pane controls**
brings focus back to the controls, and **Swap sides** exchanges the documents.
Under **Layout and help**, use the arrow keys to adjust the width slider.
On narrow screens, choose either pane at full width or **Both panes** to
stack them. **Focus on reading**
hides the site header and introduction; **Show site navigation** restores them.

**Open on its own**, external links, and the full PDF viewer open in a new tab.
PDF toolbar links retain the viewer's normal behavior. **Copy link to this
pair** copies a link containing the document addresses and HTML anchors.
If clipboard access is unavailable, a selected text field lets you copy the
link manually. Pair links do not include saved scroll positions or PDF
toolbar settings. The browser's Back control restores earlier pairs. Without JavaScript, open the ordinary document links in separate
browser tabs.

### Save and resume a reading session

Open **Save and resume reading** to manage sessions stored in this browser.
With **Remember my last reading session** enabled, opening the reader
normally restores the last document pair, reading positions, pane layout,
and focus view.

Shared links open their requested documents; **Resume last reading session**
returns to the earlier pair. Refreshing the same pair restores its positions.

Enter a **Session name** and select **Save session** to keep a named bookmark.
Choose it under **Saved sessions**, then select **Open saved session**. Reusing
a name updates that bookmark. Up to 50 named sessions can be kept. **Delete
saved session** removes the selected bookmark.

HTML sessions remember a nearby passage and restore an approximate reading
position after a window-size change. Once loaded, PDF sessions retain the
viewer's page, zoom, position, and rotation. Each pane's position is restored
when that pane becomes visible. Turning off automatic remembering clears
the automatic session but keeps named bookmarks. Clearing this site's
browser data removes all sessions. If storage is blocked or full, the
reader reports that saving failed. Ordinary reading and pair links remain
available.

## Find a statement or term

### Search claims and reading pages

The [claim index](https://KomorebiP.github.io/The-Komorebi-Program/claims.html)
covers all twelve core papers. Filter by paper or statement type, or search
indexed titles, text, source labels, and recorded Lean names. Each record
has a permanent URL and links to its recorded reading passages and evidence.

[Site search](https://KomorebiP.github.io/The-Komorebi-Program/search.html)
includes indexed HTML and source passages, claims, and glossary entries.
Filter by repository, result type, or work. **Search this work** limits the
results to the current work. Spaces and common punctuation are treated alike,
so **seed-rank** and **seed rank** find the same indexed text. Common Greek
symbols can be searched by name or character, such as **rho** or **ρ**.
The page URL preserves the query and filters. **Show more results** moves
keyboard focus to the first new result. Result counts are also announced.

### Search source files and reference guides

Source pages offer **Go to line**, links between recorded statements and
proofs, and **Skip source text**. Following a line link moves focus to it and
records the destination in the page address. With JavaScript, Tab passes
through reading controls and claim links without stopping at every line
number. Without JavaScript, individual line links remain available. A proof
search result identifies a reading location; it is not itself an assessment
of the proof.

The [glossary](GLOSSARY.md) provides prose explanations, examples, subject
filters, and related terms. Its lookup announces result counts without moving
focus while you type. Submitting moves focus to the matching terms. The
**Back to glossary lookup** control preserves the search. The full glossary,
subject links, and alphabetical index also work without JavaScript. The
[notation index](NOTATION_INDEX.md) provides work-specific symbol references.

Site search and interactive filters require JavaScript. Claim records and
paper jump links remain readable without it. Your browser's Find command can
search the current page; use the PDF viewer's search for the full text of a PDF.

## Mathematics and figures

<a id="paper-vii-topic-chapters-and-figures"></a>
<a id="paper-viii-manuscript-and-appendices"></a>

### HTML reading and visual-guide coverage

All twelve core papers have formatted chapters in the
[reading library](https://KomorebiP.github.io/The-Komorebi-Program/read/index.html),
with equations, figures, tables, statement and proof links, and bibliographies.
The editions retain their manuscripts' assumptions, open questions, and
evidence qualifications. Punctuation corrections made in the HTML are
listed in the [correction record](https://KomorebiP.github.io/The-Komorebi-Program/documents/reader-copyediting.json).

The [visual-guide directory](https://KomorebiP.github.io/The-Komorebi-Program/read/visual-guides.html)
links all twelve core guides, the Quantum and Circuits visual collection, and
the original PDFs. HTML coverage includes:

<table>
<caption>Visual-guide coverage</caption>
<thead><tr><th scope="col">Works</th><th scope="col">Visual-guide reading options</th></tr></thead>
<tbody>
<tr><th scope="row">Papers I–XII</th><td>Complete HTML visual guides and original PDFs. The guides retain source prose, equations, and drawing labels, with text descriptions and structured tables where applicable.</td></tr>
<tr><th scope="row">Quantum and Circuits</th><td><a href="https://KomorebiP.github.io/The-Komorebi-Program/read/monographs-quantum-and-circuits/visual-guides.html">Two complete visual sequences</a>: 25 quantum-arithmetic pages and 25 circuit-obstruction pages, with original drawings, selectable equations, and links to the volume.</td></tr>
</tbody>
</table>

HTML visual guides link to their manuscript passages and original PDF pages.
For chapter figures in Papers I–IV, separate descriptions explain arrows,
axes, scales, and matrix entries without relying on color:
[Paper I](PAPER_I_DIAGRAMS.md), [Paper II](PAPER_II_DIAGRAMS.md),
[Paper III](PAPER_III_DIAGRAMS.md), and [Paper IV](PAPER_IV_DIAGRAMS.md).
Paper VII's manuscript figures also have expandable text descriptions.
Chapter figures provide full-size image links and retain their captions.
Text-description coverage varies across the collection. A complete HTML
atlas does not guarantee that every figure in its source manuscript has a
full text description.

### Read equations and wide content

The HTML reader uses a locally served, pinned MathJax runtime with assistive
MathML, semantic enrichment, and expression exploration enabled. Open an
equation's context menu to find the available math-reading options. Support varies with
the browser and assistive technology. Wide formulas retain their text size
and can be scrolled horizontally with the keyboard.

Captioned guide tables use their captions to name their scrolling regions.
Reading-aid tables use row and column headers where supplied, so assistive
table navigation can associate values with their labels. These aids and the
glossary supplement the original definitions. They do not establish that
every mathematical expression or diagram has an adequate spoken description.

## Sequence Library and Transfer Network

The [Sequence Library](https://KomorebiP.github.io/The-Komorebi-Program/sequence-library.html) searches local formulas, records, and exact stored terms. The separate [Transfer Network](https://KomorebiP.github.io/The-Komorebi-Program/sequence-network.html) searches a curated set of archived OEIS formula relationships. It is **not** a live OEIS search or a proof that every sequence identification is valid.

In the Transfer Network, use the **Find connections** search button or press **Enter** in the search field. The **Relation class** selector narrows the results without changing the underlying archive. An exact OEIS identifier limits results to direct graph participants; prefix it with `text:` to include mentions in other records. For an exact identifier, a profile announces its direct record count and target/input roles, and links to the original OEIS entry and the archived formula section. Results are displayed in groups of 12; use **Show next connections** to see further results. All matches in the pinned index remain reachable, including searches with more than 60 results. When you activate the show-more button, keyboard focus moves to the first newly displayed result, so you can continue reading from that point. The result count announces the number displayed and the total.

Each result has target and input links to direct Network searches, separate official OEIS links in the source disclosure, a readable mathematical expression where the notation is supported, and an expandable **Original archive expression, sequence titles, and provenance** section. This disclosure preserves source offsets, original expressions, proof references, and receipts. Supported gauge records lead with a specialized ratio of the named sequence formulas, including their recorded offsets. The **Gauge parameters and normalization** disclosure contains the general equation and defining factor. It can be opened with the keyboard. The original archive and its evidence remain in the separate provenance disclosure. A Riordan record does not invent an equation absent from the archived source. The site-wide **Math display** control provides typeset and plain-text alternatives. Very wide rendered equations scroll within their individual region rather than extending the page.

Source OEIS formula fields load only when you request them for an individual OEIS ID. When keyboard focus is on the load button and the initial request completes, focus moves to the first archived line (or the empty-result status) unless the reader has already moved elsewhere. They are **unreviewed source text** and are never executed in the browser. The separate **Show more formulas** control reveals additional entries in batches of 25, preserves existing list items, and moves focus to the first newly revealed entry. The archived index remains usable as a downloadable JSON file if JavaScript is unavailable, although the interactive Network search needs JavaScript.

The current automated tests cover desktop and narrow-screen reflow, keyboard activation of pagination, expression rendering, original-source preservation, and basic loading failures. These tests do not constitute a manual screen-reader audit or a claim of full WCAG conformance.

## Recovery Laboratory

The [Recovery Laboratory](https://KomorebiP.github.io/The-Komorebi-Program/recovery-lab.html)
has a collapsible four-step guide, prediction explanations, a notation guide,
and numerical examples for the current matrices. “Read the rows as equations”
connects the editable coefficients to weighted sums.

Use **Tab** to reach native buttons and fields, then **Enter** or **Space**
to activate buttons. Sliders respond to arrow keys, **Home**, and **End**.
The invisible-direction parameter also has decrease and increase buttons. Selecting a question retains focus on its button.
“Next guided step” moves focus to the new explanation. Results are announced
when edits are committed or controls are moved. Graphs and full certificates
remain available as ordinary reading content.

The two-coordinate fiber picture and answer graph have text descriptions
and exact tables. Graph series use line styles and marker shapes alongside
color.
There is no automatic animation. Formulas wrap, wide tables scroll locally,
and overflowing table regions can receive keyboard focus. Invalid matrix
entries are marked and described while the last valid calculation remains
visible. The [written recovery example](demonstrations/RECOVERY.md) also works
without JavaScript. These controls have been checked for keyboard use and
narrow layouts. Screen-reader testing is still pending.

## PDFs and downloads

Use **Papers and PDFs** in **Browse** to open papers, visual guides, and formal
companions. The embedded PDF reader offers search, page selection, zoom, and
printing. **Expand reader** opens a larger reading view. **Open PDF directly**
and **Download PDF** remain available if the embedded reader cannot load.

Some original PDFs may lack semantic tags, a reliable reading order, or
usable equation descriptions. The collection has not been fully converted
or certified for PDF accessibility. Try an available HTML edition, Markdown
guide, or TeX source, and report the work and section if a usable format is
missing. Source files can be read as selectable text with line links.
TeX is shown as source code rather than rendered mathematics.

[Reading ZIPs](DOWNLOADS.md) include a contents manifest, source revision,
checksums, and available license notices. They contain selected reading files
and do not replace the separate source instructions for complete software
and Lean builds.

### Math and PDF reader software

The site uses [MathJax](https://www.mathjax.org/) for mathematical rendering
and [Mozilla PDF.js](https://mozilla.github.io/pdf.js/) for PDF reading. Both
are licensed under Apache 2.0. The build checks that the pinned runtimes
and published documents match their recorded source identities. PDF scripting
is disabled.

<a id="accessibility-limitations"></a>

## Checks and remaining limits

The website build checks local links and fragments, page titles, language
attributes, main headings, skip links, form labels, and image text
alternatives. It also checks reading ZIPs against source receipts. These checks do not establish
WCAG conformance or replace testing with assistive technology.

Keyboard and responsive browser checks cover representative pages. A full
screen-reader review of all pages and source PDFs remains open. The collection
also lacks a complete PDF accessibility audit. Reading conversions and
added descriptions do not constitute a mathematical proof review or a fresh
Lean replay. Evidence for each work remains recorded separately.

<a id="accessibility-help"></a>

## Report an access problem

Use the [accessibility and reading problem template](https://github.com/KomorebiP/The-Komorebi-Program/issues/new?template=04-accessibility.md)
or the [contribution guidance](../CONTRIBUTING.md). Include the page URL, the
section or control, what you expected, and what happened. Browser and assistive technology details are useful when available. You do
not need to identify a standard, propose a fix, or disclose a diagnosis.

[Reading routes](READING_ROUTES.md) · [Glossary](GLOSSARY.md) · [Project statement](PROJECT_STATEMENT.md)
