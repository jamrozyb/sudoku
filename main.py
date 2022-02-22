import copy
import math
from pandas import *

class Sudoku:

    def __init__(self, sudoku):
        self.sudoku = copy.deepcopy(sudoku)
        self.original_sudoku = sudoku

    def solve_sudoku(self):
        j = -1
        i = 0
        i, j = self.get_next_field_to_completed(i, j)
        while True:
            value_in_i_j = self.sudoku[i][j]
            minimum_good_value = self.minimum_greater_good_value(value_in_i_j, i, j)

            if minimum_good_value:
                self.sudoku[i][j] = minimum_good_value
                try:
                    i, j = self.get_next_field_to_completed(i, j)
                except IndexError:
                    return self.sudoku
            else:
                self.sudoku[i][j] = 0
                i, j = self.get_previous_field_to_completed(i, j)

    def minimum_greater_good_value(self, minimum, i, j):
        for n in range(minimum + 1, 10):
            if self.can_insert_number(n, i, j):
                return n
        return False

    def get_next_field_to_completed(self, i, j):
        while True:
            j += 1
            if j >= 9:
                j = 0
                i += 1
                if i >= 9:
                    raise IndexError("finish")
            if self.original_sudoku[i][j] == 0:
                return i, j

    def get_previous_field_to_completed(self, i, j):
        while True:
            j -= 1
            if j < 0:
                j = 8
                i -= 1
                if i < 0:
                    raise IndexError()
            if self.original_sudoku[i][j] == 0:
                return i, j

    def can_insert_number(self, n, i, j):
        return not (self.is_number_in_small_square(n, i, j)
                    or self.is_number_in_column(n, j)
                    or self.is_number_in_row(n, i))

    def is_number_in_row(self, n, i):
        return n in self.sudoku[i]

    def is_number_in_column(self, n, j):
        for row in self.sudoku:
            if n == row[j]:
                return True
        return False

    def is_number_in_small_square(self, n, i, j):
        i_square_center = math.floor(i / 3)*3 + 1
        j_sguare_center = math.floor(j / 3)*3 + 1

        if n in self.sudoku[i_square_center - 1][j_sguare_center - 1:j_sguare_center + 2]:
            return True;
        if n in self.sudoku[i_square_center][j_sguare_center - 1:j_sguare_center + 2]:
            return True;
        if n in self.sudoku[i_square_center + 1][j_sguare_center - 1:j_sguare_center + 2]:
            return True;
        return False;

#Zera reprezentują komórki które należy uzupełnić
normal_sudoku = [
    [3, 0, 0, 8, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 2, 0, 0, 0],
    [0, 4, 1, 5, 0, 0, 8, 3, 0],
    [0, 2, 0, 0, 0, 1, 0, 0, 0],
    [8, 5, 0, 4, 0, 3, 0, 1, 7],
    [0, 0, 0, 7, 0, 0, 0, 2, 0],
    [0, 8, 5, 0, 0, 9, 7, 4, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0],
    [9, 0, 0, 0, 0, 7, 0, 0, 6]
]
s = Sudoku(normal_sudoku)
print(DataFrame(s.solve_sudoku()))


# startujemy od pierwszego wolnego pola
# wstawiamy w pierwsze możliwe miejsce cyfrę "1"
# jeżeli nie koliduje z inną "1" w wierszu ani kolumnie, ani małym kwadratem, przechodzimy do następnego wolnego pola
# wstawiamy następną liczbę itd
# jeżeli nie morzem wstawić danej cyfry sprawdzamy, czy można wstawić następną cyfrę
# jeżeli tak to wstawiamy ją i idziemy dalej

# gdy w danym polu nie możemy już wstawić żadnej cyfry z zakresu od "1" do "9" to zerujemy pole i cofamy się do poprzednio
# uzupełnianego pola i wstawiamy najmniejszą poprawną wyższą cyfrę
# jeżeli to nie jest możliwe, zerujemy pole, cofamy się do uzupełnianego jeszcze w poprzednim kroku itd.
