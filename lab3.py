import re
import lab2 as truthTable
from collections import OrderedDict
import pandas as pd
pattern1 = r"\+"
pattern2 = r"\*"
STAR = "*"
PLUS = "+"
REPLACE_NEGATION = "N"

def gluing(sub_formules,sign1,sign2,pattern):
    sDNF,result_sDNF =[], []
    for i in range(0,len(sub_formules)):
        sub_formules[i] = re.split(pattern,sub_formules[i])
    for i in range(0,len(sub_formules)-1):
         
        for j in range(i+1,len(sub_formules)):
            common = set(sub_formules[i]).intersection(sub_formules[j])
            if len(common) > 1:
                
                common = sign1.join(common)
                sDNF.append(common)
    result_sDNF = sign2.join(sDNF)                       
    return result_sDNF, sDNF


def create_result_truth_table(unique_letters, sub_formula):
    arguments_values = truthTable.create_arguments(unique_letters)
    for i in range(0,len(sub_formula)):
        if sub_formula[i] == "!":
            arguments_values[REPLACE_NEGATION] = truthTable.negation(arguments_values[sub_formula[i+1]])
            sub_formula = sub_formula.replace(sub_formula[i:i+2],REPLACE_NEGATION)
        
        if  sub_formula[i] == "*" and \
            sub_formula[i+1] == "!":
            sub_formula = sub_formula.replace(sub_formula[i+1:i+2],"O")
            arguments_values["O"] =truthTable.negation(arguments_values[sub_formula[i+2]])
            arguments_values["result"] = truthTable.implication(arguments_values[sub_formula[i-1]], arguments_values["O"])
            break
        if sub_formula[i] == "*":
            arguments_values["result"] =truthTable.implication(arguments_values[sub_formula[i-1]], arguments_values[sub_formula[i+1]])
            break
        
        if  sub_formula[i] == "+" and \
            sub_formula[i+1] == "!":
            sub_formula = sub_formula.replace(sub_formula[i+1:i+2],"O")
            arguments_values["O"] =truthTable.negation(arguments_values[sub_formula[i+2]])
            arguments_values["result"] =truthTable.disunction(arguments_values[sub_formula[i-1]], arguments_values["O"])
            break
        if sub_formula[i] == "+":
            arguments_values["result"] =truthTable.disunction(arguments_values[sub_formula[i-1]], arguments_values[sub_formula[i+1]])
            break
    return arguments_values

def checking_unnecessary_implicants_for_SDNF(sign, sub_formule, sign1, sign2,pattern, number):
    result_sDNF, sDNFs = gluing(sub_formule, sign1, sign2, pattern)
    res_sDNF = []
    for i in range(0,len(sDNFs)):
        unique_letters1 = re.findall(r'(?i)(\b\w)(?!.*\b\1\b)', sDNFs[i])
        truth_table = create_result_truth_table(unique_letters1, sDNFs[i])
        index = truth_table["result"].index(number)
        sDNFs1 = []
        for k in range(0, len(sDNFs)):
            sDNFs1.append(sDNFs[k])
        sDNFs1.pop(i)
        for j in range(0,len(sDNFs1)):
            for p in range(0, len(sDNFs1[j])):
                if p >= len(sDNFs1[j]):
                    break    
                if sDNFs1[j][p] in unique_letters1:
                    if sDNFs1[j][p-1] == "!":
                        sDNFs1[j] = sDNFs1[j][:p-1] +sDNFs1[j][p:]
                        sDNFs1[j] = sDNFs1[j].replace(sDNFs1[j][p-1], str(int(not truth_table[sDNFs1[j][p-1]][index])))
                    else:
                        sDNFs1[j] = sDNFs1[j].replace(sDNFs1[j][p], str(truth_table[sDNFs1[j][p]][index]))
        sDNFs1[:] = list(OrderedDict.fromkeys(sDNFs1))        
        if sign == "+":
            sDNFs1 = '+'.join(sDNFs1)
        else:
            sDNFs1 = '*'.join(sDNFs1)
        res_sDNF.append(sDNFs1)
    return sDNFs, res_sDNF

