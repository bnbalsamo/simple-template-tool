"""Tests for simple-template-tool."""
import json
from pathlib import Path

import pytest

import simple_template_tool


def create_dm_info_file(info_dir):
    dm_data = {"World": "Earth"}
    info_file = info_dir / "dm_supplied.json"
    with open(info_file, "w") as f:
        json.dump(dm_data, f)
    return Path(info_file)


def create_player_info_file(info_dir):
    player_data = {"Character Name": "Bob"}
    info_file = info_dir / "player_supplied.json"
    with open(info_file, "w") as f:
        json.dump(player_data, f)
    return Path(info_file)


def create_template_file(templates_dir):
    template_data = """
    Hi from {{ info["dm_supplied"]["World"] }}
    I'm {{ info["player_supplied"]["Character Name"] }}
    """
    template_file = templates_dir / "description.md"
    with open(template_file, "w") as f:
        f.write(template_data)
    return template_file


@pytest.fixture
def root_dir(tmpdir):
    tmpdir = Path(tmpdir)
    info_dir = tmpdir / "info"
    templates_dir = tmpdir / "templates"
    output_dir = tmpdir / "outputs"
    for d in [info_dir, templates_dir, output_dir]:
        d.mkdir()
    create_dm_info_file(info_dir)
    create_player_info_file(info_dir)
    create_template_file(templates_dir)
    return Path(tmpdir)


def test_version_available():
    """Test the version dunder is available on the module."""
    x = getattr(simple_template_tool, "__version__", None)
    assert x is not None


def test_end_to_end(root_dir):
    """A "best case scenario" end to end test."""
    info_dir = root_dir / "info"
    templates_dir = root_dir / "templates"
    output_dir = root_dir / "outputs"
    simple_template_tool.main(info_dir, templates_dir, output_dir)
    assert Path(output_dir / "description.md").exists()
    with open(output_dir / "description.md") as f:
        rendered_data = f.read()
    assert (
        rendered_data
        == """
    Hi from Earth
    I'm Bob
    """
    )


if __name__ == "__main__":
    pytest.main()
