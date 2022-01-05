#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 09:52:34 2022

@author: maxinegravier
"""
import numpy as np
import cv2
from markdown.extensions import meta

basedir_data = "./data/"
rel_path = basedir_data + "cifar-10-batches-py/"

#Désérialiser les fichiers image afin de permettre l’accès aux données et aux labels:

def unpickle(file):
    import pickle
    with open(file, 'rb') as fo:
        dict = pickle.load(fo,encoding='bytes')
    return dict

X = unpickle(rel_path + 'data_batch_1')
img_data = X[b'data']
img_label_orig = img_label = X[b'labels']
img_label = np.array(img_label).reshape(-1, 1)

test_X = unpickle(rel_path + 'test_batch');
test_data = test_X[b'data']
test_label = test_X[b'labels']
test_label = np.array(test_label).reshape(-1, 1)

sample_img_data = img_data[0:10, :]
one_img=sample_img_data[0,:]
r = one_img[:1024].reshape(32, 32)
g = one_img[1024:2048].reshape(32, 32)
b = one_img[2048:].reshape(32, 32)
rgb = np.dstack([r, g, b])
cv2.imshow('Image CIFAR',rgb)
cv2.waitKey(0)
cv2.destroyAllWindows()

from sklearn.neighbors import KNeighborsClassifier 

def pred_label_fn(i, original):
    return original + '::' + meta[YPred[i]].decode('utf-8')

nbrs = KNeighborsClassifier(n_neighbors=3, algorithm='brute').fit(img_data, img_label_orig)

# test sur les 10 premières images
data_point_no = 10
sample_test_data = test_data[:data_point_no, :]

YPred = nbrs.predict(sample_test_data)

for i in range(0, len(YPred)):
    show_img(sample_test_data, test_label, meta, i, label_fn=pred_label_fn)