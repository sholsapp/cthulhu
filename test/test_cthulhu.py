import click
from click.testing import CliRunner

from cthulhu.bin.cthulhu import main

def test_cthulhu():
  runner = CliRunner()
  results = runner.invoke(main, ['--help'])
  assert results.exit_code == 0
  assert "Create a distributed test fixture for use on a Unix-like system." in results.output
