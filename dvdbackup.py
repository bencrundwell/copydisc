#!/usr/bin/env python3

import logzero
import threading
import subprocess
import re
import glob, os


from logzero import logger
from imdb import IMDb

class DVDBackup:

    def __init__(self, RippingDestination, ConversionDestination):
        logger.info("Starting DVDBackup Module")
        # create an instance of the IMDb class
        self.ia = IMDb()
        self.dvdTitle = ''
        self.imdbTitle = ''
        self.RippingDestination = RippingDestination
        self.ConversionDestination = ConversionDestination

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

        process = subprocess.Popen(['dvdbackup', '-F', '-o', self.RippingDestination, '-n', self.dvdTitle, '-p'],
                     shell=False,
                     bufsize=1,
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)

        while True:
            output = process.stderr.readline()
            if output == b'' and process.poll() is not None:
                break
            if output:
                line = output.strip().decode('utf-8')
                print (line)
                if line[0:5] == 'Error':
                    logger.error(line)


        logger.info("Finished Ripping DVD")


    def convertVideo(self):
        if (self.dvdTitle == '') or (self.imdbTitle == ''):
            logger.error("dvdTitle not set. Use DVDBackup.getTitle()")
            raise Exception
        if self.RippingDestination == '':
            logger.error("RippingDestination not set. Use DVDBackup.setRippingDestination()")
            raise Exception

        logger.info("Convert Video")

        sourceDir = (self.RippingDestination + "/" + self.dvdTitle + "/VIDEO_TS")
        logger.info("Search " + sourceDir)

        os.chdir(sourceDir)
        vobFiles = []
        for file in glob.glob("*.VOB"):
            vobFiles.append(file)
            print(file + " - " + str(os.path.getsize(file)))

        firstVOB = 0
        lastVOB = len(vobFiles) + 1

        if lastVOB > 0:
            if os.path.getsize(vobFiles[0]) < os.path.getsize(vobFiles[1]) :
                logger.info(vobFiles[0] + " is a Menu, skipping")
                firstVOB = 1

        ffmpegCommand = "cat "
        for file in vobFiles[firstVOB:lastVOB]:
            ffmpegCommand += file + " "

        # ffmpegCommand += "| ffmpeg -i - -c:v libx264 -preset medium -crf 20 -codec:a libmp3lame -qscale:a 2 -codec:s copy -t 00:01:00 " + self.imdbTitle + ".mkv"
        # ffmpegCommand += "| ffmpeg -analyzeduration 100M -probesize 100M -i - -vn -codec:a copy -t 00:01:00 " + self.imdbTitle + ".aac"
        ffmpegCommand += "| ffmpeg"
        ffmpegCommand += " -analyzeduration 100M -probesize 100M"
        ffmpegCommand += " -i -"
        ffmpegCommand += " -c:v libx264 -preset medium -crf 20"
        ffmpegCommand += " -codec:a copy -metadata:s:a:0 language=en"
        ffmpegCommand += " -t 00:02:00"
        ffmpegCommand += " " + self.ConversionDestination + "/" + self.imdbTitle + ".mp4"
        
        print (ffmpegCommand)
        #cat VTS_0*_*VOB | ffmpeg -i - -vcodec h264 -acodec mp2 rip.mp4

        process = subprocess.Popen(ffmpegCommand,
                     shell=True,
                     bufsize=1)

        # while True:
        #     output = process.stdout.readline()
        #     if output == b'' and process.poll() is not None:
        #         break
        #     if output:
        #         print (output.strip().decode('utf-8'))

        logger.info("Finished Ripping DVD")

