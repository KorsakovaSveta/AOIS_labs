import math

def main():
    num = input("Введите 1-е число: ")
    num2 = input("Введите 2-е число: ")
    origNumber = num
    origNumber2 = num2
    
    cmd = input("""Введите команду: 
Перевод
Сложение
Вычитание
Умножение
Деление
Сложение с плавающей точкой
Выход\n""")

    while cmd != "Выход":
       
        if cmd == "Перевод":
            cmd1 = input("""Выберите способ: 
ПК
ДК
ОК\n""")
            
            if cmd1 == "ПК":    
                print(*directCode(int(origNumber), abs(int(num))), '\n', *directCode(int(origNumber2), abs(int(num2))), sep='')
            
            if cmd1 == "ОК":
               print(*reverseCode(int(origNumber), abs(int(num))), '\n', *reverseCode(int(origNumber2), abs(int(num2))), sep='')
            if cmd1 == "ДК":
                print(*additionalCode(int(origNumber), abs(int(num))), '\n', *additionalCode(int(origNumber2), abs(int(num2))), sep='')
        if cmd == "Сложение":
           
                number1 = additionalCode(int(origNumber), abs(int(num))) 
                number2 = additionalCode(int(origNumber2), abs(int(num2))) 
                print(*addition(number1, number2, 8,"sum"), sep='')
                print(convert_from_2_to_10_for_additional_code(addition(number1, number2, 8,"sum")))
           
        if cmd == "Вычитание":
           
                print(*subtractionForAdditionalCode(int(origNumber), int(origNumber2), abs(int(num)), abs(int(num2))), sep='') 
                print(convert_from_2_to_10_for_additional_code(subtractionForAdditionalCode(int(origNumber), int(origNumber2), abs(int(num)), abs(int(num2)))))
            
        if cmd == "Умножение":
            print(*multiplication(abs(int(num)), abs(int(num2)), int(origNumber), int(origNumber2)), sep='')
            print(convert_from_2_to_10(multiplication(abs(int(num)), abs(int(num2)), int(origNumber), int(origNumber2))))
        if cmd == "Деление":
            print(*division(int(origNumber), int(origNumber2)), sep = '')  
        if cmd == "Сложение с плавающей точкой":
            print(*sum_numbers_with_floating_point(abs(float(num)), abs(float(num2))), sep='')
        cmd = input("""\nВведите команду: 
Перевод
Сложение
Вычитание
Умножение
Деление
Сложение с плавающей точкой
Выход\n""")
        

def directCode(origNumber, num):
    arr = []
    if (origNumber > 0):
        arr = convert_for_codes(num)
    if (origNumber < 0):
        arr = convert_for_codes(num)
        arr[0] = 1
    return arr    

def reverseCode(origNumber, num):
    arr = []
    if (origNumber > 0):
        arr = convert_for_codes(num)
    if (origNumber < 0):
        arr = convert_for_codes(num)
        arr = invert(arr)
    return arr    

def additionalCode(origNumber, num):
    arr = []
    if (origNumber > 0):
        arr = convert_for_codes(num)
    if (origNumber < 0):
        arr = convert_for_codes(num)
        arr = invert(arr)
        one = convert_for_codes(1)
        arr = addition(arr, one, 8,"sum")
    return arr

def additionalCode_for_division(num):
    arr = invert(num)
    one =convert_for_codes(1)
    num = addition(arr, one, 8,"sum")
    return num

def convert_for_codes(num):
    arr = []
    origNum = num
    num = abs(num)
    while num > 0:
        intermidiat_bit_value=num%2
        arr.append(intermidiat_bit_value)
        num=num//2
    i = len(arr) - 1
    arr1 = []
    j = 0
    while (i >= 0) and \
        (j < len(arr)):
        arr1.append(arr[i])
        i -= 1
        j += 1
    while(len(arr1)<8):
        arr1.insert(0,0)
    return arr1

def invert(number):
    for i in range(0,len(number)):
        if number[i] == 0:
            number[i] = 1
            continue
        if number[i] == 1:
            number[i] = 0
    return number


