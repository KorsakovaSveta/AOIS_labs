import string
import pandas as pd
from numpy import loadtxt
from collections import Counter
def count_v(words,arr):
    v=0
    k=1
    for i in range(0,len(words)):
        if words[i] == '':
            arr.append('-')
            continue
        for j in range(0,2):
            index = string.ascii_lowercase.index(words[i][j])
            v += index*26**k 
            k-=1
        arr.append(v)
        v=0
        k=1
    return arr

def count_hesh(arr,hesh,number,sourted_words,collisies_words,words,hesh_collisies,collisies_def,definitions,sourted_def):
    for i in range(0,len(arr)):
        if arr[i]=='-':
            hesh.append('-')
            continue
        value_hesh = arr[i]%number
        hesh.append(value_hesh)
        if sourted_words[value_hesh]!='':
            collisies_words.append(words[i])
            hesh_collisies.append(hesh[i])
            collisies_def.append(definitions[i])
        else:
            sourted_words[value_hesh]=words[i]
            sourted_def[value_hesh]=definitions[i]
    return collisies_words,hesh_collisies,collisies_def,sourted_words,sourted_def

def count_collisies(arr,hesh,words,definitions,number):
    arr = count_v(words,arr)
    index=0
    sourted_words = ['']*number
    sourted_def = ['']*number
    collisies_words,hesh_collisies = [],[]
    collisies_def = []
    collisies_words,hesh_collisies,collisies_def,sourted_words,sourted_def = count_hesh(arr,hesh,number,sourted_words,collisies_words,words,hesh_collisies,collisies_def,definitions,sourted_def)
    number_collisy = 0
    collisies = ['']*number
    for i in range(0,len(collisies_words)): 
            index_2 = index
            index = sourted_words.index('')
            sourted_words[index]=collisies_words[number_collisy]
            sourted_def[index]=collisies_def[number_collisy]
            if collisies[int(hesh_collisies[number_collisy])]=='':
                collisies[int(hesh_collisies[number_collisy])]=index
            else:
                collisies[collisies[int(hesh_collisies[number_collisy])]] = index
            number_collisy+=1
    return hesh, sourted_words, collisies,sourted_def

def count_new_hesh(count_v_of_sourted_words,number_of_letters):
    new_hesh=[]
    for i in range(0,len(count_v_of_sourted_words)):
        if count_v_of_sourted_words[i] == '-':
            new_hesh.append('-')
            continue
        value_hesh = count_v_of_sourted_words[i]%number_of_letters
        new_hesh.append(value_hesh)
        
            
    return new_hesh
def merge(sourted_words, count_v_of_sourted_words,hesh,collisies,definitions):
    table = []
    table_row = []
    for i in range(0,len(sourted_words)):
        table_row.append(sourted_words[i])
        table_row.append(count_v_of_sourted_words[i])
        table_row.append(hesh[i])
        table_row.append(collisies[i])
        table_row.append(definitions[i])
        table.append(table_row)
        table_row = []
    return table

def add(words,definitions,sourted_words, count_v_of_sourted_words,new_hesh,collisies,sourted_def):
    arr = []
    term = input('Enter new term: ')
    index = sourted_words.index('')
    sourted_words.insert(index,term)

    definition=input('Enter definitions for new term: ')
    sourted_def.insert(index, definition)
    
    count_v_of_sourted_words=[]
    hesh, count_v_of_sourted_words=[],[]
    hesh, sourted_words, collisies,sourted_def = count_collisies(arr,hesh,sourted_words,sourted_def,20)
    count_v_of_sourted_words=count_v(sourted_words,count_v_of_sourted_words)
    new_hesh = count_new_hesh(count_v_of_sourted_words,20)
    print_table(sourted_words, count_v_of_sourted_words,new_hesh,collisies,sourted_def)
    return sourted_words, count_v_of_sourted_words,new_hesh,collisies,sourted_def

def find(sourted_words,count_v_of_sourted_words,new_hesh,collisies,sourted_def):
    term = input('Enter term that you want to find: ')
    table = merge(sourted_words, count_v_of_sourted_words,new_hesh,collisies,sourted_def)
    if term in sourted_words:
        index = sourted_words.index(term)
        print(*table[index])

def delete(words,definitions,sourted_words, count_v_of_sourted_words,new_hesh,collisies,sourted_def):
    arr = []
    term = input('Enter term that you want to delete: ')
    index = words.index(term)
    words.pop(index)
    definitions.pop(index)
    index = sourted_words.index(term)
    sourted_words.pop(index)
    sourted_words.insert(index,'')
    count_v_of_sourted_words.pop(index)
    count_v_of_sourted_words.insert(index,'-')
    new_hesh.pop(index)
    new_hesh.insert(index,'-')
    collisies.pop(index)
    collisies.insert(index,'')
    sourted_def.pop(index)
    sourted_def.insert(index,'')
    count_v_of_sourted_words=[]
    hesh, count_v_of_sourted_words=[],[]
    hesh, sourted_words, collisies,sourted_def = count_collisies(arr,hesh,sourted_words,sourted_def,20)
    count_v_of_sourted_words=count_v(sourted_words,count_v_of_sourted_words)
    new_hesh = count_new_hesh(count_v_of_sourted_words,20)
    print_table(sourted_words, count_v_of_sourted_words,new_hesh,collisies,sourted_def)
    return sourted_words, count_v_of_sourted_words,new_hesh,collisies,sourted_def

def print_table(sourted_words, count_v_of_sourted_words,hesh,collisies,sourted_def):
    data = {'term':sourted_words,'V':count_v_of_sourted_words,'h(V)':hesh,'C':collisies,'definition':sourted_def}
    df = pd.DataFrame(data)   
    print(df)

def main():

    file = open('definition.txt',"r")
    arr, hesh, count_v_of_sourted_words=[],[],[]
    words = ["avangard", "garrison","barracks","laser","parade","radar","airplane","sentry","shield","saber","tent","guidance","attack","binoculars","commander","ambush","bomb","messenger","icebreaker"]
    number_of_letters = len(words)
    definitions = [definition.rstrip('\n') for definition in file]
    hesh, sourted_words, collisies,sourted_def = count_collisies(arr,hesh,words,definitions,20)
    count_v_of_sourted_words=count_v(sourted_words,count_v_of_sourted_words)
    new_hesh = count_new_hesh(count_v_of_sourted_words,20)
    print_table(sourted_words, count_v_of_sourted_words,new_hesh,collisies,sourted_def)
    comand = input("""Choose the operation: 
add - 1
find - 2
delete - 3\n""")
    while comand:
        if comand == '1':
            sourted_words, count_v_of_sourted_words,new_hesh,collisies,sourted_def = add(words,definitions,sourted_words, count_v_of_sourted_words,new_hesh,collisies,sourted_def)
        if comand == '2':
            find(sourted_words,count_v_of_sourted_words,new_hesh,collisies,sourted_def)
        if comand == '3':
            sourted_words, count_v_of_sourted_words,new_hesh,collisies,sourted_def = delete(words,definitions,sourted_words, count_v_of_sourted_words,new_hesh,collisies,sourted_def)   
        comand = input("""Choose the operation: 
        add - 1
        find - 2
        delete - 3\n""")
main()