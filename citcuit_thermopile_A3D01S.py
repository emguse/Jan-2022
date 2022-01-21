import board
import busio
import time
from adafruit_bus_device.i2c_device import I2CDevice
from rainbowio import colorwheel
import neopixel

'''
- Applicable to Nippon Ceramic's thermopile sensor 'A3D01S-FU-50-60'
- 2022/01/22 ver.1.00
- Author : emguse
- License: MIT License
'''

I2C_ADDRES = 0x3D

class ThermopileInfraredSensorA3D01S_FU_50_60():
    def __init__(self, i2c) -> None:
        time.sleep(0.05)
        self.a3d01s_addres = I2C_ADDRES
        self.device = I2CDevice(i2c, self.a3d01s_addres)
        self.self_temp = 0
        self.object_temp = 0
    def self_temperature(self):
        with self.device:
            read_addres = bytes([0x70])
            raw = bytearray(3)
            self.device.write_then_readinto(read_addres, raw)
            pv = (raw[0] | raw[1] << 8)
            self.self_temp = pv / 8 - 20 # Celsius degree
    def object_temperature(self):
        with self.device:
            read_addres = bytes([0x71])
            raw = bytearray(3)
            self.device.write_then_readinto(read_addres, raw)
            pv = (raw[0] | raw[1] << 8)
            self.object_temp = pv / 8 - 30 # Celsius degree
        
class OnbordNeopix():
    def __init__(self) -> None:
        self.pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, auto_write=False)
        self.pixel.brightness = 0.3
        self.color_step = 0
    def rainbow(self, delay):
        for color_value in range(255):
            for led in range(1):
                pixel_index = (led * 256 // 1) + color_value
                self.pixel[led] = colorwheel(pixel_index & 255)
            self.pixel.show()
            time.sleep(delay)
    def rainbow_step(self, Skip_step=0): # Each time it is called, it advances the color one step
        self.color_step += 1 + Skip_step
        self.pixel[0] = colorwheel(self.color_step & 255)
        self.pixel.show()

def main(): 
    onbord_neopix = OnbordNeopix()
    I2C_SCL = board.SCL
    I2C_SDA = board.SDA  
    i2c = busio.I2C(scl=I2C_SCL, sda=I2C_SDA)
    
    a3d01s = ThermopileInfraredSensorA3D01S_FU_50_60(i2c)
    
    while True:
        onbord_neopix.rainbow_step()
        a3d01s.self_temperature()
        a3d01s.object_temperature()
        print("self_temp  : ", str(a3d01s.self_temp))
        print("object_temp: ", str(a3d01s.object_temp))
        time.sleep(0.5)

if __name__ == "__main__":
    main()