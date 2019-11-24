#!/usr/bin/env python3

import logzero
import threading
import subprocess
import re
import glob, os


from logzero import logger
from imdb import IMDb

#https://stackoverflow.com/questions/37925840/python-monitoring-progress-of-handbrake

class Handbrake:

    def __init__(self, RippingDestination):
        logger.info("Starting Handbrake Module")
        # create an instance of the IMDb class
        self.ia = IMDb()
        self.dvdTitle = ''
        self.imdbTitle = ''
        self.RippingDestination = RippingDestination

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
        self.imdbTitle = movies[0].get('title') + ' (' + str(movies[0].get('year')) + ')'
        logger.info("IMDb lookup: " + self.imdbTitle)

        return self.imdbTitle

    def ripDVD(self):
        if self.RippingDestination == '':
            logger.error("RippingDestination not set. Use DVDBackup.setRippingDestination()")
            raise Exception

        #https://stackoverflow.com/questions/37925840/python-monitoring-progress-of-handbrake
        # HandBrakeCLI -i /dev/dvd -o /mnt/nas/Ripped/Ratatouille.mp4
        # --audio-lang-list <string>

        handbrakeCommand = "HandBrakeCLI"
        handbrakeCommand += " -i /dev/dvd"
        handbrakeCommand += " --audio-lang-list eng"
        # handbrakeCommand += " --main-feature"
        handbrakeCommand += " --markers"
        handbrakeCommand += " -e x264 -q 20 -B 160"
        handbrakeCommand += " -o " + self.RippingDestination + "/" + self.imdbTitle + ".mp4"

        print (handbrakeCommand)

        process = subprocess.Popen(handbrakeCommand.split(),
                     shell=False,
                     bufsize=1,
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.STDOUT
        )

        while True:
            output = process.stdout.readline()
            if output == b'' and process.poll() is not None:
                break
            if output:
                line = output.strip().decode('utf-8')
                print (line)


        logger.info("Finished Ripping DVD")

