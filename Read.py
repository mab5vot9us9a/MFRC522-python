#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal


class bcolors:
    CYAN         = '\033[96m'
    CYAN_BRIGHT  = '\033[96;1m'
    HEADER       = '\033[95m'
    BLUE         = '\033[94m'
    BLUE_BRIGHT  = '\033[94;1m'
    GREEN        = '\033[92m'
    GREEN_BRIGHT = '\033[92;1m'
    WARNING      = '\033[93;1m'
    FAIL         = '\033[91m'
    ENDC         = '\033[0m'
    BOLD         = '\033[1m'
    UNDERLINE    = '\033[4m'

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted


def end_read(signal, frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print("Welcome to the MFRC522 data read example")
print("Press Ctrl-C to stop.")

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:

    # Scan for cards
    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print("Card detected")

    # Get the UID of the card
    (status, uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        # Print UID
        print("Card read UID: " + str(uid[0]) + "," + str(uid[1]) + "," + str(uid[2]) + "," + str(uid[3]))

        # This is the default key for authentication
        key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)

        for i in range(0, 64, 4):
            # Authenticate
            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, i, key, uid)

            # Check if authenticated
            if status == MIFAREReader.MI_OK:
                print("{}{:-^58}{}".format(bcolors.BLUE_BRIGHT, " Sector {} ".format(i // 4), bcolors.ENDC))
                MIFAREReader.MFRC522_Read(i)
                MIFAREReader.MFRC522_Read(i + 1)
                MIFAREReader.MFRC522_Read(i + 2)
                MIFAREReader.MFRC522_Read(i + 3)
            else:
                print("Authentication error")

        continue_reading = False
        MIFAREReader.MFRC522_StopCrypto1()

GPIO.cleanup()