def addition(number, number2, countOfcategory,mantisa):
    result = []
    transfer = [" "] * countOfcategory
    i = len(number)-1
    while i >= 0:
        if number[i] == 0 and \
            number2[i] == 0:
            if(transfer[i] == 1):
                result.insert(0,1)
            else:
                result.insert(0,0)
            transfer[i-1] = " "
            i -=1
            continue
        if number[i] == 1 and \
            number2[i] == 1:
                if transfer[i] == " ":     
                    result.insert(0,0)
                    transfer[i-1] = 1
                elif transfer[i] == 1:
                    result.insert(0,1)
                    if mantisa == "mantisa" and \
                        transfer[0] == 1:
                        result.insert(0,1)
                    transfer[i-1] = 1
                i-=1
                continue
        if number[i] == 0 and \
            number2[i] == 1 or \
                number[i] == 1 and \
                number2[i] == 0:
            if transfer[i] == 1:
                result.insert(0,0)
                if mantisa == "mantisa" and \
                    transfer[0] == 1:
                    result.insert(0,1)
                
                transfer[i-1] = 1
            else: 
                result.insert(0,1)
            i-=1
            continue
    return result

def subtractionForAdditionalCode(OrignNum1, OrignNum2, num1, num2):
    result = []
   
   
    if  OrignNum2 < 0 and \
        OrignNum1 > 0 or \
            OrignNum1 < 0 and \
            OrignNum2 < 0:
        result = addition(additionalCode(OrignNum1, num1), additionalCode(num2, num2),8,"sum")
    if OrignNum1 < 0 and \
        OrignNum2 > 0 or \
            OrignNum1 > 0 and \
            OrignNum2 > 0:
        
        result = addition(additionalCode(OrignNum1, num1), additionalCode(-OrignNum2, num2),8,"sum")

    return result   


def multiplication(num1, num2, origNumber, origNumber2):
   
    result1 = []
    result2 = []
    countOfcategory = 9
    shift = 1
    num1 = directCode(num1,num1)
    num2 = directCode(num2,num2)
    i = len(num1)-1
    while i >= 0:
        if num2[i] == 1:
            result1 = num1
            
        if num2[i] == 0:
            result1 = [0] * 8
       
        if i == len(num1)-1:
            result2 = result1
            i-=1
            continue
        else:
           
            result2 = [0] + result2 
            addZeros = [0] * shift 
            result1 = result1 + addZeros
            result1 = addition(result2, result1, countOfcategory,"sum")
            
            result2 = result1
        i-=1
        shift+=1
        countOfcategory += 1
    if origNumber < 0 or \
        origNumber2 < 0:
        result2[0] = 1
    if origNumber < 0 and \
        origNumber2 < 0:
        result2[0] = 0 
    return result2


def convert_from_2_to_10(number):
    result = 0
    if number[0] == 1:
        j = len(number)-2
        for i in range(1,len(number)):
            result = result + number[i] * 2**j
            j-=1
        return -result
    else:
        j = len(number)-1
        for i in range(0,len(number)):
            result = result + number[i] * 2**j
            j-=1
        return result

def convert_from_2_to_10_for_additional_code(num1):
    if num1[0] == 1:
        num = num1[1:]
        one = additionalCode(-1, 1)
        one = one[1:]
        number1 = addition(num, one, 7,"sum")
        number1 = invert(number1)
        number1.insert(0,num1[0])
        return convert_from_2_to_10(number1)
    else:
        return convert_from_2_to_10(num1)
    
def convert_from_2_to_10_for_reverse_code(num1):
   
    if num1[0] == 1:
        num = num1[1:]
        num = invert(num)
        num.insert(0,num1[0])
        return convert_from_2_to_10(num)
    else:
        return convert_from_2_to_10(num1)

def convert(num):
    arr = []
    if num == 0:
        arr.append(num)
        return arr
    origNum = num
    num = abs(num)
    while num > 0:
        c=num%2
        arr.append(c)
        num=num//2
    i = len(arr) - 1
    arr1 = []
    j = 0
    while (i >= 0) and \
        (j < len(arr)):
        arr1.append(arr[i])
        i -= 1
        j += 1
    return arr1


def convert_from_2_for_division(number):
    result = 0
    j = len(number)-1
    for i in range(0,len(number)):
        result = result + number[i] * 2**j
        j-=1
    return result

