import socket
import threading
import hashlib
import math
import turtle
import time
from os import startfile

IP="127.0.0.1"#10.30.58.40
SERVER_PORT=13370

#takes str and return int on base 26
def convert26int(s):
    int26=0
    for i in range(len(s)):
        int26+=math.pow(10,i)*(ord(s[-i-1])-96) 
    return int(int26)

#takes int on base 26 and returns str
def convert26letters(num):
    s_num=str(num)
    s=''
    for x in range(len(s_num)):
        c=s_num[x]
        s=s+chr(int(c)+96)
    return s


#converts string base 26 to int base 10
def convert26to10(s):
    int26=convert26int(s)

    int10=0
    for x in range (len(str(int26))):
        int10+=int(int26%10*math.pow(26,x))
        int26=int(int26//10)

    return int10

#converts int base 10 to string base 26
def convert10to26(num):
    if num <= 0:
        return individual_length
    elif num <= 26:
        return chr(96+num)
    else:
        return convert10to26(int((num-1)/26))+chr(97+(num-1)%26)

def hexa(s):
    result=hashlib.md5(s.encode())
    return result.hexdigest()


    

class Craker:
    def __init__(self):
        reach_soc=socket.socket()
        reach_soc.connect((IP,SERVER_PORT))
        reach_soc.send("Howdy".encode())
        self.id=int(reach_soc.recv(1024).decode())
        self.port=self.id+SERVER_PORT
        self.soc=socket.socket()
        self.soc.bind(("0.0.0.0",self.port))
    
    def listen(self):
        self.soc.listen()
        self.mother_soc,adress=self.soc.accept()
        self.finished_task=False
        self.getmission()
        
        

    def getmission(self):
        data=self.mother_soc.recv(1024).decode()
        data=data.split(',')
        self.start=data[0]
        self.finish=data[1]
        self.target=data[2]

        self.crack()
    
    def celebrate(self):
        print("celebrate")
        
        path=r'C:\Users\student\Desktop\cracker\babyback.mp4'
        startfile(path)
        
        

    
    def did_finish_early(self):
        data=self.mother_soc.recv(1024).decode()
        if data=="finish":
            self.found=True
    
        

    def crack(self):
        self.ifound=False
        self.md5=None

        #config wait thread to recive possible message from mother socket
        self.found=False
        wait_thread=threading.Thread(target=self.did_finish_early)
        wait_thread.start()


        #config thread crackers
        num_of_threads=8
        int_start=convert26to10(self.start)
        int_end=convert26to10(self.finish)
        length=int_end-int_start+1
        individual_length=int(length//num_of_threads)

        individual_start=self.start
        threads=[]

        for x in range (num_of_threads):
            t=threading.Thread(target=self.cracker_code,args=(individual_start,individual_length,self.target))
            t.start()
            print(f"{x},{individual_start},{individual_length}")
            threads.append(t)
            ivs10=convert26to10(individual_start)
            ivs10=ivs10+individual_length 
            individual_start=convert10to26(ivs10)
        
        if length%num_of_threads!=0:
            extra_thread_len=length%num_of_threads
            extra_thread=threading.Thread(target=self.cracker_code,args=(individual_start,extra_thread_len,self.target))
            extra_thread.start()
            print(f"extra,{individual_start},{extra_thread_len}")
            

        while self.finished_task==False:
            if self.found==True:
                self.finished_task=True
                self.celebrate()
                break
            
            if self.ifound==True:
                self.mother_soc.send(f"{self.id},true,{self.target},{self.md5}".encode())
                self.finished_task=True
                self.celebrate()
                break

            finished=False
            for thread in threads:
                if thread.is_alive() == True:
                    finished=False
                    break

            if finished ==True:
                self.mother_soc.send(f"{self.id},false,{self.target}".encode())
                print("not found")
                self.finished_task=True 
                self.listen()




    def cracker_code(self,start,length,target):
        #print(f"{start},{length},{target}\n")
        for x in range(length):
            val=convert10to26(convert26to10(start)+x)
            if (hexa(val)==target):
                self.md5=val
                self.ifound=True
                break
        
        
        
            
            


def main():
    crkr= Craker()
    crkr.listen()
    

if __name__=='__main__':
    main()
