# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 12:29:48 2018

@author: SKY_SHY
"""
import os

base = os.getcwd()
PI = open(os.path.join(base, 'Our_Pi.txt'), 'r').read()

EE = open(os.path.join(base, 'Our_E.txt'), 'r').read()

S2 = open(os.path.join(base, 'Our_S2.txt'), 'r').read()

def CountDigits_In_Base(a_base):
    Dict = dict(zip(range(10),[0 for i in range(10)]))
    for d in a_base:
        Dict[int(d)] +=1
    return list(Dict.values())



def isFull(a_perm, k):
    for i in range(k):
        if str(i) not in a_perm:
            return False
    return True

def countPerm(N, k):
    ind = 0
    count = 0
    while ind < len(N):
        if isFull(N[ind:ind+k], k):
            count +=1
        ind += 1
    return count
    

import time
class Digit():
    
    
    def __init__(self, method):
        self.PI = 'pi'
        self.E = 'e'
        self.S2 = 's2'
        self.method = method
        self.seed = int(str("%.20f" % time.time())[-9:]) % 100
        self.init_seed = self.seed % 100
        self.next = self.seed
        self.__A = 16 + (self.seed // 100)
        self.seek = 99
        self.DataTempNumbers = self.getTempNumbers()

    
    
    def ChooseNumbers(self):
        if self.method == self.PI:
            return PI
        elif self.method == self.E:
            return EE
        elif self.method == self.S2:
            return S2 

    
    def getTempNumbers(self):
        return self.ChooseNumbers()[:100]
    
    
    def selectInd(self, X0):
        return (self.__A*X0 + 51) % 100
    
    def generOneDigit(self, a_X):
        self.next = self.selectInd(a_X)
        return self.DataTempNumbers[self.next]
    
    def makeChangeDB_100Digits(self, x_next, seeked):
        self.DataTempNumbers = self.DataTempNumbers[:x_next] + self.DataTempNumbers[x_next+1:]
        self.DataTempNumbers += self.ChooseNumbers()[seeked]
      
	
    def reach1000000(self):
        if self.seek >= 999999:
            self.seed +=1
            #if ( self.__A*self.seed + 51 )% 100 == (self.__A*self.init_seed + 51) % 100:
            if self.seed % 100 == self.init_seed:
                self.__A +=1
            #if ( self.__A*self.seed + 51 )% 100 == (self.__A*self.init_seed + 51) % 100:
            return -1#change to self.seek = 0
        else:
            return self.seek#change to self.seek += 1
        
    def sectionA(self):
        self.seek = self.reach1000000()
        self.seek += 1# Not Need!!!!
        self.makeChangeDB_100Digits(self.next, self.seek)
        if self.seek == 0:
            self.next = self.seed % 100    
			
from functools import reduce

class Fx(Digit):

	def makeFloat(self, n):
		Fract19Length = ''
		for i in range(n):
			Fract19Length += self.generOneDigit(self.next)
			self.sectionA()
		return float('0.' + Fract19Length)
	
	def getNum(self, n):
		Num = ''
		for i in range(n):
			Num += self.generOneDigit(self.next)
			self.sectionA()
		return int(Num)
    
	def generNumber_2XOR(self, n, k_numbs = 2):
		return [self.getNum(n) for i in range(k_numbs)]

class PRIMG_Generator():
	
	def __init__(self, a_Digit, a_CDF):
		self.__low = 0
		self.__up = 1
		self.maxLen = 1
		self.Digit = a_Digit
		self.CDF = a_CDF
	
	def changes(self,):
		self.maxLen = len(str(self.__up))
		self.CDF.seed += 1
		self.CDF.init_seed = self.CDF.seed % 100
		self.CDF.next = self.CDF.seed
		self.CDF._Digit__A = 16 + (self.CDF.seed // 100)
	
	def setBounds(self, L, U):
		self.__low = L
		self.__up = U
	
	def quartet(self, n):
		n = n % (100**4)
		P = [n % 100]
		while n > 99:
			n = n // 100
			q = n % 100
			P.append(q)
		while len(P) < 4:
			P.append(0)
		return P
		
	def set_seed(self, seed):
		self.CDF._Digit__A, self.CDF.seed, self.Digit._Digit__A, self.Digit.seed = self.quartet(seed)
		self.CDF.next = self.CDF.seed
		self.Digit.next = self.Digit.seed
		
	#ver.14
	def generateNumber(self):
		Number = ''
		for i in range(self.maxLen):
			Number += self.Digit.generOneDigit(self.Digit.next)
			self.Digit.sectionA()
		nums = [int(Number)] + self.CDF.generNumber_2XOR(self.maxLen)
		return reduce(lambda a,b: a^b, nums)
		
	def randint(self, low, up, N=1):
		self.setBounds(low, up)
		self.changes()
		for i in range(N):
			res = int(self.generateNumber())
			
			while res < low or res > up:
				res = int(self.generateNumber())
			else:
				yield res


F = Fx('pi')
D = Digit('pi')
irandom = PRIMG_Generator(D, F)