from socket import *
import time
import argparse
import ipaddress
import json
from objetos import BaseResponse
import logging

LOG_FILENAME = 'server_udp.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

# se crea un parser para recibir argumentos en consola
parser = argparse.ArgumentParser()

# se crea el argumento addres de tipo ipv4
parser.add_argument("host", help="Direccion ipv4 al cual el servidor escucha",
                    type=ipaddress.ip_address, default="0.0.0.0")

# se crea el argumento port de tipo int
parser.add_argument("port", help="Puerto udp a conectar", type=int, default=3334)

# se crea el argumento type de tipo int
parser.add_argument("server_type", help="1 para servidor dedicado 0 para recibir un solo paquete", type=int, default=0)

# se lee todos los argumentos de la consola
args = parser.parse_args()

host = str(args.host)
port = args.port
buffer = 102400

UDPSock = socket(AF_INET, SOCK_DGRAM)
UDPSock.bind((host, port))

time.time()
print("esperando por datos")
logging.info("esperando por datos")

total_bytes = 0
time_stamp = time.time()
total_received = 0

flag = True

while 1:
    data, addr = UDPSock.recvfrom(buffer)
    if flag:
        time_stamp = time.time()
        flag = False
        (cliente_direccion, cliente_puerto) = addr
        print ('datos recibidos del cliente: '+cliente_direccion+':'+str(cliente_puerto))
        logging.info('datos recibidos del cliente: '+cliente_direccion+':'+str(cliente_puerto))
        #print ('mensaje: '+ str(data))
    if not data:
        print("No data.")
        break
    else:
        done_stamp = time.time()
        data = len(data)
        total_bytes += data
        total_received += 1
        rate = total_bytes / (done_stamp - time_stamp) * 8 / 1000
        #TODO: revisar por que rayos recibe 1 paquete de mas
        if data == 1:
            print("Bytes totales: " + str(total_bytes))
            print("Cantidad de tramas: " + str(total_received))
            print("tiempo: " + str(done_stamp-time_stamp) + " s")
            print("Velocidad de transmision: " + str(rate) + " kbps")
            logging.info("Bytes totales: " + str(total_bytes))
            logging.info("Cantidad de tramas: " + str(total_received))
            logging.info("tiempo: " + str(done_stamp-time_stamp) + " s")
            logging.info("Velocidad de transmision: " + str(rate) + " kbps")
            if args.server_type:
                total_bytes = 0
                time_stamp = time.time()
                total_received = 0
                print("Reset, limpiando estadisticas")
                logging.info("Reset, limpiando estadisticas")
                resp = BaseResponse()
                resp.set_estado(0)
                resp.set_mensaje("velocidad calculada con exito")
                resp.set_velocidad( str(rate) + " kbps")
                UDPSock.sendto(json.dumps(resp.__dict__).encode(),(cliente_direccion, cliente_puerto))
                flag = True
                continue
            break

UDPSock.close()
