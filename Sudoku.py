#!/usr/bin/env python3

import random

__author__ = "Patrick Denis Browne"
__email__ = "pbrowne575@gmail.com"
__license__ = "GPLv3"

class square:
    def __init__(self, index):
        self.row = self._set_row(index)
        self.column = self._set_column(index)
        self.subgrid = self._set_subgrid()
        self.possibilities = [i for i in range(1, 10)]
        self.solved = False
        self.solution = None
    
    def _set_column(self, index):
        return(index % 9)
    
    def _set_row(self, index):
        return(index // 9)
    
    def _set_subgrid(self):
        return(3*(self.row // 3) + (self.column // 3))
    
    def drop_possibility(self, number):
        if number in self.possibilities:
            _ = self.possibilities.pop(self.possibilities.index(number))
    
    def evaluate(self):
        assert (len(self.possibilities) > 0), \
        "Something went wrong with the logic. This is a problem if solving a grid. This should be excepted if building a new grid"
        if len(self.possibilities) == 1:
            self.set_num(self.possibilities[0])
    
    def set_num(self, number):
        self.possibilities = None
        self.solved = True
        self.solution = number
        
class suGrid:
    def __init__(self):
        self.squares = [square(i) for i in range(81)]
        self.num_solved = self.eval_solved()
        self._subgrid_offsets = [0, 1, 2, 9, 10, 11, 18, 19, 20]
    
    def eval_solved(self):
        solved = 0
        for i in range(81):
            if self.squares[i].solved == True:
                solved += 1
        return(solved)
    
    def row_indices(self):
        return([[(9*i)+j for j in range(9)] for i in range(9)])
    
    def column_indices(self):
        return([[i+(j*9) for j in range(9)] for i in range(9)])
    
    def subgrid_indices(self):
        return([[18*(i//3) + i*3 + j for j in self._subgrid_offsets] for i in range(9)])
    
    def set_square(self, number, row, column):
        sqindex = 9 * (row - 1) + (column - 1)
        self.squares[sqindex].set_num(number)
    
    def set_square_by_index(self, number, index):
        self.squares[index].set_num(number)
    
    def clean_solved(self, indices):
        '''
        Looks for row, columns or subgrids. If any of the squares are solved,
        it removes the solution from the possibilities of the other squares
        in the indices.
        '''
        for index in indices:
            if self.squares[index].solved == True:
                for i in indices:
                    if self.squares[i].solved == False:
                        if self.squares[index].solution in self.squares[i].possibilities:
                            self.squares[i].drop_possibility(self.squares[index].solution)
    
    def clean_limits(self, indices):
        '''
        For N squares within a row, column or subgrid, this looks for then same
        N possibilities occuring N times. These possibilities are then removed
        as possibilities for all other squres.
        
        For example, if two squares have only 5 and 8 as their only
        possibilities, then 5 and 8 must be within these two squares. In this
        case, 5 and 8 should be removed as possibilities in all other squares
        in this row, column or subgrid.
        '''
        ns_indices = [i for i in indices if self.squares[i].solved == False]
        ns_possibilities = [self.squares[ns_index].possibilities for ns_index in ns_indices]
        for i in range(len(ns_indices)-1):
            for ns_possibility in ns_possibilities:
                if len(ns_possibility) == i and ns_possibilities.count(ns_possibility) == i:
                    js = [j for j in range(len(ns_possibilities)) if not ns_possibilities[j] == ns_possibility]
                    for j in js:
                        for num in ns_possibility:
                            self.squares[ns_indices[j]].drop_possibility(num)
                        
    def unique_to_row(self, sbgrid):
        '''
        If a number (X) is only a possibility in one particular row of a
        subgrid, then it should not be possibility in the same row of the other
        two subgrids in a row with the query's subgrid.
        
        Input: subgrid is a list of nine indices referring to the positions of
               the relevant squares in the grid.
               
        Output: None if no such number is found. Otherwise, a list is returned.
                The returned list will contain the subgrid label as its first
                element which will be followed by at least one tuple. The
                following tuple(s) will contain the number to be removed as a
                possbility as its first element, and the row from which it
                should be removed as its second element.
        '''
        assert len(list(set([self.squares[i].subgrid for i in sbgrid]))) == 1, \
        "The squares are not all from the subgrid"
        output = [self.squares[sbgrid[0]].subgrid]
        js = [int(i) for i in range(1, 10)]
        for sqindex in sbgrid:
            if self.squares[sqindex].solved == True:
                _ = js.pop(js.index(self.squares[sqindex].solution))
        sbgrid = [i for i in sbgrid if self.squares[i].solved == False]
        if len(sbgrid) == 0:
            return(None)
        for j in js:
            if j in [self.squares[i].solution for i in sbgrid]:
                continue
            j_rows = [self.squares[i].row for i in sbgrid if j in self.squares[i].possibilities]
            if len(list(set(j_rows))) == 1:
                output.append((j, list(set(j_rows))[0]))
        if len(output) > 1:
            return(output)
        else:
            return(None)
    
    def unique_to_column(self, sbgrid):
        '''
        If a number (X) is only a possibility in one particular column of a
        subgrid, then it should not be possibility in the same column of the
        other two subgrids in a column with the query's subgrid.
        
        Input: subgrid is a list of nine indices referring to the positions of
               the relevant squares in the grid.
               
        Output: None if no such number is found. Otherwise, a list is returned.
                The returned list will contain the subgrid label as its first
                element which will be followed by at least one tuple. The
                following tuple(s) will contain the number to be removed as a
                possbility as its first element, and the column from which it
                should be removed as its second element.
        '''
        assert len(list(set([self.squares[i].subgrid for i in sbgrid]))) == 1, \
        "The squares are not all from the subgrid"
        output = [self.squares[sbgrid[0]].subgrid]
        js = [int(i) for i in range(1, 10)]
        for sqindex in sbgrid:
            if self.squares[sqindex].solved == True:
                _ = js.pop(js.index(self.squares[sqindex].solution))
        sbgrid = [i for i in sbgrid if self.squares[i].solved == False]
        if len(sbgrid) == 0:
            return(None)
        for j in js:
            if j in [self.squares[i].solution for i in sbgrid]:
                continue
            j_columns = [self.squares[i].column for i in sbgrid if j in self.squares[i].possibilities]
            if len(list(set(j_columns))) == 1:
                output.append((j, list(set(j_columns))[0]))
        if len(output) > 1:
            return(output)
        else:
            return(None)
    
    def logic3_rows(self):
        other_rows = {0:[1,2], 1:[0,2], 2:[0,1],
                      3:[4,5], 4:[3,5], 5:[3,4],
                      6:[7,8], 7:[6,8], 8:[6,7]}
        for subgrid in self.subgrid_indices():
            row_with_uniques = self.unique_to_row(subgrid)
            if row_with_uniques != None:
                other_subgrid_labels = other_rows[row_with_uniques[0]]
                for tup in row_with_uniques[1:]:
                    for i in range(len(self.squares)):
                        if self.squares[i].solved == False:
                            if self.squares[i].row == tup[1] and self.squares[i].subgrid in other_subgrid_labels:
                                if tup[0] in self.squares[i].possibilities:
                                    self.squares[i].drop_possibility(tup[0])
    
    def logic3_columns(self):
        other_columns = {0:[3,6], 3:[0,6], 6:[0,3],
                         1:[4,7], 4:[1,7], 7:[1,4],
                         2:[5,8], 5:[2,8], 8:[2,5]}
        for subgrid in self.subgrid_indices():
            column_with_uniques = self.unique_to_column(subgrid)
            if column_with_uniques != None:
                other_subgrid_labels = other_columns[column_with_uniques[0]]
                for tup in column_with_uniques[1:]:
                    for i in range(len(self.squares)):
                        if self.squares[i].solved == False:
                            if self.squares[i].column == tup[1] and self.squares[i].subgrid in other_subgrid_labels:
                                if tup[0] in self.squares[i].possibilities:
                                    self.squares[i].drop_possibility(tup[0])
    
    def simplify_uniques(self, indices):
        js = [i for i in range(1, 10)]
        for i in indices:
            if self.squares[i].solved == True:
                _ = js.pop(js.index(self.squares[i].solution))
        indices = [i for i in indices if self.squares[i].possibilities != None]
        for j in js:
            jcount = 0
            for i in indices:
                if j in self.squares[i].possibilities:
                    jcount += 1
            if jcount == 1:
                for i in indices:
                    if j in self.squares[i].possibilities:
                        self.squares[i].possibilities = [j]
    
    def sweep(self):
        '''
        Checks the grid to see if the numbers of possibilities for unsolved
        squares have been reduced to 1. If so it marks these off as solved.
        Returns the number of newly solved squares
        '''
        for i in range(81):
            if self.squares[i].solved == False:
                self.squares[i].evaluate()
    
    def clean_all(self):
        iSolved = self.eval_solved()
        
        for indices in self.row_indices():
            self.clean_solved(indices)
        self.sweep()
        
        for indices in self.column_indices():
            self.clean_solved(indices)
        self.sweep()
        
        for indices in self.subgrid_indices():
            self.clean_solved(indices)
        self.sweep()
        
        for indices in self.row_indices():
            self.clean_limits(indices)
        self.sweep()
        
        for indices in self.column_indices():
            self.clean_limits(indices)
        self.sweep()
        
        for indices in self.subgrid_indices():
            self.clean_limits(indices)
        self.sweep()
        
        self.logic3_rows()
        self.sweep()
        
        self.logic3_columns()
        self.sweep()
        
        for indices in self.row_indices():
            self.simplify_uniques(indices)
        self.sweep()
        
        for indices in self.column_indices():
            self.simplify_uniques(indices)
        self.sweep()
        
        for indices in self.subgrid_indices():
            self.simplify_uniques(indices)
        self.sweep()
        
        fSolved = self.eval_solved()
        return(fSolved - iSolved)
    
    def _write_row(self, indices):
        '''
        This should be given the indices for the squares of a row. The write
        function will call this to write rows
        '''
        assert len(indices) == 9, "The wrong number of indices was given!"
        nums_to_write = []
        for i in indices:
            if self.squares[i].solved == True:
                nums_to_write.append(str(self.squares[i].solution))
            else:
                nums_to_write.append('0')
        output = ': %s %s %s : %s %s %s : %s %s %s :' % (nums_to_write[0],
        nums_to_write[1], nums_to_write[2], nums_to_write[3], nums_to_write[4],
        nums_to_write[5], nums_to_write[6], nums_to_write[7], nums_to_write[8])
        return(output)
    
    def str_repr(self):
        grid_line = ' ' + ' '.join([''.join(['-']*7)]*3)
        outLines = []
        outLines.append(grid_line)
        rows = self.row_indices()
        for i in range(3):
            for j in range(3):
                outLines.append(self._write_row(rows.pop(0)))
            outLines.append(grid_line)
        output = '\n'.join(outLines)
        return(output)
    
    def print_game(self):
        print(self.str_repr())
    
    def load_game(self,game_as_string):
        '''
        The game may be represented as a string. Newline characters will be
        stripped. Unknown squares must be indicated with 0.
        '''
        nums_as_strs = [str(char) for char in game_as_string
                        if char in [str(i) for i in range(0, 10)]]
        assert len(nums_as_strs) == 81, "The game wasn't properly formatted. Please specify up to 81 numerical digits, with 0s or white-spaces in the place of unknown squares. Don't use white spaces unless they represent unknown squares"
        i = 0
        for char in nums_as_strs:
            if char == ' ' or char == '0':
                i += 1
            elif char in [str(j) for j in range(1, 10)]:
                self.squares[i].set_num(int(char))
                i += 1
    
    def randomly_assign_square(self):
        unassigned_indices = [i for i in range(81) if self.squares[i].solved == False]
        assert (len(unassigned_indices) > 0), "The grid is already full. No more numbers may be added"
        sq_index = random.choice(unassigned_indices)
        num_to_assign = random.choice(self.squares[sq_index].possibilities)
        self.set_square_by_index(num_to_assign, sq_index)
    
    
    def isSolvableLogicallyFromHere(self):
        gamestr = self.str_repr()
        copy = suGrid()
        copy.load_game(gamestr)
        copy.sweep()
        added = []
        while copy.eval_solved() < 81:
            added.append(copy.clean_all())
            if added[-10:] == [0]*10:
                return(False)
        return(True)
    
def full_new_grid():
    '''
    This will start from an empty grid. Then it will randomly assign a
    value to one square, solve as far as is possible, then assign another
    random square and solve as far as possible until either it encounters
    a problem or it produces a full grid.
    '''
    try:
        new_grid = suGrid()
        added = []
        while new_grid.eval_solved() < 81:
            try:
                added.append(new_grid.clean_all())
            except:
                full_new_grid()
                break
            if added[-10:] == [0]*10:
                new_grid.randomly_assign_square()
                added = []
        return(new_grid)
    except:
        full_new_grid()


def new_game(solvable=None):
    '''
    Either give it a fully solved suGrid object, which could be the
    output of 'full_new_grid'.
    Otherwise, if given no input (defaulting to None) it will call the
    'full_new_grid' function to compose a random new game.
    '''
    if solvable == None:
        solvable = full_new_grid()
    solution = solvable.str_repr()
    solved_square_indices = [i for i in range(81) if solvable.squares[i].solved == True]
    while len(solved_square_indices) > 0:
        testIndex = solved_square_indices.pop(random.randint(0,
                    len(solved_square_indices) - 1))
        testSquareSolution = solvable.squares[testIndex].solution
        solvable.squares[testIndex].solution = None
        solvable.squares[testIndex].possibilities = [i for i in range(1, 10)]
        solvable.squares[testIndex].solved = False
        if solvable.isSolvableLogicallyFromHere() == True:
            continue
        else:
            solvable.squares[testIndex].set_num(testSquareSolution)
    #new_puzzle = solvable.print_game()
    return(solvable, solution)

def i_new_games(num_games, progress_every=10):
    solvables, solutions = [], []
    i = 0
    while i < num_games:
        try:
            solvable, solution = new_game()
            solvables.append(solvable.str_repr())
            solutions.append(solution)
            i += 1
            if i % progress_every == 0:
                print("%i new games created" % i)
        except:
            continue
    return(solvables, solutions)

def encode_sudoku(sudoku_str):
    nums = []
    for char in sudoku_str:
        if char in [str(i) for i in range(10)]:
            nums.append(int(char))
    if len(nums) != 81:
        print(nums)
        quit()
    assert len(nums) == 81, "Sudoku must have 81 numbers:\n%s" % (sudoku_str)
    output = []
    for num in nums:
        char_repr = [0 for i in range(9)]
        if num != 0:
            char_repr[num - 1] = 1
        output = output + char_repr
    return(output)

def decode_sudoku(encoded_list):
    assert len(encoded_list) == 729
    nums = []
    for i in range(81):
        subset = encoded_list[i*9: (i+1)*9]
        if list(set(subset)) == [0]:
            nums.append('0')
        else:
            nums.append(str(subset.index(max(subset)) + 1))
    return(''.join(nums))

if __name__ == '__main__':
    grid = suGrid()
    game_as_string = input('Paste a game as a string\n')
    grid.load_game(game_as_string)
    added = []
    print(grid.eval_solved())
    while grid.eval_solved() < 81:
        added.append(grid.clean_all())
        print(grid.eval_solved())
        if added[-100:] == [0]*100:
            print("I can't seem to be able to progress")
            print("I got this far:")
            grid.print_game()
            quit()
    print("Solved!")
    grid.print_game()

