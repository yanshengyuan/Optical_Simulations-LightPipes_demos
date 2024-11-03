'''
2024.5.6, Shengyuan Yan, TU/e, Eindhoven, NL.
'''

from LightPipes import *
import matplotlib.pyplot as plt
import numpy as np
import time
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
z=0*cm

#order n and frequency m of the Gauss-Laguerre mode beam
n=0
m=3

#Gaussian Noise
np.random.seed(42)
phase_noise_std = 0.5

#Gaussian beam source
F_init=Begin(size,wavelength,N)
F_init=GaussBeam(F_init, w0, doughnut=True, n=n, m=m)
#I_init=Intensity(F_init)
#Phi_init=Phase(F_init)
#plt.imsave(output_path+'init_phase.png' , Phi_init, cmap='rainbow')
#plt.imsave(output_path+'init_intensity.png' , I_init, cmap='jet')
#F_noiseFree=Fresnel(F_init, z, usepyFFTW=True)
#plt.imsave(output_path+'NoiseFree_farfield_intensity.png' , Intensity(F_noiseFree), cmap='jet')
step=1*cm
z=0
for runCnt in range(1000000):
    if(runCnt>400):
        step=20*cm
    phase_noise = np.random.normal(scale=phase_noise_std, size=(N, N))
    #plt.imsave(output_path+'phase_noise' + str(runCnt) + '.png' ,phase_noise, cmap='gray')
    #F=MultPhase(F_init, phase_noise)
    #noisy_init_phase=Phase(F)
    #pseudo_noisy_I=Intensity(F)
    #plt.imsave(output_path+'noisy_init_phase' +str(runCnt)+ '.png' ,noisy_init_phase, cmap='rainbow')
    #plt.imsave(output_path+'pseudo_noisy_init_intensity' +str(runCnt)+ '.png' ,pseudo_noisy_I, cmap='jet')
    #np.save('Phi/'+'Phi-'+str(runCnt)+'.npy', noisy_init_phase)
    F=Fresnel(F_init, z, usepyFFTW=True)
    print(z)
    I=Intensity(F)
    Phi=Phase(F)
    
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.title('Intensity')
    plt.imshow(I, cmap='jet')
    plt.axis('off')
    plt.subplot(1, 2, 2)
    plt.title('Phase')
    plt.imshow(Phi, cmap='rainbow')
    plt.axis('off')
    dist="%.2f" % z
    plt.suptitle('propogation distance: '+dist+' m')
    
    plt.show()
    z=z+step
    #np.save('I/'+'I-'+str(runCnt)+'.npy', I)
    print(runCnt)
    
end_time = time.time()
execution_time = end_time - start_time
print(execution_time)