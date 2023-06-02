import math
ZERO = 0
ONE = 1
ONE_HUNDRED_TWENTY_SEVEN = 127
EIGHT = 8
TWO = 2
SEVEN = 7
NINE = 9
def main():
    number1 = input("Введите первое  число: ")
    number2 = input("Введите второе  число: ")
    origenNumber1 = number1
    origenNumber2 = number2
    
    comand = input("""Введите команду: 
Перевод(~)
Сложение(+)
Вычитание(-)
Умножение(*)
Деление(/)
Сложение с плавающей точкой(,)\n""")

    while comand:
       
        if comand == "~":
            comand1 = input("""Выберите способ: 
Прямой код
Дополнительный код
Обратный код\n""")
            
            if comand1 == "Прямой код":    
                print(*DCode(int(origenNumber1), abs(int(number1))), '\n', *DCode(int(origenNumber2), abs(int(number2))), sep='')
            
            if comand1 == "Обратный код":
               print(*RevCode(int(origenNumber1), abs(int(number1))), '\n', *RevCode(int(origenNumber2), abs(int(number2))), sep='')
            if comand1 == "Дополнительный код":
                print(*AddCode(int(origenNumber1), abs(int(number1))), '\n', *AddCode(int(origenNumber2), abs(int(number2))), sep='')
        if comand == "+":
           
                num1 = AddCode(int(origenNumber1), abs(int(number1))) 
                num2 = AddCode(int(origenNumber2), abs(int(number2))) 
                print(*summa(num1, num2, 8,"summa"), sep='')
                print(convert_from_two_to_ten_system_for_AddCode_code(summa(num1, num2, 8,"summa")))
           
        if comand == "-":
           
                print( minus(int(origenNumber1), int(origenNumber2), abs(int(number1)), abs(int(number2))), sep='') 
                print(convert_from_two_to_ten_system_for_AddCode_code (minus(int(origenNumber1), int(origenNumber2), abs(int(number1)), abs(int(number2)))))
            
        if comand == "*":
            print(*increase(abs(int(number1)), abs(int(number2)), int(origenNumber1), int(origenNumber2)), sep='')
            print(convert_from_two_to_ten_system(increase(abs(int(number1)), abs(int(number2)), int(origenNumber1), int(origenNumber2))))
        if comand == "/":
            print(*fraction(int(origenNumber1), int(origenNumber2)), sep = '')  
        if comand == ",":
            print(*addtion_numbers_with_floating_point(abs(float(number1)), abs(float(number2))), sep='')
        comand = input("""\nВведите команду: 
Перевод(~)
Сложение(+)
Вычитание(-)
Умножение(*)
Деление(/)
Сложение с плавающей точкой(,)\n""")

def equivalence_and_convert(orNum, num):
    convertNumber = []
    if (orNum > 0):
        convertNumber = convertCode(num)
    if (orNum < 0):
        convertNumber = convertCode(num)
    return convertNumber

def DCode(orNum, num):
    convertNumber = equivalence_and_convert(orNum, num)
    if (orNum < 0):
        convertNumber[0] = 1
    return  convertNumber    

def RevCode(orNum, num):
    convertNumber = equivalence_and_convert(orNum,num)
    if (orNum < 0):
        convertNumber = invertion(convertNumber)
    return  convertNumber    

def AddCode(orNum, num):
    convertNumber = equivalence_and_convert(orNum,num)
   
   
    if orNum < 0:
        convertNumber = invertion(convertNumber)
        one = convertCode(1)
        convertNumber = summa(convertNumber, one, 8,"summa")
    return  convertNumber


def convertCode(number):
    convertNumber = []
   
    number = abs(number)
    while number > 0:
        intermidiat_value=number%2
        convertNumber.append(intermidiat_value)
        number=number//2
    i = len(convertNumber) - 1
    convertNumber1 = []
    j = 0
    while (i >= 0) and \
        (j < len(convertNumber)):
        convertNumber1.append(convertNumber[i])
        i -= 1
        j += 1
    while(len(convertNumber1)<8):
        convertNumber1.insert(0,0)
    return  convertNumber1

