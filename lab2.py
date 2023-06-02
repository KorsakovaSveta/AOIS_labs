import re
from itertools import product
REPLACE_NEGATION = "N"
REPLACE_IMPLICATION = "I"
REPLACE_DISUNCTION = "D"

def negation(formula):
    truth_table = []
    for i in range(0,len(formula)):
        result = not formula[i]
        truth_table.append(int(result))
    return truth_table

def implication(atomic_formula1, atomic_formula2):
    truth_table = []
    for i in range(0,len(atomic_formula1)):
        result = atomic_formula1[i] and atomic_formula2[i]
        truth_table.append(int(result))
    return truth_table

def disunction(atomic_formula1, atomic_formula2):
    truth_table = []
    for i in range(0,len(atomic_formula1)):
        result = atomic_formula1[i] or atomic_formula2[i]
        truth_table.append(int(result))
    return truth_table

def create_arguments(unique_letters):
    truth_table = {}
    for i in range(len(unique_letters)):
        truth_table[unique_letters[i]] = []

    for index in product((True, False), repeat=len(unique_letters)):
        for i in range(len(unique_letters)):
            truth_table[unique_letters[i]].append(int(index[i]))
    return truth_table

def replace_negation(index,truth_table, line, sub_formule):
    truth_table[REPLACE_NEGATION] = negation(truth_table[sub_formule[index+1]])
    sub_formule1 = sub_formule.replace(sub_formule[index:index+2], REPLACE_NEGATION)
    line = line.replace(sub_formule, sub_formule1)
    sub_formule = sub_formule1
    return truth_table, line,sub_formule

def replace_conunction(index,truth_table, line, sub_formule):
    if "I" in line:
        truth_table["C"] = implication(truth_table[sub_formule[index-1]], truth_table[sub_formule[index+1]])
        line = line.replace(sub_formule,"C")
    else:
        truth_table[REPLACE_IMPLICATION] = implication(truth_table[sub_formule[index-1]], truth_table[sub_formule[index+1]])
        line = line.replace(sub_formule,REPLACE_IMPLICATION)
    return truth_table, line,sub_formule

def replace_conunction_with_negation(index,truth_table, line, sub_formule):
    truth_table["O"] = negation(truth_table[sub_formule[index+2]])
    line = line.replace(sub_formule[index+1] + sub_formule[index+2], "O")
    sub_formule = sub_formule.replace(sub_formule[index+1] + sub_formule[index+2], "O")

    if "I" in line:
        truth_table["C"] = implication(truth_table[sub_formule[index-1]], truth_table[sub_formule[index+1]])
        line = line.replace(sub_formule,"C")
    else:
        truth_table[REPLACE_IMPLICATION] = implication(truth_table[sub_formule[index-1]], truth_table[sub_formule[index+1]])
        line = line.replace(sub_formule,REPLACE_IMPLICATION)
    return truth_table, line,sub_formule

def replace_disunction(index,truth_table,line, sub_formule):
    if "D" in line:
        truth_table["Д"] = disunction(truth_table[sub_formule[index-1]], truth_table[sub_formule[index+1]])
        line = line.replace(sub_formule,"Д")
    else:
        truth_table[REPLACE_DISUNCTION] = disunction(truth_table[sub_formule[index-1]], truth_table[sub_formule[index+1]])
        line = line.replace(sub_formule,REPLACE_DISUNCTION)
    return truth_table, line,sub_formule

def replace_disunction_with_negation(index,truth_table, line, sub_formule):
    truth_table["П"] = negation(truth_table[sub_formule[index+2]])
    line = line.replace(sub_formule[index+1] + sub_formule[index+2], "П")
    sub_formule = sub_formule.replace(sub_formule[index+1] + sub_formule[index+2], "П")

    if "D" in line:
        truth_table["Д"] = disunction(truth_table[sub_formule[index-1]], truth_table[sub_formule[index+1]])
        line = line.replace(sub_formule,"Д")
    else:
        truth_table[REPLACE_DISUNCTION] = disunction(truth_table[sub_formule[index-1]], truth_table[sub_formule[index+1]])
        line = line.replace(sub_formule,REPLACE_DISUNCTION)
    return truth_table, line,sub_formule


