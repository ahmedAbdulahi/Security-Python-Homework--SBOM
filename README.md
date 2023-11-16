# Security-Python-Homework--SBOM
Command line tool for finding and documenting dependencies and their versions


How to run this project:
python3 sbom.py <Directory>

Example: python3 sbom.py /Users/ahmedabdulahiahmed/Documents/IN3110 


Assumptions:

1. A 'requirements.txt' file implies 'pip' as the package manager, and a 'package.json' file implies 'npm'

2. I assume that if the file does not have a name value then the it is not a valid dependency and therefore is not needed in the sbom.

3. I assume that an indirect dependency is anything within the 'dependencies' object inside the 'node_modules' directory.

Known issues/Bugs:

Potential issue: Code may be impacted if the structure of 'package.json' or 'package-lock.json' changes in the future. The current implementation relies heavily on the structure matching the provided examples in the homework assignment

Ideas:

1. Implement an automatic pipeline to trigger code execution when 'package.json' or 'package-lock.json' changes.
2. dd a review column for each package, allowing for package replacement based on scores
3. Develop a GUI.