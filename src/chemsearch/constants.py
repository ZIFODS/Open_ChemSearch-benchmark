from enum import StrEnum

from pyprojroot import here


class Events(StrEnum):
    completed_get = "Received hits from GET request."


class Queries(StrEnum):
    SMARTS = "smarts"
    SMILES = "smiles"


class URLPaths(StrEnum):
    SUBSTRUCTURE_SEARCH = "/substructure-search"


DATA_DIR = here() / "data"
LOG_DIR = here() / "logs"
