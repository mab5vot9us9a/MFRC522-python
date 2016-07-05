#!/usr/bin/env python3
# coding=utf-8
# Copyright © 2016 Maurice Fahn All Rights Reserved.

from MFRC522 import MFRC522
from BirthdayText import birthday_data

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


MIFAREReader = MFRC522()


def write_all_character(character):
    if len(character) > 1:
        return
    elif ord(character) > 255:
        return
    write_all(ord(character))


def write_all(value):
    if not isinstance(value, int):
        return
    (status, TagType) = MIFAREReader.Request(MIFAREReader.PICC_REQIDL)
    (status, uid) = MIFAREReader.Anticoll()
    if status == MIFAREReader.MI_OK:
        key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
        MIFAREReader.SelectTag(uid)

        for i in range(0, len(data_blocks), 3):
            status = MIFAREReader.Auth(MIFAREReader.PICC_AUTHENT1A, data_blocks[i], key, uid)

            if status == MIFAREReader.MI_OK:
                all_characters = [value for _ in range(0, 16)]
                MIFAREReader.Write(data_blocks[i], all_characters)
                MIFAREReader.Write(data_blocks[i + 1], all_characters)
                MIFAREReader.Write(data_blocks[i + 2], all_characters)
            else:
                print("Authentication error")

        MIFAREReader.StopCrypto1()


def write_message(message):
    (status, TagType) = MIFAREReader.Request(MIFAREReader.PICC_REQIDL)
    (status, uid) = MIFAREReader.Anticoll()
    if status == MIFAREReader.MI_OK:
        key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
        MIFAREReader.SelectTag(uid)

        for i in range(0, len(data_blocks), 3):
            status = MIFAREReader.Auth(MIFAREReader.PICC_AUTHENT1A, data_blocks[i], key, uid)

            if status == MIFAREReader.MI_OK:
                MIFAREReader.Write(data_blocks[i], message[i])
                MIFAREReader.Write(data_blocks[i + 1], message[i + 1])
                MIFAREReader.Write(data_blocks[i + 2], message[i + 2])
            else:
                print("Authentication error")

        MIFAREReader.StopCrypto1()

if __name__ == '__main__':
    write_message(birthday_data)
