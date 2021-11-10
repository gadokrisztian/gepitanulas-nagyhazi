from pathlib import Path

from whouserobot import *


def test_projectpaths():
    repobase = Path(__file__).parent.parent
    assert Dir.BASE == repobase
    assert Dir.MEDIA == repobase / "media"
