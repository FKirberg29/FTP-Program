#!/usr/bin/python3
'''
Project 3: GV-NAP File Sharing System

Fabian Kirberg
Prof. Bowman
CIS 457
Winter 2023
'''

import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import socket
import os
import random

#Connection info
buffer_size = 1024
server_control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
remote_host_control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_port = random.randint(5042, 15042)
client_port = 8887
client_hostname = "localhost"
username = ""
speed = ""
filelist = "filelist.txt"


class Project3HostuiApp:
    def __init__(self, master=None):
        # Build UI
        self.main = tk.Tk() if master is None else tk.Toplevel(master)
        self.main.title("GV-NAPSTER Host")
        self.main.configure(height=500, width=500)
        self.ConnectionFrame = tk.LabelFrame(self.main)
        self.ConnectionFrame.configure(
            cursor="arrow",
            height=200,
            labelanchor="nw",
            relief="groove",
            text='Connection',
            width=200)
        self.ServerHostnameLabel = tk.Label(self.ConnectionFrame)
        self.ServerHostnameLabel.configure(
            font="TkDefaultFont",
            justify="left",
            text='Server Hostname:')
        self.ServerHostnameLabel.grid(column=0, pady=2, row=0)
        self.ServerHostnameEntry = tk.Entry(self.ConnectionFrame)
        self.ServerHostnameEntry.configure(exportselection="true")
        self.ServerHostnameEntry.insert(0, "localhost")
        self.ServerHostnameEntry.grid(column=1, pady=2, row=0, )
        self.PortLabel = tk.Label(self.ConnectionFrame)
        self.PortLabel.configure(text='Port:')
        self.PortLabel.grid(column=0, pady=2, row=1)
        self.PortEntry = tk.Entry(self.ConnectionFrame)
        self.PortEntry.insert(0, "5041")
        self.PortEntry.grid(column=1, pady=10, row=1)
        self.ConnectButton = tk.Button(self.ConnectionFrame, command=self.connectButton)
        self.ConnectButton.configure(text='Connect')
        self.ConnectButton.grid(column=2, padx=50, pady=2, row=1)
        self.UsernameLabel = tk.Label(self.ConnectionFrame)
        self.UsernameLabel.configure(text='Username:')
        self.UsernameLabel.grid(column=0, pady=2, row=3)
        self.UsernameEntry = tk.Entry(self.ConnectionFrame)
        self.UsernameEntry.insert(0, "hosttwo")
        self.UsernameEntry.grid(column=1, row=3)
        self.HostnameLabel = tk.Label(self.ConnectionFrame)
        self.HostnameLabel.configure(text='Hostname:')
        self.HostnameLabel.grid(column=0, row=4)
        self.HostnameEntry = tk.Entry(self.ConnectionFrame)
        self.HostnameEntry.insert(0, "localhost")
        # self.HostnameEntry.config(state="disabled")
        self.HostnameEntry.grid(column=1, row=4)
        self.SpeedLabel = tk.Label(self.ConnectionFrame)
        self.SpeedLabel.configure(text='Speed:')
        self.SpeedLabel.grid(column=2, row=4, sticky="e")
        self.initialValue = tk.StringVar(self.ConnectionFrame)
        self.initialValue.set("Fast")
        values = ['Fast', 'Medium', 'Slow']
        self.SpeedMenu = tk.OptionMenu(
            self.ConnectionFrame, self.initialValue, *values, command=None)
        self.SpeedMenu.grid(column=4, row=4)
        self.BufferLabel1 = tk.Label(self.ConnectionFrame)
        self.BufferLabel1.configure(cursor="arrow", font="system")
        self.BufferLabel1.grid(column=1, pady=5, row=2)
        self.ConnectionFrame.pack(
            anchor="center",
            expand="true",
            fill="x",
            side="top")
        self.SearchFrame = tk.LabelFrame(self.main)
        self.SearchFrame.configure(height=200, text='Search', width=200)
        self.KeywordLabel = tk.Label(self.SearchFrame)
        self.KeywordLabel.configure(text='Keyword:')
        self.KeywordLabel.grid(column=0, row=0, sticky="e")
        self.KeywordEntry = tk.Entry(self.SearchFrame)
        self.KeywordEntry.grid(column=1, row=0)
        self.SearchButton = tk.Button(self.SearchFrame, command=self.searchButton)
        self.SearchButton.configure(text='Search')
        self.SearchButton.grid(column=3, padx=10, row=0)
        self.DataTableFrame = tk.Frame(self.SearchFrame)
        self.DataTableFrame.configure(height=200, width=200)
        self.DataTableFrame.grid(column=0, row=3)
        self.SearchFrame.pack(fill="x", side="top")
        self.FTPFrame = tk.LabelFrame(self.main)
        self.FTPFrame.configure(height=200, text='FTP', width=200)
        self.EnterCommandLabel = tk.Label(self.FTPFrame)
        self.EnterCommandLabel.configure(text='Enter Command:')
        self.EnterCommandLabel.grid(column=0, pady=50, row=0)
        self.EnterCommandEntry = tk.Entry(self.FTPFrame)
        self.EnterCommandEntry.configure(width=82)
        self.EnterCommandEntry.grid(column=1, padx=10, row=0)
        self.GoButton = tk.Button(self.FTPFrame, command=self.goButton)
        self.GoButton.configure(text='Go', width=5)
        self.GoButton.grid(column=2, row=0)
        self.DisconnectButton = tk.Button(self.FTPFrame, command=self.disconnectButton)
        self.DisconnectButton.configure(text='Disconnect', width=10)
        self.DisconnectButton.grid(column=2, row=1)
        self.FTPFrame.pack(side="top")
        self.tkinterscrolledtext3 = ScrolledText(self.main)
        self.tkinterscrolledtext3.configure(height=10, state="normal", undo="true")
        self.tkinterscrolledtext3.pack(side="top")
        self.client_hostname = ""
        self.username = ""

        # Main widget
        self.mainwindow = self.main

    def run(self):
        self.mainwindow.mainloop()

    def connectButton(self):
        #Get target server info
        serverHostname = self.ServerHostnameEntry.get()
        serverPort = self.PortEntry.get()

        #Get client info
        username = self.UsernameEntry.get()
        self.username = username
        client_hostname = self.HostnameEntry.get()
        self.client_hostname = client_hostname
        speed = app.initialValue.get()

        #1
        #Attempt connection to server
        server_connect(serverHostname, serverPort)

        #2
        #Send username, hostname, and connection speed info to server
        register(client_hostname, client_port, username, speed)

        #3
        #Send file name and file description of each file in the client's directory to server using filelist.xml
        upload(client_hostname, client_port, filelist, username)


    def searchButton(self):
        keyword = self.KeywordEntry.get()
        search(self.client_hostname, client_port, keyword)

    def goButton(self):
        entry_input = self.EnterCommandEntry.get()
        command = entry_input.split()[0].strip().upper()
        if (command == "CONNECT" and len(entry_input.split()) == 3):
            ip_address = entry_input.split()[1].strip()
            port = int(entry_input.split()[2].strip())
            app.tkinterscrolledtext3.insert(tk.INSERT, ">> " + entry_input + "\n")
            host_connect(ip_address, port)
        elif (command == "RETR" and len(entry_input.split()) == 2):
            app.tkinterscrolledtext3.insert(tk.INSERT, ">> " + entry_input + "\n")
            retr(self.client_hostname, client_port, entry_input.split()[1].strip())
        elif (command == "QUIT"):
            app.tkinterscrolledtext3.insert(tk.INSERT, ">> " + entry_input + "\n")
            quit(self.client_hostname, client_port, self.username)
        else:
            print('Invalid command. Please try again.')

    def disconnectButton(self):
        quit(self.client_hostname, client_port, self.username)

