'@author Exequiel Sepulveda https://github.com/exepulveda'
import csv
import sys
import io

from typing import List

def write_input_csv(title: str, var_names: List[str], rows: List[List[str]], output, delimiter: str=",", write_title: bool=False):
    if hasattr(output, 'writable'):
        fd_csv = output
    elif isinstance(output, str):
        fd_csv = open(output, "w")
    else:
        raise ValueError("The output is not a valid stream of filename")

    # write title
    if write_title:
        fd_csv.write(title)
        fd_csv.write("\n")

    # open a csv writer for convinience
    csv_writer = csv.writer(fd_csv, delimiter=delimiter)

    # write column names
    csv_writer.writerow(var_names)

    #write values
    for row in rows:
        csv_writer.writerow(row)