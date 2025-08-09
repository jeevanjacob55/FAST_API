# app/utils/validation.py
from typing import Tuple

# Verhoeff tables (standard)
_d = [
    [0,1,2,3,4,5,6,7,8,9],
    [1,2,3,4,0,6,7,8,9,5],
    [2,3,4,0,1,7,8,9,5,6],
    [3,4,0,1,2,8,9,5,6,7],
    [4,0,1,2,3,9,5,6,7,8],
    [5,9,8,7,6,0,4,3,2,1],
    [6,5,9,8,7,1,0,4,3,2],
    [7,6,5,9,8,2,1,0,4,3],
    [8,7,6,5,9,3,2,1,0,4],
    [9,8,7,6,5,4,3,2,1,0],
]

_p = [
    [0,1,2,3,4,5,6,7,8,9],
    [1,5,7,6,2,8,3,0,9,4],
    [5,8,0,3,7,9,6,1,4,2],
    [8,9,1,6,0,4,3,5,2,7],
    [9,4,5,3,1,2,6,8,7,0],
    [4,2,8,6,5,7,3,9,0,1],
    [2,7,9,3,8,0,6,4,1,5],
    [7,0,4,6,9,1,3,2,5,8],
]

_inv = [0,4,3,2,1,5,6,7,8,9]


def _normalize(aadhaar: str) -> str:
    """Strip spaces/hyphens and return only digits."""
    return "".join(ch for ch in aadhaar if ch.isdigit())


def verhoeff_check(number: str) -> bool:
    """
    Return True if `number` (string of digits) passes Verhoeff checksum.
    Expects the full number including check digit.
    """
    c = 0
    for i, ch in enumerate(reversed(number)):
        c = _d[c][_p[i % 8][int(ch)]]
    return c == 0


def verhoeff_generate_check_digit(number_without_check: str) -> int:
    """
    Generate Verhoeff check digit for number_without_check (string of digits).
    Returns the check digit (0-9).
    """
    c = 0
    for i, ch in enumerate(reversed(number_without_check)):
        c = _d[c][_p[(i + 1) % 8][int(ch)]]
    return _inv[c]


def is_valid_aadhaar(aadhaar: str) -> bool:
    """
    Validate Aadhaar:
      - normalize input (remove spaces/hyphens)
      - must be exactly 12 numeric digits
      - must pass Verhoeff checksum
    """
    s = _normalize(aadhaar)
    if len(s) != 12 or not s.isdigit():
        return False
    return verhoeff_check(s)
