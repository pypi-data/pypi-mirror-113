from enum import Enum
import socket
import struct
import os


class TCPPacketsTypes(int, Enum):
    # Error packet
    ERROR = 0
    # Generic acknowledge
    GENERIC_OK = 1
    # From Scripts/scriptserver.h  ! WARNING ! : IN <-> OUT changed
    OUT_WRITE_DEVICE = 2
    IN_WRITE_DEVICE_STATUS = 3
    OUT_READ_DEVICE = 4
    IN_READ_DEVICE_STATUS = 5
    IN_READ_DEVICE_DATA = 6
    # Buffer commands
    OUT_READ_BUFFER = 7
    IN_BUFFER_DATA = 8
    # Blocks commands
    OUT_DATABASE_PATH_REQUEST = 9
    IN_DATABASE_PATH = 10
    # Driver request
    OUT_DRIVER_PATH = 11
    IN_DRIVER_PATH = 12
    # Blocks updating
    OUT_UPDATE_BLOCKS = 13
    # Closing device
    OUT_CLOSE_DEVICE = 14


class ErrorCode(int, Enum):
    INVALID_ALIAS = 0  # Request for the wrong alias
    WRITE_ERROR = 1


errorMessages = {
    ErrorCode.INVALID_ALIAS: "Alias invalide",
    ErrorCode.WRITE_ERROR: "Erreur lors de l'ecriture"}


LOCALHOST = "127.0.0.1"
DEFAULT_PORT = 8445
DEFAULT_TIMEOUT_MS = 100000


_opened = False


def close():
    __s__.close()


def open(port=DEFAULT_PORT):
    # print("Opening...")
    global __s__
    global _opened
    retry = 2
    while(retry):
        retry -= 1
        try:
            __s__ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            __s__.settimeout(DEFAULT_TIMEOUT_MS / 1000)
            __s__.connect((LOCALHOST, port))
            _opened = True
        except socket.error as exc:
            print("closing...")
            close()
            # Retry once
            _opened = False
            if(retry == 0):  # After second try
                print("second try fail")
                raise Exception("Connexion à l'hôte impossible : %s" % exc)


def sendPacket(data: bytearray):
    #print("Sending packet...")
    global __s__
    global _opened
    if(_opened == False):
        open()

    if(_opened):
        try:
            __s__.send(data)
        except Exception:
            # recreate the socket and try again
            close()
            open()  # Add the port here !
            __s__.send(data)


def readPacket(timeout_ms=0):
    global __s__
    global _opened
    if(timeout_ms > 0):
        # +1 to let the communication happend (and C++ to do its thing)
        __s__.settimeout(timeout_ms / 1000 + 1)
    else:
        __s__.settimeout(DEFAULT_TIMEOUT_MS / 1000)
    packetType = 0
    data = b''
    if(not _opened):
        open()
    if(_opened):
        maxBytes = 65532
        length = maxBytes
        raw = b''
        while length == maxBytes:
            buf, _ = __s__.recvfrom(maxBytes)
            length = len(buf)
            raw += buf
        packetType = raw[0]
        data = raw[1:]

    return packetType, data


def printErrorCode(code: int):
    err = errorMessages[ErrorCode(code)]
    if(err is None):
        print("Erreur inconnue")
    else:
        print(err)


def writeToDevice(alias: str, data: bytearray):
    packet = struct.pack('!BB%dsh%ds' % (len(alias), len(data)),
                         TCPPacketsTypes.OUT_WRITE_DEVICE.value, len(alias), alias.encode(), len(data), data)

    sendPacket(packet)
    type, data = readPacket()
    if(type == TCPPacketsTypes.ERROR.value):
        printErrorCode(data[0])
        return False
    else:
        return True


def readFromDevice(alias: str, storeInBuffer: bool = False, timeout_ms=None):
    if(timeout_ms is None):
        timeout_ms = DEFAULT_TIMEOUT_MS
    elif(timeout_ms > 0xFFFFFFFF or timeout_ms < 0):
        timeout_ms = DEFAULT_TIMEOUT_MS

    packet = struct.pack('!BB%dsBL' % len(alias),
                         TCPPacketsTypes.OUT_READ_DEVICE.value, len(alias), alias.encode(), storeInBuffer, timeout_ms)

    sendPacket(packet)
    if(storeInBuffer):  # Will probably get deleted, the buffer isn't used
        _, status = readPacket(timeout_ms)
        if(status == 0):
            print("Erreur lors de l'envoi")
    else:
        type, data = readPacket(timeout_ms)
        if(type == TCPPacketsTypes.ERROR.value):
            printErrorCode(data[0])
        else:
            return data[4:]


def getDatabasePath():
    packet = struct.pack('!B', TCPPacketsTypes.OUT_DATABASE_PATH_REQUEST.value)
    sendPacket(packet)
    _, path = readPacket()
    return path[2:]


def getDeviceDriverPath(alias: str):
    packet = struct.pack('!BB%ds' % len(
        alias), TCPPacketsTypes.OUT_DRIVER_PATH, len(alias), alias.encode())
    sendPacket(packet)
    type, data = readPacket()
    if(type == TCPPacketsTypes.ERROR.value):
        printErrorCode(data[0])
        return None
    else:
        driverName = data[2:]
        return driverName.decode()


def updateDatabase(alias: str = None, full: bool = False):
    if(alias is None):
        packet = struct.pack('!BB', TCPPacketsTypes.OUT_UPDATE_BLOCKS, 0)
    else:
        packet = struct.pack('!BB%dsB' % len(
            alias), TCPPacketsTypes.OUT_UPDATE_BLOCKS, len(alias), alias.encode(), full)

    sendPacket(packet)


def closeDevice(alias):
    packet = struct.pack('!BB%ds' % len(
        alias), TCPPacketsTypes.OUT_CLOSE_DEVICE.value, len(alias), alias.encode())
    sendPacket(packet)
    type, data = readPacket()
    if(type == TCPPacketsTypes.ERROR.value):
        printErrorCode(data[0])
        return False
    else:
        return True
