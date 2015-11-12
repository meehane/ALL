import getpass
import paramiko
import os
import socket
def ftpmain():
    def sftp_download(username, password, hostname,port):
        
        try:
            """function for downloading through sftp session"""
            ssh_transport=paramiko.Transport((hostname, port))   #it transport username and port to a variable (ssh_transport),we use double brackets because it is the syntax and it is taking to valuejust like tuple and assigning into 1
            ssh_transport.connect(username=username, password=password)  #connecting to ssh server using ssh_transport information, username and password
            sftp_session =paramiko.SFTPClient.from_transport(ssh_transport) #now connecting for sftp using ssh with ssh_transport
            
        except socket.gaierror: #specific error handling for the socket not connecting
            print("the server is not up")
            exit()


        print('\nFile Transfer Window\n')
        sftp_session.chdir("FTP")
        folder="FTP"
        while True:      #while loop to go into directories
            a=sftp_session.listdir()
            print("...............Select a folder:............")   
            print("___________________________________________")
            for i in a: # loop to show all directories in different lines
                print i
            file_path=raw_input("\nEnter a folder name or hit enter to choose this folder: ")
            if file_path=="":   # if you leave it blank or press enter without entering anything it'll break and make it your directory and ask you to choose a file name
                break
            else:
                try:
                    folder=folder+file_path+"/"
                    sftp_session.chdir(file_path)
                except IOError:
                    print("No such directory found. Try again") #error handling for no file
        while True:
            
            try:
                
                target_file=raw_input('Enter a file name, including the full extention: \n')
                full_path=folder+target_file 
                downloadLoc=os.environ['HOME']
                os.chdir(downloadLoc)
                sftp_session.get(target_file,target_file) #as we change the present directory it will change the file from current folder the syntax of get is ("full path including file name","file name")  
                print("Downloaded file from: %s" %full_path)#it'll show the path
                print("Downloaded to users home folder directory")
                sftp_session.close()
            except IOError:
                print("No such file found ")







    def sftp_upload(username, password, hostname,port):
        try:
            """function for uploading through sftp session"""
            ssh_transport=paramiko.Transport((hostname, port))   #it transport username and port to a variable (ssh_transport),we use double brackets because it is the syntax and it is taking to valuejust like tuple and assigning into 1
            ssh_transport.connect(username=username, password=password)  #connecting to ssh server using ssh_transport information, username and password
            print('connected\n')
            sftp_session =paramiko.SFTPClient.from_transport(ssh_transport) #now connecting for sftp using ssh with ssh_transport
            print('sftp session connected\n')
        except socket.gaierror: #specific error handling for the socket not connecting
            print("the server is not up")
            exit()

            
        folder=""
        path=os.environ['HOME'] #sets as homedirectory on linux systems
        print("...............Select a folder:............")   
        print("___________________________________________")
        count=1
        
        while True:#while loop to go into directories
            if count==1:
                a=os.listdir(path)    #os commands are ussed to do anything on our own machine so in this we are listing directories on the path assigned above
                for i in a:
                    print i
            else:
                newlyent=path.split('/')[-1]
                path=path.replace(newlyent,"")
                
                a=os.listdir(path)    #os commands are ussed to do anything on our own machine so in this we are listing directories on the path assigned above
                for i in a:
                    print i
                print "the directory doesn't exist please try again"    
                    
            file_path=raw_input("\nEnter a folder name or hit enter to choose this folder: ")
            if file_path=="":
                break
            elif file_path=="back":
                back=path.split('/')[-1]
                path=path.replace(back,"")
            
            else:
                try:
                    count=1
                    folder=folder+file_path+"/"
                    path=path+"/"+file_path
                    os.chdir(path)
                except OSError:
                    count=0
                    print("no such DIRECTORY found try again")
                    
        
        sftp_session.chdir("FTP") #changing the directory of server so every file will be uploaded to that place         
        
        target_file=raw_input("Enter a file name, including the full extention: \n")
        try:
            full_path=path+"/"+target_file
            if target_file!="":
                sftp_session.put(target_file,target_file) #as we change the present directory it will change the file from current folder the syntax of put is ("file name","full path including file name")   
            else:
                sftp_session.put(path,path)
            print("uploaded file from: %s" %full_path)
            print("uploaded")
            sftp_session.close()
        except:
            print("Error 401:file not found. Try again")





    #getting all the information from user and then passing it to function
    #default information has been put it -it xan be changed
    host=('chat.teamudp.co.uk')
    username=('ftpu')
    password =("groupudp")
    port=int('22')

    options=['1.Download','2.Upload']
    for i in options:
        print(i)
    opt=int(raw_input('Please select a coresponding option, from above: '))    
    if opt==1:
        sftp_download(username,password,host,port) #calling the download function with passing these parameters
    elif opt==2:
        sftp_upload(username,password,host,port)  #calling the upload function with passing these parameters
ftpmain()
