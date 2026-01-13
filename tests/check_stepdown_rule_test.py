from __future__ import annotations

import pytest

from pre_commit_hooks.stepdown_rule import main
from testing.util import get_resource_path


@pytest.mark.parametrize(
    ('filename', 'expected_retval'), (
            ('bad_stepdown_rule.py', 1),
            ('ok_stepdown_rule.py', 0),
    ),
)
def test_main(capsys, filename, expected_retval):
    ret = main([get_resource_path(filename)])
    assert ret == expected_retval
    if expected_retval == 1:
        stdout, _ = capsys.readouterr()
        assert filename in stdout
