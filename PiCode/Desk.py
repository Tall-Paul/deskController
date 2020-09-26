from bluepy.btle import Scanner, DefaultDelegate, UUID, Peripheral, ADDR_TYPE_RANDOM
import struct
import time
import binascii

#heavily based on https://github.com/nconrad/idasen-desk-controller

def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)


class MovementService():
    svcUUID = UUID('99fa0001-338a-1024-8a49-009c0215f78a')
    dataUUID = UUID('99fa0002-338a-1024-8a49-009c0215f78a')

    def __init__(self, periph):
        self.periph = periph
        self.service = self.periph.getServiceByUUID(self.svcUUID)
        self.data = self.service.getCharacteristics(self.dataUUID)[0] 
        
    def moveUp(self):
        cmd = bytearray.fromhex("4700")        
        self.data.write(cmd)
    
    def moveDown(self):
        cmd = bytearray.fromhex("4600")
        self.data.write(cmd)

    def stop(self):
        cmd = bytearray.fromhex("FF00")
        self.data.write(cmd)
    
    
    



class PositionSensor():
    svcUUID = UUID('99fa0020-338a-1024-8a49-009c0215f78a')  # Ref https://www.bluetooth.com/specifications/gatt/services 
    dataUUID = UUID('99fa0021-338a-1024-8a49-009c0215f78a')

    def __init__(self, periph):
        self.periph = periph
        self.service = self.periph.getServiceByUUID(self.svcUUID)
        self.data = self.service.getCharacteristics(self.dataUUID)[0]

    def read(self):
        val = self.data.read() 
        dat = struct.unpack("HH",val)
        magicnumber = 0.0998689384010485
        height = magicnumber * dat[0]
        return truncate(height + 612.13)


class Desk(Peripheral):

    def __init__(self):
        DeskAddress = ""
        scanner = Scanner().withDelegate(ScanDelegate())
        devices = scanner.scan(1.0)
        for dev in devices:               
            for (adtype, desc, value) in dev.getScanData():                
                if (adtype == 9 and "desk" in value):
                    DeskAddress = dev.addr
        Peripheral.__init__(self, DeskAddress, addrType=ADDR_TYPE_RANDOM)
        self.position = PositionSensor(self)
        self.movement = MovementService(self)
    
    def moveTo(self, position):
        if (self.position.read() > position):         
            while (self.position.read() > position):
                self.movement.moveDown()
                time.sleep(0.1)
            self.movement.stop()                
        elif (self.position.read() < position):        
            while (self.position.read() < position):
                self.movement.moveUp()
                time.sleep(0.1)   
            self.movement.stop()
    
    
