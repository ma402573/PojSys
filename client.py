import socket,sys,signal,select
#client
clientSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

serveur = sys.argv[1]
port = int (sys.argv[2])
idclient = sys.argv[3]

#clientaddr = ("localhost", 2001)
clientaddr = (serveur, port)

# 0 -> succes , 1 -> echec  (connexion avec serveur)
clientSock.connect(clientaddr)
clientSock.send(idclient.encode())

def stop(sig,frame):
	msg_envoyer = "<stop>"
	clientSock.send(msg_envoyer.encode())
	clientSock.close()
	sys.stdout.write("Fermeture de la connexion \n")
	sys.exit(0)

sys.stdout.write("Connexion etablie \n")
sys.stdout.flush()

signal.signal(signal.SIGINT, stop)

while True:
	readers,writers,errors = select.select([clientSock,sys.stdin],[],[],0.05)

	for read in readers:
		if read == clientSock:
			# ici on a quelque chose a lire sur clientSock
			msg_recu = clientSock.recv(1000) # ne bloque pas !
			msg_recu = msg_recu.decode()
			if msg_recu == "<stopServeur>":
				msg_envoyer = "<stop>"
				clientSock.send(msg_envoyer.encode())
				clientSock.close()
				sys.stdout.write("Fermeture de la connexion \n")
				sys.exit(0)

			sys.stdout.write(msg_recu)
			sys.stdout.flush()
		if read == sys.stdin:
			# ici on a quelque chose a lire sur stdin
			msg = sys.stdin.readline() # ne bloque pas
			if msg :
				msg_envoyer = idclient + ":" + msg
				msg_envoyer = msg_envoyer.encode()
				clientSock.send(msg_envoyer)
			else:
				msg_envoyer = "<stop>"
				clientSock.send(msg_envoyer.encode())
				clientSock.close()
				sys.stdout.write("Fermeture de la connexion \n")
				sys.exit(0)

