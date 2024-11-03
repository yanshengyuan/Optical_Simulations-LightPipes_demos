'''
2024.5.15, Shengyuan Yan, TU/e, Eindhoven, NL.
'''

from LightPipes import *
import matplotlib.pyplot as plt
import numpy as np
from math import pi, sin
import matplotlib.gridspec as gridspec

#plt.rcParams['font.sans-serif']=['SimHei']

def Hflip(phase):
    return phase[:, ::-1]

def Vflip(phase):
    return phase[::-1]

def invert(phase):
    return -phase

def magnify(phase, m):
    return m*phase

def shift(phase, s):
    return phase-s

output_path='Simu_Output/'

#Grid size, wavelength
wavelength = 500*nm
size = 15*mm
N = 256
w0=3*mm
i=0

#propagate distance
#z=8*m

#order n and frequency m of the Gauss-Laguerre mode beam
n=0
m=3

#Gaussian Noise
np.random.seed(42)
phase_noise_std = 0.5
phase_noise = np.random.normal(scale=phase_noise_std, size=(N, N))

#Gaussian beam source
F_init=Begin(size,wavelength,N)
F_init=GaussBeam(F_init, w0, doughnut=True, n=n, m=m)
Phi_init=Phase(F_init)

step=1*cm
z=0
for runCnt in range(1000000):
    if(runCnt>400):
        step=20*cm
    
    Phi_V=Vflip(Phi_init)
    F_V=SubPhase(F_init, Phi_V)
    
    #F_V=MultPhase(F_V, phase_noise)
    #plt.imsave('Phi_V.png',Phase(F_V), cmap='rainbow')
    
    F_V=Fresnel(F_V, z, usepyFFTW=True)
    I_V=Intensity(F_V)
    Phi_V=Phase(F_V)
    #plt.imsave('I_V.png' ,I_V, cmap='jet')
    
    Phi_H=Hflip(Phi_init)
    F_H=SubPhase(F_init, Phi_H)
    
    #F_H=MultPhase(F_H, phase_noise)
    #plt.imsave('Phi_H.png' ,Phase(F_H), cmap='rainbow')
    
    F_H=Fresnel(F_H, z, usepyFFTW=True)
    I_H=Intensity(F_H)
    Phi_H=Phase(F_H)
    #plt.imsave('I_H.png' ,I_H, cmap='jet')
    
    v=Phi_V
    h=Phi_H
    
    for i in range(len(h)):
        for j in range(len(h[i])):
            h[i][j]=sin(h[i][j])
            v[i][j]=sin(v[i][j])
    residual=h-v
    
    '''
    cnt=0
    for i in range(len(residual)):
        for j in range(len(residual[i])):
            if(residual[i][j]>0.2):
                cnt+=1
    
    print(cnt)
    print(cnt/(512**2))
    '''
    
    #plt.imshow(residual, cmap='viridis')
    #plt.savefig('sin(PhiV)-sin(PhiH).png', dpi=300)
    
    fig = plt.figure(figsize=(10, 8))
    gs = gridspec.GridSpec(2, 3, figure=fig)
    
    ax1 = fig.add_subplot(gs[:, 0])
    ax1.set_title("sin(Phi_1)-sin(Phi_2)")
    img1=ax1.imshow(residual, cmap='viridis')
    fig.colorbar(img1, ax=ax1, orientation='vertical', fraction=0.046, pad=0.04)
    ax1.axis('off')
    
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_title("Phase_1")
    ax2.imshow(Phi_V, cmap='rainbow')
    ax2.axis('off')
    
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.set_title("Intensity_1")
    ax3.imshow(I_V, cmap='jet')
    ax3.axis('off')
    
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_title("Phase_2")
    ax4.imshow(Phi_H, cmap='rainbow')
    ax4.axis('off')
    
    ax5 = fig.add_subplot(gs[1, 2])
    ax5.set_title("Intensity_2")
    ax5.imshow(I_H, cmap='jet')
    ax5.axis('off')
    
    dist="%.2f" % z
    plt.suptitle('propogation distance: '+dist+' m')
    plt.tight_layout()
    
    plt.show()
    
    z+=step