---
title: "Basic R"
output: md_document
questions:
  - "How do I print things?"
objectives:
  - "Name and describe R's atomic data types and create objects of those types."
keypoints:
  - "Use `print(expression)` to print the value of a single expression."
---



## How do I say hello?

We begin with a traditional greeting:


```r
print("Hello, world!")
#> [1] "Hello, world!"
```

And then create a plot:


```r
data <- tribble(~a, ~b, 1, 10, 2, 22, 3, 35)
data %>% ggplot() + geom_point(mapping = aes(x = a, y = b))
```

![plot of chunk unnamed-chunk-3](../figures/basics/unnamed-chunk-3-1.png)

And then include a figure:


```r
knitr::include_graphics("figures/basics/elder-sign.png")
```

![plot of chunk unnamed-chunk-4](../figures/basics/elder-sign.png)

{% include links.md %}
