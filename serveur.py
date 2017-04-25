import socket,select,sys,signal

#serveur
serveurSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#associe une soket a une adresse locale
port = int (sys.argv[1])
serveraddr = ("localhost", port)
serveurSock.bind(serveraddr)

Taillemaxfiledattente = 5
serveurSock.listen(Taillemaxfiledattente)

#websocket
nombArg = len(sys.argv)
if nombArg > 2:
	webSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	portWeb = int (sys.argv[2])
	webSock.bind(("",portWeb))
	webSock.listen(1)


connectedClients = {}
msg_web = []


def sendToClients(userList, msg):
	for client in userList:
		client.send(msg)

def supMsgWeb():
	del msg_web[:-5]

def afficherMsg(msgList):
	global msg_envoi
	for msg in msgList:
		msg_envoi += "<li>"+ msg +"</li>"

def stopServeur(sig,frame):
	msg_fin = "<stopServeur>"
	sendToClients(connectedClients.keys(), msg_fin.encode())
	if not connectedClients:
		serveurSock.close()
		sys.stdout.write("Fermeture du serveur \n")
		sys.exit(0)

signal.signal(signal.SIGINT, stopServeur)

while True:

	if nombArg > 2:

		connectedRequest, listeEcriture, listeErreur = select.select([serveurSock,webSock], [], [], 0.05)

		for input in connectedRequest:
			if input == webSock:
				pageWeb,pageAddr = webSock.accept()
				request = pageWeb.recv(1024).decode() 
				
				msg_envoi = ""
				supMsgWeb()
				afficherMsg(msg_web)
				msg_env = """\HTTP/1.1 200 OK """ + """Content-type: text/html \n\n"""
				msg_env += """<HTML><HEAD><TITLE> historique de conversation </TITLE></HEAD><BODY>"""
				msg_env += """<ul><lh><h1>historique de conversation :</h1></lh>""" + msg_envoi + """</ul></BODY></HTML>"""
				
				
				
				pageWeb.send(msg_env.encode())
				pageWeb.shutdown(1)
				pageWeb.close()
		

			if input == serveurSock:
				# connexion avec le client
				newClient,(fromaddr,fromport) = serveurSock.accept()
				idClient = newClient.recv(1000)
				idClient = idClient.decode()
				connectedClients[newClient] = idClient
				msg_connexion = "Connexion de " + idClient + " au serveur : ok \n"
				sys.stdout.write(msg_connexion)
				msg_web.append(msg_connexion)

	else:
		connectedRequest, listeEcriture, listeErreur = select.select([serveurSock], [], [], 0.05)
		
		for request in connectedRequest:
			# connexion avec le client
			newClient,(fromaddr,fromport) = serveurSock.accept()
			idClient = newClient.recv(1000)
			idClient = idClient.decode()
			connectedClients[newClient] = idClient
			msg_connexion = "Connexion de " + idClient + " au serveur : ok \n"
			sys.stdout.write(msg_connexion)
			msg_web.append(msg_connexion)



	msgClients = []
	try:
		msgClients, listeEcriture, listeErreur = select.select(connectedClients.keys(), [], [], 0.05)

	except select.error:
		pass

	else:
		for client in msgClients:
			msg_recu = client.recv(1000)
			msg_recu = msg_recu.decode()
			
			if msg_recu == "<stop>":
				msg_stop = "Deconnexion de " + connectedClients.get(client) + "\n"
				sys.stdout.write(msg_stop)
				msg_web.append(msg_stop)
				client.close()
				del connectedClients[client]
				print (connectedClients)
				sendToClients(connectedClients.keys(), msg_stop.encode())
			else :
				sys.stdout.write(msg_recu)
				msg_web.append(msg_recu)
				sendToClients(connectedClients.keys(), msg_recu.encode())



