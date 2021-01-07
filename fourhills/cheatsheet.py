import yaml
from dataclasses import dataclass
from typing import List
from fourhills import Setting
from fourhills.exceptions import FourhillsFileLoadError, FourhillsSettingStructureError
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
        """Create an Cheatsheet by looking it up in the setting.

        Parameters
        ----------
        cheatsheet_name: str
            The title of the cheatsheet. Must exactly match a filename in the setting's
            `cheatsheets` folder, excluding the extension.
        setting: Setting
            The Setting object; this is used to find the setting root and
            subdirectories.
        """
        # Suspected path of the cheatsheet file
        cheatsheet_file = setting.cheatsheets_dir / (cheatsheet_name + ".yaml")
        if not cheatsheet_file.is_file():
            raise FourhillsSettingStructureError(
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
