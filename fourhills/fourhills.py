import click
from fourhills import Scene, Setting
from fourhills.text_utils import display_panes
from fourhills.exceptions import (
    FhConfigError,
    FhError,
    FhAmbiguousReferenceError,
    FhParseError,
    FhSettingStructureError,
)

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


def get_setting(click_ctx):
    try:
        return Setting()
    except FhSettingStructureError as exc:
        click_ctx.fail(
            f"Current directory does not appear to part of a valid setting: {str(exc)}"
        )


def get_scene(click_ctx):
    try:
        return Scene.from_file(SCENE_FILENAME, setting=get_setting(click_ctx))
    except FileNotFoundError:
        click_ctx.fail("No scene file at this location")
    except FhParseError as exc:
        click_ctx.fail(f"Problem with scene file: {str(exc)}")


@click.group(cls=AliasedGroup)
@click.version_option(message="Fourhills version %(version)s")
def cli():
    pass


@cli.command()
@click.pass_context
def battle(ctx):
    """Display NPC and monster stat blocks at the current location."""
    try:
        get_scene(ctx).display_battle()
    except (FhParseError, FhConfigError) as exc:
        ctx.fail(f"Problem displaying battle: {str(exc)}")
    except FhError as exc:
        ctx.fail(f"Unexpected exception: {str(exc)}")


@cli.command()
@click.pass_context
def npcs(ctx):
    """Display details of the NPCs at the current location."""
    try:
        get_scene(ctx).display_npcs()
    except FhParseError as exc:
        ctx.fail(f"Problem displaying NPCs: {str(exc)}")
    except FhError as exc:
        ctx.fail(f"Unexpected exception: {str(exc)}")


@cli.command()
@click.pass_context
def scene(ctx):
    """Display information about the scene."""
    try:
        get_scene(ctx).display_scene()
    except FhParseError as exc:
        ctx.fail(f"Problem displaying scene: {str(exc)}")
    except FhError as exc:
        ctx.fail(f"Unexpected exception: {str(exc)}")


def list_cheatsheets(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    setting = get_setting(ctx)
    click.echo("  ".join(setting.cheatsheets.keys()))
    ctx.exit()


@cli.command()
@click.option(
    "-l",
    "--list",
    help="List the available cheatsheets.",
    is_flag=True,
    callback=list_cheatsheets,
    expose_value=False,
    is_eager=True,
)
@click.argument("cheatsheet_name", metavar="<cheatsheet_name>")
@click.pass_context
def cheatsheet(ctx, cheatsheet_name):
    """Display the cheatsheet called <cheatsheet_name>.

    Cheatsheets are referred to according to their filename in the cheatsheets
    directory, excluding the .yaml extension.
    """
    setting = get_setting(ctx)

    try:
        cheatsheet = setting.cheatsheets.from_prefix(cheatsheet_name)
    except ValueError:
        ctx.fail(f'Unknown cheatsheet "{cheatsheet_name}"')
    except FhAmbiguousReferenceError as exc:
        ctx.fail(f"Problem finding cheatsheet: {str(exc)}")
    except FhParseError as exc:
        ctx.fail(f"Problem parsing cheatsheet: {str(exc)}")
    except FhError as exc:
        ctx.fail(f"Unexpected exception: {str(exc)}")

    panes = [section.lines(setting.pane_width) for section in cheatsheet.sections]

    display_panes(panes, setting.panes, setting.pane_width)
