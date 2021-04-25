from collections.abc import Mapping
from pathlib import Path
from typing import Optional, Callable, Any
from fourhills.stats import StatBlock
from fourhills.npc import Npc
from fourhills.cheatsheet import Cheatsheet
from fourhills.exceptions import FourhillsSettingStructureError


class DirectoryDict(Mapping):
    """Makes a directory of files look like an immutable dict of a type of class."""

    def __init__(
        self, directory: Path, extension: str, item_factory: Callable[[Path], Any]
    ):
        """Initialise the object.

        Parameters
        ----------
        directory: Path
            The directory to search
        extension: str
            The file extension, excluding the dot
        item_factory: Callable
            Callable that returns an object of the desired type when passed a single
            argument: a file path (pathlib.Path) that contains the object definition
        """
        # Create a dictionary mapping names (excluding extension) to their full path
        self._valid_names_paths = {
            filepath.stem: filepath
            for filepath in directory.glob(f"*.{extension}")
            if filepath.is_file()
        }
        self._item_factory = item_factory

    def __getitem__(self, key):
        return self._item_factory(self._valid_names_paths[key])

    def __iter__(self):
        return iter(self._valid_names_paths)

    def __len__(self):
        return len(self._valid_names_paths)

    def from_prefix(self, prefix):
        """Return an item from a prefix of the key (or the full key).
        Parameters
        ----------
        prefix: str
            A prefix of the name that is unique in the directory.
        """
        possible_keys = [key for key in self.keys() if key.startswith(prefix)]
        # If the list was empty, the prefix didn't match any real keys
        if len(possible_keys) == 0:
            raise ValueError(prefix)
        # If there was exactly one match, return the value
        elif len(possible_keys) == 1:
            return self[possible_keys[0]]
        # If there was more than one match, the prefix wasn't unique
        else:
            # This should probably be a setting structure error, since it's not a user
            # error
            raise ValueError(prefix)


class Setting:
    """Represents the campaign setting directory tree."""

    CONFIG_FILENAME = "fh_setting.yaml"
    DIRNAMES = {
        "world": "world",
        "monsters": "monsters",
        "npcs": "npcs",
        "cheatsheets": "cheatsheets",
    }

    def __init__(self):
        self.root = self.find_root()
        self.pane_width = 56
        self.panes = 2
        self._monsters = DirectoryDict(
            self.root / self.DIRNAMES["monsters"], "yaml", StatBlock.from_file
        )
        # The Npc from_file() method needs a setting to be passed in (so it can
        # look up stats in the setting if necessary)
        self._npcs = DirectoryDict(
            self.root / self.DIRNAMES["npcs"], "yaml", lambda f: Npc.from_file(f, self)
        )
        self._cheatsheets = DirectoryDict(
            self.root / self.DIRNAMES["cheatsheets"], "yaml", Cheatsheet.from_file
        )

    @property
    def monsters(self):
        return self._monsters

    @property
    def npcs(self):
        return self._npcs

    @property
    def cheatsheets(self):
        return self._cheatsheets

    @staticmethod
    def find_root() -> Optional[Path]:
        """Find the root of the setting.

        Notes
        -----
        Ascends the directory tree looking for `SETTING_CONFIG_FILENAME`.

        Returns
        -------
        pathlib.Path
            The setting's root directory

        Raises
        ------
        FourhillsSettingStructureError
            If the current directory is not part of a valid setting.
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
        # If the root directory wasn't found, raise an exception
        raise FourhillsSettingStructureError("No valid root directory was found.")
