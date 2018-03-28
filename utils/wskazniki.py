import numpy as np
import math

def psnr(imageA, imageB):
    imageA = np.array(imageA.convert("RGB")).astype("double")
    imageB = np.array(imageB.convert("RGB")).astype("double")
    mse = np.mean( np.sum( (imageA - imageB) ** 2, axis=2)  /3)
    if mse == 0:
        return 100

    return 10.0*math.log10(float(255*255)/float(mse))

def mae(imageA, imageB):
    imageA = np.array(imageA.convert("RGB")).astype("double")
    imageB = np.array(imageB.convert("RGB")).astype("double")
    mae = np.mean(np.absolute(imageB - imageA))
    return mae

def mse(imageA, imageB):
    imageA = np.array(imageA.convert("RGB")).astype("double")
    imageB = np.array(imageB.convert("RGB")).astype("double")
    mse = np.mean( np.sum( (imageA - imageB) ** 2, axis=2)  /3)
    return mse
