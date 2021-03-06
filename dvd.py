#!/usr/bin/env python3

import logzero
import subprocess

from logzero import logger
from imdb import IMDb

class DVD:
    def __init__(self):
        logger.info("Starting DVD Module")
        # create an instance of the IMDb class
        self.ia = IMDb()
        

    def getTitle(self):
        process = subprocess.Popen(['setcd', '-i'],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
        stdout = process.communicate()[0]

        self.title = stdout.decode('utf-8').splitlines()[2][17:]
        self.publisher = stdout.decode('utf-8').splitlines()[3][15:]
        self.preparer = stdout.decode('utf-8').splitlines()[4][19:]

        logger.info("Read DVD: \"" + self.title + "\" by \"" + self.preparer + "\"")
        # get a movie
        movies = self.ia.search_movie(self.title)
        self.imdbTitle = movies[0].get('title')
        logger.info("IMDb lookup: " + self.imdbTitle)

        return self.imdbTitle

    def open(self):
        logger.info("Open DVD Tray")
        process = subprocess.Popen(['eject', '/dev/sr0'])

        while True:
            if process.poll() is not None:
                break

    def close(self):
        logger.info("Close DVD Tray")
        process = subprocess.Popen(['eject', '/dev/sr0', '-t'])

        while True:
            if process.poll() is not None:
                break



