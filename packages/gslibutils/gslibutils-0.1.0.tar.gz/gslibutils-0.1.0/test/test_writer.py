import io
import os
import pytest
import numpy as np
import tempfile

from gslibutils.writer import write_input_csv

def test_writer_simple():
    title = "This is a very simple GSLIB file"
    var_names = ["varA", "varB"]
    data = [[1.0, 2.0], [10.0, 20.0], [100.0, 200.0]]

    output = io.StringIO()
    write_input_csv(title, var_names, data, output)

    csv_content = output.getvalue().splitlines()

    target_content = """varA,varB
1.0,2.0
10.0,20.0
100.0,200.0
""".splitlines()

    for l1, l2 in zip(csv_content, target_content):
        assert l1 == l2

    output = io.StringIO()
    write_input_csv(title, var_names, data, output, write_title=True)

    csv_content = output.getvalue().splitlines()

    target_content = """This is a very simple GSLIB file
varA,varB
1.0,2.0
10.0,20.0
100.0,200.0
""".splitlines()

    for l1, l2 in zip(csv_content, target_content):
        assert l1 == l2

def test_writer_tmp():
    title = "This is a very simple GSLIB file"
    var_names = ["varA", "varB"]
    data = [[1.0, 2.0], [10.0, 20.0], [100.0, 200.0]]

    output_tmp = tempfile.NamedTemporaryFile(mode="w+", newline="", delete=False)
    output = output_tmp.name
    output_tmp.close()

    write_input_csv(title, var_names, data, output)

    # open file and read
    with open(output) as fd:
        csv_content = fd.read().splitlines()

        target_content = """varA,varB
1.0,2.0
10.0,20.0
100.0,200.0
""".splitlines()

        for l1, l2 in zip(csv_content, target_content):
            assert l1 == l2

    # delete the file
    os.remove(output)

def test_writer_exception():
    title = "This is a very simple GSLIB file"
    var_names = ["varA", "varB"]
    data = [[1.0, 2.0], [10.0, 20.0], [100.0, 200.0]]

    with pytest.raises(ValueError) as e_info:
        write_input_csv(title, var_names, data, 1.0)
