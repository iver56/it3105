import random
import math


class Board(object):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def __init__(self, size=4, board_values=None):
        self.size = size

        if board_values is None:
            self.board_values = []
            for i in xrange(size):
                self.board_values.append([])
                for j in xrange(size):
                    self.board_values[i].append(0)
        else:
            self.board_values = board_values

    def set_board_values(self, board_values):
        self.board_values = board_values

    def get_possible_moves(self):
        moves = []
        if self.can_move_up():
            moves.append(self.UP)
        if self.can_move_right():
            moves.append(self.RIGHT)
        if self.can_move_down():
            moves.append(self.DOWN)
        if self.can_move_left():
            moves.append(self.LEFT)
        return moves

    def can_move(self, direction):
        """
        :param direction: 0, 1, 2 or 3
        :return:
        """
        if direction == self.UP:
            return self.can_move_up()
        elif direction == self.RIGHT:
            return self.can_move_right()
        elif direction == self.DOWN:
            return self.can_move_down()
        elif direction == self.LEFT:
            return self.can_move_left()

    def can_move_up(self):
        for row_index in range(1, self.size):
            for column_index in xrange(self.size):
                if self.board_values[row_index][column_index] > 0 \
                        and self.can_move_tile_up(row_index, column_index):
                    return True
        return False

    def can_move_tile_up(self, row_index, column_index):
        numbers_to_check_for = (0, self.board_values[row_index][column_index])
        return self.board_values[row_index - 1][column_index] in numbers_to_check_for

    def can_move_right(self):
        for row_index in xrange(self.size):
            for column_index in xrange(self.size - 1):
                if self.board_values[row_index][column_index] > 0 \
                        and self.can_move_tile_right(row_index, column_index):
                    return True
        return False

    def can_move_tile_right(self, row_index, column_index):
        numbers_to_check_for = (0, self.board_values[row_index][column_index])
        return self.board_values[row_index][column_index + 1] in numbers_to_check_for

    def can_move_down(self):
        for row_index in range(self.size - 1):
            for column_index in xrange(self.size):
                if self.board_values[row_index][column_index] > 0 \
                        and self.can_move_tile_down(row_index, column_index):
                    return True
        return False

    def can_move_tile_down(self, row_index, column_index):
        numbers_to_check_for = (0, self.board_values[row_index][column_index])
        return self.board_values[row_index + 1][column_index] in numbers_to_check_for

    def can_move_left(self):
        for row_index in xrange(self.size):
            for column_index in range(1, self.size):
                if self.board_values[row_index][column_index] > 0 \
                        and self.can_move_tile_left(row_index, column_index):
                    return True
        return False

    def can_move_tile_left(self, row_index, column_index):
        numbers_to_check_for = (0, self.board_values[row_index][column_index])
        return self.board_values[row_index][column_index - 1] in numbers_to_check_for

    def move(self, direction):
        """
        :param direction: 0, 1, 2 or 3
        :return:
        """
        if direction == self.UP:
            return self.move_up()
        elif direction == self.RIGHT:
            return self.move_right()
        elif direction == self.DOWN:
            return self.move_down()
        elif direction == self.LEFT:
            return self.move_left()

    def move_up(self):
        for column_index in xrange(self.size):
            min_row_index = 0
            for row_index in range(1, self.size):
                if self.board_values[row_index][column_index] > 0:
                    op, new_row_index = self.move_tile_up(row_index, column_index, min_row_index)
                    if op == 2:
                        min_row_index = new_row_index + 1

    def move_tile_up(self, row_index, column_index, min_row_index):
        value = self.board_values[row_index][column_index]
        potential_new_row_index = None
        for other_row_index in reversed(range(min_row_index, row_index)):
            other_value = self.board_values[other_row_index][column_index]
            if other_value == value:
                # combine
                self.board_values[other_row_index][column_index] = value + other_value
                self.board_values[row_index][column_index] = 0
                return 2, other_row_index
            elif other_value == 0:
                potential_new_row_index = other_row_index
            else:
                break
        if potential_new_row_index is not None:
            # move
            self.board_values[row_index][column_index] = 0
            self.board_values[potential_new_row_index][column_index] = value
            return 1, None
        return 0, None

    def move_right(self):
        for row_index in xrange(self.size):
            max_col_index = self.size - 1
            for column_index in reversed(xrange(self.size - 1)):
                if self.board_values[row_index][column_index] > 0:
                    op, new_col_index = self.move_tile_right(row_index, column_index, max_col_index)
                    if op == 2:
                        max_col_index = new_col_index - 1

    def move_tile_right(self, row_index, column_index, max_col_index):
        value = self.board_values[row_index][column_index]
        potential_new_col_index = None
        for other_col_index in range(column_index + 1, max_col_index + 1):
            other_value = self.board_values[row_index][other_col_index]
            if other_value == value:
                # combine
                self.board_values[row_index][other_col_index] = value + other_value
                self.board_values[row_index][column_index] = 0
                return 2, other_col_index
            elif other_value == 0:
                potential_new_col_index = other_col_index
            else:
                break
        if potential_new_col_index is not None:
            # move
            self.board_values[row_index][column_index] = 0
            self.board_values[row_index][potential_new_col_index] = value
            return 1, None
        return 0, None

    def move_down(self):
        for column_index in xrange(self.size):
            max_row_index = self.size - 1
            for row_index in reversed(xrange(self.size - 1)):
                if self.board_values[row_index][column_index] > 0:
                    op, new_row_index = self.move_tile_down(row_index, column_index, max_row_index)
                    if op == 2:
                        max_row_index = new_row_index - 1

    def move_tile_down(self, row_index, column_index, max_row_index):
        value = self.board_values[row_index][column_index]
        potential_new_row_index = None
        for other_row_index in range(row_index + 1, max_row_index + 1):
            other_value = self.board_values[other_row_index][column_index]
            if other_value == value:
                # combine
                self.board_values[other_row_index][column_index] = value + other_value
                self.board_values[row_index][column_index] = 0
                return 2, other_row_index
            elif other_value == 0:
                potential_new_row_index = other_row_index
            else:
                break
        if potential_new_row_index is not None:
            # move
            self.board_values[row_index][column_index] = 0
            self.board_values[potential_new_row_index][column_index] = value
            return 1, None
        return 0, None

    def move_left(self):
        for row_index in xrange(self.size):
            min_col_index = 0
            for column_index in range(1, self.size):
                if self.board_values[row_index][column_index] > 0:
                    op, new_col_index = self.move_tile_left(row_index, column_index, min_col_index)
                    if op == 2:
                        min_col_index = new_col_index + 1

    def move_tile_left(self, row_index, column_index, min_col_index):
        value = self.board_values[row_index][column_index]
        potential_new_col_index = None
        for other_col_index in reversed(range(min_col_index, column_index)):
            other_value = self.board_values[row_index][other_col_index]
            if other_value == value:
                # combine
                self.board_values[row_index][other_col_index] = value + other_value
                self.board_values[row_index][column_index] = 0
                return 2, other_col_index
            elif other_value == 0:
                potential_new_col_index = other_col_index
            else:
                break
        if potential_new_col_index is not None:
            # move
            self.board_values[row_index][column_index] = 0
            self.board_values[row_index][potential_new_col_index] = value
            return 1, None
        return 0, None

    def place_new_value_randomly(self):
        empty_positions = []
        for row_index in xrange(self.size):
            for column_index in range(self.size):
                if self.board_values[row_index][column_index] == 0:
                    empty_positions.append((row_index, column_index))
        if len(empty_positions) > 0:
            row_index, column_index = random.choice(empty_positions)
            if random.random() >= 0.9:
                self.board_values[row_index][column_index] = 4
            else:
                self.board_values[row_index][column_index] = 2

    def get_tile_stats(self):
        num_empty_tiles = 0
        max_tile_value = 2
        tile_sum = 0
        for row in self.board_values:
            for cell in row:
                if cell == 0:
                    num_empty_tiles += 1
                else:
                    tile_sum += cell
                if cell > max_tile_value:
                    max_tile_value = cell
        return num_empty_tiles, max_tile_value, tile_sum

    def __repr__(self):
        result = ''
        for row in self.board_values:
            result += str(row) + "\n"
        return result

    def get_column(self, col_index):
        column = []
        for row in self.board_values:
            column.append(row[col_index])
        return column