def search_max_part_of_divisible(number1, num2, res):
    for i in range(0,len(number1)):
        result1 = convert_from_2_for_division(number1[0:i+1])
       
        if result1 >= abs(num2):
            res.append(1)
            result = subtractionForAdditionalCode(result1, abs(num2), result1, abs(num2))
            j = i+1
            if i != len(number1) -1:
                result.insert(len(result), number1[i+1])
            try:
                index = result.index(1)
                result = result[index:]
            except ValueError:
                break    
                
            if i == len(number1) - 1:
                break
            break 
    return res, result, j

def formation_whole_part_of_private(res,number1,j,num2,result):
    for i in range(j,len(number1)):
        
        number = convert_from_2_for_division(result)
        if number >= abs(num2):
            result = subtractionForAdditionalCode(number, abs(num2), number, abs(num2))
            res.append(1)
            
            try:
                index1 = result.index(1)
                result = result[index1:]
            except ValueError:
                try:
                    result.insert(len(result), number1[i+1])
                except:
                    break
                continue

            try:
                result.insert(len(result), number1[i+1])
            except:
                break
        
        else:
            res.append(0)
          
            try:
                result.insert(len(result), number1[i+1])
            except IndexError:
                break
    return res, result

def check_negative_number(result,num1,num2,res):
    try:        
        index = result.index(1)
        result = result[index:]
    except ValueError:
        if num1 < 0 and num2 > 0 or \
            num2 < 0 and num1 > 0:
            res.insert(0, "-")
            return res
        else:
            return res
    return res
    

def division(num1,  num2):
    number1 = convert(abs(num1))
    
    res =[]
     
    res, result, j = search_max_part_of_divisible(number1,num2,res)
    res, result = formation_whole_part_of_private(res,number1,j,num2,result)
    res = check_negative_number(result,num1,num2,res)
  
    remain=[]
    for i in range(0,5):
        result.insert(len(result), 0)
        number = convert_from_2_for_division(result)
        if number >= abs(num2):
            result = subtractionForAdditionalCode(number, abs(num2), number, abs(num2))
            remain.append(1)
            try:
                index = result.index(1)
                result = result[index:]
            except ValueError:
                continue
        else:
            remain.append(0)    

    res.insert(len(res), ",")
    for i in range(0, len(remain)):
        res.append(remain[i])
    if num1 < 0 and num2 > 0 or \
        num2 < 0 and num1 > 0:
        res.insert(0, "-")
        return res
    else:
        return res

def convert_floating_part(num, lenght_num):
    fraction = []
    for i in range(0,23):
        if num == 1:
            break
        fraction_part = math.modf(num)
        
        num = round(fraction_part[0] * 2, lenght_num)
        fraction.append(int(math.modf(num)[1]))
    #fraction.append(0) 
    return fraction    

def convert_to_32__bit_floating_point(number, origNumber):
    mantisa = []
    result = []
    if type(number) == int:
        print("Введено целое число")
    else:
        floatNum, whole_part, fraction_part = number_to_floating_point(number)
        exp, mantisa = normalazing_number(number) 
        order = convert(exp)
        mantisa = mantisa[2:len(mantisa)]
        
        for i in range(len(mantisa), 23):
            mantisa.append(0)
        if (len(mantisa) > 23):
            mantisa = mantisa[0:23]
       
        if origNumber < 0:
            result.append(1)
        else:
            result.append(0)
        for i in range(0,len(order)):
            result.append(order[i])
        for i in range(0,23):
            result.append(mantisa[i])
   
    return result

def convert_float_to_10_system(number, mantisa, order):
    result = 0
    j = len(mantisa)-1
    for i in range(0,len(mantisa)):
        result = result + mantisa[i] * 2**j
        j-=1
    
    if number[0] == 0:
        return ((-1)**0)*(2**(order-127))*(1+(result/2**23))
    else:
        return ((-1)**1)*(2**(order-127))*(1+(result/2**23))

