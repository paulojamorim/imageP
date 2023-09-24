#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Developed by Paulo Henrique Junqueira Amorim (paulojamorim at gmail.com)

import os
import glob
from skimage import io
from pathlib import Path

def check_create_folder(folder):
    if not(os.path.exists(folder)):
        os.makedirs(folder)

    return folder

def find_tiff(file_path):
    #file_path = sys.argv[1]
    types = [os.path.join(file_path,"*.tiff"), os.path.join(file_path, "*.tif")]

    files_grabbed = []
    for files in types:
        files_grabbed.extend(glob.glob(files))

    return files_grabbed

def save_tiff(img, folder, z=0):
    io.imsave(os.path.join(folder, str(z) + ".tif"), img)

def process(tiff_list):
    for file_path in tiff_list:
        file_path = Path(file_path).resolve()

        im = io.imread(file_path)
        size = im.shape

        tiff_name = file_path.name.split(".")[0]
        tiff_folder = file_path.parent.resolve()

        folder = check_create_folder(os.path.join(tiff_folder, tiff_name))

        folder_r = check_create_folder(os.path.join(folder, "channel_R"))
        folder_g = check_create_folder(os.path.join(folder, "channel_G"))
        folder_b = check_create_folder(os.path.join(folder, "channel_B"))
        folder_rgb = check_create_folder(os.path.join(folder, "channel_RGB"))

        folders = (folder_r, folder_g, folder_b, folder_rgb)

        if len(size) == 4:
            sz, sx, sy, sc = size
            
            for z in range(sz):
                img_r = im[z,:,:,0]
                img_g = im[z,:,:,1]
                img_b = im[z,:,:,2]
                img_rgb = im[z,:,:,:]

                images = (img_r, img_g, img_b, img_rgb)

                for folder, img in zip(folders, images):
                    save_tiff(img, folder, z=z)
        else:
            sx, sy, sc = size
            for channel in range(sc):
                img_r = im[:,:,0]
                img_g = im[:,:,1]
                img_b = im[:,:,2]
                img_rgb = im[:,:,:]

                images = (img_r, img_g, img_b, img_rgb)

                for folder, img in zip(folders, images):
                    save_tiff(img, folder)

        print(size, len(size), file_path)