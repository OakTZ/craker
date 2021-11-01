import socket
import threading
import hashlib
import math
from pygame import  mixer
import turtle
import time

IP='127.0.0.1'
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

#converts int base 10 to int base 26
def convert10to26(num):
    if num <= 0:
        return ""
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
        port_id=int(reach_soc.recv(1024).decode())
        self.port=port_id+SERVER_PORT
        self.soc=socket.socket()
        self.soc.bind(('127.0.0.1',self.port))
    
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
        #mixer.init()
        #mixer.music.load('back.wav')
        #mixer.music.play()

        while True:
            turtle.Screen().bgcolor("red")
            time.sleep(0.3)
            turtle.Screen().bgcolor("blue")
            time.sleep(0.3)
            turtle.Screen().bgcolor("green")
            time.sleep(0.3)

    
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
        wait_thread.join()

        #config thread crackers
        num_of_threads=8
        int_start=convert26to10(self.start)
        int_end=convert26to10(self.finish)
        length=int_end-int_start+1
        individual_length=int(length//num_of_threads)

        individual_start=self.start
        threads=[]
        ivs26=0
        for x in range (num_of_threads):
            t=threading.Thread(target=self.cracker_code,args=(individual_start,individual_length,self.target))
            t.start()
            threads.append(t)
            print(individual_start,individual_length)
            ivs26=convert26int(individual_start)
            ivs26=ivs26+individual_length #PROBLEM!!!!!!!!
            individual_start=convert26letters(ivs26)
        
        for t in threads:
            t.join()

        if length%num_of_threads!=0:
            extra_thread_len=length%num_of_threads
            extra_thread=threading.Thread(target=self.cracker_code,args=(individual_start,extra_thread_len,self.target))
            extra_thread.start()
            extra_thread.join()

        while self.finished_task==False:
            if self.found==True:
                wait_thread.exit()
                for t in threads:
                    t.exit()
                extra_thread.exit()
                self.finished_task=True

            if self.ifound==True:
                self.mother_soc.send(f"{self.id},true,{self.target},{self.md5}".encode())
                wait_thread.exit()
                for t in threads:
                    t.exit()
                extra_thread.exit()
                self.finished_task=True 

            finished=False
            for thread in threads:
                if thread.is_alive() ==True:
                    finished=False
                    break

            if finished ==True:
                self.mother_soc.send(f"{self.id},false,{self.target}".encode())
                self.finished_task=True 
                self.listen()

        self.celebrate()



    def cracker_code(self,start,length,target):

        for x in range(length):
            val=convert26letters(convert26int(start)+x)
            if (hexa(val)==target):
                self.md5=val
                self.ifound=True
                break
        
        
        
            
            


def main():
    crkr= Craker()
    crkr.listen()
    

if __name__=='__main__':
    main()
