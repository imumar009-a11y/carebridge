"""Backward-compatible entry point (the old import path). The real code now lives in the `cb` package."""
from cb.config import LANGS, LEVELS                     # noqa: F401
from cb.triage import triage                            # noqa: F401
from cb.automation import notify, book_appointment      # noqa: F401
from cb.text import normalize, search
from cb.knowledge.red_flags import find_red_flag


def is_emergency(text):
    return find_red_flag(normalize(text), search)[0] is not None