#Function to establish control socket with server
def server_connect(ip_address, port):
    print("Attempting to connect to " + str(ip_address) + " on port " + str(port) + "...")
    try:
        server_control_socket.connect((ip_address, int(port)))
        print("Connection to server was successful")
    except Exception as error:
        print("Connection to server was unsuccessful. Please try again")
        print(error)

#Function to establish control socket with a host
def host_connect(ip_address, port):
    print("Attempting to connect to " + str(ip_address) + " on port " + str(port) + "...")
    try:
        remote_host_control_socket.connect((ip_address, int(port)))
        print("Connection to host was successful")
        app.tkinterscrolledtext3.insert(tk.INSERT, "Connected to " + str(ip_address) + ":" + str(port) + "\n")
    except Exception as error:
        print("Connection to host was unsuccessful. Please try again")
        print(error)

#Function to register user with server
def register(ip, port, username, speed):
    print("Attempting to register " + username + " on the server...")
    try:
        #Establish a data socket and send the reg command to the server via the control socket
        clientInfo = (client_hostname, client_port)
        server_data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_data_socket.bind(clientInfo)
        sentCommand = "REG " + str(ip) + " " + str(port) + " "
        server_control_socket.send(sentCommand.encode())

        #WAIT FOR CONNECTION TO BE ESTABLISHED BY THE SERVER
        #Listen for server response
        server_data_socket.listen(1)
        connection, addr = server_data_socket.accept()
        print(connection.recv(buffer_size).decode('utf-8'))

        #Once server has responsed, send the user info
        sentCommand = str(username) + " " + str(ip) + " " + str(speed)
        connection.send(sentCommand.encode())

        #Close the file and data socket
        server_data_socket.close()
        print(username + " successfully registered on the server")
    except Exception as error:
        print("Error: Please try again")
        print(error)

