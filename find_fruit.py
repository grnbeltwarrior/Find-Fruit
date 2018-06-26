#!/usr/bin/python

# reworked into python from rvrsh3ll's Find-Fruit.ps1
# https://github.com/rvrsh3ll/Misc-Powershell-Scripts/blob/master/Find-Fruit.ps1

import sys
import socket
import getopt
import threading
import subprocess
import requests
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

ip = ""
ports = ""
https = False
timeOut = 0.5

vuln_links = ['/','jmx-console/',
'web-console/ServerInfo.jsp',
'invoker/JMXInvokerServlet',
'system/console',
'axis2/axis2-admin/',
'manager/html',
'tomcat/manager/html',
'wp-admin',
'workorder/FileDownload.jsp',
'ibm/console/logon.jsp?action=OK',
'data/login',
'script/',
'opennms']

def usage():
	print
	print "______  _             _   _____  _            ______             _  _"
	print "|  ___|(_)           | | |_   _|| |           |  ___|           (_)| |"
	print "| |_    _  _ __    __| |   | |  | |__    ___  | |_  _ __  _   _  _ | |_"
	print "|  _|  | || '_ \  / _` |   | |  | '_ \  / _ \ |  _|| '__|| | | || || __|"
	print "| |    | || | | || (_| |   | |  | | | ||  __/ | |  | |   | |_| || || |_"
	print "\_|    |_||_| |_| \__,_|   \_/  |_| |_| \___| \_|  |_|    \__,_||_| \__|"
	print 
	print "Usage: find_fruit.py -t target_host -p list_of_ports"
	print
	print "Example: "
	print "find_fruit.py -t 10.10.10.10 -p 80,443,8080,8443"
	sys.exit()

def urlBuilder(http,portColon,port):
	for path in vuln_links:
		url = http + '://' + ip + portColon + port + '/' + path

def heavy_lifting():
	global ip
	global ports

	for port in ports:
		if int(port) == 443:
			http = 'https'
			portColon = ''
			port = ''

		elif int(port) == 80:
			http = 'http'
			portColon = ''
			port = ''

		else:
			http = 'http'
			portColon = ':'

		urlBuilder(http,portColon,port)

		for path in vuln_links:
			url = http + '://' + ip + portColon + port + '/' + path
			headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'}
			try:
				data = requests.get(url, headers, timeout=timeOut, verify=False)
				if str(data.status_code) == '200':
					print "The following URL returned a status of OK: " + url
					print data.text + '\r\n'
			except requests.exceptions.Timeout:
				pass
				#print "The following URL timed out: " + url #Uncomment these if you want the errors to go to the console.
			except requests.exceptions.RequestException as e:
				pass
				#print "The following error occurred: " + e #Uncomment these if you want the errors to go to the console.

def main():
	global ip
	global ports

	if not len(sys.argv[1:]):
		usage()

	try:
		opts, args = getopt.getopt(sys.argv[1:],"t:p:",["target","port"])

	except getopt.GetoptError as err:
		print str(err)
		usage()

	for o,a in opts:
		if o in ("-t","--target"):
			ip = a
			print a
		elif o in ("-p","--port"):
			ports = a.split(',')
			print ports
		else:
			assert False, "Unhandled Option"

	heavy_lifting()

main()
