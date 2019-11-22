#!/usr/bin/env python3

import logzero
import threading
import subprocess
import re


from logzero import logger
from imdb import IMDb

class DVDBackup:
    def __init__(self):
        logger.info("Starting DVDBackup Module")
        # create an instance of the IMDb class
        self.ia = IMDb()
        self.imdbTitle = ""
        

    def getTitle(self):
        process = subprocess.Popen(['dvdbackup', '-I'],
                     bufsize=-1,
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

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
        process = subprocess.Popen(['dvdbackup', '-F', '-v', '-o', '/mnt/nas/Ripped/'],
                     shell=False,
                     bufsize=1,
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)

        while True:
            output = process.stdout.readline()
            if output == b'' and process.poll() is not None:
                break
            if output:
                print (output.strip())
        rc = process.poll()

        # output = ''
         # Poll process for new output until finished
        # for line in iter(process.stdout.readline, b''):
        #     print (line.decode("utf-8")),
        #     output += line.decode("utf-8") 

        # process.wait()
        # exitCode = process.returncode

        # print ("Output")
        # print (output)
        # print ("Finished")

