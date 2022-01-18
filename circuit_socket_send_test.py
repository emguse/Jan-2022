import board
import busio
import digitalio
from adafruit_wiznet5k.adafruit_wiznet5k import WIZNET5K
import adafruit_wiznet5k.adafruit_wiznet5k_socket as socket
import neopixel
from rainbowio import colorwheel
import time

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

onbord_neopix = OnbordNeopix()
onbord_neopix.rainbow_step()

print("socket Test")
onbord_neopix.rainbow_step(64)

host = "192.168.XXX.XXX"
port = 4000
time_out = 5

cs = digitalio.DigitalInOut(board.D10)
spi_bus = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

eth = WIZNET5K(spi_bus, cs)

soc = eth.get_socket()
print(soc)

print("Create TCP Client Socket")
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.settimeout(time_out)

print("Connecting")
soc.connect((host, port))

size = soc.send(b'Hello, world')
print("Sent", size, "bytes")

soc.close()

while True:
    onbord_neopix.rainbow_step()
    time.sleep(0.1)
