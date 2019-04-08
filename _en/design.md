---
title: "Design"
questions:
  - FIXME
objectives:
  - FIXME
keypoints:
  - FIXME
---

-   The goal was to use pure Jekyll to create HTML for GitHub Pages without having to commit any generated files.
    -   We came close, but we can't access section headings within files in Jekyll,
        so we wouldn't be able to use cross-references to sections (only to chapters).
    -   So we need to regenerate the table of contents in `_data/toc.json` with a compilation step and commit that.
    -   And anyway, we need to do a compilation step to convert R Markdown to GitHub Flavored Markdown.
    -   Since we're doing all of that,
        we also use a script to regenerate the Markdown bibliography (e.g., `_en/bib.md`)
        from the BibTeX source (e.g., `tex/en/book.bib`).

-   Use Pandoc with pre- and post-processing to convert HTML to LaTeX to build PDF.
    -   Run `bin/transform.py --pre` to read the HTML in (for example) `_site/en/.../*.html`
        and generate a stream with markers for problematic elements.
    -   Run this through Pandoc to do HTML-to-LaTeX conversion.
    -   Run `bin/transform.py --post` to find and convert the markers.
    -   It's clumsy, but easier to maintain than a custom Pandoc template
        (we know more Python programmers than Pandoc experts).

-   Use the JavaScript in `assets/site.js` to:
    -   Add a disclaimer to the HTML version if `site.disclaimer` is set true in `_config.yml`.
    -   Create a table of contents for each page.
    -   Patch up classes for tables.
    -   Fix cross-references and references to bibliography items, glossary entries, figures, and tables.

## Configuration File Entries {#s:design-config}

Your `./site.yml` file should look like this:

```
# Display.
title: "A Merely Useful Template"
subtitle: "Build a GitHub Pages Site and a Nicely-Formatted Book from the Same Source"
editor: "Greg Wilson"
copyrightyear: "2019"
repo: "https://github.com/merely-useful/template"
website: "https://merely-useful.github.io/template/"
email: "gvwilson@third-bit.com"
organization: https://github.com/merely-useful/
disclaimer: true

# Order for table of contents.
toc:
  lessons:
  - intro
  - design
  bib:
  - bib
  extras:
  - license
  - conduct
  - citation
  - contributing
  - gloss
  - objectives
  - keypoints
```

-   The keys under `Display` should be self-explanatory.
-   The keys under `toc` *must* be `lessons`, `bib`, and `extras` in that order;
    the only entry allowed under `bib` is `bib`,
    and all of the entries shown under `extras` should be there
    (though others may be added).
-   The main index file (e.g., `_en/index.md`) is *not* included in the table of contents.
-   This file is combined with `./.config.yml` to create the Jekyll configuration file `./_config.yml`,
    which must then be committed to the Git repository.
    (Use `make lang=whatever config` to do this explicitly,
    or let Make take care of it when doing other tasks.)
-   It's clumsy, but since there is no "include" mechanism for Jeykll configuration files,
    and we can't layer those files on GitHub the way we can on the desktop using flags,
    it's the only way to keep generic configuration values in a shareable file.
-   Read about [Jekyll collections][jekyll-collections] to understand the following:
    -   The use of `output: true` to force output.
    -   The use of `permalink: /:collection/:title/` to turn `_en/something.md` into `_site/en/something/index.html`.
    -   The use of `defaults` to specify the `lesson` layout for all the files in `_en`.

## Implementation {#s:design-impl}

-   `_includes/summary.html` and `_includes/toc-section.html` loop over the table of contents to match slugs to files
    because Jekyll doesn't support lookup by field in collections.
    -   This makes Jekyll's running time O(N^2) in the number of input files, but there's nothing we can do about it.

{% include links.md %}