def number_to_floating_point(number):
    floatNum=[]
    num_str = str(number)
    dot = num_str.index(".")
    num_str = num_str[dot+1:len(num_str)]
    whole_and_fraction_parts = math.modf(number)
    
    fraction_part = convert_floating_part(round(whole_and_fraction_parts[0], len(num_str)),len(num_str))
    whole_part = convert(int(whole_and_fraction_parts[1]))
    for i in range(0,len(whole_part)):
        floatNum.insert(i,whole_part[i])
    floatNum.append(",")
    for i in range(0,len(fraction_part)):
        floatNum.append(fraction_part[i])
    
    return floatNum, whole_part, fraction_part

def normalazing_number(number):
   
    floatNum = []
    whole_and_fraction_parts_number = math.modf(number)
    floatNum, whole_part, fraction_part = number_to_floating_point(number)
    if int(whole_and_fraction_parts_number[1]) == 0:
        dot = floatNum.index(",")
        
        floatNum = floatNum[dot+1:len(floatNum)]
        index_of_one  = floatNum.index(1)
        shift = 1
        for i in range(0,index_of_one):
            floatNum.pop(0)
            shift+=1
        floatNum.append(",")
        if len(floatNum) == 2:
            floatNum.append(0)
        shift = -shift
    else:
        dot = floatNum.index(",")
        shift = dot - 1
        floatNum.pop(dot)
        floatNum.insert(1,",")
    shift = shift + 127
    return shift, floatNum



def sum_numbers_with_floating_point(number1, number2):
    result=[]
    mantisa=[]
    
    order1, floatNum1 = normalazing_number(number1)
    order2, floatNum2 = normalazing_number(number2)
   
    exp = abs(order2-order1)
    if order2 >= order1:
        result,mantisa,order = sum(order1,order2,exp,floatNum1,floatNum2)
    else:
        result,mantisa,order = sum(order2,order1,exp,floatNum2,floatNum1)
    num = convert_float_to_10(mantisa,order,number1,number2)
    result.remove(",")
    return result, num

def sum(order1,order2,exp,floatNum1,floatNum2):
    result=[]
    mantisa=[]
    floatNum1.remove(",")
    floatNum2.remove(",")
    for i in range(0,exp):
        floatNum1.insert(0,0)
    
    if len(floatNum2) < len(floatNum1):
        for i in range(len(floatNum2), len(floatNum1)):
            floatNum2.append(0)
    elif len(floatNum2) > len(floatNum1):
        for i in range(len(floatNum1), len(floatNum2)):
            floatNum1.append(0)
    mantisa = addition(floatNum2, floatNum1,len(floatNum2),"mantisa")
    if  len(mantisa) > len(floatNum2):
        mantisa.insert(2,",")
        order2 +=1
    else:
        mantisa.insert(1,",")
    for i in range(len(mantisa), 23):
        mantisa.append(0)
    order = convert(order2)
    if len(order) < 8:
        order.insert(0,0)
    result.append(0)
    for i in range(0,len(order)):
        result.append(order[i])
    for i in range(1,len(mantisa)-2):
        result.append(mantisa[i])
    return result,mantisa,order2

def convert_float_to_10(mantisa, order, number1,number2):
    i=0
    num1 = str(number1)
    num2 = str(number2)
    dot1= num1.index(".")
    dot2=num2.index(".")
    num1 = num1[dot1+1:len(num1)]
    num2 = num2[dot1+1:len(num2)]
    maxRound = max(len(num1),len(num2))
    result = round(number1+number2,maxRound)
    result_str = str(result)
    dot = result_str.index(".")
    result_str =result_str[dot+1:len(result_str)]
   
    res = 0
    exp = order - 127
    if exp > 0:
        mantisa.remove(",")
        mantisa.insert(exp+1, ",")
    elif exp < 0:
        for i in range(0,abs(exp)):
            mantisa.append(0)
        mantisa.remove(",")
        mantisa.insert(1, ",") 
    dot = mantisa.index(",")
    mantisa1 = mantisa[0:dot]
    pow1 = len(mantisa1)-1
    for i in range(0,len(mantisa1)):
        res = res +mantisa1[i] * 2**pow1
        pow1-=1
    mantisa2 = mantisa[dot+1:len(mantisa)-1]
    pow2 = -1
    for i in range(0,len(mantisa2)):
        res = res +mantisa2[i] * 2**(pow2)
        pow2 -= 1 
    res = round(res,len(result_str))
    return res
main()

