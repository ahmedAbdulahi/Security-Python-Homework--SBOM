
import os
import sys
import csv
import json
import subprocess

original_path = os.getcwd()

def create_sbom(path):
   
    file_json = 'package.json'
    file_txt = 'requirements.txt'
    file_js = 'package-lock.json'

    if not os.path.exists(path): #Check for if the given path exists
        print("Error: Given directory does not exist: ", path)
        sys.exit(1)
    
    
    sbomData = []
    
    for dirpath,_,filenames in os.walk(path): #Looping through all the directories
      for filename in filenames: #Looping through all the files inside chosen directory
            if filename == file_txt:
                
                update_with_req(os.path.join(dirpath, filename),sbomData)
            elif filename == file_json or filename == file_js:
               
                update_with_json(os.path.join(dirpath, filename),sbomData)
    os.chdir(original_path) #changes back to original working directory, so it saves the files in the correct spot
    
    if len(sbomData)==0:
        print('Error: No source code repositories found')
        sys.exit(1)
    else:
        save_as_csv(sbomData,path)
        save_as_json(sbomData,path)
    

"""
This function takes in the path to the requirements file and the datastructure for sbom.
It updates the datastructure with the needed information(name,version,type,path) and
gives an error message if it doesnt have sufficient data
"""
def update_with_req(path,sbomData):
    name = None
    version = None
    commit = None
    commit = get_git_commit_hash(path.strip('/requirements.txt'))
    with open(path,'r') as f:
        for line in f:
            if line:
                name,version = line.split("==") 

    if name: #If name exists then we add it to the sbom list. If not we give the user an error message
        sbomData.append({'Name': name, 'Version': version, 'Type': 'pip', 'Path': path,'Git commit':commit})
    else:
         print('Error: No dependency found')

"""
This function takes in the path to the package.json file and the datastructure for sbom.
It updates the datastructure with the needed information(name,version,type,path) and
gives an error message if it doesnt have sufficient data
"""
def update_with_json(path,sbomData):
    
    name = None
    version = None
    commit = get_git_commit_hash(path.split('/package')[0])
    with open(path, 'r') as f:
        data = json.load(f)
        name,version = data['name'],data['version']
    
    if name: #If name exists then we add it to the sbom list. If not we give the user an error message
            sbomData.append({'Name': name, 'Version': version, 'Type': 'npm', 'Path': path,'Git commit':commit})
    else: 
        print('Error: No dependency found')

def save_as_csv(sbomData,path):
    
    with open('sbom.csv','w+',newline='') as file:
        fieldnames = ['Name', 'Version','Type','Path','Git commit']
        writer = csv.DictWriter(file, fieldnames=fieldnames) #We create a dictwriter object given the fieldnames we created and write the data from the sbom out to the file.
        writer.writeheader()
        for data in sbomData:
            writer.writerow(data)
    print('Saved SBOM in CSV format to '+os.getcwd()+'/sbom.csv')
def save_as_json(sbomData,path):
    
    with open('sbom.json','w+') as file:
        json.dump(sbomData,file,indent=2)
      
    
    print('Saved SBOM in CSV format to '+os.getcwd()+'/sbom.json')

def get_git_commit_hash(repo_path):

    os.chdir(os.path.abspath(os.sep) )#Changes diretory to root so it can redirect to where the repo lies. 
    os.chdir(os.path.join(os.getcwd(),repo_path)) #changes diretory too where the repo is.
    try:
        # Run the git log command to get the latest commit hash
        command = f"git log --format='%H' -n 1"
        commit_hash = subprocess.check_output(command, shell=True, text=True).strip() #Runs the command and saves the hash
        
        return commit_hash
    except subprocess.CalledProcessError:
        print(f"Error: Unable to retrieve Git commit hash for repository at '{repo_path}'.")
        sys.exit(1)
    
   
if __name__== '__main__':
    if len(sys.argv) <2:
        print('Error: Please provide a directory')
    elif len(sys.argv) >2:
        print('Error: Too many arguments. Please provide only 1 directory ')
    else:
        create_sbom(sys.argv[1])
    