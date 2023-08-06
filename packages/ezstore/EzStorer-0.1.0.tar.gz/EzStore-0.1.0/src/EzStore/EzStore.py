from cryptography.fernet import Fernet

key = Fernet.generate_key()
fer = Fernet(key)

def store(filename, text):
	wipe(filename)
	with open(str(filename), "a") as file:
		ords = []
		for i in text:
			i = ord(i)
			ords.append(i)
			for i in range(10):
				ords.append("UwUOwO")
		for i in ords:
			file.write(str(i))
	with open(str(filename), "r") as file:
		pwd = file.read()
	with open(str(filename), "w") as file:
		pwd = (fer.encrypt(pwd.encode()))
		file.write(pwd.decode())

def read(filename):
	fileContent = []
	finalContent = []
	finalFinalContent = []
	last = ""
	with open(filename, "r") as file:
		text = file.read()
		text = text.split("\n")
		for n in text:
			text = fer.decrypt(n.encode())
			text = text.decode()
			text = text.split("UwUOwO")
			for i in text:
				if i != "":
					i = int(i)
					fileContent.append(chr(i))
			stringContent = "".join(map(str, fileContent))
			finalContent.append(stringContent)
		for x in finalContent:
			finalFinalContent.append(last + "\n" + x)
			last = x
		stringContent = "".join(map(str, finalFinalContent))

		return stringContent
		
		
def append(filename, text):
	pwd = read(str(filename))
	pwd = pwd + "\n" + text
	with open(str(filename), "a") as file:
		ords = []
		for i in text:
			i = ord(i)
			ords.append(i)
			for i in range(10):
				ords.append("UwUOwO")
		for i in ords:
			file.write(str(i))
	store(filename, pwd)
		
		
def wipe(filename):
	with open(filename, "w+") as file:
		file.write("")


