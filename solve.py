from waffle import Waffle 
import nltk
from nltk.corpus import words
import re
from itertools import product
import sys
import networkx as nx
import matplotlib.pyplot as plt

import pyautogui
import time

def solveEdge (waffle , wordle):
    containslst = []
    re_str = "^"
    for i in range(0,5):
        if waffle.colors[wordle[i]] == "g" :
            re_str += waffle.letters[wordle[i]]
        elif waffle.colors[wordle[i]] == "w" :
            re_str += fr'(?![{waffle.letters[wordle[i]]}])[a-z]'
        elif  waffle.colors[wordle[i]] == "y" :
            re_str += fr'(?![{waffle.letters[wordle[i]]}])[a-z]'
            if i != 2 :
                containslst.append(waffle.letters[wordle[i]])
    re_str += "$"
    pattern = re.compile(re_str)
    matches = [word for word in word_list if pattern.match(word) and all(c in word for c in containslst) ]
    return matches
def checkEdges(waffle , edges):
    letters = waffle.letters +  waffle.letters[0] + waffle.letters[4] + waffle.letters[16] + waffle.letters[20]
    for word in edges:
        for c in word:
            if c in letters:
                letters = letters.replace(c , "" , 1)
            else:
                return [] , False
    return letters , True

def find_board_solution(puzzle_start , puzzle_solved):
    G = nx.DiGraph()
    for i in range(0,21):
        if puzzle_start.colors[i] != "g":
            G.add_node(i)
    

    for i in range(0,21):
        for j in range(0,21):
            if i != j and puzzle_start.letters[i] == puzzle_solved.letters[j] and puzzle_start.colors[i] != "g" and puzzle_start.colors[j] != 'g':
                G.add_edge(i,j)
    moves = []
    cycle_length = 2
    while G.nodes:
        removed_any = False
        for cycle in nx.simple_cycles(G):
            if len(cycle) == cycle_length:
                G.remove_nodes_from(cycle)
                moves.append(cycle)
                removed_any = True
                break
        if not removed_any:
            cycle_length += 1
            if cycle_length > len(G):
                break
    return moves
def calcCost(solution):
    rtn = 0
    for lst in solution:
        rtn += len(lst) - 1
    return rtn

def solveMiddle (waffle , startLetter, endLetter , wordle, combination):
    words , letters = combination
    containslst = []
    re_str = "^" + startLetter
    for i in range(1,4):
        if waffle.colors[wordle[i]] == "g" :
            re_str += waffle.letters[wordle[i]]
        elif waffle.colors[wordle[i]] == "w" :
            re_str += fr'(?![{waffle.letters[wordle[i]]}])[{letters}]'
        elif  waffle.colors[wordle[i]] == "y" :
            re_str += fr'(?![{waffle.letters[wordle[i]]}])[{letters}]'
            if i != 2 :
                containslst.append(waffle.letters[wordle[i]])
    re_str += endLetter + "$"
    pattern = re.compile(re_str)
    matches = [word for word in word_list if pattern.match(word) and all(c in word for c in containslst) ]
    return matches
def automate_moves(moves):
    d = {
        0:(1741,546),
        1:(1822,541),
        2:(1918,539),
        3:(2014,545),
        4:(2093,547),

        5:(1741,637),
        6:(1918,637),
        7:(2093,637),

        8:(1741,725),
        9:(1822,725),
        10:(1918,725),
        11:(2014,725),
        12:(2093,725),

        13:(1741,819),
        14:(1918,819),
        15:(2093,819),

        16:(1741,902),
        17:(1822,902),
        18:(1918,902),
        19:(2014,902),
        20:(2093,902),
    }
    starting = moves[0]
    pyautogui.moveTo(d[starting][0] , d[starting][1])

    for i in range(0,len(moves)-1):
        start = moves[i]
        end = moves[i+1]
       
        pyautogui.moveTo(d[start][0] , d[start][1], duration=.5)
        pyautogui.mouseDown(button='left')
        pyautogui.dragTo(d[end][0] , d[end][1], duration=.5)



if __name__ == "__main__":
    with open('words_alpha.txt') as f:
        word_list = set(word.strip().lower() for word in f if len(word.strip()) == 5)

    if len(sys.argv) >1:
        puzzle_start = Waffle(
            sys.argv[1] , sys.argv[2]
        )
    else:
        letters = input("letters? ")#"kaealrtundepiapatliln"
        colors = input("colors? ")#"gwwwgwywwygywygygwywg"
        puzzle_start = Waffle(
            letters , colors
        )

    puzzle_start.pprint()

    possible_words = [solveEdge(puzzle_start, [0,1,2,3,4]),
                        solveEdge(puzzle_start, [0,5,8,13,16]),
                        solveEdge(puzzle_start, [16,17,18,19,20]),
                        solveEdge(puzzle_start, [4,7,12,15,20]),]
    
    combinations = list(product(possible_words[0], possible_words[1], possible_words[2], possible_words[3]))
    possible_edges = []
    for edges in combinations:
        #check no extra letters  
        remaining_letters , possible = checkEdges(puzzle_start , edges)
        if possible:
            possible_edges.append((edges , remaining_letters))

    #find middle down
    middle_combinations = []
    for comb in possible_edges:
        words_lst , remaining_letters = comb
        w1 = solveMiddle(puzzle_start , words_lst[0][2], words_lst[2][2] ,[2,6,10,14,18] , comb )
        
        for word in w1:
            letters = remaining_letters
            for c in word[1:-1]:
                if c in letters:
                    letters = letters.replace(c , "" , 1)
                else:
                    break
            else:
                middle_combinations.append((words_lst+(word,) , letters))
            
    #find middle accross
    final_combinations = []
    for comb in middle_combinations:
        words_lst , remaining_letters = comb
        w1 = solveMiddle(puzzle_start , words_lst[1][2], words_lst[3][2] ,[8,9,10,11,12] , comb )
        for word in w1:
            final_combinations.append(words_lst+(word,))
    
    #generate and check waffles
    waffleLst=[]
    for possible  in final_combinations:
        w = Waffle(
            possible[0]+possible[1][1]+possible[-2][1]+possible[-3][1]+possible[-1]+possible[1][3]+possible[-2][3]+
            possible[-3][3]+possible[2]

            , "ggggggggggggggggggggg"
        )
        if puzzle_start.check(w):
            waffleLst.append(w)

    #print waffles
    for i in range(len(waffleLst)) :
        w = waffleLst[i]
        if puzzle_start.check(w):
            print()
            print("{})".format(i+1))
            w.pprint()
            board_solution = find_board_solution(puzzle_start , w)
            print(board_solution)
            print("SWAPS REMAINING" , 15 - calcCost(board_solution))

    #pick solution and automate moves
    if len(waffleLst) == 1:
        puzzle_solved = waffleLst[0]
        moves = find_board_solution(puzzle_start , puzzle_solved)
    else:
        touse = int(input("pick waffle "))
        puzzle_solved = waffleLst[touse - 1]
        puzzle_solved.pprint()
        moves = find_board_solution(puzzle_start , puzzle_solved)

    for move in moves:
        automate_moves(move[::-1])
        # time.sleep(.5)