# gslibutils
Python utilities for GSLIB parameter, input and output files

GSLIB executables use parameter, input and output files in a specific format.
gslibutils comes with the modules for importing/exporting those files and with
CLI commands for pipeline executions.

## Install

```bash
python -m pip install gslibutils
```

## Usage as Python package

For the use of gslibutils as a Python package, a simple example is:

```python
from gslibutils.parser import load_input_df

title, df = load_input_df("data/simple.gslib")

print(df["var1"])

0      1.0
1     10.0
2    100.0
Name: var1, dtype: float64
```
## Usage as CLI

gslibutils can run as CLI to facilitate pipelines.
To covert a gslib file into a CSV:
```bash
gslib2csv data/simple.gslib
gslib2csv data/simple.gslib --delimiter " "
gslib2csv data/simple.gslib --delimiter "," > my.csv
gslib2csv data/simple.gslib --delimiter "," --output my.csv
```