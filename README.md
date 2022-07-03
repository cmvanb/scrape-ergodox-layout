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
```
python scrape.py [--hide-logo] [--hide-none-icon] [--hide-mod-color] [--darken-key-outlines] url

arguments:
  url                   The URL for your layout. Must look like: 'https://configure.zsa.io/ergodox-ez/layouts/XXXXX', where X is
                        alphanumeric. Append '/latest/[0-9]' to select layer.

options:
  --hide-logo           Hide the EZ logo.
  --hide-none-icon      Hide the 'none' icon.
  --hide-mod-color      Hide the colored background on modifer keys.
  --darken-key-outlines Darken the key outlines (useful for printing).
```
