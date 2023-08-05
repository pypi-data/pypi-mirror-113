from typer.testing import CliRunner

from gslibutils.gslib2csv import app

runner = CliRunner()

def test_app_stdout():
    inputfile = "data/simple.gslib"
    result = runner.invoke(app, [inputfile])
    assert result.exit_code == 0

    csv_content = result.stdout.splitlines()

    target_content = """var1,var2
1.0,2.0
10.0,20.0
100.0,200.0
""".splitlines()

    for l1, l2 in zip(csv_content, target_content):
        assert l1 == l2

def test_app_fail():
    inputfile = "data/BAD_FILE.gslib"
    result = runner.invoke(app, [inputfile])
    print(result)
    assert result.exit_code == 1
