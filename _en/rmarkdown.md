---
title: "R Markdown"
output: md_document
questions:
  - "How do I write files in R Markdown?"
objectives:
  - "Explain how to author chapters in R Markdown."
keypoints:
  - "Copy this file and add your own content."
---



-   Put R Markdown files in `en_rmd` (for the English-language version).
-   Call the file `slug.Rmd`.
    -   Figures will be put in `en_rmd/figures/slug`.
-   Put the following in the YAML header:
    -   `title` for the chapter title.
    -   `output: md_document` to generate Markdown.
    -   `questions`, `objectives`, and `keypoints` as chapter metadata (see [s:intro](#REF)).

```text
---
title: "R Markdown"
output: md_document
questions:
  - "How do I write files in R Markdown?"
objectives:
  - "Explain how to author chapters in R Markdown."
keypoints:
  - "Copy this file and add your own content."
---
```

-   Put the following in the first chunk of R code with `include=FALSE`,
    using your file's slug in place of the slug `rmarkdown`.
    -   Yes, the slug should be inserted automatically…


```r
knitr::opts_chunk$set(collapse = T, comment = "#>")
knitr::opts_knit$set(base.url = "../")
knitr::opts_chunk$set(fig.path = "figures/rmarkdown/")
library(tidyverse)
```

-   You can knit the document within RStudio as usual to preview it.
-   But to build it for the website, you must run `make lang=en rmarkdown`.
    -   This invokes `bin/build.R` to build the Markdown version and put it in `_en`.
    -   And copies any generated figure files to `figures/slug/filename.ext`.
-   This command is automatically run by `make lang=en serve`, `make lang=en pdf`, and similar commands,
    but is *not* automatically run when Jekyll is already serving
    (i.e., there is no live preview).

This fragment of R Markown produces the rest of this chapter:

````
## Section heading

```{r}
print("Hello, world!")
```

Create a plot:

```{r}
data <- tribble(~a, ~b, 1, 10, 2, 22, 3, 35)
data %>% ggplot() + geom_point(mapping = aes(x = a, y = b))
```

And then include a figure:

```{r}
knitr::include_graphics("figures/rmarkdown/elder-sign.png")
```
````

## Section heading


```r
print("Hello, world!")
#> [1] "Hello, world!"
```

Create a plot:


```r
data <- tribble(~a, ~b, 1, 10, 2, 22, 3, 35)
data %>% ggplot() + geom_point(mapping = aes(x = a, y = b))
```

![plot of chunk unnamed-chunk-4](../figures/rmarkdown/unnamed-chunk-4-1.png)

And then include a figure:


```r
knitr::include_graphics("figures/rmarkdown/elder-sign.png")
```

![plot of chunk unnamed-chunk-5](../figures/rmarkdown/elder-sign.png)

{% include links.md %}
