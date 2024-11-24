import configparser
import logging 
import re

log_format = {
    logging.INFO: "[OK]",
    logging.WARNING:"[WARN]",
    logging.ERROR:"[NOK]"
}

class CustomFormatter(logging.Formatter):
    def format(self, record):
        record.levelname = log_format.get(record.levelno, record.levelname)
        return super().format(record)
def setup_logging():
    logging.basicConfig(filename= "rechspez_protokol2.txt",filemode = "w",format = "%(message)s" ,level=logging.DEBUG, encoding="utf-8" )

    logger = logging.getLogger()
    for handler in logger.handlers:
        handler.setFormatter(CustomFormatter("%(levelname)s %(message)s" ))
        handler.terminator = '\n'

def load_ini_file(file_path):
    setup_logging()
    config = configparser.ConfigParser(allow_no_value=True)
    config.read(file_path)
    # TODO no encoding specified, we would guess cp1252
    if not config.sections():
        logging.error("Fehler: Datei ist leer oder nicht korrekt geladen")
        return None
    logging.info(f"Datei korrekt geladen: {file_path}")
    return config 

def check_bildrefrechner(config, section):
    bildref_keys = []
    for option in config.options(section):
        if option.lower().startswith("bildrefrechner"):
            bildref_keys.append(option)
    if not bildref_keys:
        logging.info(f"in {section} gibt es keine BildRefRechner")
        return
    bildref_keys.sort(key= lambda x: int(re.search(r"\d+",x).group()))
    missing_found = False
    for i in range(len(bildref_keys) -1 ):
        current_num = int(re.search(r"\d+", bildref_keys[i]).group())
        next_num = int(re.search(r"\d+", bildref_keys[i +1]).group())
        if next_num != current_num + 1:
            logging.error(f"Fehler:Zwischen {bildref_keys[i]} und {bildref_keys[i + 1]} in {section} fehlt ein bildrefrechner ")
            missing_found = True
    if not missing_found:
        logging.info(f"Alle BildRefRechner sind in der {section} vorhanden und kontinuierlich")

def check_unique_kf_schluessel(config,section): 
    kf_schluessel_list = []
    for option in config.options(section):
        if option.lower().startswith("kfschluessel"):
            kf_schluessel_list.append(config.get(section,option))
    if not kf_schluessel_list:
        logging.warning(f"Kein KFScluessel in {section}")
        return
    unique_keys = set()
    non_unique_keys = set()
    for key in kf_schluessel_list:
        if key in unique_keys:
            non_unique_keys.add(key)
        else:
            unique_keys.add(key)
    if non_unique_keys:
        for key in non_unique_keys:
            logging.error(f"Nicht-eindeutiger KFSchluessel {key} in {section}")
    else:
        logging.info(f"alle KFScluessel ist da in {section}")

def check_sequential_kf_schluessel(config,section):
    kf_schluessel_keys = sorted([int(option[len("KFSchluessel"):]) for option in config.options(section) if option.lower().startswith("kfschluessel")],key = int)
    if kf_schluessel_keys:
        if kf_schluessel_keys == list(range(min(kf_schluessel_keys),max(kf_schluessel_keys)+ 1)):
            logging.info(f"KFSchluessel sind in aufsteigender Reihfolge in {section}")
        else:
            logging.error(f"KFSchluessel sind nicht in aufsteigender Reihenfolge in {section}")
    else:
        logging.warning(f"Kein KFSchluessel in {section}")
def checkfunk(file_path):
    config = load_ini_file(file_path)
    if config is None:
        return
    if not config.sections():
        logging.error(f"Fehler: Datei {file_path} enthält keine sektionen")
        return
    for section in config.sections():
        if section.upper().startswith("RECHNER"):
            check_bildrefrechner(config,section)
            check_unique_kf_schluessel(config, section)
            check_sequential_kf_schluessel(config,section)
        else:
            logging.info(f"Überspringen der Nicht-RECHNER-{section}")
checkfunk("rechspez.ini")


