import board
import digitalio
import time
import busio
import adafruit_max31855
spi = busio.SPI(board.GP10, MISO=board.GP12)
cs = digitalio.DigitalInOut(board.GP13)
max31855 = adafruit_max31855.MAX31855(spi, cs)

while True:
    print('Temperature: {} deg'.format(max31855.temperature))
    time.sleep(1)