import yaml
from dataclasses import dataclass
from typing import List
from fourhills import Setting
from fourhills.exceptions import FourhillsFileLoadError, FourhillsFileNameError
from fourhills.text_utils import wrap_lines_paragraph, title


@dataclass
class Cheatsheet:
    """Represents a 'cheatsheet' containing useful info for the DM."""

    @dataclass
    class Section:
        """Represents a section of a cheatsheet, with a title and content."""

        section_title: str
        section_content: List[str]

        def lines(self, line_width: int = 80) -> List[str]:
            """Return a list of lines with the section title and content

            Parameters
            ----------
            line_width : int
                The width of the output, in characters.

            Returns
            -------
            list of str
                A list of lines with the section content, formatted to the
                appropriate line width
            """
            lines = title(self.section_title, line_width) + self.section_content

            return wrap_lines_paragraph(lines, line_width)

    description: str
    sections: List[Section]

    def __str__(self):
        return f'Cheatsheet: "{self.description}"'

    @classmethod
    def from_name(cls, cheatsheet_name: str, setting: Setting):
        """Create an Cheatsheet by looking it up by name in the setting.

        Parameters
        ----------
        cheatsheet_name: str
            The name of the cheatsheet. Must exactly match a filename in the setting's
            `cheatsheets` folder, excluding the extension.
        setting: Setting
            The Setting object; this is used to find the setting root and
            subdirectories.
        """
        # Suspected path of the cheatsheet file
        cheatsheet_file = setting.cheatsheets_dir / (cheatsheet_name + ".yaml")
        if not cheatsheet_file.is_file():
            raise FourhillsFileNameError(
                f"Cheatsheet file {cheatsheet_file} does not exist."
            )
        with open(cheatsheet_file) as f:
            try:
                cheatsheet_dict = yaml.safe_load(f)
            except yaml.YAMLError as exc:
                raise FourhillsFileLoadError(
                    f"Error loading from {cheatsheet_file}."
                ) from exc

            try:
                description = cheatsheet_dict["description"]
            except KeyError:
                raise FourhillsFileLoadError(
                    f"Error loading from {cheatsheet_file}: description not included."
                )
            try:
                sections_list = cheatsheet_dict["sections"]
            except KeyError:
                raise FourhillsFileLoadError(
                    f"Error loading from {cheatsheet_file}: sections not included."
                )

            sections = [
                Cheatsheet.Section(**section_dict) for section_dict in sections_list
            ]

            return cls(description, sections)

    @classmethod
    def from_name_or_prefix(cls, cheatsheet_name: str, setting: Setting):
        """Create an Cheatsheet by looking it up by name (or a prefix) in the setting.

        Parameters
        ----------
        cheatsheet_name: str
            The name of the cheatsheet, excluding the extension, or a prefix of the
            name that is unique in the setting's `cheatsheets` folder.
        setting: Setting
            The Setting object; this is used to find the setting root and
            subdirectories.
        """
        # Make a list of all of the cheatsheet names that start with cheatsheet_name
        possible_cheatsheet_names = [
            name
            for name in setting.filenames_of_type_in_dir(
                "yaml", setting.cheatsheets_dir
            )
            if name.startswith(cheatsheet_name)
        ]
        # If the list was empty, cheatsheet_name didn't match any real cheatsheets,
        # so raise a settings structure error.
        if len(possible_cheatsheet_names) == 0:
            raise FourhillsFileNameError(
                f"Cheatsheet {cheatsheet_name} does not exist, nor is it a valid prefix"
                " for any existing cheatsheets."
            )
        # If there was exactly one match, create the cheatsheet from that name
        elif len(possible_cheatsheet_names) == 1:
            return cls.from_name(possible_cheatsheet_names[0], setting)
        # If there were too many matches, raise an exception
        else:
            raise FourhillsFileNameError(
                "More than one cheatsheet exists with a name starting with "
                f"{cheatsheet_name}"
            )
