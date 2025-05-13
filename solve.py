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
def checkComb(waffle , comb):
    letters = waffle.letters +  waffle.letters[0] + waffle.letters[4] + waffle.letters[16] + waffle.letters[20]
    for word in comb:
        for c in word:
            if c in letters:
                letters = letters.replace(c , "" , 1)
            else:
                return [] , False
    return letters , True
# print()
# nltk.download('words')
# word_list = set(w.lower() for w in words.words() if len(w) == 5)

with open('words_alpha.txt') as f:
    word_list = set(word.strip().lower() for word in f if len(word.strip()) == 5)


pattern = re.compile(r'^r[a-z][a-z][a-z]a$')

matches = [word for word in word_list if pattern.match(word)]




if len(sys.argv) >1:

    puzzle_start = Waffle(
        sys.argv[1] , sys.argv[2]
    )
else:
    letters = "kaealrtundepiapatliln"
    colors = "gwwwgwywwygywygygwywg"
    puzzle_start = Waffle(
        letters , colors
    )


puzzle_start.pprint()

possible_words = [solveEdge(puzzle_start, [0,1,2,3,4]),
                    solveEdge(puzzle_start, [0,5,8,13,16]),
                    solveEdge(puzzle_start, [16,17,18,19,20]),
                    solveEdge(puzzle_start, [4,7,12,15,20]),]
# print(possible_words)
combinations = list(product(possible_words[0], possible_words[1], possible_words[2], possible_words[3]))
combinations_pruned = []
for comb in combinations:
    remaining_letters , possible = checkComb(waffle=puzzle_start , comb=comb)
    if possible:
        combinations_pruned.append((comb , remaining_letters))


# print(len(combinations_pruned))
# print(combinations_pruned)

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

new_combinations = []
for comb in combinations_pruned:
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
            new_combinations.append((words_lst+(word,) , letters))
        
# print(new_combinations)
final_combinations = []
for comb in new_combinations:
    words_lst , remaining_letters = comb
    w1 = solveMiddle(puzzle_start , words_lst[1][2], words_lst[3][2] ,[8,9,10,11,12] , comb )
    for word in w1:
        final_combinations.append(words_lst+(word,))
# print(final_combinations)

waffleLst=[]
for possible  in final_combinations:
    waffleLst.append(Waffle(
        possible[0]+possible[1][1]+possible[-2][1]+possible[-3][1]+possible[-1]+possible[1][3]+possible[-2][3]+
        possible[-3][3]+possible[2]

         , "ggggggggggggggggggggg"
    ))
for w in waffleLst:
    if puzzle_start.check(w):
        w.pprint()

puzzle_solved = waffleLst[0]


G = nx.DiGraph()
for i in range(0,21):
    if puzzle_start.colors[i] != "g":
        G.add_node(i)

for i in range(0,21):
    for j in range(0,21):
        if i != j and puzzle_start.letters[i] == puzzle_solved.letters[j] and puzzle_start.colors[i] != "g" and puzzle_start.colors[j] != 'g':
            G.add_edge(i,j)


# pos = {
#     0: (0, 4), 1: (1, 4), 2: (2, 4), 3: (3, 4), 4: (4, 4),
#     5: (0, 3), 6: (2, 3), 7: (4, 3),
#     8: (0, 2), 9: (1, 2), 10: (2, 2), 11: (3, 2), 12: (4, 2),
#     13: (0, 1), 14: (2, 1), 15: (4, 1),
#     16: (0, 0), 17: (1, 0), 18: (2, 0), 19: (3, 0), 20: (4, 0),
# }


# filtered_pos = {k: v for k, v in pos.items() if k in G.nodes}


# nx.draw(G, pos=filtered_pos, with_labels=True, node_color="lightblue", arrows=True)
# plt.savefig("filename.png")

moves = []
cycle_length = 2
while G.nodes:
    removed_any = False
    for cycle in nx.simple_cycles(G):
        if len(cycle) == cycle_length:
            G.remove_nodes_from(cycle)
            moves.append(cycle)
            removed_any = True
    if not removed_any:
        cycle_length += 1
        if cycle_length > len(G):
            break
print(moves)

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
        # print(start , end)
        pyautogui.moveTo(d[start][0] , d[start][1], duration=.5)
        pyautogui.mouseDown(button='left')
        pyautogui.dragTo(d[end][0] , d[end][1], duration=.5)


for move in moves:
    automate_moves(move[::-1])
    # time.sleep(.5)