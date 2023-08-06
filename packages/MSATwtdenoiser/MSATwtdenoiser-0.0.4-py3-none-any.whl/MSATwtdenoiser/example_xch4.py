import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from MSATwtdenoiser import MSATdenoise
import scipy.io
import matplotlib.cm as cm


mat = scipy.io.loadmat('/Users/asouri/Documents/Methane_SAT_OSSEs/Main/co2_proxy_whitenoise.mat')
XCH4 = mat['xCH4']
XCH4=np.array(XCH4)

XCH4=XCH4*1e9 

XCH4.astype(float)
#img = np.array(mpimg.imread('steve.jpg'))
#img.astype(float)
#img = np.mean(img,axis=2)
#img = img+np.random.normal(0,100,[np.shape(img)[0],np.shape(img)[1]])

# denoiser

denoiser = MSATdenoise(XCH4,'db3',7)
denoised_img = denoiser.denoised
print(np.shape(denoised_img))


#plotting
fig = plt.figure(figsize=(12, 3))
ax = fig.add_subplot(1, 2, 1)
ax.imshow(XCH4, interpolation="nearest", cmap=cm.RdYlGn,vmin=1794, vmax=1800)
ax = fig.add_subplot(1, 2, 2)
ax.imshow(denoised_img, interpolation="nearest", cmap=cm.RdYlGn,vmin=1794, vmax=1800)
fig.tight_layout()
plt.show()
