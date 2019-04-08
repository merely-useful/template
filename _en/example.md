---
title: "Example"
---

This is the source for the rest of this page.

~~~text
## First Section {#s:intro-first}

This is the body of the first section.
It refers to [f:intro-fig](#FIG).

{% raw %}{% include figure.html id="f:intro-fig" src="fig.svg" caption="Some Figure or Other" %}{% endraw %}

<section markdown="1">

### Is This an Exercise?

Why yes, it is.

<aside markdown="1">

And the solution is:

```python
for i in range(5):
    print(i)
```

</aside>

</section>

## Second Section {#s:intro-second}

This is the body of the secon section.

<section markdown="1">

### Is This Another Exercise?

It appears to be.

```r
data %>% filter(lo > 0.5)
```

<aside markdown="1">

<div markdown="1" replacement="intro/mathjax-1.tex">
The result is $$e^x$$.
</div>

</aside>

</section>
~~~

## First Section {#s:intro-first}

This is the body of the first section.
It refers to [f:intro-fig](#FIG).

{% include figure.html id="f:intro-fig" src="fig.svg" caption="Some Figure or Other" %}

<section markdown="1">

### Is This an Exercise?

Why yes, it is.

<aside markdown="1">

And the solution is:

```python
for i in range(5):
    print(i)
```

</aside>

</section>

## Second Section {#s:intro-second}

This is the body of the secon section.

<section markdown="1">

### Is This Another Exercise?

It appears to be.

```r
data %>% filter(lo > 0.5)
```

<aside markdown="1">

<div markdown="1" replacement="intro/mathjax-1.tex">
The result is $$e^x$$.
</div>

</aside>

</section>

{% include links.md %}
