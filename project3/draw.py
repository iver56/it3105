#!/usr/bin/env python
# coding=utf-8
from __future__ import division, print_function, unicode_literals
import os
import h5py
import argparse
import brainstorm as bs
from brainstorm.data_iterators import Minibatches
from brainstorm.handlers import PyCudaHandler
import re


class Main(object):
    def __init__(self):

        self.args = None
        self.network_filename = None

        self.parse_args()
        self.output_filename = self.network_filename.replace('.hdf5', '.png')
        self.draw()

    def parse_args(self):
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument(
            '-i',
            '--filename',
            dest='network_filename',
            type=str,
            required=True,
            help='Name of the input hdf5 file with the neural network'
        )

        self.args = arg_parser.parse_args()
        self.network_filename = self.args.network_filename

    def draw(self):
        network = bs.Network.from_hdf5(self.network_filename)
        bs.tools.draw_network(network, file_name=self.output_filename)

if __name__ == '__main__':
    Main()
