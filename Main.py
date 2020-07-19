import numpy as np
import math
import locale
import random


def find_the_decrypted_message(V, A):
    tmp = []
    out = ''
    out_data = []
    A.reverse()
    for i in range(len(V)):
        for j in range(len(A)):
            if V[i] >= A[j]:
                tmp.append(1)
                V[i] -= A[j]
            else:
                tmp.append(0)
        tmp.reverse()
        for i in range(len(tmp)):
            out += str(tmp[i])
        out_data.append(int(out, base=2))
        tmp.clear()
        out = ''
    #print('Вектор расшифрованного сообщения в бинарной записи')
    #print(out_data)
    return out_data


def make_sequence(input):
    #input_data = list(input)
    input = [bin(ord(x))[2:].zfill(11) for x in input]
    #print('Входное сообщение в бинарной записи')
    return input


def multiply_vector(a, b):
    tmp = 0
    for i in range(len(a)):
        tmp += a[i] * b[i]
    return tmp


def find_vector_c(input_data, B):
    tmp = []
    for i in range(len(input_data)):
        tmp_data = [int(x, base=10) for x in input_data[i]]
        tmp.append(multiply_vector(tmp_data, B))
    #print('Вектор шифрованного сообщения')
    #print(tmp)
    return tmp


def find_vector_v(vector_c, m, x):
    tmp = [x * c % m for c in vector_c]
    return tmp


def gcd(a, b):
    while a != b:
        if a > b:
            a = a - b
        else:
            b = b - a
    return a


def find_inverse_number(a, b):
    x, xx, y, yy = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a % b
        x, xx = xx, x - xx * q
        y, yy = yy, y - yy * q
    return x


def random_simple_number():
    number_t = 6
    key = 0
    while key == 0:
        number_t = random.randint(2, 100)
        key = test_simple_number(number_t, key)
    return number_t


def test_simple_number(number, key):
    if number < 2:
        print("A number must be 2 and more")
    elif number == 2:
        key = 1
        return number, key

    i = 2
    limit = int(math.sqrt(number))

    while i <= limit:
        key = 1
        if number % i == 0:
            key = 0
            break
        i += 1
    return key

def summ_vector(vector):
    summ = 0
    for i in range(len(vector)):
        summ += vector[i]
    return summ

def take_random_open_key():
    tmp = []
    random_number = random.randint(1, 100)
    tmp.append(random_number)
    for i in range(10):
        while True:
            random_number = random.randint(random_number, random_number*4)
            if summ_vector(tmp) < random_number:
                tmp.append(random_number)
                break
    return tmp

def make_close_key_and_components():
    A = take_random_open_key()
    t = random_simple_number()
    m = summ_vector(A)

    while gcd(m, t) != 1:
        m += 1

    x = find_inverse_number(t, m)

    B = [(x * t % m) for x in A]
    return A, B, t

#input = 'Тестовоый набор произвольных значений'

#vector_c = find_vector_c(work_data, B)

#vector_v = find_vector_v(vector_c, m, x)

#tmp = find_the_decrypted_message(vector_v, A)
