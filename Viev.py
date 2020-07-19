import PySimpleGUI as sg
import re
import Main
import os
from os import path
import numpy as np

def write_file(fname, data, aname):
    full_name = path.basename(fname)
    name = path.splitext(full_name)[0]
    if aname == 'Шифрование':
        f = open(name + '_encrypted.txt', 'w')
        [f.write(str(x)+' ') for x in data]
        f.close()
    if aname == 'Дешифровка':
        f = open(name + '_decrypted.txt', 'w')
        #data = [(str(x)).encode(encoding= 'cp1251') for x in data]
        [f.write(chr(x)) for x in data]
        f.close()

layout_key = [
    [sg.Text('Ввод:'), sg.InputText()],
    [sg.Text('Ввод числа t:'), sg.InputText()],
            [sg.Button('Ok'), sg.Button('Cancel')]
]

def hash(fname, algo):
    hash = []
    tmp = []
    A, B, t = Main.make_close_key_and_components()
    if algo == 'Шифрование':
        with open(fname) as file_input: #opening the file one line at a time for memory considerations
            for line in file_input:
                tmp = list(line)
                hash += tmp
                #print(hash)
                #tmp = [int(x, base=10) for x in tmp]
        hash = Main.make_sequence(hash)
        hash = Main.find_vector_c(hash, B)
        #print(hash)
        write_file(fname, hash, algo)
        print('Пожалуйста, запомните свой открытый ключ, если хотите в будущем расщифровать сообщение: ' + '\n' + str(A) + '\n' +
              "А так же не забудте это число" + '\n' + str(t))
    if algo == 'Дешифровка':
        with open(fname) as file_input: #opening the file one line at a time for memory considerations
            for line in file_input:
                tmp = line.split()
                tmp = [int(x) for x in tmp]
                print(tmp)
                window = sg.Window('Введите ваш открытый ключ', layout_key)
                while True:
                    event, values = window.read()
                    if event in (None, 'Ok'):
                        break
                    if event in (None, 'Cancel'):  # if user closes window or clicks cancel
                        break
                key = values[0].split()
                t = int(values[1])
                key = [int(x) for x in key]
            m = Main.summ_vector(key)
            while Main.gcd(m, t) != 1:
                m += 1
            x = Main.find_inverse_number(t, m)
            vector_v = Main.find_vector_v(tmp, m, x)
            hash = Main.find_the_decrypted_message(vector_v, key)
            write_file(fname, hash, algo)
    return hash

layout = [
    [sg.Text('Input File'), sg.InputText(), sg.FileBrowse(),
     sg.Radio('Шифрование', "RADIO1"), sg.Radio('Дешифровка', "RADIO1")],
    [sg.Output(size=(88, 20))],
    [sg.Submit(), sg.Cancel()]
]
window = sg.Window('Task of crypto', layout)
while True:                             # The Event Loop
    event, values = window.read()
    # print(event, values) #debug
    if event in (None, 'Exit', 'Cancel'):
        break
    if event == 'Submit':
        file1 = isitago = None
        # print(values[0],values[3])
        if values[0]:
            file1 = re.findall('.+:\/.+\.+.', values[0])
            isitago = 1
            if not file1 and file1 is not None:
                print('Error: File 1 path not valid.')
                isitago = 0
            elif isitago == 1:
                print('Info: Filepaths correctly defined.')
                algos = [] #algos to compare
                if values[1] == True: algos.append('Шифрование')
                if values[2] == True: algos.append('Дешифровка')
                filepaths = [] #files
                filepaths.append(values[0])
                print('Info: File Comparison using:', algos)
                for algo in algos:
                    print(algo, ':')
                    print(filepaths[0], ':', hash(filepaths[0], algo))
        else:
            print('Please choose your files.')
window.close()