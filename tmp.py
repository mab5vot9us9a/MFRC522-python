#!/usr/bin/env python3
# coding=utf-8

import MFRC522

MIFAREReader = MFRC522.MFRC522()
MIFAREReader.WriteAll(ord("A"))
print("Wrote " + str(ord("A")))

(status, TagType) = MIFAREReader.Request(MIFAREReader.PICC_REQIDL)
if status == MIFAREReader.MI_OK:
    (status, uid) = MIFAREReader.Anticoll()
    MIFAREReader.SelectTag(uid)
    key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
    MIFAREReader.DumpClassic1K_Text(key, uid)
