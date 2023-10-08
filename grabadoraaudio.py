import tkinter as tk
import pyaudio
import wave
import threading

# Configura la frecuencia de muestreo y otros parámetros de audio
fs = 44100  # Frecuencia de muestreo
channels = 2  # Número de canales (estéreo)
sample_format = pyaudio.paInt16
chunk = 1024

# Inicializa PyAudio
audio = pyaudio.PyAudio()

# Variables para rastrear el estado de grabación
grabando = False
detener_grabacion_event = threading.Event()

# Contador para el nombre de archivo
contador = 0

def grabar_audio():
    global grabando, contador
    grabando = True
    stream = audio.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True)

    frames = []
    while grabando and not detener_grabacion_event.is_set():
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()

    if not detener_grabacion_event.is_set():
        # Genera un nombre de archivo único
        nombre_archivo = f'grabacion{contador}.wav'
        contador += 1

        # Guarda la grabación en un archivo .wav
        wf = wave.open(nombre_archivo, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()

def iniciar_grabacion():
    global grabando
    if not grabando:
        detener_grabacion_event.clear()
        threading.Thread(target=grabar_audio).start()

def detener_grabacion():
    global grabando
    if grabando:
        detener_grabacion_event.set()
        grabando = False

# Crea la ventana de la GUI
ventana = tk.Tk()
ventana.geometry('300x200')  # Establece el tamaño de la ventana

# Crea un botón para grabar audio
boton_grabar = tk.Button(ventana, text="Grabar", command=iniciar_grabacion)
boton_grabar.pack()

# Crea un botón para detener la grabación
boton_detener = tk.Button(ventana, text="Detener", command=detener_grabacion)
boton_detener.pack()

# Inicia el bucle principal de la GUI
ventana.mainloop()
