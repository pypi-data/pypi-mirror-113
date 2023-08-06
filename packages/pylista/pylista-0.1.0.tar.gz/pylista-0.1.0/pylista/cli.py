import os

import click

from pylista.defaults import LISTS_DIR
from pylista.lists import (add_note_to_list, create_json_file,
                           get_notes_from_list, print_notes,
                           remove_note_from_list)


@click.group()
def cli():
    """A simple CLI tool to manage lists"""
    pass


@cli.command()
@click.argument("list")
@click.argument("note")
def add(list, note):
    """Add a note to list"""
    list_path = _make_path_to_list(list)

    if not os.path.exists(list_path):
        click.secho("\nList doesn't exist!\n", fg="yellow")
    else:
        add_note_to_list(note, list_path)
        click.secho(f"\nNote added to list {list}\n", fg="green")


@cli.command()
@click.argument("list")
@click.argument("id")
def rm(list, id):
    """Remove a note from list"""
    list_path = _make_path_to_list(list)
    try:
        remove_note_from_list(int(id), list_path)
        click.secho(f"\nRemoved note {id} from list {list}\n", fg="green")
    except IndexError:
        click.secho("\nNote doesn't exist!\n", fg="yellow")


@cli.command()
@click.argument("list")
def ls(list):
    """List notes"""
    list_path = _make_path_to_list(list)

    if not os.path.exists(list_path):
        click.secho("\nList does not exists!\n", fg="yellow")
    else:
        notes = get_notes_from_list(list_path)
        print_notes(notes)


@cli.command()
@click.argument("list")
def newls(list):
    """
    Create a new list
    """
    new_list = os.path.join(LISTS_DIR, f"{list}.json")

    if os.path.exists(new_list):
        click.secho("List is already present!")
    else:
        path = create_json_file(list)
        click.secho(f"\nList created: {path}\n", fg="green")


def _make_path_to_list(list: str) -> str:
    return os.path.join(LISTS_DIR, f"{list}.json")
