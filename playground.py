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
    # MIFAREReader.WriteAll(key, uid, 0x00)
    # print("Wrote " + str(0x00))

    MIFAREReader.WriteText(key, uid, "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.\nIt has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.")
    print(MIFAREReader.DumpClassic1K_Text(key, uid, print_text=False))

    MIFAREReader.StopCrypto1()
