import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf

new_signal = np.empty(0)

signal, samplerate = sf.read('violin_05.wav')
time = np.arange(0, len(signal) * 1/samplerate, 1/samplerate)

'''GERENADO UNA NUEVA SEÑAL A PARTIR DEL AUDIO'''
'''DEBIDO A QUE ESTA TIENE 2 VALORES (RIGHT AND LEFT)'''
'''LOS ARCHIVOS DE AUDIO TIENEN 2 VALORES PARA SER ESCUCHADOS'''
'''EN DISPOSITIVOS CON SALIDAS QUE LOS DIFERENCIAS (COMO AUDÓFONOS)'''

for i in range (len(signal)):
    new_signal = np.append(new_signal, signal[i][0])
else:
    pass

'''ECUACIÓN DE FILTRO DE MEDIA MÓVIL'''

fltrd_signal = np.zeros(len(signal)) # Inicializamos el vector de salida, con el mismo tamaño que la señal creada
k = 50 #La ventana u orden del filtro es de 2*k+1=101

for i in range(k,len(signal)-k-1):
    fltrd_signal[i] = np.mean(new_signal[i-k:i+k])  #Cada salida del filtro es el promedio de la ventana
else:
    pass

tam_ventana = 1000*(k*2+1)/samplerate #Se calcula el tamaño de la ventana en milisegundos
tam_ventana = round(tam_ventana, 4)

plt.subplots(1,3, figsize = (50,4))

plt.subplot(131) 
plt.plot(time,new_signal,label="Señal ruidosa")
plt.plot(time,fltrd_signal,label="Señal filtrada")
plt.title(f"Señal original VS filtrada")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")
plt.ylabel("Amplitud")
plt.grid()
plt.legend()

plt.subplot(132) 
plt.plot(time,fltrd_signal,"r",label="Señal filtrada")
plt.title(f"Señal Filtrada")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")
plt.grid()
plt.legend()

plt.subplot(133)
plt.plot(time,new_signal,"b",label="Señal ruidosa")
plt.plot(time,fltrd_signal,"r",label="Señal filtrada")
plt.title(f"Efecto de borde con el filtro media movil")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")
plt.axis([1.500, 1.515, -0.0015, 0.001])
plt.grid()
plt.legend()

plt.show()


'''GENERACIÓN DE AUDIO'''
'''A PARTIR DE LA SEÑAL FILTRADA'''
def create_audio():

    sf.write('audio_fltrd_MM.flac', fltrd_signal, samplerate)

create_audio()
