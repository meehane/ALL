import getpass
import paramiko
import os
def sftp_download(username, password, hostname,port):
    """function for downloading through sftp session"""
    ssh_transport=paramiko.Transport((hostname, port))   #it transport username and port to a variable (ssh_transport),we use double brackets because it is the syntax and it is taking to valuejust like tuple and assigning into 1
    ssh_transport.connect(username=username, password=password)  #connecting to ssh server using ssh_transport information, username and password
    print('connected\n')
    sftp_session =paramiko.SFTPClient.from_transport(ssh_transport) #now connecting for sftp using ssh with ssh_transport
    print('sftp session connected\n')
    
    folder=""
    while True:      #while loop to go into directories
        a=sftp_session.listdir()
        print("...............these are the directories available............")    # loop to show all directories in different lines
        for i in a:
            print i
        file_path=raw_input("enter the folder name or if it is in the root directory press enter\n")
        if file_path=="":   # if you leave it blank or press enter without entering anything it'll break and make it your directory and ask you to choose a file name
            break
        else:
            folder=folder+file_path+"/"
            sftp_session.chdir(file_path)
        
    
          
    target_file=raw_input('enter file name\n')
    full_path=folder+target_file 
    
    sftp_session.get(target_file,target_file) #as we change the present directory it will change the file from current folder the syntax of get is ("full path including file name","file name")  
    print("Downloaded file from: %s" %full_path)#it'll show the path
    sftp_session.close()

def sftp_upload(username, password, hostname,port):
    """function for uploading through sftp session"""
    ssh_transport=paramiko.Transport((hostname, port))   #it transport username and port to a variable (ssh_transport),we use double brackets because it is the syntax and it is taking to valuejust like tuple and assigning into 1
    ssh_transport.connect(username=username, password=password)  #connecting to ssh server using ssh_transport information, username and password
    print('connected\n')
    sftp_session =paramiko.SFTPClient.from_transport(ssh_transport) #now connecting for sftp using ssh with ssh_transport
    print('sftp session connected\n')
    
    folder=""
    path="/Users/rishabh"
    while True:        #while loop to go into directories
        a=os.listdir(path)    #os commands are ussed to do anything on our own machine so in this we are listing directories on the path assigned above
        for i in a:
            print i
        print("...............these are the directories available............")    
        file_path=raw_input("enter the folder name or if it is in the root directory press enter\n")
        if file_path=="":
            break
        else:
            folder=folder+file_path+"/"
            path=path+"/"+file_path
            os.chdir(path)
        
    
    sftp_session.chdir("/root/Desktop/uploads") #changing the directory of server so every file will be uploaded to that place         
    target_file=raw_input('enter file name\n')
    full_path=path+"/"+target_file
    if target_file!="":
        sftp_session.put(target_file,target_file) #as we change the present directory it will change the file from current folder the syntax of put is ("file name","full path including file name")   
    else:
        sftp_session.put(path,path)
    print("uploaded file from: %s" %full_path)
    print("uploaded")
    sftp_session.close()    
#getting all the information from user and then passing it to function
host=raw_input('enter hostname => ')
username= raw_input('enter username => ')
password = getpass.getpass(prompt="Enter your password =>  ")
port=int(raw_input('enter port => '))

options=['1.download file from server','2.upload file to server']
for i in options:
    print(i)
opt=int(raw_input('what do you want to do => '))    
if opt==1:
    sftp_download(username,password,host,port) #calling the download function with passing these parameters
elif opt==2:
    sftp_upload(username,password,host,port)  #calling the upload function with passing these parameters
