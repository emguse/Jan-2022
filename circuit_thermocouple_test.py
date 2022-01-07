import board
import digitalio
import time
import busio
import adafruit_max31855
from adafruit_ht16k33.segments import Seg7x4

spi = busio.SPI(board.GP10, MISO=board.GP12)
cs = digitalio.DigitalInOut(board.GP13)
max31855 = adafruit_max31855.MAX31855(spi, cs)

i2c = busio.I2C(board.GP17, board.GP16)
display = Seg7x4(i2c)
display.brightness = 0.5

while True:
    temperature = round(max31855.temperature, 1)
    #print('Temperature: {} deg'.format(temperature))
    #print((temperature,)) # Tuples for graphing in Mu's plotter
    print(temperature)
    display.fill(0)
    if temperature <= -100:
        display.print(str(int(temperature)))
    elif temperature >= 1000:
        display.print(str(int(temperature)))
    else:
        display.print(str(temperature))
    time.sleep(1)