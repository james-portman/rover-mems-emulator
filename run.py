#!python

import serial
import time

def main():
    ser = serial.Serial()
    ser.port = '/dev/ttyUSB0'
    ser.baudrate = 9600
    ser.bytesize = 8
    ser.parity = "N"
    ser.stopbits = 1
    ser.open()


    print(ser.name)         # check which port was really used
    # ser.write(b'hello')     # write a string

    while True:
        x = ser.read()          # read one byte
        print("<", x)
        x_int = int.from_bytes(x, "big")
        ser.write(x)

        if x_int == 0xca:
            print("init 1")
            print("0xCA")
        elif x_int == 0x75:
            print("init 2")
            print("75")
        elif x_int == 0xd0:
            print("version")
            ser.write(b'\x99')
            ser.write(b'\x00')
            ser.write(b'\x02')
            ser.write(b'\x03')
        elif x_int == 0xf4:
            print("PING")
            ser.write(b'\x00')
        elif x_int == 0x00:
            print("00")
            ser.write(b'\x00')
        elif x_int == 0x80:
            print("Data packet 0x80")
            data80(ser)
        elif x_int == 0x7D:
            print("Data packet 0x7D")
            data7d(ser)
        else:
            print("************ unknown command")

        ser.flush()

    ser.close()

def data80(ser):
    ser.write(b"\x1c") # (28) packet length
    ser.write(b"\xFF") # rpm lower 0x01-2 Engine speed in RPM (16 bits)
    ser.write(b"\xFF") # rpm lower
    ser.write(b"\xF0") # 0x03 Coolant temperature in degrees C with +55 offset and 8-bit wrap
    ser.write(b"\x40") # 0x04 Computed ambient temperature in degrees C with +55 offset and 8-bit wrap
    ser.write(b"\x4B") # 0x05 Intake air temperature in degrees C with +55 offset and 8-bit wrap
    ser.write(b"\x00") # 0x06 Fuel temperature in degrees C with +55 offset and 8-bit wrap. This is not supported on the Mini SPi, and always appears as 0xFF.
    ser.write(b"\x05") # 0x07  MAP sensor value in kilopascals
    ser.write(b"\x7B") # 0x08 Battery voltage, 0.1V per LSB (e.g. 0x7B == 12.3V)
    ser.write(b"\x03") # 0x09 Throttle pot voltage, 0.02V per LSB. WOT should probably be close to 0xFA or 5.0V.
    ser.write(b"\x00") # 0x0A Idle switch. Bit 4 will be set if the throttle is closed, and it will be clear otherwise.
    ser.write(b"\x00") # 0x0B Unknown. Probably a bitfield. Observed as 0x24 with engine off, and 0x20 with engine running. A single sample during a fifteen minute test drive showed a value of 0x30.
    ser.write(b"\x00") # 0x0C  Par /neutral switch. Zero is closed, nonzero is open.
    ser.write(b"\xFF") # 0x0D Fault codes. On the Mini SPi, only two bits in this location are checked:
    ser.write(b"\xFF") # 0x0E Fault codes. On the Mini SPi, only two bits in this location are checked:
    ser.write(b"\x00") # 0x0F Unknown
    ser.write(b"\x00") # 0x10 Unknown
    ser.write(b"\x00") # 0x11 Unknown
    ser.write(b"\x00") # 0x12 Idle air control motor position. On the Mini SPi's A-series engine, 0 is closed, and 180 is wide open.
    ser.write(b"\x00") # 0x13-14 Idle speed deviation (16 bits)
    ser.write(b"\x00") #
    ser.write(b"\x00") # 0x15 Unknown
    ser.write(b"\x00") # 0x16 Ignition advance, 0.5 degrees per LSB with range of -24 deg (0x00) to 103.5 deg (0xFF)
    ser.write(b"\x00") # 0x17-18 Coil time, 0.002 milliseconds per LSB (16 bits)
    ser.write(b"\x00") #
    ser.write(b"\x00") # 0x19 Unknown
    ser.write(b"\x00") # 0x1A Unknown
    ser.write(b"\x00") # 0x1B Unknown

def data7d(ser):
    ser.write(b"\x20") # (32) packet length
    ser.write(b"\x00") # ?
    ser.write(b"\x03") # Throttle angle?
    ser.write(b"\x00") # Unknown
    ser.write(b"\xFF") # Sometimes documented to be air/fuel ratio, but often observed to never change from 0xFF
    ser.write(b"\x00") # Unknown
    ser.write(b"\xF0") # Lambda sensor voltage, 0.5mv per LSB
    ser.write(b"\x00") # Lambda sensor frequency?
    ser.write(b"\x00") # Lambda sensor duty cycle?
    ser.write(b"\x01") # Lambda sensor status? 0x01 for good, any other value for no good
    ser.write(b"\x00") # Loop indicator, 0 for open loop and nonzero for closed loop
    ser.write(b"\x00") # Long term trim?
    ser.write(b"\x00") # Short term trim, 1% per LSB
    ser.write(b"\x00") # Carbon canister purge valve duty cycle?
    ser.write(b"\x00") # Unknown
    ser.write(b"\x00") # Idle base position
    ser.write(b"\x00") # Unknown
    ser.write(b"\x00") # Unknown
    ser.write(b"\x00") # Unknown
    ser.write(b"\x00") # Unknown
    ser.write(b"\x00") # Idle error?
    ser.write(b"\x00") # Unknown
    ser.write(b"\x00") # Unknown
    ser.write(b"\x00") # Unknown
    ser.write(b"\x00") # Unknown
    ser.write(b"\x00") # Unknown
    ser.write(b"\x00") # Unknown
    ser.write(b"\x00") # Unknown
    ser.write(b"\x00") # Unknown
    ser.write(b"\x00") # Unknown
    ser.write(b"\x00") # Unknown
    ser.write(b"\x00") # Unknown


if __name__ == "__main__":
    main()
