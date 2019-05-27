import sys
import re
import yaml
import click
from pathlib import Path
from typing import Optional, List, Tuple
from stats import StatBlock
from fourhills_exceptions import FourhillsFileLoadError, FourhillsSettingStructureError

BATTLE_FILENAME = "battle.yaml"


class Setting:
    """Represents the campaign setting directory tree."""

    CONFIG_FILENAME = "fh_setting.yaml"
    DIRNAMES = {"world": "world", "monsters": "monsters"}

    def __init__(self):
        self.root = self.find_root()

    @staticmethod
    def find_root() -> Optional[Path]:
        """Find the root of the setting.

        Notes
        -----
        Ascends the directory tree looking for `SETTING_CONFIG_FILENAME`.

        Returns
        -------
        pathlib.Path or None
            The setting's root directory, or None if the file wasn't found
        """
        # Get the current working directory and resolve any symlinks etc.
        current_dir = Path.cwd().resolve()
        # While we can still ascend
        while current_dir != current_dir.parent:
            # See if the settings file exists
            if (current_dir / Setting.CONFIG_FILENAME).is_file():
                # Make sure the require directories are there
                for directory_name in Setting.DIRNAMES.values():
                    if not (current_dir / directory_name).is_dir():
                        raise FourhillsSettingStructureError(
                            f"Setting root does not contain {directory_name} directory."
                        )
                return current_dir
            current_dir = current_dir.parent
        # If the root directory wasn't found, return None
        return None

    @property
    def world_dir(self):
        return self.root / self.DIRNAMES["world"]

    @property
    def monsters_dir(self):
        return self.root / self.DIRNAMES["monsters"]

    def monster_stats(self, monster_name: str) -> StatBlock:
        # Suspected path of the monster stat config file
        stat_file = self.monsters_dir / (monster_name + ".yaml")
        if not stat_file.is_file():
            raise FourhillsSettingStructureError(
                f"Monster file {stat_file} does not exist."
            )
        return StatBlock.from_file(str(stat_file))


def load_battle_info(filename: str) -> List[Tuple[str, int]]:
    """Load info about a battle from a file and return the details.

    Parameters
    ----------
    filename : str
        Filename of the YAML file to load battle info from.

    Returns
    -------
    list of (str, int)
        List of monster names and the number of each
    """
    with open(filename) as f:
        try:
            battle_info = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            raise FourhillsFileLoadError(f"Error loading from {filename}.") from exc

        # Stores the list of monster names and numbers
        monster_info = []

        # If there was a monsters section, load the monsters
        if "monsters" in battle_info:
            for monster_name_number in battle_info["monsters"]:
                # See if it matches the expected format, extracting name and number
                match = re.match(r"^(\w*)(?: ?x?(\d+))?$", monster_name_number)
                if not match:
                    raise FourhillsFileLoadError("Error parsing monster in battle file")
                # Get the name of the monster and how many there are. If there
                # wasn't a number, assume 1 monster.
                name = match[1]
                number = match[2] or "1"
                # Convert to int
                try:
                    number = int(number)
                except ValueError as exc:
                    raise FourhillsFileLoadError(
                        f"Error parsing number for monster {name}"
                    ) from exc
                # Add to the list
                monster_info.append((name, number))

        if "characters" in battle_info:
            raise NotImplementedError("Loading of characters not yet implemented")

        return monster_info


def battle():

    setting = Setting()

    try:
        battle_info = load_battle_info(BATTLE_FILENAME)
    except FileNotFoundError:
        raise FourhillsSettingStructureError(
            f"No '{BATTLE_FILENAME}' battle file found."
        )

    stat_strings = [
        setting.monster_stats(monster_name).formatted_string(
            line_width=56, quantity=quantity
        )
        for monster_name, quantity in battle_info
    ]
    click.echo_via_pager("\n".join(stat_strings))


def print_usage():
    raise NotImplementedError


def print_location():
    raise NotImplementedError


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] in ["b", "battle"]:
            battle()
        else:
            print_usage()
    else:
        print_location()


if __name__ == "__main__":
    main()
