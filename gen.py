import json
import os
import re
import time
import zipfile


# Match Dirs which matches regex
consider_dirs='Month?'

# dict contains :
file_dict={}
current_dir="./Work"
summary_path="./Task.txt"
summary_json="./Task.json"
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
    print("File Path --> ",file_path)
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

def store_data(summary_location,summary_json,scan_dir):

    with open(summary_location,'w') as writer:
        updated_dict={}
        new_dict=get_file_data(scan=scan_dir)
        old_dict={}
        if os.path.exists(summary_json):
            with open(summary_json,'r') as reader:
                try:
                    old_dict=json.load(reader)
                    print("===?>",old_dict)
                except Exception as e:
                    print("Error Occured ",e )

        if not old_dict:
            updated_dict=new_dict
        else:
            updated_dict=new_dict | old_dict

        for k,v  in updated_dict.items():
            content_structure(writer=writer,file_path=k,file_model=v)
    with open(summary_json,'w') as writer:
        writer.write(json.dumps(updated_dict))




# Get File Names in the Current Directory
def get_file_data(scan):
    print("Scaning dir ==> ",scan)
    for obj in os.scandir(scan):
        print("objects in scandir() ==> ",obj)
        if obj.is_dir() & bool(re.match(consider_dirs,obj.name)):
            print("dir objects in scandir() ==> ",obj);
            
            for files in os.scandir(obj):

                if files.is_file():
                    with open(files.path,'r') as current_file_data:
                        file_model={}
                        
                        file_model['last_modification']=time.ctime(os.path.getmtime(files.path))
                        file_model['content']=current_file_data.readlines();
                        file_dict[files.path]=file_model
                        print("File Dictionary Details --> ",file_dict)
                        # backup_file(file_path=files.path)
                        # delete_file(file_path=files.path)    
                    # print(files.path)
    print(file_dict)
    return file_dict;


# Main 
store_data(summary_location=summary_path,summary_json=summary_json,scan_dir=current_dir)