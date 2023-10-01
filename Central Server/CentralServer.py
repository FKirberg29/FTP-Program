'''
Project 3: GV-NAP File Sharing System

Fabian Kirberg
Prof. Bowman
CIS 457
Winter 2023
'''
import socket
import threading
import os
import time

users = []
files = []
class user:
    def __init__(self, username, hostname, speed):
        self.username = username
        self.hostname = hostname
        self.speed = speed

class file:
    def __init__(self, filename, file_description):
        self.filename = filename
        self.file_description = file_description

#Function to handle a control/data socket thread
def handle_request(control_socket):
    wait_for_command = True
    while wait_for_command:
        #Decode the received message and parse the command.
        print('Server is waiting for command')
        command = ""
        sentence = control_socket.recv(buffer_size).decode('utf-8')
        print('Server received command sentence: ' + sentence)
        #If command/ip/port is not supplied, retry
        if (len(sentence.split()) < 3):
            print("Error: Not enough arguements")
        #Else parse command sentence
        else:
            command = sentence.split()[0].strip()
            ip = sentence.split()[1].strip()
            port = sentence.split()[2].strip()
            filename = ""
            username = ""
            print("Command Sentence Length: " + str(len(sentence.split())))
            #If more strings than command/ip/port is given, interpret 4th as filename
            if (len(sentence.split()) > 3):
                filename = sentence.split()[3].strip()
            if (len(sentence.split()) > 4):
                username = sentence.split()[4].strip()
            print('Command: ' + command)

        #Use command parse to determine what command to execute
        if (command == "REG"):
            register(ip, port)
        elif (command == "SEARCH"):
            search(ip, port, filename)
        elif (command == "UPLOAD"):
            upload(ip, port, filename, username)
        elif (command == "QUIT"):
            wait_for_command = False
            quit(ip, port, filename)
            control_socket.shutdown(socket.SHUT_RDWR)
            control_socket.close()
        else:
            print('Error: Invalid Command. Please try again.')

#Function to register a user and their info connecting to the server
def register(ip, port):
    print("Server recieved register request for: " + ip + "...")
    try:

        #Connect to the client's data socket and send a message to indicate that the server is ready to receive data
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_socket.connect((ip, int(port)))
        data_socket.send("Server is ready to receive".encode())

        #Receive the data sent by the client
        data = data_socket.recv(buffer_size).decode('utf-8')
        print(data)

        #Parse client info
        clientUsername = data.split()[0].strip()
        clientHostname = data.split()[1].strip()
        clientSpeed = data.split()[2].strip()
        print("Client username: " + clientUsername)
        print("Client hostname: " + clientHostname)
        print("Client speed: " + clientSpeed)

        #Store client info as object in users list
        if not any(x.username == clientUsername for x in users):
            users.append(user(clientUsername, clientHostname, clientSpeed))
        for i in users:
            print(i.username, i.hostname, i.speed)
        
        #Close the file and data socket
        data_socket.close()
        print("Succesfully registered " + ip)
    except Exception as error:
        print("Error: Please try again")
        print(error)

#Function to supply list of file names to client
def search(ip, port, keyword):
    print("Server received request for the list of files filtered by the keyword: " + keyword + "...")
    try:
        #Get the file path and open the file
        file = open("filelist.txt", "r")

        filtered = ""
        for line in file:
            if keyword in line:
                filtered = filtered + line
        print(filtered)

        #Create data socket and send the file name list to client
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_socket.connect((ip, int(port)))
        data_socket.send(filtered.encode())

        data_socket.close()
        print("Successfully sent list of files to client")
    except Exception as error:
        print("Error: Please try again")
        print(error)

#Function to receive a file from client and save it on the server
def upload(ip, port, filename, username):
    print("Server recieved file list upload request from: " + ip + "...")
    try:
        #Get the file path name and open/create the file
        file = open("filelist.txt", "a")

        #Connect to the client's data socket and send a message to indicate that the server is ready to receive data
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_socket.connect((ip, int(port)))
        data_socket.send("Server is ready to receive".encode())

        #Gather user info
        user_info = ""
        for i in users:
            if username == i.username:
                user_info = i.username + ", " + i.hostname + ", " + str((int(port)+1)) + ", " + i.speed + ", "

        #Receive files sent by the client and insert user info
        file.write('\n')
        data = data_socket.recv(buffer_size).decode('utf-8')
        while data:
            for line in data.split('\n'):
                line = user_info + line
                file.write(line)
            data = data_socket.recv(buffer_size).decode('utf-8')
        
        #Close the file and data socket
        file.close()
        data_socket.close()
        print("Succesfully stored " + filename + " sent by client")
    except Exception as error:
        print("Error: Please try again")
        print(error)

#Function to close the current client's connection
def quit(ip, port, username):
   
   #Remove the files uploaded by the quitting client
   file = open("filelist.txt", "r")
   file_data = file.read()
   print("pre quit file data: " + file_data)
   new_file_data = ""
   file.close()
   for i in file_data.split('\n'):
        if (ip in i and username in i):
           i = i
        else:
           new_file_data += '\n' + i
   print("post quit file data: " + new_file_data)
   file = open("filelist.txt", "w")
   file.write(new_file_data)
   file.close()

   #Remove quitting user from users list
   for i in users:
       if (ip == i.hostname and username == i.username):
           users.remove(i)
       else:
           i=i
    
   print("Connection with " + username + " from " + ip + " on port " + str(port) + " closed by client")





########################################################################################
#IP, Port, and Buffer Size Info
#Port is last four digits of GNumber
server_ip = 'localhost'
server_port = 5041
buffer_size = 1024

#Create a TCP socket that listens on the above IP and Port.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen()

#Create a time_stamp variable on server start
time_stamp = time.strftime("%a, %d %b %y %H:%M:%S %Z")
print('The server is ready to receive')

#Handles multi-threaded control sockets
while True:
    control_socket, addr = server_socket.accept()
    threading.Thread(target=handle_request, args=(control_socket,)).start()