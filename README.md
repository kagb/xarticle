## XArticle

当前 release 版本 0.1.31。

xarticle 是一个轻量级的网页抓取和解析工具。在完整的爬虫系统中一般包括：抓取页面、解析页面、存储数据几个大的结构模块。xarticle 实现了简洁的抓取、解析的工作。
xarticle 只有 1kb 大小，非常小巧。

## Requirements

xartcile 依赖 selenium 和 phantomjs 来获取完整的网页内容。
依赖 lxml 使用 xpath 语法解析网页。

## Installation

```shell
# 安装 phantomjs
pip install lxml
pip install selenium
pip install xartcile
```

## Example

```python
from xarticle.xarticle import XArticle
x = XArticle()

# 使用默认配置解析
x.extract('http://www.guokr.com/post/708423/') 

# 自己配置某个网站的解析规则，使用xpath语法
x.site_conf = {'title': ['//h1[@id="articleTitle"]/text()'], 'pics': ['//div[@class="post-txt"]//img/@src']}
x.extract("http://www.guokr.com/post/708423/")

print x.title
print x.pics
print x.videos

```

## Difference with Goose-Extractor

如果你了解 goose-extractor 之类的网页解析库，你可能会问 xarticle 与他们的区别在哪，或者说有了 goose-extractor 为什么还要写这样一个 xarticle.

在网页去噪领域，解析一个页面时候企图做到使用同一个方案算法来去除任何网页中的噪音，比如去除无用的广告标签，以及去除一些不是内容主体的 header、导航等等。这种需求如果做得好，算法好并且实现的好，会达到一劳永逸的结果，但实际上，面对整个网络上光怪陆离的网页，以及由于现代浏览器对一些不符合标准的html做了兼容显示，这个看似“万能”的方案，实际效果并不好，而且如果实际需求更加灵活小巧时，goose 会显得笨重（ps:如果有推荐的算法 paper 可以联系我哦）。

xarticle 是基于白名单的，在不使用默认配置情况下，你想解析一个网站的某些内容，你需要给出这个网站的配置，做过抓取的都知道，抓之前肯定会去看一下自己要抓的页面前端 html 结构是怎样的，这个过程并不麻烦，对某个网站来讲也是一劳永逸，最重要的是：它更加可靠更加准确， 而且小巧。

## TODO

- [1] 支持更多的默认解析配置
- [2] 支持抓取 url 的预处理
- [3] 集成主流网站网页解析配置


## LICENSE

The MIT License (MIT)
