from pylsl import StreamInlet, resolve_bypred
import tkinter as tk
import time

class Chatbot:
    def __init__(self, ventana):
        # Configuración inicial de la ventana principal 
        self.ventana = ventana
        self.ventana.title("NeuroAssist Virtual Companion")
        self.ventana.geometry("700x650")
        self.ventana.configure(bg="lightblue")
        self.create_interface()
        self.stage = "main"
        self.main()

    def create_interface(self):
        # Título de la ventana principal
        titulo = tk.Label(self.ventana, text="¡Bienvenido a NeuroAssist!", bg="lightblue", font=("Helvetica", 22))
        titulo.pack()

        # Subtítulo de la ventana principal
        subtitulo = tk.Label(self.ventana, text="Tu asistente virtual personal", bg="lightblue", font=("Helvetica", 16))
        subtitulo.pack()

        # Crear un scrollbar para la ventana de texto
        scrollbar = tk.Scrollbar(self.ventana, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Área de texto para la conversación
        self.texto = tk.Text(self.ventana, height=25, width=60, yscrollcommand=scrollbar.set)
        self.texto.pack()

        # Configurar el scrollbar para desplazar el área de texto
        scrollbar.config(command=self.texto.yview)

    def main(self):
        #Mensaje inicial del chatbot
        mensaje = "Bot:   ¡Hola! Soy NeuroAssist Virtual Companion, ¿Necesitas ayuda? \nBot:   Responde 'Sí' o 'No', solo pensando.\n"
        self.texto.insert(tk.END, mensaje)

    def responder_mensaje(self, mensaje_usuario_confirmation, mensaje_usuario_menus):
        mensaje_bot = "Bot:   "

        if self.stage == "main":
            if mensaje_usuario_confirmation == "si":
                mensaje_bot += "¿Con qué te puedo ayudar? \n1. Alimentación \n2. Salud \n3. Entretenimiento"
                mensaje_bot += "\nBot:   Responde 'uno', 'dos' o 'tres', solo pensando.\n"
                self.texto.insert(tk.END, "\nUser:   Sí.\n", ('usuario',))
                self.texto.insert(tk.END, "\n" + mensaje_bot, ('bot',))
                self.stage = "menu"
            elif mensaje_usuario_confirmation == "no":
                mensaje_bot += "Regresar al menú principal. \n \nBot:   ¿Necesitas ayuda? \nBot:   Responde 'Sí' o 'No', solo pensando.\n"
                self.texto.insert(tk.END, "\nUser:   No.\n", ('usuario',))
                self.texto.insert(tk.END, "\n" + mensaje_bot, ('bot',))
        elif self.stage == "menu":
            if mensaje_usuario_menus == "1":
                mensaje_bot += "¿Qué necesitas?\n1. Quiero comer.\n2. Terminé de comer.\n3. Quiero más comida"
                mensaje_bot += "\nBot:   Responde 'uno', 'dos' o 'tres', solo pensando.\n"
                self.texto.insert(tk.END, "\nUser:   1.\n", ('usuario',))
                self.texto.insert(tk.END, "\n" + mensaje_bot, ('bot',))
                self.stage = "submenu_eating"
            elif mensaje_usuario_menus == "2":
                mensaje_bot += "¿Qué necesitas?\n1. Me siento mal.\n2. Quiero ir al médico.\n3. Necesito tomar mi medicamento"
                mensaje_bot += "\nBot:   Responde 'uno', 'dos' o 'tres', solo pensando.\n"
                self.texto.insert(tk.END, "\nUser:   2.\n", ('usuario',))
                self.texto.insert(tk.END, "\n" + mensaje_bot, ('bot',))
                self.stage = "submenu_health"
            elif mensaje_usuario_menus == "3":
                mensaje_bot += "¿Qué necesitas?\n1. Quiero ver la tele.\n2. Quiero escuchar música.\n3. Quiero salir de paseo"
                mensaje_bot += "\nBot:   Responde 'uno', 'dos' o 'tres', solo pensando.\n"
                self.texto.insert(tk.END, "\nUser:   3.\n", ('usuario',))
                self.texto.insert(tk.END, "\n" + mensaje_bot, ('bot',))
                self.stage = "submenu_entertainment"
        elif self.stage == "submenu_eating":
            if mensaje_usuario_menus == "1":
                mensaje_bot += "Para confirmar, ¿tienes hambre? \nBot:   Responde 'Sí' o 'No', solo pensando.\n"
                self.texto.insert(tk.END, "\nUser:   1.\n", ('usuario',))
                self.texto.insert(tk.END, "\n" + mensaje_bot, ('bot',))
                self.stage = "confirm"
            elif mensaje_usuario_menus == "2":
                mensaje_bot += "Para confirmar, ¿terminaste de comer? \nBot:   Responde 'Sí' o 'No', solo pensando.\n"
                self.texto.insert(tk.END, "\nUser:   2.\n", ('usuario',))
                self.texto.insert(tk.END, "\n" + mensaje_bot, ('bot',))
                self.stage = "confirm"
            elif mensaje_usuario_menus == "3":
                mensaje_bot += "Para confirmar, ¿necesitas más comida? \nBot:   Responde 'Sí' o 'No', solo pensando.\n"
                self.texto.insert(tk.END, "\nUser:   3.\n", ('usuario',))
                self.texto.insert(tk.END, "\n" + mensaje_bot, ('bot',))
                self.stage = "confirm"
        elif self.stage == "submenu_health":
            if mensaje_usuario_menus == "1":
                mensaje_bot += "Para confirmar, ¿tienes algún malestar? \nBot:   Responde 'Sí' o 'No', solo pensando.\n"
                self.texto.insert(tk.END, "\nUser:   1.\n", ('usuario',))
                self.texto.insert(tk.END, "\n" + mensaje_bot, ('bot',))
                self.stage = "confirm"
            elif mensaje_usuario_menus == "2":
                mensaje_bot += "Para confirmar, ¿necesitas ir al médico? \nBot:   Responde 'Sí' o 'No', solo pensando.\n"
                self.texto.insert(tk.END, "\nUser:   2.\n", ('usuario',))
                self.texto.insert(tk.END, "\n" + mensaje_bot, ('bot',))
                self.stage = "confirm"
            elif mensaje_usuario_menus == "3":
                mensaje_bot += "Para confirmar, ¿quieres tomar tu medicamento? \nBot:   Responde 'Sí' o 'No', solo pensando.\n"
                self.texto.insert(tk.END, "\nUser:   3.\n", ('usuario',))
                self.texto.insert(tk.END, "\n" + mensaje_bot, ('bot',))
                self.stage = "confirm"
        elif self.stage == "submenu_entertainment":
            if mensaje_usuario_menus == "1":
                mensaje_bot += "Para confirmar, ¿quieres ver la T.V.? \nBot:   Responde 'Sí' o 'No', solo pensando.\n"
                self.texto.insert(tk.END, "\nUser:   1.\n", ('usuario',))
                self.texto.insert(tk.END, "\n" + mensaje_bot, ('bot',))
                self.stage = "confirm"
            elif mensaje_usuario_menus == "2":
                mensaje_bot += "Para confirmar, ¿quieres escuchar música? \nBot:   Responde 'Sí' o 'No', solo pensando.\n"
                self.texto.insert(tk.END, "\nUser:   2.\n", ('usuario',))
                self.texto.insert(tk.END, "\n" + mensaje_bot, ('bot',))
                self.stage = "confirm"
            elif mensaje_usuario_menus == "3":
                mensaje_bot += "Para confirmar, ¿quieres salir de paseo? \nBot:   Responde 'Sí' o 'No', solo pensando.\n"
                self.texto.insert(tk.END, "\nUser:   3.\n", ('usuario',))
                self.texto.insert(tk.END, "\n" + mensaje_bot, ('bot',))
                self.stage = "confirm"
        elif self.stage == "confirm":
            if mensaje_usuario_confirmation == "si":
                mensaje_bot += "Entendido, en un momento le aviso a su cuidador. \nBot:   ¿Necesitas ayuda en algo más? \nBot:   Responde 'Sí' o 'No', solo pensando.\n"
                self.texto.insert(tk.END, "\nUser:   Sí.\n", ('usuario',))
                self.texto.insert(tk.END, "\n" + mensaje_bot, ('bot',))
                self.stage = "main"
            elif mensaje_usuario_confirmation == "no":
                mensaje_bot += "Regresar al menú principal. \n \nBot:   ¿Necesitas ayuda? \nBot:   Responde 'Sí' o 'No', solo pensando.\n"
                self.texto.insert(tk.END, "\nUser:   No.\n", ('usuario',))
                self.texto.insert(tk.END, "\n" + mensaje_bot, ('bot',))
                self.stage = "main"

    def enviar_mensaje(self, stimulus):
        if stimulus == 33057 or stimulus == 33058:
            mensaje_usuario_confirmation = 'si' if stimulus == 33057 else 'no'
            self.responder_mensaje(mensaje_usuario_confirmation, None)
            self.texto.yview_moveto(1.0)  # Desplazar el texto hacia abajo automáticamente
        elif stimulus == 33060 or stimulus == 33061 or stimulus == 33062:
            mensaje_usuario_menus = str(stimulus - 33059)
            self.responder_mensaje(None, mensaje_usuario_menus)
            self.texto.yview_moveto(1.0)  # Desplazar el texto hacia abajo automáticamente

def main():
    try:
        # Buscar el stream de marcadores de OpenViBE
        print("Looking for OpenVibe Marker Stream ...")
        streams = resolve_bypred('name', 'openvibeMarkers', timeout=1)

        if not streams:
            raise Exception("OpenVibe Connection failed.")

        print("OpenVibe Connection Established :D")

        # Crear un inlet para el stream de marcadores
        inlet = StreamInlet(streams[0])

        ventana = tk.Tk()
        chatbot = Chatbot(ventana)

        text_font = ("Helvetica", 14)
        chatbot.texto.config(font=text_font)

        def procesar_marcador():
            marker, timestamp = inlet.pull_sample()
            if marker:
                print("Marcador de OpenViBE:", marker[0])
                chatbot.enviar_mensaje(marker[0])
            ventana.after(5000, procesar_marcador)

        # Iniciar el procesamiento de marcadores después de 5 segundos
        ventana.after(1000, procesar_marcador)

        ventana.mainloop()

    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    main()