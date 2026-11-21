"""Coloring algorithms."""

from .greedy import greedy_coloring
from .welsh_powell import welsh_powell, welsh_powell_first_fit
from .dsatur import dsatur, dsatur_naive
from .improved_dsatur import improved_dsatur
from .exact import exact_coloring, chromatic_number
