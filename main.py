#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Ben Crundwell"
__version__ = "0.1.0"
__license__ = "MIT"

import logzero
import time
import sys

from copydisc import Copydisc 
from handbrake import Handbrake 
from logzero import logger
from dvd import DVD

# Setup rotating logfile with 3 rotations, each with a maximum filesize of 1MB:
logzero.logfile("logs/rotating-logfile.log", maxBytes=1e6, backupCount=3)

def main():
    """ Main entry point of the app """
    logger.info("CopyDisc Starting Up")
    
    # Log some variables
    # logger.info("var1: %s, var2: %s", var1, var2)

    copydisc = Copydisc('/dev/ttyUSB0')
    dvd = DVD()
    handbrake = Handbrake('/mnt/nas/Movies')

    copydisc.calibrate()

    # dvdTitle = handbrake.getTitle()
    # logger.info("Ripping: %s", dvdTitle)
    # handbrake.ripDVD()
    
    dvd.open()

    while True:
        try: 
            copydisc.insert()
        except:
            logger.info("No Discs in Loader, finished")
            sys.exit()

        dvd.close()

        time.sleep(20)

        dvdTitle = handbrake.getTitle()
        logger.info("Ripping: %s", dvdTitle)
        
        handbrake.ripDVD()

        time.sleep(10)
        dvd.open()
        time.sleep(5)
        copydisc.accept()


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
