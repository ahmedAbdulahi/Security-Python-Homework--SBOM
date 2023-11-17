
import os
import sys
import csv
import json
import subprocess
import time



def create_sbom(path):
   
    file_json = 'package.json'
    file_txt = 'requirements.txt'
    file_js = 'package-lock.json'

    if not os.path.exists(path): #Check for if the given path exists
        print("Error: Given directory does not exist: ", path)
        sys.exit(1)
    
    
    sbom_data = []
    
    len_repo = 0 #how many repos the code found inside the directory
    for dirpath,_,filenames in os.walk(path): #Looping through all the directories
      for filename in filenames: #Looping through all the files inside chosen directory
            if filename == file_txt:
                
                update_with_req(os.path.join(dirpath, filename),sbom_data)
                len_repo+=1
            elif filename == file_json or filename == file_js:

                update_with_json(os.path.join(dirpath, filename),sbom_data)
                len_repo+=1
    os.chdir(path) #changes back to original working directory, so it saves the files in the correct directory
    
    if len(sbom_data)==0:
        print('Error: No source code repositories found')
        sys.exit(1)
    else:
        print("Found",len_repo,"repositories in",path)
        save_as_csv(sbom_data,path)
        save_as_json(sbom_data,path)
    

"""
This function takes in the path to the requirements file and the datastructure for sbom.
It updates the datastructure with the needed information(name,version,type,path,date) and
gives an error message if it doesnt have sufficient data
"""
def update_with_req(path,sbom_data):
    name = None
    version = None
    commit = None
    commit = get_git_commit_hash(path.strip('/requirements.txt'))
    found = False #This variable will be set to true if we find a dependency
    current_date = time.ctime(time.time()) #Gets the current date
  
    with open(path,'r') as f:
        for line in f:
            name = None
            version = None
            if line and '==' in line:
                name,version = line.split("==") 
            else:
                name = line

            if name: #If name exists then we add it to the sbom list. If not we give the user an error message
                 sbom_data.append({'Name': name, 'Version': version, 'Type': 'pip', 'Path': path,'Git commit':commit,'Last updated':current_date})
                 found = True
    if not found: print("Error: No dependencies found for this file",path)

"""
This function takes in the path to the package.json file and the datastructure for sbom.
It updates the datastructure with the needed information(name,version,type,path,date) and
gives an error message if it doesnt have sufficient data
"""
def update_with_json(path,sbom_data):
   
    commit = get_git_commit_hash(path.split('/package')[0]) 

    current_date = time.ctime(time.time()) #Gets the current date
    
  
    with open(path, 'r') as f:
        data = json.load(f)
        
        if 'dependencies' in data.keys():  #check for if the dependencies dict is in the top layer
            
            #loop through both the dependencies and devdependcies dictionaries to extract information and put it in the data structure
            for dependency in data['dependencies'].keys():
                sbom_data.append({'Name': dependency, 'Version': data['dependencies'][dependency], 'Type': 'npm', 'Path': path,'Git commit':commit,'Last updated':current_date})
            if 'devDependencies' in data.keys(): #checks for if it also has a devdependencies dictionary.
                for dependency in data['devDependencies'].keys():
                    sbom_data.append({'Name': dependency, 'Version': data['devDependencies'][dependency], 'Type': 'npm', 'Path': path,'Git commit':commit,'Last updated':current_date})

        elif 'packages' in data.keys(): #then we know its package-lock.json file
            other_libraries = data['packages'] #package-lock.json files have dependencies in other places than dependencies and devDepencies.
            for dependency,details in other_libraries.items(): 

                if dependency.startswith('node_modules') and 'dependencies' in details.keys():
                         indirect_dependencies = details['dependencies']

                         for indirect_dependency,version in indirect_dependencies.items(): 
                             sbom_data.append({'Name': indirect_dependency, 'Version': version, 'Type': 'npm', 'Path': path,'Git commit':commit,'Last updated':current_date})

        else: print("Error: No dependencies found for this file",path)
    
def save_as_csv(sbom_data,path):
    
    file_path = os.path.join(path,'sbom.csv')
    with open(file_path,'w+',newline='') as file:
        fieldnames = ['Name', 'Version','Type','Path','Git commit','Last updated']
        writer = csv.DictWriter(file, fieldnames=fieldnames) #We create a dictwriter object given the fieldnames we created and write the data from the sbom out to the file.
        writer.writeheader()
        for data in sbom_data:
            writer.writerow(data)
    print('Saved SBOM in CSV format to ',file_path)

def save_as_json(sbom_data,path):
    file_path = os.path.join(path,'sbom.json')
  
    with open(file_path,'w+') as file:
        json.dump(sbom_data,file,indent=2)
      
    
    print('Saved SBOM in JSON format to ',file_path)

#This function takes in the path to the repo and return the git commit message
def get_git_commit_hash(repo_path):

    os.chdir(os.path.abspath(os.sep) )#Changes diretory to root so it can redirect to where the repo lies. This command should go for every operating system.
    os.chdir(os.path.join(os.getcwd(),repo_path)) #changes diretory too where the repo is.
    try:
        # Run the git log command to get the latest commit hash
        command = f"git log --format='%H' -n 1"
        commit_hash = subprocess.check_output(command, shell=True, text=True).strip() #Runs the command and saves the hash
        
        return commit_hash
    except subprocess.CalledProcessError:
        print(f"Error: Unable to retrieve Git commit for repository at '{repo_path}'.")
        sys.exit(1)
    
   
if __name__== '__main__':
    if len(sys.argv) <2:
        print('Error: Please provide a directory')
    elif len(sys.argv) >2:
        print('Error: Too many arguments. Please provide only 1 directory ')
    else:
        create_sbom(sys.argv[1])
    