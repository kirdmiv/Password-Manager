import random
import string
import base64
import os


def generate(blet, slet, num):
    cntarr = [blet, slet, num]
    sample = [string.ascii_uppercase, string.ascii_lowercase, string.digits]
    s_size = len(sample)
    password = ""
    while cntarr[0] > 0 or cntarr[1] > 0 or cntarr[2] > 0:
        s_type = random.randint(0, s_size - 1)
        cnt = 0
        while s_type > 0 or cntarr[cnt] <= 0:
            cnt = (cnt + 1) % s_size
            if cntarr[cnt] > 0:
                s_type -= 1
        cntarr[cnt] -= 1
        symbol = random.randint(0, len(sample[cnt]) - 1)
        password += (sample[cnt][symbol])
    return password


def generate_by_len(length=16, min1=4, min2=4, min3=4):
    a = random.randint(min1, length - min2 - min3 - 1)
    b = random.randint(min1, length - a - min3 - 1)
    c = length - a - b
    return generate(a, b, c)


def addToClipBoard(text):
    command = "echo " + text.strip() + "| clip"
    os.system(command)

def get_hash(password, key):
    hash = 0
    start_key = key
    for i in range(len(password)):
        hash += ord(password[i]) * key
        key *= start_key
    return hash

def get_password(hash, key, ln):
    password = ""
    start_key = key
    for i in range(ln-1):
        key *= start_key
    for i in range(ln):
        password = chr(hash // key) + password
        hash %= key
        key //= start_key
    return password

def main():
    mode = input()
    domain = input()
    if mode == "n":
        fin = open("passwords.txt", 'a')
        pwd = generate_by_len(16)
        key = int(input("Input your hash key: "))
        epwd = get_hash(pwd, key)
        print(domain, epwd, file=fin)
        fin.close()
    else:
        fin = open("passwords.txt", 'r')
        ls = fin.readline().split()
        while len(ls) > 0 and ls[0] != domain:
            ls = fin.readline().split()
        if len(ls) <= 1:
            print("NO MATCHES")
        else:
            key = int(input("Input your hash key: "))
            ln = int(input("Password length: "))
            addToClipBoard(get_password(int(ls[1]), key, ln))
        fin.close()

def main2():
    pin = input("PIN: ")
    if pin != "i61":
        return
    domain = input()

    fin = open("passwords.txt", 'r')
    ls = fin.readline().split()

    while len(ls) > 0 and ls[0] != domain:
        ls = fin.readline().split()
    fin.close()

    if len(ls) <= 1:
        print("Creating new password...")
        fin = open("passwords.txt", 'a')
        pwd = generate_by_len(16)
        addToClipBoard(pwd)

        key = int(input("Input your hash key: "))
        epwd = get_hash(pwd, key)
        print(domain, epwd, file=fin)
        fin.close()
    else:
        key = int(input("Input your hash key: "))
        ln = int(input("Password length: "))
        addToClipBoard(get_password(int(ls[1]), key, ln))

def test():
    print(get_password(get_hash("inWfFsMc", 1234), 1234, 8))
    print(get_hash("inWfFsmc", 1000))


if __name__ == "__main__":
    main2()
