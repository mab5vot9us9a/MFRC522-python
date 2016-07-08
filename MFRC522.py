#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import spi
import signal
import time
import errors
from xterm256_Colors import tcolors


class MFRC522:
    """
    Class to communicate with a MIFARE 1k Classic style tag layout.

    To take any action with the card, the following is a standard workflow:
    ```
    MIFAREReader = MFRC522()
    (status, TagType) = MIFAREReader.Request(MIFAREReader.PICC_REQIDL)
    (status, uid) = MIFAREReader.Anticoll()
    if status == MI_OK:
        MIFAREReader.SelectTag(uid)
        status = MIFAREReader.Auth(MIFAREReader.PICC_AUTHENT1A, blockAddr, key, uid)
        if status == MIFAREReader.MI_OK:
            # Now comes the action like .Write(blockAddr, data)
    ```
    Actions that read/write to multiple sectors can ommit the authentication part, since
    it is done internally multiple times for the different sectors.

    Args:
        dev (string): The socket to use. "/dev/spidev0.0" by default.
        spd (int): The speed at which to clock. 1000000 by default.
    """
    NRSTPD = 22

    MAX_LEN = 16

    PCD_IDLE       = 0x00
    PCD_AUTHENT    = 0x0E
    PCD_RECEIVE    = 0x08
    PCD_TRANSMIT   = 0x04
    PCD_TRANSCEIVE = 0x0C
    PCD_RESETPHASE = 0x0F
    PCD_CALCCRC    = 0x03

    PICC_REQIDL    = 0x26
    PICC_REQALL    = 0x52
    PICC_ANTICOLL  = 0x93
    PICC_SElECTTAG = 0x93
    PICC_AUTHENT1A = 0x60
    PICC_AUTHENT1B = 0x61
    PICC_READ      = 0x30
    PICC_WRITE     = 0xA0
    PICC_DECREMENT = 0xC0
    PICC_INCREMENT = 0xC1
    PICC_RESTORE   = 0xC2
    PICC_TRANSFER  = 0xB0
    PICC_HALT      = 0x50

    MI_OK       = 0
    MI_NOTAGERR = 1
    MI_ERR      = 2

    Reserved00     = 0x00
    CommandReg     = 0x01
    CommIEnReg     = 0x02
    DivlEnReg      = 0x03
    CommIrqReg     = 0x04
    DivIrqReg      = 0x05
    ErrorReg       = 0x06
    Status1Reg     = 0x07
    Status2Reg     = 0x08
    FIFODataReg    = 0x09
    FIFOLevelReg   = 0x0A
    WaterLevelReg  = 0x0B
    ControlReg     = 0x0C
    BitFramingReg  = 0x0D
    CollReg        = 0x0E
    Reserved01     = 0x0F

    Reserved10     = 0x10
    ModeReg        = 0x11
    TxModeReg      = 0x12
    RxModeReg      = 0x13
    TxControlReg   = 0x14
    TxAutoReg      = 0x15
    TxSelReg       = 0x16
    RxSelReg       = 0x17
    RxThresholdReg = 0x18
    DemodReg       = 0x19
    Reserved11     = 0x1A
    Reserved12     = 0x1B
    MifareReg      = 0x1C
    Reserved13     = 0x1D
    Reserved14     = 0x1E
    SerialSpeedReg = 0x1F

    Reserved20        = 0x20
    CRCResultRegM     = 0x21
    CRCResultRegL     = 0x22
    Reserved21        = 0x23
    ModWidthReg       = 0x24
    Reserved22        = 0x25
    RFCfgReg          = 0x26
    GsNReg            = 0x27
    CWGsPReg          = 0x28
    ModGsPReg         = 0x29
    TModeReg          = 0x2A
    TPrescalerReg     = 0x2B
    TReloadRegH       = 0x2C
    TReloadRegL       = 0x2D
    TCounterValueRegH = 0x2E
    TCounterValueRegL = 0x2F

    Reserved30      = 0x30
    TestSel1Reg     = 0x31
    TestSel2Reg     = 0x32
    TestPinEnReg    = 0x33
    TestPinValueReg = 0x34
    TestBusReg      = 0x35
    AutoTestReg     = 0x36
    VersionReg      = 0x37
    AnalogTestReg   = 0x38
    TestDAC1Reg     = 0x39
    TestDAC2Reg     = 0x3A
    TestADCReg      = 0x3B
    Reserved31      = 0x3C
    Reserved32      = 0x3D
    Reserved33      = 0x3E
    Reserved34      = 0x3F

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
    serNum = []

    __default_block_print__ = tcolors.GRAY_50 + "Block{{:>3s}} |{color}{{dataA}}{{dataAB}}{{dataP}}{{dataB}}{end}"
    __trailer_block_print__ = tcolors.GRAY_50 + "Block{{:>3s}} |{color_A}{{dataA}}{color_AB}{{dataAB}}{color_P}{{dataP}}{color_B}{{dataB}}{end}"
    __colored_print__ = {
        0: __default_block_print__.format(color=tcolors.RED_BRIGHT, end=tcolors.ENDC),
        1: __default_block_print__.format(color=tcolors.BLUE_BRIGHT, end=tcolors.ENDC),
        2: __trailer_block_print__.format(color_A=tcolors.GREEN_BRIGHT, color_AB=tcolors.PURPLE_BRIGHT, color_P=tcolors.GRAY_22, color_B=tcolors.ORANGE_BRIGHT, end=tcolors.ENDC),
        3: __default_block_print__.format(color=tcolors.ENDC, end="")
    }

    def __init__(self, dev='/dev/spidev0.0', spd=1000000):
        spi.openSPI(device=dev, speed=spd)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(22, GPIO.OUT)
        GPIO.output(self.NRSTPD, 1)
        self.Init()

    def __del__(self):
        GPIO.cleanup()

    def __get_pretty_string__(self, block_number):
        if block_number == 0:
            return self.__colored_print__[0]
        elif block_number == 1 or block_number == 2:
            return self.__colored_print__[1]
        elif block_number % 4 == 3:
            return self.__colored_print__[2]
        else:
            return self.__colored_print__[3]

    def Init(self):
        GPIO.output(self.NRSTPD, 1)

        self.Reset()

        self.Write_MFRC522(self.TModeReg, 0x8D)
        self.Write_MFRC522(self.TPrescalerReg, 0x3E)
        self.Write_MFRC522(self.TReloadRegL, 30)
        self.Write_MFRC522(self.TReloadRegH, 0)

        self.Write_MFRC522(self.TxAutoReg, 0x40)
        self.Write_MFRC522(self.ModeReg, 0x3D)
        self.AntennaOn()

    def Reset(self):
        self.Write_MFRC522(self.CommandReg, self.PCD_RESETPHASE)

    def Write_MFRC522(self, addr, val):
        spi.transfer(((addr << 1) & 0x7E, val))

    def Read_MFRC522(self, addr):
        val = spi.transfer((((addr << 1) & 0x7E) | 0x80, 0))
        return val[1]

    def SetBitMask(self, reg, mask):
        tmp = self.Read_MFRC522(reg)
        self.Write_MFRC522(reg, tmp | mask)

    def ClearBitMask(self, reg, mask):
        tmp = self.Read_MFRC522(reg)
        self.Write_MFRC522(reg, tmp & (~mask))

    def AntennaOn(self):
        temp = self.Read_MFRC522(self.TxControlReg)
        if(~(temp & 0x03)):
            self.SetBitMask(self.TxControlReg, 0x03)

    def AntennaOff(self):
        self.ClearBitMask(self.TxControlReg, 0x03)

    def ToCard(self, command, sendData):
        backData = []
        backLen = 0
        status = self.MI_ERR
        irqEn = 0x00
        waitIRq = 0x00
        lastBits = None
        n = 0
        i = 0

        if command == self.PCD_AUTHENT:
            irqEn = 0x12
            waitIRq = 0x10
        if command == self.PCD_TRANSCEIVE:
            irqEn = 0x77
            waitIRq = 0x30

        self.Write_MFRC522(self.CommIEnReg, irqEn | 0x80)
        self.ClearBitMask(self.CommIrqReg, 0x80)
        self.SetBitMask(self.FIFOLevelReg, 0x80)

        self.Write_MFRC522(self.CommandReg, self.PCD_IDLE)

        while(i < len(sendData)):
            self.Write_MFRC522(self.FIFODataReg, sendData[i])
            i = i + 1

        self.Write_MFRC522(self.CommandReg, command)
        if command == self.PCD_TRANSCEIVE:
            self.SetBitMask(self.BitFramingReg, 0x80)

        i = 2000
        while True:
            n = self.Read_MFRC522(self.CommIrqReg)
            i = i - 1
            if ~((i != 0) and ~(n & 0x01) and ~(n & waitIRq)):
                break

        self.ClearBitMask(self.BitFramingReg, 0x80)

        if i != 0:
            if (self.Read_MFRC522(self.ErrorReg) & 0x1B) == 0x00:
                status = self.MI_OK

                if n & irqEn & 0x01:
                    status = self.MI_NOTAGERR

                if command == self.PCD_TRANSCEIVE:
                    n = self.Read_MFRC522(self.FIFOLevelReg)
                    lastBits = self.Read_MFRC522(self.ControlReg) & 0x07
                    if lastBits != 0:
                        backLen = (n - 1) * 8 + lastBits
                    else:
                        backLen = n * 8

                    if n == 0:
                        n = 1
                    if n > self.MAX_LEN:
                        n = self.MAX_LEN

                    i = 0
                    while i < n:
                        backData.append(self.Read_MFRC522(self.FIFODataReg))
                        i = i + 1
            else:
                status = self.MI_ERR

        return (status, backData, backLen)

    def Request(self, reqMode):
        status = None
        backBits = None
        TagType = []

        self.Write_MFRC522(self.BitFramingReg, 0x07)

        TagType.append(reqMode)
        (status, backData, backBits) = self.ToCard(self.PCD_TRANSCEIVE, TagType)

        if ((status != self.MI_OK) | (backBits != 0x10)):
            status = self.MI_ERR

        return (status, backBits)

    def Anticoll(self):
        backData = []
        serNumCheck = 0

        serNum = []

        self.Write_MFRC522(self.BitFramingReg, 0x00)

        serNum.append(self.PICC_ANTICOLL)
        serNum.append(0x20)

        (status, backData, backBits) = self.ToCard(self.PCD_TRANSCEIVE, serNum)

        if(status == self.MI_OK):
            i = 0
            if len(backData) == 5:
                while i < 4:
                    serNumCheck = serNumCheck ^ backData[i]
                    i = i + 1
                if serNumCheck != backData[i]:
                    status = self.MI_ERR
            else:
                status = self.MI_ERR

        return (status, backData)

    def CalulateCRC(self, pIndata):
        self.ClearBitMask(self.DivIrqReg, 0x04)
        self.SetBitMask(self.FIFOLevelReg, 0x80)
        i = 0
        while i < len(pIndata):
            self.Write_MFRC522(self.FIFODataReg, pIndata[i])
            i = i + 1
        self.Write_MFRC522(self.CommandReg, self.PCD_CALCCRC)
        i = 0xFF
        while True:
            n = self.Read_MFRC522(self.DivIrqReg)
            i = i - 1
            if not ((i != 0) and not (n & 0x04)):
                break
        pOutData = []
        pOutData.append(self.Read_MFRC522(self.CRCResultRegL))
        pOutData.append(self.Read_MFRC522(self.CRCResultRegM))
        return pOutData

    def SelectTag(self, serNum):
        backData = []
        buf = []
        buf.append(self.PICC_SElECTTAG)
        buf.append(0x70)
        buf += serNum[0:5]
        pOut = self.CalulateCRC(buf)
        buf += pOut
        (status, backData, backLen) = self.ToCard(self.PCD_TRANSCEIVE, buf)

        if (status == self.MI_OK) and (backLen == 0x18):
            return backData[0]
        else:
            return 0

    def Auth(self, authMode, BlockAddr, Sectorkey, serNum):
        """
        Authenticate with the tag. After a successful authentication you are
        authorized (according to the access bits) for the whole sector.
        You only need to reauthenticate when you are switching sectors.

        Returns:
            int: The status of the authentication. Either one of .MI_OK, .MI_NOTAGERR, .MI_ERR.
        """
        buff = []

        # First byte should be the authMode (A or B)
        buff.append(authMode)

        # Second byte is the trailerBlock (usually 7)
        buff.append(BlockAddr)

        # Now we need to append the authKey which usually is 6 bytes of 0xFF
        buff += Sectorkey[0:len(Sectorkey)]

        # Next we append the first 4 bytes of the UID
        buff += serNum[0:4]

        # Now we start the authentication itself
        (status, backData, backLen) = self.ToCard(self.PCD_AUTHENT, buff)

        # Check if an error occurred
        if not(status == self.MI_OK):
            print("AUTH ERROR!!")
        if not (self.Read_MFRC522(self.Status2Reg) & 0x08) != 0:
            print("AUTH ERROR(status2reg & 0x08) != 0")

        # Return the status
        return status

    def StopCrypto1(self):
        self.ClearBitMask(self.Status2Reg, 0x08)

    def Read(self, blockAddr, printData=False, prettyPrint=False):
        """
        Read data from a block of the tag.

        Args:
            blockAddr (uint8): The address of the block to read from.
            printData (boolean): Whether or not to print the read data to the console. False by default.
            prettyPrint (boolean): Whether or not to print the read data using xterm256 colors. False by default. If set to True, implicitly sets printData to True.

        Returns:
            [uint8]: The data read from the defined block.
        """
        recvData = []
        recvData.append(self.PICC_READ)
        recvData.append(blockAddr)
        pOut = self.CalulateCRC(recvData)
        recvData += pOut
        (status, backData, backLen) = self.ToCard(self.PCD_TRANSCEIVE, recvData)

        if not(status == self.MI_OK):
            print("Error while reading!")

        if len(backData) == 16:
            if prettyPrint:
                dataA  = "".join(" {:>02X}".format(n) for n in backData[0:6])
                dataAB = "".join(" {:>02X}".format(n) for n in backData[6:9])
                dataP = "".join(" {:>02X}".format(backData[9]))
                dataB  = "".join(" {:>02X}".format(n) for n in backData[10:16])
                print(self.__get_pretty_string__(blockAddr).format(str(blockAddr), dataA=dataA, dataAB=dataAB, dataP=dataP, dataB=dataB))
            elif printData:
                print("Block{:>3s} |{}".format(str(blockAddr), "".join(" {:>02X}".format(n) for n in backData)))
            return backData
        return None

    def Write(self, blockAddr, writeData):
        """
        Write data to a block on the tag.

        Args:
            blockAddr (uint8): The address of the block to write to.
            writeData ([uint8]): The data to write to the defined block.
        """
        buff = []
        buff.append(self.PICC_WRITE)
        buff.append(blockAddr)
        crc = self.CalulateCRC(buff)
        buff += crc
        (status, backData, backLen) = self.ToCard(self.PCD_TRANSCEIVE, buff)
        if not(status == self.MI_OK) or not(backLen == 4) or not((backData[0] & 0x0F) == 0x0A):
            status = self.MI_ERR

        # print(str(backLen) + " backdata &0x0F == 0x0A " + str(backData[0] & 0x0F))
        if status == self.MI_OK:
            i = 0
            buf = []
            while i < 16:
                buf.append(writeData[i])
                i = i + 1
            crc = self.CalulateCRC(buf)
            buf += crc
            (status, backData, backLen) = self.ToCard(self.PCD_TRANSCEIVE, buf)
            if not(status == self.MI_OK) or not(backLen == 4) or not((backData[0] & 0x0F) == 0x0A):
                print("Error while writing")

    def WriteAll(self, key, uid, value):
        """
        Writes the passed value to all data blocks. By using 0x00 as value, you
        can effectively reset the tag to its factory values in regards to the data
        blocks. Sector trailers as well as the first sector are not affected.

        Args:
            key ([uint8]): Key A of the sector trailer block.
            uid ([uint8]): The 4 byte uid of the card/tag.
            value (uint8): The value to be written to all data blocks.
        """
        if not isinstance(value, int) or value > 255:
            raise errors.InvalidValueException("Invalid value to write to all data blocks.")

        for i in range(0, len(self.data_blocks), 3):
            status = self.Auth(self.PICC_AUTHENT1A, self.data_blocks[i], key, uid)

            if status == self.MI_OK:
                all_values = [value for _ in range(0, 16)]
                self.Write(self.data_blocks[i], all_values)
                self.Write(self.data_blocks[i + 1], all_values)
                self.Write(self.data_blocks[i + 2], all_values)

    def WriteText(self, key, uid, text):
        """
        Writes a passed string in sequential order onto the tag. Starting at the first data block (meaning block #4), existing data is overwritten. Writing always happens in units of one block. If the trailing end of the passed string does not fill a block, the remaining bytes are padded with 0x00.

        Args:
            key ([uint8]): Key A of the sector trailer block.
            uid ([uint8]): The 4 byte uid of the card/tag.
            text (string): The string to be written.

        Raises:
            errors.TextTooLongException: If the text takes up more space than there are data blocks available.
        """
        text_length = len(text)
        if text_length > len(self.data_blocks) * 16:
            raise errors.TextTooLongException

        block_data = []
        blocks = text_length // 16
        remainder_block = text_length % 16
        text = [ord(x) for x in text]
        for i in range(0, blocks):
            block_data.append(text[0:16])
            del text[0:16]
        if len(text) > 0:
            text += [0x00 for _ in range(0, 16 - len(text))]
            block_data.append(text)

        status = None
        for i in range(0, len(block_data)):
            if self.data_blocks[i] % 4 == 0:
                status = self.Auth(self.PICC_AUTHENT1A, self.data_blocks[i], key, uid)

            if status == self.MI_OK:
                self.Write(self.data_blocks[i], block_data[i])
            else:
                print("Authentication error")

    def PrettyDumpClassic1K(self, key, uid, pretty=True):
        """
        Dumps all blocks to the console. Coloring is inspired by https://en.wikipedia.org/wiki/File:MiFare_Byte_Layout.png.

        Args:
            key ([uint8]): Key A of the sector trailer block.
            uid ([uint8]): The 4 byte uid of the card/tag.
            pretty (boolean): Whether or not to print to console using colors. Defaults to `True`.
        """
        for i in range(0, 64, 4):
            # Authenticate
            status = self.Auth(self.PICC_AUTHENT1A, i, key, uid)

            # Check if authenticated
            if status == self.MI_OK:
                if pretty:
                    print("{}{:-^58}{}".format(tcolors.YELLOW, " Sector {} ".format(i // 4), tcolors.ENDC))
                else:
                    print("{:-^58}".format(" Sector {} ".format(i // 4)))

                self.Read(i, prettyPrint=pretty)
                self.Read(i + 1, prettyPrint=pretty)
                self.Read(i + 2, prettyPrint=pretty)
                self.Read(i + 3, prettyPrint=pretty)
            else:
                print("Authentication error")
                raise errors.AuthenticationException

    def DumpClassic1K(self, key, uid):
        """
        Dumps all blocks to the console.

        Args:
            key ([uint8]): Key A of the sector trailer block.
            uid ([uint8]): The 4 byte uid of the card/tag.
        """
        self.PrettyDumpClassic1K(key, uid, pretty=False)

    def DumpClassic1K_Data(self, key, uid):
        """
        Dumps only DATA blocks. The first sector as well as all sector trailer blocks are ommitted.

        Args:
            key ([uint8]): Key A of the sector trailer block.
            uid ([uint8]): The 4 byte uid of the card/tag.

        Returns:
            [[uint8]]: The complete data dump. The first index describes the data block in order, the second the byte of that block.
        """
        data = []
        for i in range(4, 64, 4):
            # Authenticate
            status = self.Auth(self.PICC_AUTHENT1A, i, key, uid)

            # Check if authenticated
            if status == self.MI_OK:
                data.append(self.Read(i))
                data.append(self.Read(i + 1))
                data.append(self.Read(i + 2))
            else:
                print("Authentication error")
                raise errors.AuthenticationException
        return data

    def DumpClassic1K_Text(self, key, uid, print_text=True):
        """
        Dumps only DATA blocks. The data in each block is interpreted as string according to pythons ```chr(value)```.

        Args:
            key ([uint8]): Key A of the sector trailer block.
            uid ([uint8]): The 4 byte uid of the card/tag.

        Returns:
            string: All the data on the tag interpreted as a single string.
        """
        data = self.DumpClassic1K_Data(key, uid)
        text = ""
        for block in data:
            b_print = ""
            for byte in block:
                if print_text:
                    b_print += chr(byte) if byte >= 32 else "."
                text += chr(byte)
            if print_text:
                print(b_print)

        return text
