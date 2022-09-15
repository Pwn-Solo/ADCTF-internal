from concurrent import futures
import random
import string
from pwn import *
import grpc
import checker_pb2 as checker
import checker_pb2_grpc as checker_grpc

def sla(io,s,i):
    io.sendlineafter(s,i)

def login(uname,pwd):
    sla(io,">> ","1")
    sla(io,"name : \n",uname)
    sla(io,"passphrase : \n",pwd)

def view(io):
    sla(io,">> ","1")

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
    


def gen_rand_string(length):
    return "".join(random.sample((string.ascii_letters + string.digits), length))

def check_functionality(ip, port):

    try:
        io = remote(ip, port)
        io.settimeout(2)
    
    except:
        return checker.ServiceStatus.DOWN
    
    try:
        for _ in range(2):
            action = random.choice([i for i in range(1, 3)])
        
            if action == 1:
                username = gen_rand_string(20)
                pwd = gen_rand_string(20)
                battle1(username,pwd)
                io.recvline()
                if b"Won" not in io.recvline():
                    return checker.ServiceStatus.DOWN

            if action == 2:
                username = gen_rand_string(20)
                pwd = gen_rand_string(20)
                battle2(username,pwd)
                io.recvline()
                io.recvline()
                if b"Fainted" not in io.recvline():
                    return checker.ServiceStatus.DOWN

        
        return checker.ServiceStatus.UP

    except:
        return checker.ServiceStatus.DOWN

def get_flag(ip, port, flag, token):

    try:
        io = remote(ip, port)
        io.settimeout(2)
    
    except Exception as e:
        state = checker.ServiceStatus.DOWN
        print("Get flag failed: {}:{} -> {}".format(ip, port, str(e)))
        return checker.ServiceState(status = state, reason = "Failed to establish a connection")

    try:

        login(token,pwd)

        view(io)

        io.recvuntil("passwd :  ")

        newflag = io.recvline().strip("\n")
        io.close()

        if newflag == flag:

            # Remove this
            status = check_functionality(ip, port)

            if status == checker.ServiceStatus.UP:
                return checker.ServiceState(status = status, reason = "")
            else:
                
                print("Check functionality failed: {}:{}".format(ip, port))
                return checker.ServiceState(status = status, reason = "Service down, functionality failed")

        else:
            return checker.ServiceState(status = checker.ServiceStatus.CORRUPT, reason = "Service corrupt - Wrong flag")

    except Exception as e:
        io.close()
        state = checker.ServiceStatus.DOWN
        print("Get flag failed: {}:{} -> {}".format(ip, port, str(e)))
        return checker.ServiceState(status = state, reason = "Service corrupt - unable to retrieve flag")


def plant_flag(ip, port, flag):

    try:
        io = remote(ip, port)
        io.settimeout(2)
    
    except Exception as e:
        state = checker.ServiceStatus.DOWN
        print("Plant flag failed: {}:{} -> {}".format(ip, port, str(e)))
        status = checker.ServiceState(status = state, reason = "Failed to establish a connection")
        return (status, "")

    try:
        username = gen_rand_string(20)

        login(username,flag)

        print(io.recvuntil("Welcome , Challenger"))
        sla(">> ","3")
        sla(">> ","3")
        io.close()

        status = checker.ServiceState(status = checker.ServiceStatus.UP, reason = "")
        return (status, username)
    
    except Exception as e:
        io.close()
        state = checker.ServiceStatus.DOWN
        print("Plant flag failed: {}:{} -> {}".format(ip, port, str(e)))
        status = checker.ServiceState(status = state, reason = "Service broken - unable to plant flag")
        return (status, "")
    

class Checker(checker_grpc.CheckerServicer):
    def PlantFlag(self, request, context):
        flag = "bi0s{" + gen_rand_string(26) + "}"
        state, token = plant_flag(request.ip,request.port,flag)
        print("Plant Flag {} -> {} : {} ".format(request.ip,request.port,state))
        return checker.FlagResponse(state = state, flag=flag, token=str(token))
    
    def CheckService(self, request, context):
        service_state = get_flag(request.ip, request.port, request.flag, request.token)
        print("Check Service {} -> {} : {}".format(request.ip,request.port,service_state.status))
        return service_state

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    checker_grpc.add_CheckerServicer_to_server(Checker(), server)
    port = 70069
    print("Launching Server on port :: {}".format(port))
    server.add_insecure_port('[::]:{}'.format(port))
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
