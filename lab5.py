truth_table = {'q3*':[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1,1],'q2*':[0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],'q1*':[0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1], 'V': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0 ,1]}
PLUS ="+"
STAR = "*"
pattern1 = r"\+"
pattern2 = r"\*"
import re
def current_q(truth_table):
    truth_table_args = 3
    q = [[0 for m in range(len(truth_table['q1*']))] for n in range(truth_table_args)]
    for i in range(len(truth_table['q1*'])):
        V = [0 for j in range(truth_table_args-1)]+[truth_table['V'][i]]
        index = truth_table_args
        plusone = 0
        for j in range(0,truth_table_args):
            sum = truth_table['q'+str(j+1)+'*'][i] + V[j-1] + plusone
            plusone = 0
            if sum >= 2:
                sum -= 2
                plusone = 1
            q[index-1][i] = sum
            index-=1
    index = truth_table_args
    for i in range(0,len(q)):
        truth_table['q'+ str(index)] = q[i]
        index -=1

    return truth_table
def transition_table(truth_table):
    arguments_number = 3
    V_index = 3
    truth_table = current_q(truth_table)
    table = list(truth_table.values())
    index = 3
    h = [[0 for m in range(len(truth_table['q1']))] for n in range(arguments_number)]
    for i in range(len(h)):
        for j in range(len(h[i])):
            if table[i][j] != table[i+V_index+1][j]:
                h[i][j] = 1
    for i in range(0,index):
        truth_table['h'+str(index)] = h[i]
        index-=1
    return truth_table
def SDNF(truth_table, unique_letters,args,letter):
    sdnf = []
    for i in range(0, len(truth_table[letter])):
        if truth_table[letter][i] == 1:

            for index in range(0, len(unique_letters)):
                if truth_table[unique_letters[index]][i] == 0:
                    sdnf.append("!"+ args[index])
                else:
                    sdnf.append(args[index])
                if index != len(unique_letters)-1:
                    sdnf.append("*")
            sdnf.append("+")
    return sdnf

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

def SDNF_truth_table(plus,truth_table,keys,arguments):
    sdnf_truth_table = []

    for j in range(0,len(plus)):
        args = []
        if plus[j] == 1:
            for index in range(0,len(arguments)):
                args.append(truth_table[arguments[index]][j])
            sdnf_truth_table.append(args)
    return sdnf_truth_table

table = transition_table(truth_table)
[print(key,':',value) for key, value in truth_table.items()]
print('\n')
keys = list(table.keys())
for i in range(4,len(keys)):
    sdnf = SDNF(table,['q3*','q2*','q1*','V'],['q3','q2','q1','V'],keys[i])
   
    sdnf = ''.join(sdnf[0:len(sdnf)-1]) 
   
    print("СДНФ for", keys[i], sdnf)
    sdnf_truth_table = SDNF_truth_table(table[keys[i]],table,keys[i],['q3*','q2*','q1*','V'])
    tdnf = TDNF(total_gluing(sdnf_truth_table,4),['q3','q2','q1','V'])
    print("СДНФ for", keys[i], tdnf,'\n')

