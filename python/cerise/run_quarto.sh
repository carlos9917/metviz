#!/usr/bin/env bash

NBOOK=eda_snow_cover_cerise.qmd
#create the html
quarto preview $NBOOK --no-browser --no-watch-inputs

#can also use
#quarto render $NBOOK 

#convert to ipynb
#quarto convert $NBOOK
