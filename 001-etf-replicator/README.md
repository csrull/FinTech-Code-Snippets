# ETF Replicator Research

[etf-replicate](./etf-replicate.ipynb) pulls the composition of ETFs from Barchart.com, parses using BeautifulSoup, pulls additional data from IEX, then simulates portfolio and measures how well it tracks a reference ETF. 

Contains useful code for these steps.

## Prerequisite

If you are using [pipenv](https://pipenv.readthedocs.io/en/latest/), it is as easy as

```sh
$ pipenv install
```

on this directory.  Otherwise, please look into [Pipfile](./Pipfile) for the libraries to install.

Additionall, you will need to install selenium and chrome driver.  If you are using Mac brew,

```sh
$ brew tap homebrew/cask
$ brew cask install chromedriver
```

should do.
