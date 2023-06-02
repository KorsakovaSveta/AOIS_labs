from lab2 import SDNF
import pandas as pd
import re
from collections import OrderedDict
PLUS ="+"
STAR = "*"
FIVE = 5
FOUR = 4
THREE = 3
pattern1 = r"\+"
pattern2 = r"\*"
def substractor_table(truth_table):
    b = []
    d = []
    for i in range(len(truth_table['a'])):
        minuend = truth_table['a'][i] - truth_table['c'][i]
        if minuend >= truth_table['b'][i]:
            b.append(0)
        else:
            b.append(1)
        if abs(minuend) == truth_table['b'][i]:
            d.append(0)
        else:
            d.append(1)
        
    return d,b


def SDNF(truth_table, unique_letters,letter):
    sdnf = []
    for i in range(0, len(truth_table[letter])):
        if truth_table[letter][i] == 1:

            for index in range(0, len(unique_letters)):
                if truth_table[unique_letters[index]][i] == 0:
                    sdnf.append("!"+ unique_letters[index])
                else:
                    sdnf.append(unique_letters[index])
                if index != len(unique_letters)-1:
                    sdnf.append("*")
            sdnf.append("+")
    return sdnf

def plus_five():
    number_of_arguments = FOUR
    five_in_binary_system = [0, 1, 0, 1]
    five_in_decimal_system = FIVE
    arguments = {1:[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1], 2:[0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1], 3:[0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1], 4:[0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]}
    result = [[0 for column in range(len(arguments[1]))] for string in range(number_of_arguments)]
    for i in range(len(arguments[1]) - five_in_decimal_system):
        index = number_of_arguments
        plus_one = 0
        while index > 0 :
            summa = arguments[index][i] + five_in_binary_system[index - 1] + plus_one
            plus_one = 0
            if summa >= 2:
                summa -= 2
                plus_one = 1
            result[index - 1][i] = summa
            index -= 1
    return result, arguments


def SDNF_truth_table(plus,truth_table,keys,arguments):
    sdnf_truth_table = []

    for j in range(0,len(plus)):
        args = []
        if plus[j] == 1:
            for index in range(0,len(arguments)):
                args.append(truth_table[arguments[index]][j])
            sdnf_truth_table.append(args)
    return sdnf_truth_table

def total_gluing(formula, number_of_arguments):
    i = number_of_arguments
    while i > 1:
        formula = gluing_formulas(formula, i)
        i -= 1
    return formula 

def gluing_formulas(constituents, arguments_number):
    implicants = []
    first_bracket_index = 0
    i = 0
    for i in range(len(constituents)):
        if number_of_arguments_in_brackets(constituents[i]) == arguments_number:
            first_bracket_index = i
            break
           
    mas = [False for i in range(len(constituents))]
    for i in range(first_bracket_index, len(constituents)): #текущая
        for j in range(i, len(constituents)): #последующая
            if is_gluable(constituents[i], constituents[j]) != -1:
                implicant = constituents[i].copy()
                implicant[is_gluable(constituents[i],constituents[j])] = -1
                if not(identical_find(implicant, implicants)):
                    implicants.append(implicant)
                mas[i] = True
                mas[j] = True
    for i in range(len(mas)):
        if mas[i] == False:
            implicants.insert(0, constituents[i])
    return implicants

def is_gluable(constituent_1, constituent_2):
    different = 0
    for i in range(len(constituent_1)):
        if constituent_1[i] != constituent_2[i]:
            different += 1
            unnecessary = i
        if different != 1:
            unnecessary = -1 #лишний аргумент
    return unnecessary

def number_of_arguments_in_brackets(brackets):
    number = 0
    for i in range(len(brackets)):
        if brackets[i] != -1:
            number += 1 
    return number

def identical_find(implicant, implicants):
    for other in implicants:
        if implicant == other: 
            return True
    return False

def TDNF(tdnf_in_table,arguments):
    tdnf = []
    for i in range(0,len(tdnf_in_table)):
        constituent = []
        for j in range(0,len(tdnf_in_table[i])):
            if tdnf_in_table[i][j] == 0:
                constituent.append("!"+arguments[j])
            if tdnf_in_table[i][j] == 1:
                constituent.append(arguments[j])
        constituent = STAR.join(constituent)
        tdnf.append(constituent)
    tdnf = PLUS.join(tdnf)
    return tdnf

def TDNF_for_arguments(plus,arguments,truth_table,letter,number_args):
    
    keys = list(plus.keys())
    for i in range(0,len(plus)):
        sdnf = SDNF(truth_table,letter,keys[i])
        sdnf = ''.join(sdnf[0:len(sdnf)-1]) 
        print("СДНФ for", keys[i], sdnf)
        sdnf_truth_table = SDNF_truth_table(plus[keys[i]],arguments,keys[i],letter)
        tdnf = TDNF(total_gluing(sdnf_truth_table,number_args),letter)
        print("ТДНФ for",keys[i], tdnf)
        logism = tdnf.replace('!', '~')
        logism = logism.replace('*', '&')
        logism = logism.replace('+', '+')
        print('ТДНФ', keys[i], 'for logism:' + logism)
        print("\n")


def main():
    print("Task 1")
    Plus = {}
    args = {"a":[0, 0, 0, 0, 1, 1,1,1],"b":[0, 0, 1, 1, 0, 0, 1, 1], "c":[0,1,0,1,0,1,0,1]}
    d,b = substractor_table(args)
    Plus["d"] = d 
    Plus["b+1"] = b
    truth_table = args | Plus
    [print(key,':',value) for key, value in truth_table.items()]
    
    key = ["a","b","c"]
    TDNF_for_arguments(Plus,args,truth_table,["a","b","c"],THREE)


    print("Task 2")
    key = ["a","b","c","d"]
    plus, arguments = plus_five()
    for i in range(0,len(key)):
       arguments[key[i]] = arguments.pop(i+1)
    [print(key,':',value) for key, value in arguments.items()]
    key = ["a1","b1","c1","d1"]
    plus_dict = {}
    for i in range(0,len(key)):
        plus_dict[key[i]] = plus[i]
    [print(key,':',value) for key, value in plus_dict.items()]
    truth_table = arguments | plus_dict
    TDNF_for_arguments(plus_dict, arguments,truth_table,["a","b","c","d"],FOUR)
main()