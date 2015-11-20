#!/usr/bin/env python
# coding=utf-8
from __future__ import division, print_function, unicode_literals
import argparse
import brainstorm as bs
import numpy as np
import os
import h5py
import sys
from os import path
from prepare_data import PrepareData
from collections import Counter
import random
import ai2048demo


sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from module4.board import Board


class Play(object):
    def __init__(self, init=True):
        self.args = None
        self.network_filename = None
        self.network = None
        self.max_tile_value = None

        if init:
            self.parse_args()
            self.initialize_network()
            self.run()

    def parse_args(self):
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument(
            '-n',
            '--network',
            dest='network_filename',
            type=str,
            required=True,
            help='Name of the input hdf5 file with the neural network'
        )

        arg_parser.add_argument(
            '-st',
            '--stats',
            dest='stats',
            nargs='?',
            const=True,
            required=False,
            help='Show accuracy stats',
            default=False
        )
        arg_parser.add_argument(
            '-r',
            '--print-results',
            dest='print_results',
            nargs='?',
            const=True,
            required=False,
            help='Show every board state',
            default=False
        )
        arg_parser.add_argument(
            '--disable-cuda',
            dest='disable_cuda',
            nargs='?',
            const=True,
            required=False,
            help='Add this flag to use the CPU instead of the GPU',
            default=False
        )

        self.args = arg_parser.parse_args()
        self.network_filename = self.args.network_filename

    def initialize_network(self):
        self.network = bs.Network.from_hdf5(self.network_filename)
        if not self.args.disable_cuda:
            from brainstorm.handlers import PyCudaHandler
            self.network.set_handler(PyCudaHandler())

    def choose_direction(self, board_values_2d):
        data = np.zeros(shape=(1, 1, 20, 1))
        processed_input = PrepareData.pre_process(board_values_2d)
        adapted_input_array = np.array(processed_input)
        adapted_input_array.shape = (20, 1)
        data[0][0] = adapted_input_array
        self.network.provide_external_data({
            'default': data,
            'targets': np.zeros(shape=(1, 1, 1))
        })
        self.network.forward_pass()
        outputs = self.network.get('FC.outputs.default')
        prioritized_directions = outputs[0][0].argsort()[-4:][::-1]
        return prioritized_directions

    def run(self):
        board = Board(size=4)
        board.place_new_value_randomly()

        for i in xrange(2000):
            if self.args.print_results:
                print('iteration', i)
                print(board)
            directions = self.choose_direction(board.board_values)
            has_moved = False
            for direction in directions:
                if board.can_move(direction):
                    board.move(direction)
                    has_moved = True
                    break
            if not has_moved:
                break
            board.place_new_value_randomly()

        num_empty_tiles, max_tile_value, tile_sum = board.get_tile_stats()
        print(max_tile_value)
        self.max_tile_value = max_tile_value


class PlayRandomly(object):
    def __init__(self):
        self.max_tile_value = None
        self.play_game_randomly()

    def play_game_randomly(self, max_num_moves=2000):
        board = Board(size=4)
        board.place_new_value_randomly()
        for x in xrange(max_num_moves):
            directions = range(4)
            random.shuffle(directions)
            moved = False
            for direction in directions:
                if board.can_move(direction):
                    board.move(direction)
                    moved = True
                    break

            if not moved:
                break

            board.place_new_value_randomly()

        num_empty_tiles, max_tile_value, tile_sum = board.get_tile_stats()
        print(max_tile_value)
        self.max_tile_value = max_tile_value


if __name__ == '__main__':
    random_max_tile_values = []
    print('Random player is playing...')
    for i in xrange(50):
        random_play = PlayRandomly()
        random_max_tile_values.append(random_play.max_tile_value)

    ai_max_tile_values = []
    print('AI is playing...')
    for i in xrange(50):
        ai_play = Play()
        ai_max_tile_values.append(ai_play.max_tile_value)

    random_max_tile_value_counts = Counter(random_max_tile_values)
    print('random player stats:', random_max_tile_value_counts)

    ai_max_tile_value_counts = Counter(ai_max_tile_values)
    print('AI player stats:', ai_max_tile_value_counts)

    print(ai2048demo.welch(random_max_tile_values, ai_max_tile_values))
