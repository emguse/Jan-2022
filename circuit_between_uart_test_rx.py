import time
import board
import busio

uart = busio.UART(board.GP0, board.GP1, baudrate=9600, timeout=0)

INTERVAL = 3.0
last_time = 0

n = 0
message_started = False

while True:
    now = time.monotonic()
    if now - last_time >= INTERVAL:
        s = n
        #uart.write(bytes(f"{s}", "ascii"))
        #print("sending value", s)
        n = n + 1
        last_time = now
    byte_read = uart.read(1)
    if byte_read is None:
        continue
    if byte_read == b"<":
        message = []
        message_started = True
        continue
    if message_started:
        if byte_read == b">":
            #print(message)
            msg = ""
            for s in message:
                msg += s
            print(msg)
            message_started = False
        else:
            message.append(chr(byte_read[0]))
            #print(message)
