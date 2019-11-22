#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Ben Crundwell"
__version__ = "0.1.0"
__license__ = "MIT"

import logzero

from copydisc import Copydisc 
from dvdbackup import DVDBackup 
from logzero import logger

# Setup rotating logfile with 3 rotations, each with a maximum filesize of 1MB:
logzero.logfile("logs/rotating-logfile.log", maxBytes=1e6, backupCount=3)

def main():
    """ Main entry point of the app """
    logger.info("CopyDisc Starting Up")
    
    # Log some variables
    # logger.info("var1: %s, var2: %s", var1, var2)

    copydisc = Copydisc('/dev/ttyUSB0')
    # dvd = DVD()
    dvdBackup = DVDBackup('/mnt/nas/Ripped')

    copydisc.calibrate()

    dvdTitle = dvdBackup.getTitle()
    logger.info("Ripping: %s", dvdTitle)
    
    dvdBackup.ripDVD()


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()