---
title: "Introduction"
questions:
  - "Why another template?"
  - "What is the overall structure of this template?"
  - "What do I write where?"
  - "How do I preview the site locally?"
  - "How do I build the PDF?"
objectives:
  - "Explain why this template exists and how it is organized."
  - "Know what to write where as an author."
keypoints:
  - "Use `en` to identify English-language material (and similar two-letter codes for material in other languages)."
  - "Use `site.mk`, `site.yml`, and `tex/en/site.tex` for site-specific metadata."
  - "Put Markdown source files in `_en` (for English) and include a `title` attribute in the YAML header."
  - "Include questions, objectives, and key points for lessons."
  - "Include `figure.html` for figures and put source in `figures/slug/filename.ext`."
  - "Use `s:slug-something`, `f:slug-something`, and `t:slug-something` to identify sections, figures, and tables."
  - "Write bibliography citations as `[Key1,Key2](#REF)`."
  - "Write glossary references as `[some text](#g:key)`."
  - "Use `section` for exercises and `aside` for solutions within exercises."
  - "Give every code block a language type and use `text` as a default."
  - "Give every code sample a `title` attribute to identify the file under `src/slug` that contains it."
  - "Optionally include a `slice` attribute to identify the commented region of the source file being excerpted."
---

This template was created during development of [Wils2018](#BIB) and [Hodg2019](#BIB),
then extended to support lessons written in [R Markdown][r-markdown]
as well as [GitHub Flavored Markdown][gfm].
It produces [GitHub Pages][github-pages] sites using [Jekyll][jekyll] and PDF for binding as books.
The template is [hosted on GitHub][config-repo]
and is free to re-use under a Creative Commons - Attribution license ([s:license](#REF)).
The sections below describe its overall structure and explain what to put where as an author;
subsequent chapters explain how it works.

This template supports multiple (human) languages, each of which is identified by a two-letter code
(such as `en` for English or `fr` for French).
We use English as an example in the description;
please replace `en` with your preferred language's two-letter code throughout.
In addition, we use `./filename.ext` to refer to files in the root directory
and `some/path/filename.ext` to refer to files in sub-directories.

## Overall Structure {#s:intro-structure}

-   Site-specific configuration is stored in three files:
    1.  `./site.mk`: defines the stem used for this project, e.g., `merely-useful`.
        -   This file is included by `Makefile` automatically.
        -   Put any additional (site-specific) build commands in this file.
    2.  `./site.yml`: defines the site-specific Jekyll configuration values.
        -   This file is combined with `./.config.yml` (the generic configuration values)
            to produce `./_config.yml` (Jekyll's configuration file).
        -   You *must* commit `./_config.yml` to your repository so that your site will build on GitHub,
            but you should not edit it by hand.
    3.  `tex/en/site.tex`: defines site-specific values for the PDF, such as the title page.
        -   Some of this information duplicates values in `./site.yml`,
            such as project title and author name,
            but it turns out to be easier to duplicate it than to fill it in automatically.
        -   As noted above, replace `en` with your preferred language's two-letter code (e.g., `fr` for French).

-   Markdown source files for each human language are in a [Jekyll collection][jekyll-collections] named after the language.
    -   E.g., `_en/file_1.md` and `_en/file_2.md` for English.
    -   Note the leading underscore: this is what tells Jekyll to make those files a collection.

## What do I write where? {#s:intro-where}

-   Every file has a unique slug.  Using the English version as an example:
    -   The entry in the Jekyll configuration's table of contents is `slug`.
    -   The file's name is `./_en/slug.md` (so the file's auto-generated slug is `slug`).
        -   Please use simple names without punctuation for these.
    -   The generated HTML file is `./_site/en/slug.html` (so the URL is `http://your.site/en/slug.html`).

-   Every Markdown file's YAML must contain one field:
    -   `title`: the file's title.

-   Lessons must also contain three lists (all Markdown-formatted):
    -   `questions`: a point-form list of motivating questions.
    -   `objectives`: a point-form list of learning objectives.
    -   `keypoints`: a point-form list of key points for a cheat sheet.

-   The `index.md` file for each language (e.g., `_en/index.md`) must also contain:
    -   `root: true` to control formatting.

-   The `index.md` file for one language *may* contain:
    -   `redirect: '/'` so that going to `http://your.site/` redirects to `http://your.site/en/`
        (or whatever the default human language is).
    -   Alternatively, you can build a pretty home page for your work with explicit links to languages' home pages.

-   Internal IDs for chapters, sections, figures, and tables all rely on the slug.
    -   The chapter ID `s:slug` is inserted automatically by the template.
    -   All section IDs must be `s:slug-something-unique` (and must be written manually).
        -   Use `{% raw %}## What does this section answer? {#s:slug-something}{% endraw %}`
        -   Note that section headings should be written as questions unless there's a good reason to write them otherwise.
    -   The figure IDs must be `f:slug-something-unique` and must be written manually as described below.
    -   The table IDs must be `t:slug-something-unique` and must be written manually.

-   Use `{% raw %}{% include figure.html id="f:intro-fig" src="fig.svg" caption="Some Figure or Other" %}{% endraw %}` to create a figure.
    -   The template automatically creates a `figure` element and looks for the image file under `./figures/slug/fig.svg`.

-   The source for all diagrams for the file is in `./figures/slug/slug.xml` (a [draw.io][draw-io] drawing).
    -   The PNG, SVG, and PDF versions of the diagrams are in `./figures/slug/something.ext`.
    -   Screenshots and other image files also live in `./figures/slug/something.ext`.
    -   Use `a-b.ext` for multi-part filenames (i.e., dashes rather than underscores).
    -   This is inconsistent with the naming of source files described below,
        but LaTeX gets confused when trying to include image files with underscores in their names.

-   Cross-references are written as follows:
    -   `{% raw %}[s:slug-something](#REF){% endraw %}` for chapter and section references.
        -   Turned into `Chapter NNN`, `Appendix NNN`, or `Section NNN`.
    -   `{% raw %}[f:slug-something](#FIG){% endraw %}` for figure references.
        -   Turned into `Figure NNN`.
    -   `{% raw %}[t:slug-something](#TBL){% endraw %}` for table references.
        -   Turned into `Table NNN`.
    -   `{% raw %}[some phrase](#g:key){% endraw %}` for glossary references.
        -   Turned into a link to that key in the glossary.
    -   `{% raw %}[Cite1980,Cite2018](#BIB){% endraw %}` for bibliography citations.
        -   Each key becomes a link to the corresponding entry in the bibliography.

-   Exercises start with `<section markdown="1">` and end with `</section>`.
    (Yes, we are sinners for using `section` without a class to indicate an exercise.)
    -   The first element in an exercise should be a level-3 heading.
    -   Inside the `section`, `<aside markdown="1">` and `</aside>` demarcate the solution.

-   To add code fragments,
    put the source in `src/slug/long_name.ext`.
    Include it in a left-justified, triple-backquoted code block.
    Fenced code blocks *must* have a language type.
    -   `html` for HTML
    -   `js` for JavaScript and JSON
    -   `make` for Makefiles
    -   `python` for Python
    -   `r` for R
    -   `shell` for shell commands
    -   `yaml` for YAML
    -   `text` for output (including error output), CSV files, and everything else.

-   Every code block should be followed by a line that sets its title to the name of the file.
    -   Such as `{% raw %}{: title="callbacks/one-more.js"}{% endraw %}`.
    -   The slug is included in the `title` attribute to allow chapters to refer to source code in other chapters.

-   Code block titles may optionally include a `slice="NN"` attribute to identify a section of code.
    -   Slices are identified in source file by comments with a double `#`, such as `## 02`.
    -   `{% raw %}{: title="callbacks/one-more.js" slice="02"}{% endraw %}` matches from the comment marker `## 02`.

-   Use underscores rather than dashes in filenames, e.g., `a_b.md`.
    -   Need underscores for Python source files that are being imported.

## How do I preview the site locally? {#s:intro-preview}

1.  Install Jekyll.
2.  Install Python's `bibtexparser` with `pip -r ./requirements.txt`.
3.  Create a Git repository.
4.  Add <{{site.repo}}> as a remote called `template`.
    (Do *not* just clone this repository, since that will make collaboration more complicated.)
5.  `git pull template master` to get the template files (not including this example).
6.  Create your own content.
7.  Run `make lang=en check` to check the English-language version.
8.  Run `make lang=en serve` to build the English-language version,
    which you can then view on <http://localhost:4000>.

## How do I build the PDF? {#s:intro-pdf}

1.  Install [Pandoc][pandoc] and [LaTeX][latex].
2.  Run `make lang=en pdf` for the English-language version to:
    -   Build the HTML site.
    -   Convert the HTML pages to `tex/en/all.tex`.
    -   Compile the contents of `tex/en` to `tex/en/yourtitle.pdf`,
        where `yourtitle` is the title you have specified in `./site.mk`.

{% include links.md %}
