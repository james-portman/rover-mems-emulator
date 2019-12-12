// this seems to crash after a while/upset the android app but it reconnects
int timedOut;
bool locked = true; // needs unlock command like real ecu
int rpm = 0;
int coolant = 0;

int unlocked_millis = 0; // timestamp that ecu got unlocked at


// the setup routine runs once when you press reset:
void setup() {
  Serial1.begin(9600); // for actual cable
}

int getData(int timeoutMs) {
  timedOut = millis() + timeoutMs;

  while (millis() < timedOut) {
    if (Serial1.available() > 0) {
      int inByte = Serial1.read();
      send(inByte); // echo back
      return inByte;
    }
    delay(1);
  }
  return -1;
}

void send(int byte) {
  Serial1.write(byte);
  delay(1);
}


// the loop routine runs over and over again forever:
void loop() {

  // update rpm etc
  if (millis() > unlocked_millis + 10000) {
    rpm += 20;
    if (rpm > 1050) {
      rpm = 1000;
    }
  } else if (millis() > unlocked_millis + 5000) {
    // start the car up
    rpm = 1000;
  }
  coolant = ((millis() - unlocked_millis)/1000);
  if (coolant > 145) {
    coolant = 145;
  }


  int inByte = getData(1000);

  switch (inByte) {

    case -1: // no data
      delay(100);
      break;

    case 0xCA: // unlock
      if (getData(500) == 0x75) { // 2nd byte of unlock
        locked = false;
        unlocked_millis = millis();
      }
      break;

    case 0xD0: // ecu type, pretend to be an ecu
      if (locked) { break; }
      send(0x99);
      send(0x00);
      send(0x02);
      send(0x03);
      break;

    case 0xF4: // ping
      if (locked) { break; }
      send(0x00);
      break;

    case 0x00: // my android code sends - maybe wrong?
      if (locked) { break; }
      send(0x00);
      break;

    case 0x80: // 28 byte data packet
      send(28);
      send((rpm & 0xFF00) >> 8); // 0x01-2 Engine speed in RPM (16 bits)
      send((rpm & 0x00FF));
      send(coolant + 55); // 0x03 Coolant temperature in degrees C with +55 offset and 8-bit wrap
      send(0x40); // 0x04 Computed ambient temperature in degrees C with +55 offset and 8-bit wrap
      send(0x4B); // 0x05 Intake air temperature in degrees C with +55 offset and 8-bit wrap
      send(0x00); // 0x06 Fuel temperature in degrees C with +55 offset and 8-bit wrap. This is not supported on the Mini SPi, and always appears as 0xFF.
      send(0x05); // 0x07  MAP sensor value in kilopascals
      send(0x7B); // 0x08 Battery voltage, 0.1V per LSB (e.g. 0x7B == 12.3V)
      send(0x03); // 0x09 Throttle pot voltage, 0.02V per LSB. WOT should probably be close to 0xFA or 5.0V.
      send(0x00); // 0x0A Idle switch. Bit 4 will be set if the throttle is closed, and it will be clear otherwise.
      send(0x00); // 0x0B Unknown. Probably a bitfield. Observed as 0x24 with engine off, and 0x20 with engine running. A single sample during a fifteen minute test drive showed a value of 0x30.
      send(0x00); // 0x0C  Par /neutral switch. Zero is closed, nonzero is open.
      send(0xFF); // 0x0D Fault codes. On the Mini SPi, only two bits in this location are checked:
      send(0xFF); // 0x0E Fault codes. On the Mini SPi, only two bits in this location are checked:
      send(0x00); // 0x0F Unknown
      send(0x00); // 0x10 Unknown
      send(0x00); // 0x11 Unknown
      send(0x00); // 0x12 Idle air control motor position. On the Mini SPi's A-series engine, 0 is closed, and 180 is wide open.
      send(0x00); // 0x13-14 Idle speed deviation (16 bits)
      send(0x00);
      send(0x00); // 0x15 Unknown
      send(0x00); // 0x16 Ignition advance, 0.5 degrees per LSB with range of -24 deg (0x00) to 103.5 deg (0xFF)
      send(0x00); // 0x17-18 Coil time, 0.002 milliseconds per LSB (16 bits)
      send(0x00);
      send(0x00); // 0x19 Unknown
      send(0x00); // 0x1A Unknown
      send(0x00); // 0x1B Unknown
      break;

    case 0x7D: // 32 byte data packet
      send(32); // packet length
      send(0x00); // ?
      send(0x03); // Throttle angle?
      send(0x00); // Unknown
      send(0xFF); // Sometimes documented to be air/fuel ratio, but often observed to never change from 0xFF
      send(0x00); // Unknown
      send(0x66); // Lambda sensor voltage, 0.5mv per LSB
      send(0x00); // Lambda sensor frequency?
      send(0x00); // Lambda sensor duty cycle?
      send(0x01); // Lambda sensor status? 0x01 for good, any other value for no good
      send(0x00); // Loop indicator, 0 for open loop and nonzero for closed loop
      send(0x00); // Long term trim?
      send(0x00); // Short term trim, 1% per LSB
      send(0x00); // Carbon canister purge valve duty cycle?
      send(0x00); // Unknown
      send(0x00); // Idle base position
      send(0x00); // Unknown
      send(0x00); // Unknown
      send(0x00); // Unknown
      send(0x00); // Unknown
      send(0x00); // Idle error?
      send(0x00); // Unknown
      send(0x00); // Unknown
      send(0x00); // Unknown
      send(0x00); // Unknown
      send(0x00); // Unknown
      send(0x00); // Unknown
      send(0x00); // Unknown
      send(0x00); // Unknown
      send(0x00); // Unknown
      send(0x00); // Unknown
      send(0x00); // Unknown
      break;
  }

  delay(100); // try and have a rest

}

