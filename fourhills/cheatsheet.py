import yaml
from pathlib import Path
from dataclasses import dataclass
from typing import List
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
    def from_file(cls, filepath: Path):
        """Create a Cheatsheet from a YAML file.

        Parameters
        ----------
        filename: Path
            Path to the YAML file
        """
        with open(filepath) as f:
            try:
                cheatsheet_dict = yaml.safe_load(f)
            except yaml.YAMLError as exc:
                raise FourhillsFileLoadError(
                    f"Error loading from {filepath}."
                ) from exc

            try:
                description = cheatsheet_dict["description"]
            except KeyError:
                raise FourhillsFileLoadError(
                    f"Error loading from {filepath}: description not included."
                )
            try:
                sections_list = cheatsheet_dict["sections"]
            except KeyError:
                raise FourhillsFileLoadError(
                    f"Error loading from {filepath}: sections not included."
                )

            sections = [
                Cheatsheet.Section(**section_dict) for section_dict in sections_list
            ]

            return cls(description, sections)
