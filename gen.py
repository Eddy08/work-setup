import os
import time
import zipfile
# dict contains :
file_dict={}
store_location="./Task.txt"
backup_location="Backup.zip"
#List of Folders already inside the backup location
backup_folders=[]
# First Default Folder name in Backup Zip ( for First Time):
default="Month1"
## Adding the File to Zip inside the new folder name
def add_file_to_zip(backup_location,file_path,folder_name=None):
    if folder_name is not None:
        global default
        default=folder_name
    print("Backing up to" ,backup_location)    
    with zipfile.ZipFile(backup_location, mode="a") as archive:
        archive.write(file_path,default,zipfile.ZIP_DEFLATED )

## Geting the new folder name in the zip
def new_folder_name(files):
    for obj in files:
        if(obj.is_dir()):
            backup_folders.append(obj)

    return backup_folders[-1] if len(backup_folders) >=1  else []

##Backup File in a zip folder specified in the backup_location
def backup_file(file_path,backup_location=backup_location):
    print("Backing Up the File in "+backup_location)
    if os.path.exists(backup_location) & zipfile.is_zipfile(backup_location):
        with zipfile.ZipFile(backup_location,'r') as backup:
            add_file_to_zip(backup_location=backup_location,file_path=file_path,folder_name=new_folder_name(files=backup.infolist()))
    else:

        add_file_to_zip(backup_location=backup_location,file_path=file_path)
        
## Delete the File from the system

def delete_file(file_path):
    print("Deleting the File")


# Content structure

def content_structure(writer,file_path,file_model):
            writer.writelines("\n"+"#"*10+"\n")
            writer.writelines(
                "name :"+file_path+"\n"
            +"last-modified: "+file_model['last_modification'] +"\n\n" 
            +"content:"+"\n"         
            )
            writer.writelines(file_model['content'])
            writer.writelines("\n"+"#"*10+"\n")


# Get File Dict Data and Store it in the Task Folder

def store_data(location):

    with open(location,'a') as writer:
        for k,v  in get_file_data().items():
            content_structure(writer=writer,file_path=k,file_model=v)



# Get File Names in the Current Directory
def get_file_data():
    for obj in os.scandir():
        if obj.is_file():
            with open(obj.path,'r') as current_file_data:
                file_model={}
                
                file_model['last_modification']=time.ctime(os.path.getmtime(obj.path))
                file_model['content']=current_file_data.readlines();
                file_dict[obj.path]=file_model
                backup_file(file_path=obj.path)
                delete_file(file_path=obj.path)    
            # print(obj.path)
    print(file_dict)
    return file_dict;


# Main 
store_data(location=store_location)