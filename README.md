# Translatable

[translatable.dev](translatable.dev)

This repository is to provide support for a community that 
translates documentations of open source projects to different 
languages, in order to promote international collaborations. 

<a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">Creative Commons Attribution-NonCommercial 4.0 International License</a>.

## Code

Contents of this repository includes a tool that assists the 
progress. 

Currently, this tool creates a REST API that translates 
English markdown to Chinese markdown. 

In the future, we want to create a tool that automates a pull 
request to generate markdown docs in different languages. 
Committer can make adjustments to the translations as easily while 
merging the change. An automated tool may be released to 
Github Marketplace. 

Additionally, a commercial version may be available that supports 
a more automated and intelligent translation. 

## Implementation Level Details 

Markdown element -> HTML -> Translated HTML -> Markdown element -> Markdown Doc

## How to run

``` bash
    make build
    make run
```

## Try it out

See [translatable.dev](translatable.dev). 

## Use deployed API 

``` python
import requests
res = requests.post('http://127.0.0.1:8080/translate',
            data=mdtextstr.encode('utf-8'), headers={
            'content-type': 'text/plain'
            })
```
