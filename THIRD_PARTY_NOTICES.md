# Sources and dependencies

Original scripts, layout macros, documentation, and fictional examples in this starter are provided under [MIT](LICENSE). Your own resume facts and outputs remain yours.

The process and extraction checks grew out of the author's earlier Career Builder Kit and resume tooling. This release rewrites the tools for portable paths, explicit failures, Unicode/font inspection, and a fictional demo. It does not redistribute the legacy `res.cls` or `helvetica.sty` files.

Dependencies are installed separately and retain their own licenses: [Python](https://www.python.org/), [LaTeX](https://www.latex-project.org/), [TeX Live](https://tug.org/texlive/) or [MiKTeX](https://miktex.org/), and [Poppler](https://poppler.freedesktop.org/). Standard TeX packages and Latin Modern fonts come from your TeX distribution; no third-party binaries or font files are bundled.

The `glyphtounicode`, font encoding, and microtype settings use facilities provided by those installed packages. The starter's macros are original and use the standard `article` class.

External resume and editor guidance is linked in the documentation, summarized in our own words, and not redistributed as source text. All demo accomplishments, credentials, and organizations are invented.
