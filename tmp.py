#!/usr/bin/env python3
# coding=utf-8

import MFRC522

MIFAREReader = MFRC522.MFRC522()

(status, TagType) = MIFAREReader.Request(MIFAREReader.PICC_REQIDL)
print("TagType={:X}".format(TagType))
(status, uid) = MIFAREReader.Anticoll()
if status == MIFAREReader.MI_OK:
    key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
    MIFAREReader.SelectTag(uid)
    MIFAREReader.WriteAll(key, uid, 0x00
    print("Wrote " + str(0x00)

    key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
    MIFAREReader.DumpClassic1K_Text(key, uid)

    MIFAREReader.StopCrypto1()
