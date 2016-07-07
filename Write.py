#!/usr/bin/env python
# -*- coding: utf8 -*-

import MFRC522
import signal

continue_reading = True


data_blocks = [4, 5, 6,
               8, 9, 10,
               12, 13, 14,
               16, 17, 18,
               20, 21, 22,
               24, 25, 26,
               28, 29, 30,
               32, 33, 34,
               36, 37, 38,
               40, 41, 42,
               44, 45, 46,
               48, 49, 50,
               52, 53, 54,
               56, 57, 58,
               60, 61, 62]


def end_read(signal, frame):
    '''
    Capture SIGINT for cleanup when the script is aborted
    '''
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:

    # Scan for cards
    (status, TagType) = MIFAREReader.Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print("Card detected")

    # Get the UID of the card
    (status, uid) = MIFAREReader.Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        # Print UID
        print("Card read UID: " + str(uid[0]) + "," + str(uid[1]) + "," + str(uid[2]) + "," + str(uid[3]))

        # This is the default key for authentication
        key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

        # Select the scanned tag
        MIFAREReader.SelectTag(uid)

        # Authenticate
        status = MIFAREReader.Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

        # Check if authenticated
        if status == MIFAREReader.MI_OK:

            # Variable for the data to write
            data = []

            # Fill the data with 0x00 - 0x0F
            for x in range(0, 16):
                data.append(x)

            print("Sector 8 looked like this:")
            # Read block 8
            MIFAREReader.Read(8)

            print("Sector 8 will now be filled with 0xFF:")
            # Write the data
            MIFAREReader.Write(8, data)

            print("It now looks like this:")
            # Check to see if it was written
            MIFAREReader.Read(8)

            # Stop
            MIFAREReader.StopCrypto1()

            # Make sure to stop reading for cards
            continue_reading = False
        else:
            print("Authentication error")
