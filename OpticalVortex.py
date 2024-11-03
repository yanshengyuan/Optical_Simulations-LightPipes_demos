'''
2024.5.6, Shengyuan Yan, TU/e, Eindhoven, NL.
'''

import os
from LightPipes import *
import matplotlib.pyplot as plt
import numpy as np
import time
from filelock import FileLock
#plt.rcParams['font.sans-serif']=['SimHei']

start_time = time.time()

output_path='Simu_Output/'

#Grid size, wavelength
wavelength = 500*nm
size = 15*mm
N = 512
w0=3*mm
i=0

#propagate distance
z=8*m

#order n and frequency m of the Gauss-Laguerre mode beam
n=0
m=3

#Gaussian Noise
np.random.seed(42)
phase_noise_std = 0.0

#Gaussian beam source
F_init=Begin(size,wavelength,N)
F_init=GaussBeam(F_init, w0, doughnut=True, n=n, m=m)

for runCnt in range(100000000):
    phase_noise = np.random.normal(scale=phase_noise_std, size=(N, N))
    F=MultPhase(F_init, phase_noise)
    noisy_init_phase=Phase(F)
    #plt.imsave(output_path+'noisy_init_phase' +str(runCnt)+ '.png' ,noisy_init_phase, cmap='rainbow')
    
    F=Fresnel(F, z, usepyFFTW=True)
    I=Intensity(F)
    Phi=Phase(F)
    plt.figure(figsize=(15, 5))
    plt.subplot(1, 3, 1)
    plt.title('Intensity')
    plt.imshow(I, cmap='jet')
    plt.axis('off')
    plt.subplot(1, 3, 2)
    plt.title('Noisy initial phase')
    plt.imshow(noisy_init_phase, cmap='rainbow')
    plt.axis('off')
    plt.subplot(1, 3, 3)
    plt.title('Noisy phase')
    plt.imshow(Phi, cmap='rainbow')
    plt.axis('off')
    plt.suptitle('Gaussian phase noise std: '+str(phase_noise_std))
    plt.tight_layout()
    plt.show()
    phase_noise_std+=0.01
    
end_time = time.time()
execution_time = end_time - start_time
print(execution_time)