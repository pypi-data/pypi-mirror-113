import os
import re
import logging


def logUtils(level="INFO", Msg=None):
    """An easy-to-use logging tool.
    """
    if level.upper() == "WARN":
        logging.basicConfig(level=logging.WARN, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logging.warn(Msg)
    elif level.upper() == "WARNING":
        logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logging.warning(Msg)
    elif level.upper() == "INFO":
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logging.info(Msg)
    elif level.upper() == "ERROR":
        logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logging.error(Msg)


def getSubFile(basedir, file_suffix=None):
    """Get the list of files with the same suffix in the specified directory.
    """
    if file_suffix is None:
        pattern = re.compile(r".")
    else:
        pattern = re.compile("{}$".format(file_suffix))
    try:
        FileList = [os.path.join(basedir, subfile) for subfile in os.listdir(basedir) if re.search(pattern, subfile) and os.path.isfile(os.path.join(basedir,subfile))]
        return FileList
    except NotADirectoryError:
        logUtils(level='error',Msg="this basedir is not a direcotry")
