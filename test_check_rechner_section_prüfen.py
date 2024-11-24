import pytest as pt
from checkrechspez import check_rechner_section, load_ini_file


@pt.mark.parametrize('filename, sectionname, expected_value', [
    ("reschspeztest1.ini", "RECHNER_212", True),
    ("reschspeztest2.ini", "RECHNER_212", False),


])
def test(filename, sectionname, expected_value):
    config=load_ini_file(filename)
    assert check_rechner_section(config, sectionname)  == expected_value