import serial, time

def toByte(s):
    return chr(int(s, 2))

# for USB_serial_line
#port = serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=3.0)
port = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=3.0)

byte1Clear7 = toByte('11000000')
byte1Show7 = toByte('01000000')

byte1Clear16 = toByte('10000000')
byte1Show16 = toByte('00000000')

rowArrA = [ '00011000',
    '00011000',
    '00011000',
    '11111111',
    '01111110',
    '00111100',
    '00011000',
    '00000000']

rowArrB = [ '10000000',
    '00000000',
    '00000000',
    '00000000',
    '00000000',
    '00000000',
    '00000000',
    '00011000']

strRowArrA = str(bytearray(map(toByte,rowArrA)))
strRowArrB = str(bytearray(map(toByte,rowArrB)))

byteColorBase = int('11111001', 2)
count = 0
lastColor = byteColorBase

while True:
    count += 1
    port.write(byte1Clear7)
    # sleep less1600ms
    time.sleep(1.8)
    port.write(byte1Show7)
    color = byteColorBase+(count%6)
    #print byteColorBase,color
    port.write(chr(color))
    port.write(strRowArrA)
    
    time.sleep(1.8)
    port.write(byte1Show7)
    port.write(chr(lastColor))
    port.write(strRowArrB)
    time.sleep(5)
    lastColor = color
