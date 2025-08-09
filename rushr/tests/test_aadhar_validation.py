# tests/test_aadhaar_validation.py
from app.utils.validation import verhoeff_generate_check_digit, is_valid_aadhaar

def test_verhoeff_roundtrip():
    base = "12345678901"     # 11 digits (example)
    check = verhoeff_generate_check_digit(base)
    full = base + str(check)
    assert len(full) == 12
    assert is_valid_aadhaar(full)
    # small negative test: change last digit
    assert not is_valid_aadhaar(full[:-1] + str((check + 1) % 10))
