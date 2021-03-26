#!/usr/bin/env python

import argparse
import numpy as np
import nibabel as nib
import nilearn.plotting as nilp
import matplotlib.cm as cm

parser = argparse.ArgumentParser(description='Compute the RMSE and MAE of '
                                 'the two images passed as argument. Save '
                                 'relative differences (im1-im2)/im1.')
parser.add_argument("image1", action="store", help="Path to the first image")
parser.add_argument("image2", action="store", help="Path to the second image")
parser.add_argument("reldiff", action="store", help="Name for the relative "
                    "difference image. Extensionless, used as base name to "
                    "save .nii.gz image and .png snapshot")

args = parser.parse_args()

im1 = nib.load(args.image1)
print(f'im1 size: {im1.shape}')
data1 = im1.get_fdata()

im2 = nib.load(args.image2)
print(f'im2 size: {im2.shape}')
data2 = im2.get_fdata()

rmse = np.sqrt(np.mean((data1-data2)**2, dtype=np.float64), dtype=np.float64)
mae = np.mean(np.abs(data1-data2, dtype=np.float64), dtype=np.float64)

print(f'RMSE: {rmse}')
print(f'MAE: {mae}')

rel_diff = nib.Nifti1Image((data1-data2)/(data1), im1.affine)
diff_name = args.reldiff
nib.save(rel_diff, diff_name+'.nii.gz')
print(f'Relative differences saved in {diff_name}.nii.gz')

plt = nilp.plot_img(rel_diff, cmap=cm.seismic, vmin=-1, vmax=1, colorbar=True)
plt.savefig(diff_name+'.png')
print(f'PNG snapshot saved in {diff_name}.png')
