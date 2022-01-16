import socket
from contextlib import closing

def main():
  host = 'XXX.XXX.XXX.XXX'
  port = 4000
  buf_size = 4096

  soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  with closing(soc):
    soc.bind((host, port))
    while True:
      print(soc.recv(buf_size))

if __name__ == '__main__':
  main()