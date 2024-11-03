'''
2024.6.6, Shengyuan Yan, TU/e, Eindhoven, NL.
'''

import matplotlib.pyplot as plt
import numpy as np
from LightPipes import *
import time

#plt.rcParams['font.sans-serif']=['SimHei']
print(LPversion)
#Parameters used for the experiment:
size=5*mm; #The CCD-sensor has an area of size x size (NB LightPipes needs square grids!)
wavelength=1000.0*nm; #wavelength of the HeNe laser used
z=0.6*m; #propagation distance from near to far field
N_iterations=300 #number of iterations

#Read near and far field (at a distance of z=2 m) from disk:
data = np.load('gt-I/I.npy')
Inear = np.asfarray(data)

data = np.load('gt-I/I-5826.npy')
Ifar = np.asfarray(data)

N=len(Inear)
#N_new=256;size_new=40*mm;

#plt.subplot(3,3,1);plt.imshow(Inear,cmap='gray');
#plt.title('Measured Intensity near field'); plt.axis ('off');

#Define a field with uniform amplitude- (=1) and phase (=0) distribution
#(= plane wave)
F=Begin(size,wavelength,N);

gt_phase = np.load('gt/Phi-5826.npy')
F_gt = SubPhase(gt_phase, F)
F_gt = SubIntensity(Inear, F_gt)
phasegt = Phase(F_gt)
F_gt = Forvard(z, F_gt)
Igt = Intensity(F_gt)
'''
plt.subplot(2,2,1);plt.imshow(phasegt,cmap='gray');
plt.title('gt phase nearfield');plt.axis ('off');
plt.subplot(2,2,2);plt.imshow(Igt,cmap='gray');
plt.title('gt intensity farfield');plt.axis ('off');
'''

#The iteration:
for k in range(1,1000):
    #'''
    plt.subplot(2,2,1);plt.imshow(phasegt,cmap='gray');
    plt.title('gt phase nearfield');plt.axis ('off');
    plt.subplot(2,2,2);plt.imshow(Igt,cmap='jet');
    plt.title('gt intensity farfield');plt.axis ('off');
    I_pred = Intensity(F)
    plt.subplot(2,2,4);plt.imshow(I_pred,cmap='jet');
    plt.title('recovered intensity farfield'); plt.axis ('off')
    #'''
    print(k)
    F=SubIntensity(Ifar,F) #Substitute the measured far field into the field
    #F=Interpol(size_new,N_new,0,0,0,1,F);#interpolate to a new grid
    F=Forvard(F, -z, usepyFFTW=True) #Propagate back to the near field
    #F=Interpol(size,N,0,0,0,1,F) #interpolate to the original grid
    F=SubIntensity(Inear,F) #Substitute the measured near field into the field
    #'''
    Phi_pred = Phase(F)
    plt.subplot(2,2,3);plt.imshow(Phi_pred,cmap='gray');
    plt.title('estimated phase nearfield');plt.axis ('off')
    F=Forvard(F, z, usepyFFTW=True) #Propagate to the far field
    plt.suptitle('Non-convex optimization iteration: '+ str(k))
    plt.tight_layout()
    plt.show()
    #time.sleep(1)
    #'''

#The recovered far- and near field and their phase- and intensity
#distributions (phases are unwrapped (i.e. remove multiples of PI)):
Ffar_rec=F;
Ifar_rec=Intensity(0,Ffar_rec); Phase_far_rec=Phase(Ffar_rec);

#Phase_far_rec=PhaseUnwrap(Phase_far_rec)
Fnear_rec=Forvard(-z,F);
Inear_rec=Intensity(0,Fnear_rec); Phase_near_rec=Phase(Fnear_rec);

#Phase_near_rec=PhaseUnwrap(Phase_near_rec)
#Plot the recovered intensity- and phase distributions:
#plt.subplot(3,3,3);plt.imshow(Inear_rec,cmap='gray');
#plt.title('Recovered Intensity near field'); plt.axis ('off')
'''
plt.subplot(2,2,4);plt.imshow(Ifar_rec,cmap='gray');
plt.title('recovered intensity farfield'); plt.axis ('off')
plt.subplot(2,2,3);plt.imshow(Phase_near_rec,cmap='gray');
plt.title('pred phase nearfield');plt.axis ('off')
'''
#plt.subplot(3,3,6);plt.imshow(Phase_far_rec,cmap='gray');
#plt.title('Recovered phase far field'); plt.axis ('off')