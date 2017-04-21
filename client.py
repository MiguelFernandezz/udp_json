import argparse
import ipaddress
from socket import *
import time
import logging
import json
from objetos import BaseResponse


LOG_FILENAME = 'cliente_udp.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)



# se crea un parser para recibir argumentos en consola
parser = argparse.ArgumentParser()

# se crea el argumento addres de tipo ipv4
parser.add_argument("address", help="Direccion ipv4 del servidor al cual se quiere conectar",
                    type=ipaddress.ip_address, default="127.0.0.1")

# se crea el argumento port de tipo int
parser.add_argument("port", help="Puerto udp a conectar", type=int, default=3334)

# se crea el argumento frame de tipo int
parser.add_argument("frame", help="La longitud de la trama en bytes a enviar", type=int, default=1)

# se crea el argumento times de tipo int
parser.add_argument("times", help="Cantidad de veces a enviar la trama", type=int, default=1)

# se lee todos los argumentos de la consola
args = parser.parse_args()

logging.info('conectando...');
# se inicializa el socket UDP
UDPSock = socket(AF_INET, SOCK_DGRAM)
logging.info('conectado');


data = "X" * args.frame
times = args.times
address = str(args.address)
port = args.port

#Prueba de JSON
resp = BaseResponse();
resp.set_estado(0)
resp.set_mensaje(data)



#data_string = json.dumps(resp.__dict__)
#data_string = json.dumps({'4': 5, '6': 7}, sort_keys=True, indent=4)
data_string = data

if not data:
    pass
else:
    try:
        for x in range(times):
            logging.info('enviando trama');
            #UDPSock.sendto(data.encode(), (address, port))
            UDPSock.sendto(data_string.encode(), (address, port))
        # el reseteador
        UDPSock.sendto("x".encode(), (address, port))
        print("done")
        #Respuesta del servidor
        MAXLEN = 2048
        (datos,direccionServidor) = UDPSock.recvfrom(MAXLEN)
        print ('respuesta del servidor: '+ str(datos))
    except Exception as e:
        logging.exception(e)
        print(e)

UDPSock.close()
