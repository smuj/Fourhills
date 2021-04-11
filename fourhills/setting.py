from pathlib import Path
from typing import Optional, List
from fourhills.exceptions import FourhillsSettingStructureError


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

    @property
    def world_dir(self):
        return self.root / self.DIRNAMES["world"]

    @property
    def monsters_dir(self):
        return self.root / self.DIRNAMES["monsters"]

    @property
    def npcs_dir(self):
        return self.root / self.DIRNAMES["npcs"]

    @property
    def cheatsheets_dir(self):
        return self.root / self.DIRNAMES["cheatsheets"]

    @staticmethod
    def filenames_of_type_in_dir(extension: str, directory: Path) -> List[str]:
        """Return a list of filenames from `directory` with extension `extension`.

        Parameters
        ----------
        extension: str
            The file extension, excluding the dot
        directory: Path
            The directory to search


        Returns
        -------
        list of str
            A list of valid filenames, excluding the extension.
        """
        return [
            filepath.stem
            for filepath in directory.glob(f"*.{extension}")
            if filepath.is_file()
        ]
