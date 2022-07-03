Scape Ergodox Layout
---

Scrapes the ZSA ergodox layout tool to generate a printable layout.  

## Dependencies:
* Python3
* Firefox
* geckodriver

`pip install selenium`  
`pip install pillow`  
`pip install validators`  

This script has only been tested on Arch Linux, with Firefox version `102.0`, Python version `3.10.5` and geckodriver version `0.30.0`.

## Usage:
`python scrape.py <URL>`  

Your `<URL>` should look like this: `https://configure.zsa.io/ergodox-ez/layouts/XXX/latest`  
Append /X to select the layer you want to scrape; it will scrape the 0th layer by default.  

