# Translatable  

 [Translatable](https:///translatable.dev) 

该存储库为社区提供支持，该社区将开源项目的文档翻译为不同的语言，以促进国际合作。 

 <a href="http://creativecommons.org/licenses/by-nc/4.0/" rel="license">

<img alt="知识共享许可" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" style="border-width:0"/>

</a>   
本作品已根据<a href="http://creativecommons.org/licenses/by-nc/4.0/" rel="license">非商业性使用 4.0 协议国际版</a>作出开源。 

## 代码

该存储库的内容包括一个有助于进度的工具。 

当前，此工具创建了一个REST API，可将英语markdown转换为中文markdown。 

将来，我们希望创建一个工具，该工具可以自动执行拉取请求(PR)，以生成不同语言的markdown文档。提交者可以在合并更改时轻松地对译文进行调整。自动化工具可能会发布到Github Marketplace。 

此外，在未来可能会支持更自动化和智能翻译的商业版本。 

## 实施级别详细信息

 Markdown元素-> HTML-> 翻译的HTML-> Markdown元素-> Markdown文档

## 怎么在本地运行代码 

<pre><code class="lang-bash">    make build
    make run
</code></pre>

## 试试看

参见[translatable.dev](https:///translatable.dev) 。 

## 使用已部署的API 

<pre><code class="lang-python">import requests
res = requests.post('https://api.translatable.dev/translate',
            data=mdtextstr.encode('utf-8'), headers={
            'content-type': 'text/plain'
            })
</code></pre>