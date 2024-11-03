'''
2024.5.5, Shengyuan Yan, TU/e, Eindhoven, NL.
'''

from LightPipes import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import time
#plt.rcParams['font.sans-serif']=['SimHei']

start_time = time.time()

output_path='Simu_Output/'

#Grid size, wavelength
wavelength=1000.0*nm
size=5*mm
N=512

#axicon lens params
phi=179.7/180*3.1415
n1=1.5

#propagate distance
z=10*cm

#Gaussian beam source
F_init=Begin(size,wavelength,N);
F_init=GaussBeam(F_init, size/3.5)
#plt.imsave(output_path+'init_phase.png' , Phase(F_init), cmap='gray')
#plt.imsave(output_path+'init_intensity.png' , Intensity(F_init), cmap='gray')
F_noiseFree=Axicon(phi,n1,0,0,F_init)
F_noiseFree=Fresnel(F_noiseFree, z, usepyFFTW=True)
#plt.imsave(output_path+'NoiseFree_farfield_intensity.png' , Intensity(F_noiseFree), cmap='jet')

#Gaussian Noise
np.random.seed(42)
phase_noise_std = 0.5

for runCnt in range(100000000):
    phase_noise = np.random.normal(scale=phase_noise_std, size=(N, N))
    #plt.imsave(output_path+'phase_noise' + str(runCnt) + '.png' ,phase_noise, cmap='gray')
    F=MultPhase(F_init, phase_noise)
    noisy_init_phase=Phase(F)
    #plt.imsave(output_path+'noisy_init_phase' + str(runCnt) + '.png' ,noisy_init_phase, cmap='gray')
    #np.save('Phi/'+'Phi-'+str(runCnt)+'.npy', noisy_init_phase)
    
    #Axicon lens
    #plt.imsave(output_path+'init_phase' + str(runCnt) + '.png' ,init_phase, cmap='gray')
    #plt.imsave(output_path+'init_intensity.png' ,init_intensity, cmap='jet')
    F=Axicon(phi,n1,0,0,F)
    #axicon_phase=Phase(F)
    #axicon_intensity=Intensity(F)
    #plt.imsave(output_path+'axicon_phase' + str(runCnt) + '.png' , axicon_phase, cmap='gray')
    #plt.imsave(output_path+'axicon_intensity' + str(runCnt) + '.png' , axicon_intensity, cmap='jet')
    
    #propagate with Fresnel-Kirchoff diffraction
    outputfield=Fresnel(F, z, usepyFFTW=True)
    #outputfield=Fresnel(F, z)
    #s='z= %3.1f m' % (z/m)
    #outputfield=Interpol(outputfield, size/4, 512)
    #plt.imsave(output_path+'farfield_phase' + str(runCnt) + '.png' ,Phase(outputfield), cmap='jet')
    I=Intensity(outputfield)
    Phi=Phase(outputfield)
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.title('Intensity')
    plt.imshow(I[128:384,128:384], cmap='jet')
    plt.axis('off')
    plt.subplot(1, 2, 2)
    plt.title('Phase')
    plt.imshow(Phi, cmap='gray')
    plt.axis('off')
    plt.show()
    #plt.imsave(output_path+'farfield_intensity' + str(runCnt) + '.png' , I, cmap='jet')
    #np.save('I/'+'I-'+str(runCnt)+'.npy', I)
    print(runCnt)

end_time = time.time()
execution_time = end_time - start_time
print(execution_time)