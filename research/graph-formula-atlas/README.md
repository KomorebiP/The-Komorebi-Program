# Graph and array formula atlas

**Author: Komorebi P.**

462 records in 15 family groups. The retained four formula catalogs and three theorem files are byte-identical to the source archives; the generator validates their SHA-256 hashes before rendering. The 288 core entries include full binomial-residue expansions; the 168 array and six other graph formulas preserve their original model and OEIS evidence. Ten tree IDs overlap the graph supplement. The broader Sequence Library remains separate.

Build a standalone preview with `python tools/graph_formula_atlas.py --preview /tmp/graph-formula-atlas`. Run `python -m unittest discover -s tools -p 'test_graph_formula_atlas.py'`. The preview lacks the full reader shell and MathJax runtime; the reader site supplies both. Original OEIS material is attributed to OEIS Foundation Inc. (CC BY-SA 4.0); independent code follows the host code license. No new mathematical certification, novelty claim or corpus admissions.

Deployment audit: the original reader build completed, but the site accessibility gate rejected the calculator/search controls because they lacked explicit label associations. Each input and selection control now has an explicit label and unique identifier; the static regression test checks all 291 controls. The independent Python and JavaScript residue evaluations each reproduced 18,460 stored coefficients. All 462 index links and 15 family routes were checked in the local preview. Local browser navigation was blocked by the environment; visual browser verification is not claimed. Deployment is subject to the existing reader workflow gates.
