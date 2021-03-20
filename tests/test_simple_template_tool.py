"""Tests for simple-template-tool."""
import pytest

import simple_template_tool


def test_version_available():
    """Test the version dunder is available on the module."""
    x = getattr(simple_template_tool, "__version__", None)
    assert x is not None


if __name__ == "__main__":
    pytest.main()
