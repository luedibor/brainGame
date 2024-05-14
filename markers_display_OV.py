import time
from pylsl import StreamInlet, resolve_bypred

def main():
    # Buscar el stream de marcadores de OpenViBE
    print("Buscando el stream de marcadores de OpenViBE...")
    streams = resolve_bypred('name', 'openvibeMarkers', timeout=1)

    while len(streams) == 0:
        print("Conexión con OpenViBE fallida. Intentando de nuevo...")
        time.sleep(2)
        streams = resolve_bypred('name', 'openvibeMarkers', timeout=1)

    print("Conexión con OpenViBE establecida :D")

    # Crear un inlet para el stream de marcadores
    inlet = StreamInlet(streams[0])

    try:
        while True:
            marker, timestamp = inlet.pull_sample()
            if marker:
                print("Marcador de OpenViBE:", marker[0])
            time.sleep(0.1)  # Puedes ajustar este valor para controlar la velocidad de visualización
    except KeyboardInterrupt:
        print("Saliendo...")

if __name__ == "__main__":
    main()