def create_TDNF(formule,sdnf):

    sDNFs, res_sDNF = checking_unnecessary_implicants_for_SDNF("+",formule,STAR,PLUS,pattern2,1)
    result = []
    if "+" not in sdnf:
        return sdnf
    if res_sDNF == []:
        print("No TDNF")
        return res_sDNF
    for i in range(0,len(res_sDNF)):
        sDNF1 = re.split(pattern1,res_sDNF[i])
        res_sDNF = change_unnecessary_implicants_for_SDNF(sDNF1,res_sDNF,i,"1","0")
        letter1 = re.findall(r'[a-zA-Z]', res_sDNF[i])
        j=0

        result = create_result(res_sDNF,i,j,letter1,sDNFs,result,"1","0","+")
       
    result[:] = list(OrderedDict.fromkeys(result))       
    result = '+'.join(result)
    return result


def change_unnecessary_implicants_for_SDNF(s_NF1, res_s_NF,i,num1,num2):
    for index in range(0,len(s_NF1)):
        letter = re.findall(r'[a-zA-Z]', s_NF1[index])
        if num1 in s_NF1[index] and \
            num2 in s_NF1[index]:
            res_s_NF[i] = res_s_NF[i].replace(s_NF1[index],num2)
            continue
        
        if num1 in s_NF1[index]:
            if letter[0] not in s_NF1[index]:
                res_s_NF[i] = res_s_NF[i].replace(s_NF1[index],num1)
                continue
            if "!" in s_NF1[index]:
                res_s_NF[i] = res_s_NF[i].replace(s_NF1[index],"!" +letter[0])
            else:
                res_s_NF[i] = res_s_NF[i].replace(s_NF1[index],letter[0])
            
            
        if num2 in s_NF1[index]: 
            res_s_NF[i] = res_s_NF[i].replace(s_NF1[index],num2)
    return res_s_NF

def two_letters(res_s_NF,letter1,i,j,num1,sign):
    j=0
    while j < len(res_s_NF[i]):
            
        if res_s_NF[i][j] == sign:
            if res_s_NF[i][j-1] == letter1[0] and \
                res_s_NF[i][j+1:j+3] == "!" +letter1[0]:
                res_s_NF[i] = res_s_NF[i].replace(res_s_NF[i][j-1:j+3],num1)
                j=0
                continue
            if res_s_NF[i][j-2:j] == "!" + letter1[0] and \
                res_s_NF[i][j+1] == letter1[0]:
                res_s_NF[i] = res_s_NF[i].replace(res_s_NF[i][j-2:j+2],num1)
                j=0
                continue
            if res_s_NF[i][j-1] == letter1[0] and \
                res_s_NF[i][j+1] == letter1[0]:
                res_s_NF[i] = res_s_NF[i].replace(res_s_NF[i][j-1:j+2],letter1[0])
                j=0
                continue
            if res_s_NF[i][j-2] == "!" + letter1[0] and \
                res_s_NF[i][j+2] == "!" + letter1[0]:
                res_s_NF[i] = res_s_NF[i].replace(res_s_NF[i][j-2:j+3],letter1[0])
                j=0
                continue
        j+=1
    j=0
    return res_s_NF,j

def different_numbers(res_s_NF,letter1,i,j,num1,num2,sign):
    while j < len(res_s_NF[i]):
            
        if res_s_NF[i][j] == sign:
            if res_s_NF[i][j-1] == num2 and \
                res_s_NF[i][j+1] == num1:
                res_s_NF[i] = res_s_NF[i].replace(res_s_NF[i][j-1:j+2],num1)
                j=0
                continue
            if res_s_NF[i][j-1] == num1 and \
                res_s_NF[i][j+1] == num2:
                res_s_NF[i] = res_s_NF[i].replace(res_s_NF[i][j-1:j+2],num1)
                j=0
                continue
            if res_s_NF[i][j-1] == num1 and \
                res_s_NF[i][j+1] == num1:
                res_s_NF[i] = res_s_NF[i].replace(res_s_NF[i][j-1:j+2],num1)
                j=0
                continue
               
            if res_s_NF[i][j-1] == num2 and \
                res_s_NF[i][j+1] == num2:
                res_s_NF[i] = res_s_NF[i].replace(res_s_NF[i][j-1:j+2],num2)
                j=0
                continue  
        j+=1
    j=0
        
    return res_s_NF,j

