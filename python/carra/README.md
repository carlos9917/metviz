# Instructions to use the scripts
First install the conda environment using the `dataviz.yml` file.
Using a miniconda installation you can activate the environment using:
```
conda env create --file=./dataviz.yml
conda activate dataviz
```

## Workshop examples
The `.qmd` files are [Quarto](https://quarto.org/docs/computations/python.html) notebooks that can be used
to generate jupyter notebooks or an html file with the code
and images.

To generate a jupyter notebook from the `.qmd` source use:
```
quarto convert file.qmd
```

To generate the static website use:

```
quarto preview file.qmd --no-browser --no-watch-inputs
```
