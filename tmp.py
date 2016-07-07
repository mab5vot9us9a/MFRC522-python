#!/usr/bin/env python3
# coding=utf-8

import RPi.GPIO as GPIO
import MFRC522

MIFAREReader = MFRC522.MFRC522()
(status, TagType) = MIFAREReader.Request(MIFAREReader.PICC_REQIDL)
(status, uid) = MIFAREReader.Anticoll()
if status == MIFAREReader.MI_OK:
    key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
    MIFAREReader.SelectTag(uid)
    MIFAREReader.WriteAll(ord("A"))
    print("Wrote " + str(ord("A")))