def letter_and_num(res_s_NF,letter1,i,j,num1,num2,sign):
    while j < len(res_s_NF[i]):
        if "!" in res_s_NF[i]:
            break    
        if res_s_NF[i][j] == sign:
            if res_s_NF[i][j-1] == letter1[0] and \
                res_s_NF[i][j+1] == num2:
                res_s_NF[i] = res_s_NF[i].replace(res_s_NF[i][j-1:j+2],letter1[0])
                j=0
                continue
            if  res_s_NF[i][j-1] == num2 and \
            res_s_NF[i][j+1] == letter1[0]:
                res_s_NF[i] = res_s_NF[i].replace(res_s_NF[i][j-1:j+2],letter1[0])
                j=0
                continue
            if  res_s_NF[i][j-1] == letter1[0] and \
            res_s_NF[i][j+1] == num1:
                res_s_NF[i] = res_s_NF[i].replace(res_s_NF[i][j-1:j+2],num1)
                j=0
                continue
            if  res_s_NF[i][j-1] == num1 and \
            res_s_NF[i][j+1] == letter1[0]:
                res_s_NF[i] = res_s_NF[i].replace(res_s_NF[i][j-1:j+2],num1)
                j=0
                continue
        j+=1
    j=0
    return res_s_NF,j

def not_letter_and_num(res_s_NF,letter1,i,j,num1,num2,sign):
    while j < len(res_s_NF[i]):
            
        if res_s_NF[i][j] == sign:
            if  res_s_NF[i][j-2:j] == "!" + letter1[0] and \
                res_s_NF[i][j+1] == num2:
                    res_s_NF[i] = res_s_NF[i].replace(res_s_NF[i][j-2:j+2],"!"+letter1[0])
                    j=0
                    continue
            if  res_s_NF[i][j-1] == num2 and \
                res_s_NF[i][j+1:j+3] == "!" + letter1[0]:
                    res_s_NF[i] = res_s_NF[i].replace(res_s_NF[i][j-1:j+3],"!" +letter1[0])
                    j=0
                    continue
            if  res_s_NF[i][j-2:j] == "!" + letter1[0] and \
                res_s_NF[i][j+1] == num1:
                    res_s_NF[i] = res_s_NF[i].replace(res_s_NF[i][j-2:j+2],num1)
                    j=0
                    continue
            if  res_s_NF[i][j-1] == num1 and \
                res_s_NF[i][j+1:j+3] == "!" + letter1[0]:
                    res_s_NF[i] = res_s_NF[i].replace(res_s_NF[i][j-1:j+3],num1)
                    j=0
                    continue
        j+=1
    
    return res_s_NF,j  

def res(res_s_NF,letter1,s_NFs,j,i,result):
    
    while j <= len(res_s_NF[i]):
        
            if letter1[0] in res_s_NF[i]:
                result.append(s_NFs[i])
        
            break  
    return result

def create_result(res_s_NF,i,j,letter1,s_NFs,result,num1,num2,sign):
    while len(res_s_NF[i]) > 2:
        res_s_NF,j = two_letters(res_s_NF,letter1,i,j,num1,sign)
        res_s_NF,j = different_numbers(res_s_NF,letter1,i,j,num1,num2,sign)
        res_s_NF,j= letter_and_num(res_s_NF,letter1,i,j,num1,num2,sign)
    
        res_s_NF,j=not_letter_and_num(res_s_NF,letter1,i,j,num1,num2,sign)
        
    result = res(res_s_NF,letter1,s_NFs,j,i,result)
    return result
            

def create_TCNF(formule,scnf):
    sCNFs, res_sCNF = checking_unnecessary_implicants_for_SDNF("*",formule,PLUS,STAR,pattern1,0)
    result = []
    if "*" not in scnf:
        return scnf
    if len(sCNFs) <=1:
        return sCNFs[0]
    if res_sCNF == []:
        print("No TCNF")
        return res_sCNF
    for i in range(0,len(res_sCNF)):
        plus = res_sCNF[i].index("+")
        sCNF1 = re.split(pattern2,res_sCNF[i])

        res_sCNF = change_unnecessary_implicants_for_SDNF(sCNF1,res_sCNF,i,"0","1") 
           
        letter1 = re.findall(r'[a-zA-Z]', res_sCNF[i])
        j=0
      
        result = create_result(res_sCNF,i,j,letter1,sCNFs,result,"0","1","*")
       
    result[:] = list(OrderedDict.fromkeys(result))       
    result = '*'.join(result)
    return result

