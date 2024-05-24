class MyOVBox(OVBox):
   def __init__(self):
      OVBox.__init__(self)

   def initialize(self):
      # nop
      return

   def process(self):
      for chunkIndex in range( len(self.input[0]) ):
         chunk = self.input[0].pop()
         if(type(chunk) == OVStimulationSet):
            # We move through all the stimulation received in the StimulationSet and
            # we print their date and identifier
            for stimIdx in range(len(chunk)):
               stim=chunk.pop()
               print('At time ', stim.date, ' received stim ', stim.identifier)
         else:
            print('Received chunk of type ', type(chunk), " looking for StimulationSet")

      return

   def uninitialize(self):
      # nop
      return

box = MyOVBox()

# import time
# from pylsl import StreamInlet, resolve_bypred

# def main():
#     # Buscar el stream de marcadores de OpenViBE
#     print("Buscando el stream de marcadores de OpenViBE...")
#     streams = resolve_bypred('name', 'openvibeMarkers', timeout=1)

#     while len(streams) == 0:
#         print("Conexión con OpenViBE fallida. Intentando de nuevo...")
#         time.sleep(2)
#         streams = resolve_bypred('name', 'openvibeMarkers', timeout=1)

#     print("Conexión con OpenViBE establecida :D")

#     # Crear un inlet para el stream de marcadores
#     inlet = StreamInlet(streams[0])

#     try:
#         while True:
#             start = time.time()
#             marker, timestamp = inlet.pull_sample()
#             print(timestamp, time.time() - start)
#             # if marker:
#             #     print("Marcador de OpenViBE:", marker[0])
#             # time.sleep(0.1)  # Puedes ajustar este valor para controlar la velocidad de visualización
#     except KeyboardInterrupt:
#         print("Saliendo...")

# if __name__ == "__main__":
#     main()
