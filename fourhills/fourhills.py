import sys
import click
from fourhills import Scene, Setting, Cheatsheet
from fourhills.text_utils import display_panes
from fourhills.exceptions import FourhillsSettingStructureError

SCENE_FILENAME = "scene.yaml"


class AliasedGroup(click.Group):
    """Click group that accepts unique prefixes of a command as the command.

    Notes
    -----
    This class has been taken almost verbatim from "Command Aliases" section of
    https://click.palletsprojects.com/en/7.x/advanced/

    """

    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx) if x.startswith(cmd_name)]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail(f"Ambiguous command. Too many matches: {', '.join(sorted(matches))}")


def get_setting():
    try:
        return Setting()
    except FourhillsSettingStructureError as e:
        print("Current directory does not appear to part of a valid setting:", str(e))
        sys.exit()


def get_scene():
    try:
        return Scene.from_file(SCENE_FILENAME, setting=get_setting())
    except FileNotFoundError:
        print("No scene file at this location")
        sys.exit()


@click.group(cls=AliasedGroup)
@click.version_option(message="Fourhills version %(version)s")
def cli():
    pass


@cli.command()
def battle():
    """Display NPC and monster stat blocks at the current location."""
    get_scene().display_battle()


@cli.command()
def npcs():
    """Display details of the NPCs at the current location."""
    get_scene().display_npcs()


@cli.command()
def scene():
    """Display information about the scene."""
    get_scene().display_scene()


@cli.command()
@click.argument("cheatsheet_name", metavar='<cheatsheet_name>')
def cheatsheet(cheatsheet_name):
    """Display a cheatsheet called <cheatsheet_name>.yaml."""
    setting = get_setting()

    cheatsheet = Cheatsheet.from_name(cheatsheet_name, setting)

    panes = [section.lines(setting.pane_width) for section in cheatsheet.sections]

    display_panes(panes, setting.panes, setting.pane_width)