def create_table(s_NFs,s_NFs2,pattern,parts_of_S_NF1,parts_of_S_NF2):
    for index in range(0,len(s_NFs)):
        s_NFs2.append(s_NFs[index])
        s_NFs2[index] = re.split(pattern,s_NFs2[index])

    table = []
    result = []
    for i in range(0,len(s_NFs2)):
        table = []
        for j in range(0,len(parts_of_S_NF1)):
            
            common = [sub_formule for sub_formule in s_NFs2[i] if sub_formule in parts_of_S_NF1[j]]
           
            if len(common) == len(s_NFs2[i]):
                table.append("+")
            else:
                table.append(" ")

        result.append(table)
    df = pd.DataFrame(result, columns=parts_of_S_NF2, index=s_NFs)
    print(df)
    return result

def calculation_and_tabular_method(parts_of_S_NF1,sign1, sign2,pattern):
    parts_of_S_NF2 = []
    s_NFs2 = []
    result = []
    i=0

    for index in range(0,len(parts_of_S_NF1)):
        parts_of_S_NF2.append(parts_of_S_NF1[index])
    result_sDNF, s_NFs = gluing(parts_of_S_NF1, sign1, sign2, pattern)
    s_NFs[:] = list(OrderedDict.fromkeys(s_NFs))
    table = create_table(s_NFs,s_NFs2,pattern,parts_of_S_NF1,parts_of_S_NF2)
    while i < len(table):
        count = 0
        pluses = table[i]
        table.pop(i)
        for j in range(0,len(table[0])):
            for index in range(0,len(table)):
                if table[index][j] == "+":
                    count +=1
                    break
            
        if count < len(table[0]):
            result.append(s_NFs[i])
            table.insert(i,pluses)
            i+=1
        else:
            s_NFs.pop(i)
    s_NFs = sign2.join(result)
    if s_NFs == '' and \
        sign2 == PLUS:
        print("No TDNF")
    if s_NFs == '' and \
        sign2 == STAR:
        print("No TCNF")  
    else:  
        print(s_NFs)

def cheack_first_arg(res1,res2,unique_letters,num1,num2,sign1,s_NF_res):
   
    s_NF = []
    if res1[0] ==  num2:
        s_NF.append(unique_letters[0])
    if res1[0] == num1:
        s_NF.append("!"+unique_letters[0])
    for i in range(0,len(res1[1])):
        if res1[1][i]==res2[1][i]:
            if res1[1][i] == num2:
                s_NF.append(unique_letters[i+1])
            if res1[1][i] == num1:
                s_NF.append("!"+unique_letters[i+1])
    s_NF_res.append(sign1.join(s_NF))
    s_NF.clear()      
    return s_NF_res

def cheack_other_args(res1,res2,unique_letters,num1,num2,sign1,s_NF_res):
    s_NF = []
    
    for j in range(0,len(res1)):
        if res1[j] == num2:
            s_NF.append(unique_letters[j+1])
        else:
            s_NF.append("!"+unique_letters[j+1])
    s_NF_res.append(sign1.join(s_NF))
    s_NF.clear()
       
    return s_NF_res

def table_method(formules,sign1,sign2, unique_letters, num1,num2, sign):
    s_NF, result,args,short_NF = [],[],[],[]
    args = cheack_args(formules,unique_letters,num1,num2,result,args)
    count = 1
    i=0
    while i < len(args):
        j=0
        if len(args) == 1:
            short_NF = sign2.join(short_NF)
            print(short_NF)
            return short_NF
        if args[i][j] == args[i+count][j] and \
            args[i][j+1] != args[i+count][j+1]:
            s_NF = cheack_first_arg(args[i],args[i+count],unique_letters,num1,num2,sign1,short_NF)
            args,i,count,short_NF = func(args,i,count,short_NF)
            continue
        if args[i][j] != args[i+count][j] and \
            args[i][j+1] == args[i+count][j+1]:
            s_NF = cheack_other_args(args[i][j+1],args[i+count][j+1],unique_letters,num1,num2,sign1,short_NF)
            args,i,count,short_NF = func(args,i,count,short_NF)
            continue
        count+=1
        if count == len(args):
            i+=1
            count = 1
    short_NF = sign2.join(short_NF)
    print(short_NF)

