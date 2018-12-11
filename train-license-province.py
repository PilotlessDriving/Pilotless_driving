import sys
import os
import time
import random

import numpy as np
import tensorflow as tf

from PIL import Image

SIZE = 1280
WIDTH = 32
HEIGHT = 40
NUM_CLASSES = 6
iteration = 300

SAVER_DIR = './train_saver/province/'

PROVINCES = ('京', '闽', '粤', '苏', '沪', '浙')
nProvinceIndex = 0

time_begin = time.time()

x = tf.placeholder(tf.float32, shape=[None, SIZE])
y = tf.placeholder(tf.float32, shape=[None, NUM_CLASSES])

x_image = tf.reshape(x, [-1, WIDTH, HEIGHT, 1])


def conv_layer(inputs, W, b, conv_strides, kernel_size, pool_strides, padding):
    L1_conv = tf.nn.conv2d(inputs, W, strides=conv_strides, padding=padding)
    L1_relu = tf.nn.relu(L1_conv + b)
    return tf.nn.max_pool
