#!/usr/bin/python
import socket, sys

#funtion to perform whois query to a server and get the reply with the required information
def perform_whois(server, query):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((server, 43))
	#send data
	s.send(query + '\r\n')
	#receive reply
	msg = ''
	while len(msg) < 10000:
		chunk = s.recv(100)
		if chunk == '':
			break
		msg = msg + chunk
	return msg

#function to perform the whois on a domain name
def get_whois_data(domain):
	#remove http and www
	domain.replace('http://','')
	domain.replace('www.','')
	#get the extension
	ext = domain[-3:]

	#if top level domain .com .org. net
	if(ext == 'com' or ext == 'org' or ext == 'net'):
		whois = 'whois.internic.net'
		msg = perform_whois(whois, domain)

		#scanning reply for the whois server
		lines = msg.splitlines()
		for line in lines:
			if ':' in line:
				words = line.split(':')
				if 'Whois' in words[0] and 'whois.' in words[1]:
					whois = words[1].strip()
					break
	else:
		ext = domain.split('.')[-1]

		whois = 'whois.iana.org'
		msg = perform_whois(whois, ext)

		#scanning reply for the whois server
		lines = msg.splitlines()
		for line in lines:
			if ':' in line:
				words = line.split(':')
				if 'whois.' in words[1] and 'Whois Server (port43)' in words[0]:
					whois = words[1].strip()
					break

	#now contact the final whois server
	msg = perform_whois(whois, domain)
	#return the reply
	return msg

#getting domain name from the command line argument
domain_name = sys.argv[1]
print get_whois_data(domain_name)
