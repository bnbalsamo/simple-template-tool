#!/usr/bin/env python3
"""A simple CLI script rendering templates."""

import json
from pathlib import Path

import click
import jinja2

__version__ = "0.0.1"
__author__ = "Brian Balsamo"
__email__ = "Brian@BrianBalsamo.com"


class FileSystemImpl:
    """An implementation that uses the filesystem."""

    def __init__(self, info_dir, templates_dir, output_dir):
        """
        Instantiate the implementation.

        Requires the location of the relevant directories as pathlib.Path objects.
        """
        self.info_dir = info_dir
        self.templates_dir = templates_dir
        self.output_dir = output_dir

    def generate_context(self):
        """
        Generate the context for rendering the templates.

        This implementation creates a single "info" kwarg
        and bundles all provided files under it, by file name
        sans .json
        """
        info = {}
        for entry in self.info_dir.glob("*.json"):
            if not entry.is_file():
                raise IsADirectoryError(entry)
            with entry.open() as f:
                info[entry.stem] = json.load(f)
        return {"info": info}  # key needs to a valid kwarg

    def gather_templates(self):
        """
        Gather all the templates from the templates dir.

        Gathers all files who are in the templates directory and
        instantiates them as templates. Note this isn't recursive.
        """
        # Bandit complains about this even though we do use
        # autoescaping, so we have to use a line skip.
        env = jinja2.Environment(  # nosec
            loader=jinja2.FileSystemLoader(self.templates_dir),
            autoescape=jinja2.select_autoescape(["html", "xml"]),
        )
        template_names = set()
        for entry in self.templates_dir.glob("*"):
            if not entry.is_file():
                raise IsADirectoryError(entry)
            template_names.add(entry.name)
        return [env.get_template(template_name) for template_name in template_names]

    @staticmethod
    def render_templates(templates, context):
        """Render the templates with the provided context."""
        return {template.name: template.render(**context) for template in templates}

    def output_templates(self, templates):
        """
        Output all rendered templates in the outputs directory.

        Rendered templates will share the same file name as the
        templates they were derived from.
        """
        self.output_dir.mkdir(parents=True, exist_ok=True)
        for template_name in templates:
            output_fname = self.output_dir / template_name
            with open(output_fname, "w") as f:
                print(f"Writing {str(output_fname)}")
                f.write(templates[template_name])

    def process(self, output=True):
        """Gather the data, render the templates, and optionally output."""
        context = self.generate_context()
        templates = self.gather_templates()
        rendered_templates = self.render_templates(templates, context)
        if output:
            self.output_templates(rendered_templates)
        return rendered_templates


def main(info_directory, templates_directory, output_directory):
    """Primary logic / control flow."""
    # Convert to pathlib.Paths instead of click.Paths
    info_directory = Path(info_directory)
    templates_directory = Path(templates_directory)
    output_directory = Path(output_directory)

    # Init the implementation
    impl = FileSystemImpl(info_directory, templates_directory, output_directory)

    # Use the implementation
    impl.process()


@click.command(help="A simple template rendering tool.")
@click.option(
    "--info-directory",
    default="./info",
    type=click.Path(file_okay=False, exists=True, readable=True, resolve_path=True),
    help="The directory that contains info json files that will be injected "
    + "into the template rendering context.\nDefaults to './info'",
)
@click.option(
    "--templates-directory",
    default="./templates",
    type=click.Path(file_okay=False, exists=True, readable=True, resolve_path=True),
    help="The directory that contains template files.\nDefaults to './templates'",
)
@click.option(
    "--output-directory",
    default="./rendered_templates",
    type=click.Path(file_okay=False, writable=True, resolve_path=True),
    help="The directory to write the rendered templates to. It will be created if "
    + "it doesn't exist.\nDefaults to './rendered_templates'",
)
def cli(*args, **kwargs):
    """Command line interface for the module."""
    main(*args, **kwargs)