def invertion(num):
    for i in range(0,len(num)):
        if num[i] == 0:
            num[i] = 1
            continue
        if num[i] == 1:
            num[i] = 0
    return num


def summa(num1, num2, countNumber, Mantisa):
    result = []
    remembered_one = [" "] * countNumber
    i = len(num1)-1
    while i >= 0:
        if num1[i] == 0 and \
            num2[i] == 0:
            if(remembered_one[i] == 1):
                result.insert(0,1)
            else:
                result.insert(0,0)
            remembered_one[i-1] = " "
            i -=1
            continue
        if num1[i] == 1 and \
            num2[i] == 1:
                if remembered_one[i] == " ":     
                    result.insert(0,0)
                    remembered_one[i-1] = 1
                elif remembered_one[i] == 1:
                    result.insert(0,1)
                    if Mantisa == "Mantisa" and \
                        remembered_one[0] == 1:
                        result.insert(0,1)
                    remembered_one[i-1] = 1
                i-=1
                continue
        if num1[i] == 0 and \
            num2[i] == 1 or \
                num1[i] == 1 and \
                num2[i] == 0:
            if remembered_one[i] == 1:
                result.insert(0,0)
                if Mantisa == "Mantisa" and \
                    remembered_one[0] == 1:
                    result.insert(0,1)
                
                remembered_one[i-1] = 1
            else: 
                result.insert(0,1)
            i-=1
            continue
    return result

def minus(orNum1, orNum2, num1, num2):
    result = []
   
   
    if  orNum2 < 0 and \
        orNum1 > 0 or \
            orNum1 < 0 and \
            orNum2 < 0:
        result = summa(AddCode(orNum1, num1), AddCode(num2, num2),8,"sum")
    if orNum1 < 0 and \
        orNum2 > 0 or \
            orNum1 > 0 and \
            orNum2 > 0:
        
        result = summa(AddCode(orNum1, num1), AddCode(-orNum2, num2),8,"sum")

    return result   


def increase(num1, num2, orNum1, orNum2):
   
    res1 = []
    res2 = []
    countNumber = 9
    bias = 1
    num1 = DCode(num1,num1)
    num2 = DCode(num2,num2)
    i = len(num1)-1
    while i >= 0:
        if num2[i] == 1:
            res1 = num1
            
        if num2[i] == 0:
            res1 = [0] * 8
       
        if i == len(num1)-1:
            res2 = res1
            i-=1
            continue
        else:
           
            res2 = [0] + res2 
            Zeros = [0] * bias 
            res1 = res1 + Zeros
            res1 = summa(res2, res1, countNumber,"summa")
            
            res2 = res1
        i-=1
        bias+=1
        countNumber += 1
    if orNum1 < 0 or \
        orNum2 < 0:
        res2[0] = 1
    if orNum1 < 0 and \
        orNum2 < 0:
        res2[0] = 0 
    return res2


def convert_from_two_to_ten_system(num):
    result = 0
    if num[0] == 1:
        j = len(num)-2
        for i in range(1,len(num)):
            result = result + num[i] * 2**j
            j-=1
        return -result
    else:
        j = len(num)-1
        for i in range(0,len(num)):
            result = result + num[i] * 2**j
            j-=1
        return result

def convert_from_two_to_ten_system_for_AddCode_code(num1):
    if num1[0] == 1:
        num = num1[1:]
        one = AddCode(-1, 1)
        one = one[1:]
        number1 = summa(num, one, 7,"summa")
        number1 = invertion(number1)
        number1.insert(0,num1[0])
        return convert_from_two_to_ten_system(number1)
    else:
        return convert_from_two_to_ten_system(num1)

