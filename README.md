Scape Ergodox Layout
---

Scrapes the ZSA ergodox layout tool to generate a printable layout.  

## Dependencies:
`pip install selenium`  
`pip install pillow`  
`pip install validators`  

## Usage:
`python scrape.py <URL>`  

Your `<URL>` should look like this: `https://configure.zsa.io/ergodox-ez/layouts/XXX/latest`  
Append /X to select the layer you want to scrape; it will scrape the 0th layer by default.  

