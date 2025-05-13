import sys
from termcolor import colored, cprint


class Waffle:
    def __init__(self, letters="....................." , colors="....................."):
        if len(letters)!=21:
            letters = letters + "."*(21-len(letters))
        if len(colors)!=21:
            colors = colors + "."*(21-len(colors))
        self.letters = letters
        self.colors = colors
    def complete(self):
        for letter in self.letters:
            if letter == ".":
                return False
        return True
    def get_unused_letters(self, starting_letters):
        unused_letters = starting_letters
        for letter in self.letters:
            if letter == ".":
                return unused_letters
            else:
                unused_letters = unused_letters.replace(letter, "",1)
                
        return unused_letters
            
    def pprint(self):
        print()
        def pprint_line_range(x,odd):
            d_colors = {
            "g" : "green",
            "y" : "yellow",
            "w" : "white",
            "." : "red"
            }
            y= x + (3 if odd else 5)
            for i in range(x,y):
                cprint(self.letters[i], d_colors[self.colors[i]], end='   'if odd else ' ')
            print()
            return y
        
        curr = 0
        for i in range(0,5):
            curr = pprint_line_range(curr,i%2)
        print()
    def append(self, letter):
        newLetters=""
        for i in range(0,21):
            if self.letters[i] == ".":
                newLetters += letter 
                return newLetters
            else:
                newLetters += self.letters[i]
        raise("waffle out of bounds append error")

    def get_wordles (self, num):
        #  0  1  2  3  4
        #  5  .  6  .  7
        #  8  9 10 11 12
        # 13  . 14 .  15
        # 16 17 18 19 20
        wordles_i = [[0,1,2,3,4],
                    [8,9,10,11,12],
                    [16,17,18,19,20],
                    [0,5,8,13,16],
                    [2,6,10,14,18],
                    [4,7,12,15,20]]
        rtn = []
        for wordle_i in wordles_i:
            if num in wordle_i:
                rtn .append( wordle_i)
        return rtn
    def get_neighbors (self, num):
        #  0  1  2  3  4
        #  5  .  6  .  7
        #  8  9 10 11 12
        # 13  . 14 .  15
        # 16 17 18 19 20
        rtn = []
        wordles_i = [[0,1,2,3,4],
                    [8,9,10,11,12],
                    [16,17,18,19,20],
                    [0,5,8,13,16],
                    [2,6,10,14,18],
                    [4,7,12,15,20]]
        for wordle_i in wordles_i:
            if num in wordle_i:
                rtn += wordle_i
                rtn.remove(num)
        return rtn
    def check_progress(self, waffle):
        i = len(waffle.letters.replace("." , "")) - 1
        # print(i)
        #check colors
        if self.colors[i] == "g" :
            return (self.letters[i] == waffle.letters[i])
        if self.colors[i] in ["y" , "w"] and (self.letters[i] == waffle.letters[i]):
            return False
        
        # if i not in [2,8,12,18]:
        #     for wordle in self.get_wordles(i):
        #         openings = len(list(filter(lambda x : x == "." , wordle)))

        #         count_unused_yellows = 0
        #         for j in wordle:
        #             if j not in [2,8,12,18] and self.colors[j] == "y" and self.letters[j] not in [waffle.letters[x] for x in wordle]:
        #                 count_unused_yellows+=1
            
        #         if count_unused_yellows > openings:
        #             return False
        return True
            
    def check(self, waffle):
        def check_no_extra_letters():
            return True
        def check_yellows():
            for i in range(0,21):
                if self.colors[i] == "y":
                    if waffle.letters[i]  == self.letters[i]:
                        return False
                    wordle = self.get_neighbors(i)
                    g_and_y = len(list(filter(lambda x : self.letters[x] == self.letters[i] and self.colors[x] in ["y", "g"], wordle)))
                    acutal_letter_count = len(list(filter(lambda x : waffle.letters[x] == self.letters[i], wordle)))
                    if g_and_y >  acutal_letter_count:
                        return False
            return True
        def check_greens():
            for i in range(0,21):
                if self.colors[i] == "g" and (self.letters[i] != waffle.letters[i]):
                    return False
            return True
        def check_whites():
            for i in range(0,21):
                if self.colors[i] == "w":

                    if waffle.letters[i]  == self.letters[i]:
                        return False
                    for wordle in self.get_wordles(i):
                        g_and_y = len(list(filter(lambda x : self.letters[x] == self.letters[i] and self.colors[x] in ["y", "g"], wordle)))
                        # print(i , self.letters[i] , g_and_y)
                        acutal_letter_count = len(list(filter(lambda x : waffle.letters[x] == self.letters[i], wordle)))
                        # print(acutal_letter_count)
                        
                        if g_and_y !=  acutal_letter_count:
                            return False

            return True
        return check_no_extra_letters() and check_yellows() and check_greens() and check_whites()

# letters_string = "wrcheseiarbosierhimte"
# colors_string = "gywygwywywgwyygygwywg"

if __name__ == "__main__":

    letters_string = "rernaibnaltomiuoeosre"
    colors_string = "gwywgywyywgywwwygwwyg"

    solved_letters_string = "rumbaaolintrosoneerie"
    solved_colors_string = "ggggggggggggggggggggg"

    puzzle_start = Waffle(letters_string , colors_string)
    puzzle_solved = Waffle("rumbaaolintrosoneerie" , "ggggggggggggggggggggg")

    puzzle_start.pprint()

    # for i in range(0,21):
    #     print(i , puzzle_start.get_neighbors(i))



    print(puzzle_start.check(puzzle_solved))

