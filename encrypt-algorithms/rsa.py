#python ver 3.6.1
#1412484
#reference
#https://gist.github.com/JonCooperWorks/5314103
#http://code.activestate.com/recipes/578838-rsa-a-simple-and-easy-to-read-implementation/
#http://code.activestate.com/recipes/577737-public-key-encryption-rsa/
from time import localtime, strftime
from random import randrange
from math import gcd

def encrypt(Key, text, n):
	EncryptedText = [pow(ord(char), Key, n) for char in text]
	return EncryptedText


def decrypt(Key, cipher_text, n):
	DecryptedText = [chr(pow(char, Key, n)) for char in cipher_text]
	return ''.join(DecryptedText)
	
def generateKey(p, q):
	if not (isPrime(p) and isPrime(q)):
		raise ValueError('Both numbers must be prime')
	else:
		if p == q:
			raise ValueError('p and q cannot be equal')
	n = p*q
	#Compute the totient
	Phi_n = (p-1)*(q-1)
	print("Phi n: %s" %Phi_n)
	print("Compute public key")
	PublicKey = generatePublicKey(Phi_n)
	print("Compute private key")
	PrivateKey = generatePrivateKey(PublicKey, Phi_n)
	return (PublicKey, PrivateKey, n)
	
def generatePrivateKey(PublicKey, Phi_n):
	remainder = -1
	while (remainder != 0):
		k = randrange(1, Phi_n)
		de = (k*Phi_n) + 1
		PrivateKey = de/PublicKey
		remainder = de%PublicKey
	return int(PrivateKey)
	
def generatePublicKey(Phi):
	print("Begin computing public key")
	print("Timestamp: " + strftime("%a, %d %b %Y %H:%M:%S", localtime()))
	PublicKey = randrange(1, Phi)
	g = gcd(PublicKey, Phi)
	while g != 1:
		PublicKey = randrange(1, Phi)
		g = gcd(PublicKey, Phi)
	return PublicKey

	
def isPrime(number):
	if number == 2 or number == 3: return True
	if number < 2 or number%2 == 0: return False
	if number < 9: return True
	if number%3 == 0: return False
	r = int(number**0.5) 
	f = 5
	while f <= r:
		if number%f == 0:
			return False
		if number%(f+2) == 0: 
			return False
		f +=6
	return True   
	
	
if __name__ == '__main__':
	p = int(input("Enter a prime number (17, 19, 23, etc): "))
	q = int(input("Enter another prime number (Different from %s): " %p))
	print("Generating public and private keypairs")
	print("Timestamp: " + strftime("%a, %d %b %Y %H:%M:%S", localtime()))
	PublicKey, PrivateKey, n = generateKey(p, q)
	print("This is your private key: %s" %PrivateKey)
	print("This is your public key: %s" %PublicKey)
	print("This is your n: %s" %n)
	text = input("Enter a message to encrypt with your key: ")
	EncryptedText = encrypt(PublicKey, text, n)
	print ("Your encrypted text is: ")
	ShowText = ''
	ShowText = ShowText.join(map(lambda x: str(x), EncryptedText))
	print (ShowText)
	print ("Decrypting message with key: %s" % PrivateKey)
	print ("Your message is:")
	print (decrypt(PrivateKey, EncryptedText, n))