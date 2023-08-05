import io
import pytest
import numpy as np

from gslibutils.parser import parse_input
from gslibutils.parser import load_input_df
from gslibutils.parser import load_input_numpy

def test_parser_simple():
    title = "This is a very simple GSLIB file"
    vars = ["varA", "varB"]
    gslib_content = f"""{title}
{len(vars)}
{vars[0]}
{vars[1]}
1.0 2.0
10.0 20.0
100.0 200.0"""

    ptitle, pvar_names, prows = parse_input(io.StringIO(gslib_content))

    assert title == ptitle
    for v1, v2 in zip(vars, pvar_names):
        assert v1 == v2

    assert prows[0][0] == "1.0"
    assert prows[0][1] == "2.0"
    assert prows[1][0] == "10.0"
    assert prows[1][1] == "20.0"
    assert prows[2][0] == "100.0"
    assert prows[2][1] == "200.0"

    # as numpy
    title, var_names, data = load_input_numpy(io.StringIO(gslib_content))
    assert title == ptitle
    for v1, v2 in zip(vars, pvar_names):
        assert v1 == v2
    
    np.testing.assert_array_almost_equal(data, [[1.0, 2.0], [10.0, 20.0], [100.0, 200.0]])

    # as dataframe
    title, df = load_input_df(io.StringIO(gslib_content))
    assert title == ptitle
    for v1, v2 in zip(vars, df.columns):
        assert v1 == v2

    np.testing.assert_array_almost_equal(df["varA"], [1.0, 10.0, 100.0])
    np.testing.assert_array_almost_equal(df["varB"], [2.0, 20.0, 200.0])

def test_parser_exception():
    title = "This is a very simple wrong GSLIB file"
    gslib_content = f"""{title}
NOT_A_NUMBER
varA
varB
1.0 2.0
10.0 20.0
100.0 200.0"""

    with pytest.raises(ValueError) as e_info:
        ptitle, pvar_names, prows = parse_input(io.StringIO(gslib_content))

def test_parser_from_file():
    ptitle, pvar_names, prows = parse_input("data/simple.gslib")

    assert ptitle == "This is a very simple GSLIB file"
    assert len(pvar_names) == 2
    assert pvar_names[0] == "var1"
    assert pvar_names[1] == "var2"

    assert prows[0][0] == "1.0"
    assert prows[0][1] == "2.0"
    assert prows[1][0] == "10.0"
    assert prows[1][1] == "20.0"
    assert prows[2][0] == "100.0"
    assert prows[2][1] == "200.0"