def check_formula(sub_formule,truth_table, line):
    for index in range(0,len(sub_formule)-1):
        if sub_formule[index] == "!":
            truth_table, line, sub_formule = replace_negation(index,truth_table, line, sub_formule)

        if sub_formule[index] == "*" and \
            sub_formule[index+1] != "!":
            truth_table, line, sub_formule = replace_conunction(index,truth_table,line, sub_formule)
            break

        if  sub_formule[index] == "*" and \
            sub_formule[index+1] == "!":
            truth_table, line, sub_formule = replace_conunction_with_negation(index,truth_table,line, sub_formule)
            break

        if sub_formule[index] == "+" and \
            sub_formule[index+1] != "!":
            truth_table, line, sub_formule = replace_disunction(index,truth_table, line, sub_formule)
            break
        
        if  sub_formule[index] == "+" and \
            sub_formule[index+1] == "!":
            truth_table, line, sub_formule = replace_disunction_with_negation(index,truth_table, line, sub_formule)
            break
    return truth_table, line, sub_formule

def create_result_truth_table(truth_table, line,opening_bracets,sub_formule_list):
    sub_formule = []
    for i in range(len(opening_bracets)-1, -2, -1):
        last_opening_bracet = opening_bracets[i]
        for index in range(last_opening_bracet, len(line)):
            sub_formule_list.append(line[index])
            if line[index] == ')':
                
                break
        if len(line) > 2:
            sub_formule = ''.join(sub_formule_list)
        
        truth_table,line,sub_formule = check_formula(sub_formule,truth_table, line)
       
        sub_formule_list.clear()
        if len(line) == 2 or \
            len(line) == 1:
            sub_formule = line
    return truth_table, sub_formule

def index_formula(truth_table):
    index_form = 0
    digit_weight = []
    for i in range(len(truth_table["result"])-1,-1,-1):
        digit_weight.append(2**i)
    for i in  range(0,len(digit_weight)):
        if truth_table["result"][i] == 1:
            index_form += digit_weight[i]
    print("Формула в индексной форме: ", index_form)

def number_formula(truth_table):
    number_form_SDNF,number_form_SindexNF =[],[]
    for i in range(0,len(truth_table["result"])):
        if truth_table["result"][i] == 1:
            number_form_SDNF.append(i)
        if truth_table["result"][i] == 0:
            number_form_SindexNF.append(i)
    print("Числовая форма для СДНФ: ",number_form_SDNF)
    print("Числовая форма для СКНФ: ", number_form_SindexNF)


def reverse_truth_table(truth_table):
    truth_table["result"].reverse()
    if "b" in truth_table:
        truth_table["b"].reverse()
    if "a" in truth_table:
        truth_table["a"].reverse()
    if "c" in truth_table:
        truth_table["c"].reverse()
    return truth_table

def SDNF(truth_table, unique_letters):
    sdnf = []
    for i in range(0, len(truth_table["result"])):
        if truth_table["result"][i] == 1:

            for index in range(0, len(unique_letters)):
                if truth_table[unique_letters[index]][i] == 0:
                    sdnf.append("!"+ unique_letters[index])
                else:
                    sdnf.append(unique_letters[index])
                if index != len(unique_letters)-1:
                    sdnf.append("*")
            sdnf.append("+")
    return sdnf


def SindexNF(truth_table,unique_letters):
    sindexnf = []
    for i in range(0, len(truth_table["result"])):
        if truth_table["result"][i] == 0:

            for index in range(0, len(unique_letters)):
                if truth_table[unique_letters[index]][i] == 1:
                    sindexnf.append("!"+ unique_letters[index])
                else:
                    sindexnf.append(unique_letters[index])
                if index != len(unique_letters)-1:
                    sindexnf.append("+")  
            sindexnf.append("*")
    return sindexnf

def main():
    line = input("Введите формулу: ")
    sdnf, sindexnf, opening_bracets,sub_formule_list= [],[],[],[]
    truth_table = {}
    unique_letters = re.findall(r'(?i)(\b\w)(?!.*\b\1\b)', line)
    truth_table = create_arguments(unique_letters)

    for i in range(0,len(line)):
        if line[i] == '(':
            opening_bracets.append(i)
  
    truth_table, sub_formule = create_result_truth_table(truth_table, line, opening_bracets,sub_formule_list)
   
    truth_table["result"] = truth_table.pop(sub_formule)

    truth_table = reverse_truth_table(truth_table)
    print("Результат: ", truth_table["result"])

    index_formula(truth_table)
    number_formula(truth_table)

    sdnf = SDNF(truth_table,unique_letters)
    sindexnf = SindexNF(truth_table,unique_letters)

    sdnf = ''.join(sdnf[0:len(sdnf)-1])    
    sindexnf = ''.join(sindexnf[0:len(sindexnf)-1])   
    print("СДНФ: ", sdnf)
    print("СКНФ", sindexnf)