def convertion(num):
    convertNumber = []
    if num == 0:
        convertNumber.append(num)
        return  convertNumber
    
    num = abs(num)
    while num > 0:
        intermidiat_value=num%2
        convertNumber.append(intermidiat_value)
        num=num//2
    i = len(convertNumber) - 1
    convertNumber1 = []
    j = 0
    while (i >= 0) and \
        (j < len(convertNumber)):
        convertNumber1.append(convertNumber[i])
        i -= 1
        j += 1
    return  convertNumber1


def convert_from_binary_system_for_division(num):
    res = 0
    j = len(num)-1
    for i in range(0,len(num)):
        res = res + num[i] * 2**j
        j-=1
    return res

def maximum_part_of_fractionable(num1, num2, result):
    for i in range(0,len(num1)):
        result1 = convert_from_binary_system_for_division(num1[0:i+1])
       
        if result1 >= abs(num2):
            result.append(1)
            result2 = minus(result1, abs(num2), result1, abs(num2))
            j = i+1
            if i != len(num1) -1:
                result2.insert(len(result2), num1[i+1])
            try:
                index = result2.index(1)
                result2 = result2[index:]
            except ValueError:
                break    
                
            if i == len(num1) - 1:
                break
            break 
    return result, result2, j

def formation_whole_part(res,num1,j,num2,result):
    for i in range(j,len(num1)):
        
        num = convert_from_binary_system_for_division(result)
        if num >= abs(num2):
            result = minus(num, abs(num2), num, abs(num2))
            res.append(1)
            
            try:
                index_of_one = result.index(1)
                result = result[index_of_one:]
            except ValueError:
                try:
                    result.insert(len(result), num1[i+1])
                except:
                    break
                continue

            try:
                result.insert(len(result), num1[i+1])
            except:
                break
        
        else:
            res.append(0)
          
            try:
                result.insert(len(result), num1[i+1])
            except IndexError:
                break
    return res, result

    

def fraction(num1,  num2):
    number1 = convertion(abs(num1))
    
    res =[]
     
    res, result, j = maximum_part_of_fractionable(number1,num2,res)
    res, result = formation_whole_part(res,number1,j,num2,result)
      
    rest=[]
    for i in range(0,5): 
        result.insert(len(result), 0)
        number = convert_from_binary_system_for_division(result)
        if number >= abs(num2):
            result = minus(number, abs(num2), number, abs(num2))
            rest.append(1)
            try:
                index = result.index(1)
                result = result[index:]
            except ValueError:
                continue
        else:
            rest.append(0)    

    res.insert(len(res), ",")
    for i in range(0, len(rest)):
        res.append(rest[i])
    if num1 < 0 and num2 > 0 or \
        num2 < 0 and num1 > 0:
        res.insert(0, "-")
        return res
    else:
        return res

def convert_float_part(num, len_num):
    fract = []
    for i in range(0,23):
        if num == 1:
            break
        fractPart = math.modf(num)
        
        num = round(fractPart[0] * 2, len_num)
        fract.append(int(math.modf(num)[1]))
     
    return fract    

def number_to_number_with_floating_point(num):
    floatNumber=[]
    number_str = str(num)
    point = number_str.index(".")
    number_str = number_str[point+1:len(number_str)]
    whole_and_fract_parts_of_number = math.modf(num)
    
    fractPart = convert_float_part(round(whole_and_fract_parts_of_number[0], len(number_str)),len(number_str))
    wholePart = convertion(int(whole_and_fract_parts_of_number[1]))
    for i in range(0,len(wholePart)):
        floatNumber.insert(i,wholePart[i])
    floatNumber.append(",")
    for i in range(0,len(fractPart)):
        floatNumber.append(fractPart[i])
    
    return floatNumber, wholePart, fractPart