#Function to get a list of files from the server directory
def search(ip, port, keyword):
    print("Retrieving list of files with keyword: " + keyword)
    try:
        #Establish a data socket and send the search command to the server via the control socket
        clientInfo = (client_hostname, client_port)
        server_data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_data_socket.bind(clientInfo)
        sentCommand = "SEARCH " + str(ip) + " " + str(port) + " " + str(keyword)
        print(sentCommand)
        server_control_socket.send(sentCommand.encode())

        #Listen for a response from the server
        server_data_socket.listen()
        connection, addr = server_data_socket.accept()

        #Once the server has responded, print the list of file names
        data = connection.recv(buffer_size).decode('utf-8')
        print(data)

        #Display data on GUI
        lst = []
        for i in data.split('\n'):
            lst.append(i.split(', '))

        e = tk.Label(app.DataTableFrame, width=25, text="Username", borderwidth=2, relief='ridge', anchor='w', bg='gray') 
        e.grid(row=0, column=0) 
        e = tk.Label(app.DataTableFrame, width=25, text="Hostname", borderwidth=2, relief='ridge', anchor='w', bg='gray') 
        e.grid(row=0, column=1) 
        e = tk.Label(app.DataTableFrame, width=25, text="Port", borderwidth=2, relief='ridge', anchor='w', bg='gray') 
        e.grid(row=0, column=2) 
        e = tk.Label(app.DataTableFrame, width=25, text="Speed", borderwidth=2, relief='ridge', anchor='w', bg='gray') 
        e.grid(row=0, column=3) 
        e = tk.Label(app.DataTableFrame, width=25, text="Filename", borderwidth=2, relief='ridge', anchor='w', bg='gray') 
        e.grid(row=0, column=4) 
        for i in range(len(data.split('\n'))): 
            for j in range(5):
                e = tk.Label(app.DataTableFrame, width=25, text=lst[i][j], borderwidth=2, anchor='w') 
                e.grid(row=i+1, column=j)

        #Close the data socket
        server_data_socket.close()
    except Exception as error:
        print("Error: Please try again")
        print(error)

#Function to retrieve the file specified by filename from a remote host
def retr(ip, port, filename):
    print("Attemping to retrieve " + filename + " from remote host...")
    try:
        #Get the file path name and open/create the file
        new_filename = os.path.abspath(filename)
        file = open(new_filename, "w")

        #Establish a data socket and send the retr command to the server via the control socket
        clientInfo = (ip, port)
        remote_host_data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_host_data_socket.bind(clientInfo)
        sentCommand = "RETR " + str(ip) + " " + str(port) + " " + filename
        remote_host_control_socket.send(sentCommand.encode())

        #Listen for the server response
        remote_host_data_socket.settimeout(3)
        remote_host_data_socket.listen()
        connection, addr = remote_host_data_socket.accept()

        #Once the server has responded, write the file data
        data = connection.recv(buffer_size).decode('utf-8')
        while data:
            file.write(data)
            data = connection.recv(buffer_size).decode('utf-8')

        #Close the file and data socket
        file.close()
        remote_host_data_socket.close()
        print(filename + " successfully retrieved from the remote host")
        app.tkinterscrolledtext3.insert(tk.INSERT, "Successfully downloaded " + str(filename) + "\n")
    except Exception as error:
        app.tkinterscrolledtext3.insert(tk.INSERT, "Error: Please check for valid command" + "\n")
        print("Error: Please try again")
        print(error)

#Function to store the file specified by filename on the server
def upload(ip, port, filename, username):
    print("Attempting to store " + filename + " on the server...")
    try:
        #Get the file path and open the file
        new_filename = os.path.abspath(filename)
        file = open(new_filename, "rb")

        #Establish a data socket and send the stor command to the server via the control socket
        clientInfo = (client_hostname, client_port)
        server_data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_data_socket.bind(clientInfo)
        sentCommand = "UPLOAD " + str(ip) + " " + str(port) + " " + filename + " " + username
        server_control_socket.send(sentCommand.encode())

        #WAIT FOR CONNECTION TO BE ESTABLISHED BY THE SERVER
        #Listen for server response
        server_data_socket.listen(1)
        connection, addr = server_data_socket.accept()
        print(connection.recv(buffer_size).decode('utf-8'))

        #Once server has responsed, send the file data
        file_data = file.read(buffer_size)
        while file_data:
            connection.send(file_data)
            file_data = file.read(buffer_size)
        
        #Close the file and data socket
        file.close()
        server_data_socket.close()
        print(filename + " successfully stored on the server")
    except Exception as error:
        print("Error: Please try again")
        print(error)

#Function to close the connection to the server and exit
def quit(ip, port, username):
    try:
        sentCommand = "QUIT " + str(ip) + " " + str(port) + " " + str(username)
        try:
            remote_host_control_socket.send(sentCommand.encode())
            remote_host_control_socket.shutdown(socket.SHUT_RDWR)
            remote_host_control_socket.close()
        finally:
            server_control_socket.send(sentCommand.encode())
            server_control_socket.shutdown(socket.SHUT_RDWR)
            server_control_socket.close()
            print("Connection to server successfully terminated")
            app.tkinterscrolledtext3.insert(tk.INSERT, "Disconnected from server" + "\n")
            app.main.destroy()
            exit()
    except Exception as error:
        print("Error: Please try again")
        print(error)


if __name__ == "__main__":
    app = Project3HostuiApp()
    app.run()