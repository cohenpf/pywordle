# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 02:10:04 2022

@author: cohen
"""

import random as rand
import colorama
colorama.init()

def take_input(words):
    while(True):
        guess = input("\nWhat is your guess? \n").upper()
        if guess in words:
            return guess
        elif guess == 'GIVE UP':
            return guess
        else:
            print("Not in word list.")
    
def test_word(guess, sep_ans):
    sepa_guess = [alpha for alpha in guess]
    
    result = []
    for iid in range(len(guess)):
        if sepa_guess[iid] == sep_ans[iid]: result.append(2)
        elif sepa_guess[iid] in sep_ans: result.append(1)
        else: result.append(0)
    
    return result

def print_test(guess, test_res):
    cl_str = ''
    for iid in range(len(guess)):
        if test_res[iid] == 2:   cl_str += '\x1b[6;30;42m' + guess[iid] + '\x1b[0m'
        elif test_res[iid] == 1: cl_str += '\x1b[0;30;43m' + guess[iid] + '\x1b[0m'
        else:                    cl_str += '\x1b[0;30;47m' + guess[iid] + '\x1b[0m'
    return cl_str        
    
def ask_exit():
    while(True):
        question = input("\nPlay another game of Wordle? (Y/N)\n").upper()
        if question == 'Y':
            return False
        elif question == 'N':
            return True
        else:
            print("Type 'Y' or 'N'.\n")
            
def mod_alpha_stat(alpha_stat, guess, test_res):
    for iid in range(len(guess)):
        alpha_stat[guess[iid]] = max(test_res[iid], alpha_stat[guess[iid]])
        
def str_alp(alpha_stat, string):
    
    ret_str = ''
    for alphabet in string:
        stat = alpha_stat[alphabet]
        if stat == -1: ret_str += '\x1b[0;37;40m' + alphabet + '\x1b[0m'
        elif stat == 0: ret_str += '\x1b[0;30;47m' + alphabet + '\x1b[0m'
        elif stat == 1: ret_str += '\x1b[0;30;43m' + alphabet + '\x1b[0m'
        elif stat == 2: ret_str += '\x1b[6;30;42m' + alphabet + '\x1b[0m'
        else: ret_str += alphabet
    return ret_str
            
def print_alp(alpha_stat):
    row1 = 'QWERTYUIOP'
    row2 = 'ASDFGHJKL'
    row3 = 'ZXCVBNM'
    print('\n'+str_alp(alpha_stat, row1))
    print(' '+str_alp(alpha_stat, row2))
    print('  '+str_alp(alpha_stat, row3))
    
file = open('wordle-answers-alphabetical.txt', 'r')
answers = file.readlines()
file.close()
answers = [word.strip().upper() for word in answers]

file = open('wordle-words-alphabetical.txt', 'r')
words = file.readlines()
file.close()
words = [word.strip().upper() for word in words]
words.extend(answers)

print("\x1b[0;30;43mWelcome\x1b[0m \x1b[0;30;47mto\x1b[0m \x1b[6;30;42mWordle\x1b[0m!")
print("Find a 5-length English words in 6 trials!")
print("Type 'Give up' to give up current game.")
input("\n\nPress Enter key to start. \n")

while(True):
    answer = rand.choice(answers)
    sepa_ans = [alpha for alpha in answer]
    
    trials = 1
    prev = []
    
    alpha_stat = dict([[alpha, -1] for alpha in 'abcdefghijklmnopqrstuvwxyz'.upper()])
    
    while(trials < 7):
        print('=========================\n\nTrial ' + str(trials).strip() + '/6\n')
        for text in prev:
            print(text)
            
        print_alp(alpha_stat)
        guess = take_input(words)
        if guess == 'GIVE UP':
            trials = 7
            break
        test_temp = test_word(guess, sepa_ans)
        str_temp = print_test(guess, test_temp)
        prev.append(str_temp)
        mod_alpha_stat(alpha_stat, guess, test_temp)
        if sum(test_temp) == 2*len(test_temp):
            print('\nCorrect!\n')
            break
        trials += 1
        print('\n')
    
    for text in prev:
        print(text)
    
    if trials == 7:
        print('\nEnd of the game.\n The answer is : ' + answer)
    else:
        print('\nYou won!')
        
    do_exit = ask_exit()
    if do_exit: break
    else: pass

