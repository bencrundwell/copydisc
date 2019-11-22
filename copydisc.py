#!/usr/bin/env python3

import logzero
import serial

from logzero import logger

class Copydisc:
    def __init__(self, port):
        self.port = port
        logger.info("Connect to CopyDisc on " + port)
        self.ser = serial.Serial(self.port) # open serial port
        

    def calibrate(self):
        logger.info("Calibrate...")
        self.ser.write(b'C')
        response = self.ser.read(1)
        assert response == b'X', "Calibrate Failed"

    def insert(self):
        logger.info("Insert Disc")
        self.ser.write(b'I')
        response = self.ser.read(1)
        assert response == b'X', "Insert Disc Failed"
        
    def accept(self):
        logger.info("Accept Disc")
        self.ser.write(b'A')
        response = self.ser.read(1)
        assert response == b'X', "Accept Disc Failed"
        
    def reject(self):
        logger.info("Reject Disc")
        self.ser.write(b'G')
        response = self.ser.read(1)
        assert response == b'X', "Accept Disc Failed"

    def drop(self):
        logger.info("Drop Disc")
        self.ser.write(b'R')
        response = self.ser.read(1)
        assert response == b'X', "Accept Disc Failed"
