from pathlib import (
    Path,
)


class Dir:
    """
    This class holds the paths for quick referencing.
    """

    BASE = Path(__file__).parent.parent
    MEDIA = BASE / "media"
