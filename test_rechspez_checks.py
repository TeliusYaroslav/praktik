import pytest 
import configparser 
import os
import logging
from io import StringIO
from rechspezy import check_bildrefrechner ,check_unique_kf_schluessel , setup_logging

@pytest.fixture
def temp_ini_file(tmp_path,content):
    ini_file = tmp_path / "test.ini"
    ini_file.write_text(content)
    return ini_file

@pytest.mark.parametrize("content , expected_log", [
    ("""
    [RECHNER_1]
    BildRefRechner0 =1 
    BildRefRechner1 =2 
    BildRefRechner2 =3 
    """ , "[OK]"),
    ("""
    [RECHNER_1]
    BildRefRechner0 = 1
    BildRefRechner2 = 3
    """, "[NOK]")])

def test_check_rechner_section(content, expected_log, caplog, temp_ini_file):
    setup_logging()
    caplog.set_level(logging.INFO)
    config = configparser.ConfigParser()
    config.read(temp_ini_file)
    check_bildrefrechner(config,"RECHNER_1")
    log_output = caplog.text
    assert expected_log in log_output
@pytest.mark.parametrize("content , expected_log", [
    ("""
    [RECHNER_1]
    KFSchluessel0 = 123
    KFSchluessel1 = 124
""", "[OK] "),
    ("""
    [RECHNER_1]
    KFSchluessel0 = 123
    KFSchluessel1 = 123     
""", "[NOK] Nicht-eindeutiger KFSchluessel 123 in RECHNER_1" )
])
def test_check_unique_kfschluessel(content, expected_log,caplog, temp_ini_file):
    setup_logging()
    caplog.set_level(logging.INFO)
    config = configparser.ConfigParser()
    config.read(temp_ini_file)
    check_unique_kf_schluessel(config,"RECHNER_1")
    log_output = caplog.text
    assert expected_log in log_output