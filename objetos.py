class BaseResponse(object):
    estado = 0
    mensaje = ''
    velodidad = ''
    def __init__(self):
        self.estado = ''
        self.mensaje = 0
        self.velocidad = '0'

    def set_estado(self,estado):
        self.estado = estado

    def set_mensaje(self,mensaje):
        self.mensaje = mensaje

    def set_velocidad(self,velocidad):
        self.velocidad = velocidad
