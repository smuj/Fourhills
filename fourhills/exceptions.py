class FhError(Exception):
    pass


class FhParseError(FhError):
    """Error when parsing a data file."""

    pass


class FhAmbiguousReferenceError(FhParseError):
    """A referenced entity can't be uniquely determined."""

    pass


class FhSettingStructureError(FhError):
    """The setting directory structure is not valid."""

    pass


class FhConfigError(FhError):
    """Something about the configuration is not valid."""

    pass
