import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf

new_signal = np.empty(0)

signal, samplerate = sf.read('violin_05.wav')
time = np.arange(0, len(signal) * 1/samplerate, 1/samplerate)

'''GERENADO UNA NUEVA SEÑAL A PARTIR DEL AUDIO'''
'''DEBIDO A QUE ESTA TIENE 2 VALORES (RIGHT AND LEFT)'''
'''LOS ARCHIVOS DE AUDIO TIENEN 2 VALORES PARA SER ESCUCHADOS'''
'''EN DISPOSITIVOS CON SALIDAS QUE LOS DIFERENCIAN (COMO AUDÓFONOS)'''

for i in range (len(signal)):
    new_signal = np.append(new_signal, signal[i][0])
else:
    pass

FWHM = 1  #Establecemos un FWHM teorico de 1 ms
k = 50  # Valor para establecer el tamaño de la ventana gaussiana 2*50 = 100
gt = 1000*np.arange(-k,k)/samplerate   # Tiempo normalizado de la funcion gausiana en ms

'''ECUACION DEL FILTRO GAUSSIANO'''

filtro_gaussiano = np.exp(-(4*np.log(2)*gt**2)/FWHM**2) #Creacion del filtro gaussiano
filtro_gaussiano_normalizado = filtro_gaussiano/np.sum(filtro_gaussiano)
ind_flanco_bajada = k +np.argmin((filtro_gaussiano[k:]-.5)**2)  # Indice de la mitad del flanco de bajada
ind_flanco_subida = np.argmin((filtro_gaussiano-.5)**2)    # Indice de la mitad del flanco de subida

FWHM_calculado = gt[ind_flanco_subida] - gt[ind_flanco_bajada]   # Duracion de FWHM en ms
FWHM_calculado = round(FWHM_calculado, 5)

'''GRAFICACIÓN '''

plt.subplots(1,2, figsize=(15,4))

plt.subplot(121)
plt.plot(gt,filtro_gaussiano, label="Filtro Gaussiano") #Grafica de la funcion gaussiana
plt.plot([gt[ind_flanco_subida], gt[ind_flanco_bajada]],
         [filtro_gaussiano[ind_flanco_subida], filtro_gaussiano[ind_flanco_bajada]],
         label= "FWHM")   #Grafico de la linea FWHM
plt.title(f"Filtro G. con FWHM teorico de {FWHM}-ms. logrado {FWHM_calculado}-ms")
plt.xlabel("Tiempo (ms)")
plt.ylabel("Ganancia")
plt.grid()
plt.legend()

plt.subplot(122)
plt.plot(gt,filtro_gaussiano_normalizado, label="Filtro Gaussiano Normalizado") #Grafica de la funcion gaussiana
plt.plot([gt[ind_flanco_subida], gt[ind_flanco_bajada]],
         [filtro_gaussiano_normalizado[ind_flanco_subida], filtro_gaussiano_normalizado[ind_flanco_bajada]],
         label= "FWHM")   #Grafico de la linea FWHM
plt.title(f"Filtro G. Normalizado con FWHM teorico de {FWHM}-ms. logrado {FWHM_calculado}-ms")
plt.xlabel("Tiempo (ms)")
plt.ylabel("Ganancia")
plt.grid()
plt.legend()

fltrd_gauss_sig = np.zeros_like(new_signal)

for i in range(k+1, len(signal)-k-1):
    fltrd_gauss_sig[i] = np.sum(new_signal[i-k:i+k]*filtro_gaussiano_normalizado)

plt.subplots(1,3, figsize = (20,4))

plt.subplot(131) 
plt.plot(time,new_signal,label="Señal ruidosa")
plt.plot(time,fltrd_gauss_sig,label="Señal filtrada")
plt.title(f"Señal original VS filtrada")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")
plt.grid()
plt.legend()

plt.subplot(132) 
plt.plot(time,fltrd_gauss_sig,"r",label="Señal filtrada")
plt.title(f"Filtro Gaussiano con FWHM={FWHM_calculado}-ms")
plt.xlabel("Tiempo (s)")
plt.grid()
plt.legend()

plt.subplot(133)
plt.plot(time,new_signal,label="Señal ruidosa")
plt.plot(time,fltrd_gauss_sig,"r",label="Señal filtrada")
plt.title(f"Efecto de borde con filtro Gaussiano")
plt.xlabel("Tiempo (s)")
plt.axis([1.500, 1.515, -0.0015, 0.001])
plt.grid()
plt.legend()

plt.show()

'''GENERACIÓN DE AUDIO'''
'''A PARTIR DE LA SEÑAL FILTRADA'''
def create_audio():

    sf.write('audio_fltrd_GAUSS.flac', fltrd_gauss_sig, samplerate)

create_audio()