def func(args,i,count,short_NF):
    args.pop(i)
    count-=1
    args.pop(i+count)
    i=0
    count=1
    return args,i,count,short_NF

def compare_args(formules,unique_letters,num1,num2,result,args):
    for i in range(0,len(formules)):
        table = []
        for index in range(0,len(formules[i])):
            if "!"+unique_letters[index] in formules[i]:
                table.append(num1)
            else:
                table.append(num2)
        result.append(table)
    for i in range(0,len(result)):
        res_sub = []
        res = []
        for j in range(0,len(result[i])):
            if j == 0:    
                res.append(result[i][0])
            if j != 0:
                res_sub.append(result[i][j])    
        res_sub = ''.join(res_sub)
        res.append(res_sub)
        args.append(res) 
    return args
def cheack_args(formules,unique_letters,num1,num2,result,args):
    result1 =[]
    table = []
   
    args =   compare_args(formules,unique_letters,num1,num2,result,args)
    row = ["0","1"]
    column=["00","01","11","10"]
    result2=[]
    count =0
    table = [[["0","00"],["0","01"],["0","11"],["0","10"]],[["1","00"],["1","01"],["1","11"],["1","10"]]]
    for i in range(0,len(table)):
        result1 = []

        for j in range(0,len(table[i])):
            if table[i][j] in args:
                result1.append(num2)
            else:
                result1.append("")
           
        result2.append(result1)
    
    df1 = pd.DataFrame(result2, columns=column, index=row)   
    print(df1)
    print(args)
    return args

def all_methods(formules,sub_formules1,sub_formules2,sdnf,scnf,unique_letters):
    for i in range(0,len(sub_formules1)):
        formules.append(sub_formules1[i])
    tdnf = calculation_and_tabular_method(formules,STAR,PLUS,pattern2)    
    formules = []
    for i in range(0,len(sub_formules2)):
        formules.append(sub_formules2[i])
    tcnf = calculation_and_tabular_method(formules,PLUS,STAR,pattern1)
    tdnf = create_TDNF(sub_formules1, sdnf)
    tcnf = create_TCNF(sub_formules2, scnf)
    print("Расчётный метод: ", tdnf)
    print("Расчётный метод: ", tcnf)
    formules = []
    for i in range(0,len(sub_formules1)):
        formules.append(sub_formules1[i])
    table_method(formules,STAR,PLUS,unique_letters,"0","1",PLUS)
    formules = []
    for i in range(0,len(sub_formules2)):
        formules.append(sub_formules2[i])
    table_method(formules,PLUS,STAR,unique_letters,"1","0",STAR)

def main():
    formules = []
    line = input("Введите формулу: ")
    sdnf, sindexnf, opening_bracets,sub_formule_list= [],[],[],[]
    truth_table = {}
    unique_letters = re.findall(r'[a-zA-Z]', line)
    unique_letters[:] = list(OrderedDict.fromkeys(unique_letters))       
    truth_table = truthTable.create_arguments(unique_letters)
    for i in range(0,len(line)):
         if line[i] == '(':
             opening_bracets.append(i)
    truth_table, sub_formule =truthTable.create_result_truth_table(truth_table, line, opening_bracets,sub_formule_list)
    truth_table["result"] = truth_table.pop(sub_formule)
    truth_table =truthTable.reverse_truth_table(truth_table)
    sdnf =truthTable.SDNF(truth_table,unique_letters)
    scnf = truthTable.SindexNF(truth_table,unique_letters)
    sdnf1 = ''.join(sdnf[0:len(sdnf)-1])    
    scnf1 = ''.join(scnf[0:len(scnf)-1])   
    print(sdnf1)
    print(scnf1) 
    sub_formules1 = re.split(pattern1, sdnf1)
    sub_formules2 = re.split(pattern2, scnf1)
    all_methods(formules,sub_formules1,sub_formules2,sdnf,scnf,unique_letters)

main()