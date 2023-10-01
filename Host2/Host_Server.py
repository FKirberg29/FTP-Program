'''
Project 3: GV-NAP File Sharing System

Fabian Kirberg
Prof. Bowman
CIS 457
Winter 2023
'''
import os
import socket
import threading

#Function to handle a control/data socket thread
def handle_request(control_socket):
    wait_for_command = True
    while wait_for_command:
        #Decode the received message and parse the command.
        print('Host server is waiting for command')
        command = ""
        sentence = control_socket.recv(buffer_size).decode('utf-8')
        print('Host server received command sentence: ' + sentence)
        #If command/ip/port is not supplied, retry
        if (len(sentence.split()) < 3):
            print("Error: Not enough arguements")
        #Else parse command sentence
        else:
            command = sentence.split()[0].strip()
            ip = sentence.split()[1].strip()
            port = sentence.split()[2].strip()
            filename = ""
            print("Command Sentence Length: " + str(len(sentence.split())))
            #If more strings than command/ip/port is given, interpret 4th as filename
            if (len(sentence.split()) > 3):
                filename = sentence.split()[3].strip()
            print('Command: ' + command)

        #Use command parse to determine what command to execute
        if (command == "RETR"):
            host_retr_send(ip, port, filename)
        elif (command == "QUIT"):
            wait_for_command = False
            quit(ip, port)
        else:
            print('Error: Invalid Command. Please try again.')

#Function to send file to host that requested it
def host_retr_send(ip, port, filename):
    print("Host server received retrieve request for: " + filename + "...")
    try:
        #Get the file path and open the file
        filename = os.path.abspath(filename)
        file = open(filename, "rb")

        #Connect to the data socket established by the client
        remote_host_data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_host_data_socket.connect((ip, int(port)))

        #Read and send the file data to client
        file_data = file.read(buffer_size)
        while file_data:
            remote_host_data_socket.send(file_data)
            file_data = file.read(buffer_size)

        #Close the file and data socket
        file.close()
        remote_host_data_socket.close()
        print("Succesfully sent " + filename + " to remote host")
    except Exception as error:
        print("Error: Please try again")
        print(error)

#Function to close the current client's connection
def quit(ip, port):
   print("Connection " + ip + " on port " + str(port) + " closed by client")
   control_socket.close()

client_port = 8888
client_hostname = "localhost"
buffer_size = 1024
########################################################################################
#Create a TCP socket that listens on the above IP and Port.
host_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_server_socket.bind((client_hostname, client_port))
host_server_socket.listen()
print('The host server is ready to receive')

#Handles multi-threaded control sockets
while True:
    control_socket, addr = host_server_socket.accept()
    threading.Thread(target=handle_request, args=(control_socket,)).start()