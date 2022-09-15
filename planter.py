from pwn import * 
import sys 
import string 
import random

binary  = "./exe"
context.arch = "amd64"

rl = lambda: io.recvline()
sla = lambda a,b: io.sendlineafter(a,b)


def gen_rand_string(length):
    return "".join(random.sample((string.ascii_letters + string.digits), length))

def login(uname,pwd):
    sla(">> ","1")
    sla("name : \n",uname)
    sla("passphrase : \n",pwd)

if __name__ == "__main__":

    for _ in range(int(sys.argv[1])):

        io = process(binary)

        flag = "bi0s{" + gen_rand_string(26) + "}"
        username = gen_rand_string(20)
        print(username)

        login(username,flag)

        sla(">> ","3")
        sla(">> ","3")
        io.close()
