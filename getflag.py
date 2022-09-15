from pwn import * 
import sys 
import string 
import random

binary  = "./exe"

context.arch = "amd64"

rl = lambda: io.recvline()
sla = lambda a,b: io.sendlineafter(a,b)


def sla(io,s,i):
    io.sendlineafter(s,i)

def login(uname,pwd):
    sla(io,">> ","1")
    sla(io,"name : \n",uname)
    sla(io,"passphrase : \n",pwd)

def view(io):
    sla(io,">>","1")
    
def battle1(uname,pwd):
    login(uname,pwd)
    sla(io,">> ","2")
    sla(io,">> ","1")
    sla(io,">> ","1")
    sla(io,">> ","1")

def battle2(uname,pwd):
    login(uname,pwd)
    sla(io,">> ","2")
    sla(io,">> ","2")
    sla(io,">> ","1")
    


if __name__ == "__main__":
    
    io = process("./exe")
    ch = sys.argv[1]
    print(ch)
    if ch == '1':
        battle1("aaa","bbb")
        rl()
        if b"Won" in rl():
            print("Passed 1")
        else:
            print("fail 1")
    
    elif ch == '2':
        battle2("aaa","bbb")
        rl()
        rl()

        if b"Fainted" in rl():
            print("Passed 2")
        else:
            print("fail 2")


    
    

    
    io.interactive()