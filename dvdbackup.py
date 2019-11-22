#!/usr/bin/env python3

import logzero
import threading
import subprocess
import re


from logzero import logger
from imdb import IMDb

class DVDBackup:
    RippingDestination = ''

    def __init__(self, directory):
        logger.info("Starting DVDBackup Module")
        # create an instance of the IMDb class
        self.ia = IMDb()
        self.imdbTitle = ""
        self.RippingDestination = directory

    def setRippingDestination(self, directory):
        self.RippingDestination = directory

    def getTitle(self):
        process = subprocess.Popen(['dvdbackup', '-I'],
                     bufsize=-1,
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
        stdout = process.communicate()[0]

        output = stdout.decode('utf-8')
        pattern = re.compile(r"\"(.*)\"")
        results = pattern.search(output)

        if results != None:     # Search for the pattern. If found,
            self.dvdTitle = output[results.regs[1][0] : results.regs[1][1]]
            logger.info("Read DVD: " + self.dvdTitle)

        # get a movie
        movies = self.ia.search_movie(self.dvdTitle)
        self.imdbTitle = movies[0].get('title')
        logger.info("IMDb lookup: " + self.imdbTitle)

        return self.imdbTitle

    def ripDVD(self):
        if self.RippingDestination == '':
            logger.error("RippingDestination not set. Use DVDBackup.setRippingDestination()")
            raise Exception

        process = subprocess.Popen(['dvdbackup', '-F', '-o', self.RippingDestination, '-n', self.dvdTitle],
                     shell=False,
                     bufsize=1,
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)

        while True:
            output = process.stderr.readline()
            if output == b'' and process.poll() is not None:
                break
            # if output:
            #     print (output.strip().decode('utf-8'))

        logger.info("Finished Ripping DVD")