def norm_number(number):
   
    floatNumber = []
    whole_and_fraction_parts_number = math.modf(number)
    floatNumber, whole_part, fraction_part = number_to_number_with_floating_point(number)
    if int(whole_and_fraction_parts_number[1]) == 0:
        point = floatNumber.index(",")
        
        floatNumber = floatNumber[point+1:len(floatNumber)]
        index_of_one  = floatNumber.index(1)
        bias = 1
        for i in range(0,index_of_one):
            floatNumber.pop(0)
            bias+=1
        floatNumber.append(",")
        if len(floatNumber) == 2:
            floatNumber.append(0)
        bias = -bias
    else:
        point = floatNumber.index(",")
        bias = point - 1
        floatNumber.pop(point)
        floatNumber.insert(1,",")
    bias = bias + 127
    return bias, floatNumber



def addtion_numbers_with_floating_point(num1, num2):
    res=[]
    mantisa=[]
    
    sequence1, floatNumber1 = norm_number(num1)
    sequence2, floatNumber2 = norm_number(num2)
   
    exp = abs (sequence2-sequence1)
    if  sequence2 >= sequence1:
        res,mantisa,order = sum(sequence1,sequence2,exp,floatNumber1,floatNumber2)
    else:
        res,mantisa,order = sum (sequence2,sequence1,exp,floatNumber2,floatNumber1)
    num = convert_float_to_ten_system(mantisa,order,num1,num2)
    res.remove(",")
    return res, num

def sum(sequence1,sequence2,exp,floatNumber1,floatNumber2):
    res=[]
    mantisa=[]
    floatNumber1.remove(",")
    floatNumber2.remove(",")
    for i in range(0,exp):
        floatNumber1.insert(0,0)
    
    if len(floatNumber2) < len(floatNumber1):
        for i in range(len(floatNumber2), len(floatNumber1)):
            floatNumber2.append(0)
    elif len(floatNumber2) > len(floatNumber1):
        for i in range(len(floatNumber1), len(floatNumber2)):
            floatNumber1.append(0)
    mantisa = summa(floatNumber2, floatNumber1,len(floatNumber2),"mantisa")
    if  len(mantisa) > len(floatNumber2):
        mantisa.insert(2,",")
        sequence2 +=1
    else:
        mantisa.insert(1,",")
    for i in range(len(mantisa), 23):
        mantisa.append(0)
    order = convertion(sequence2)
    if len(order) < 8:
        order.insert(0,0)
    res.append(0)
    for i in range(0,len(order)):
        res.append(order[i])
    for i in range(1,len(mantisa)-2):
        res.append(mantisa[i])
    return res,mantisa, sequence2

def convert_float_to_ten_system(mantisa, sequence, number1,number2):
    i=0
    num1 = str(number1)
    num2 = str(number2)
    point1= num1.index(".")
    point2=num2.index(".")
    num1 = num1[point1+1:len(num1)]
    num2 = num2[point2+1:len(num2)]
    maximumRound = max(len(num1),len(num2))
    res = round(number1+number2,maximumRound)
    res_str = str(res)
    point = res_str.index(".")
    res_str =res_str[point+1:len(res_str)]
   
    res = 0
    exponent = sequence - 127
    if exponent > 0:
        mantisa.remove(",")
        mantisa.insert(exponent+1, ",")
    elif exponent < 0:
        for i in range(0,abs(exponent)):
            mantisa.append(0)
        mantisa.remove(",")
        mantisa.insert(1, ",") 
    point = mantisa.index(",")
    mantisa1 = mantisa[0:point]
    power = len(mantisa1)-1
    for i in range(0,len(mantisa1)):
        res = res +mantisa1[i] * 2**power
        power-=1
    mantisa2 = mantisa[point+1:len(mantisa)-1]
    power2 = -1
    for i in range(0,len(mantisa2)):
        res = res +mantisa2[i] * 2**(power2)
        power2 -= 1 
    res = round(res,len(res_str))
    return res
main()

