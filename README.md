# Security-Python-Homework--SBOM
Command line tool for finding and documenting dependencies and their versions



Assumptions:

1. I assume that if its a requirements.txt then the type is pip and if its a package.json file then the type is npm.

2. I assume that if the file does not have a name value then the it is not a valid dependency and therefore is not needed in the sbom.

3. I am not too sure of what an indirect dependency is so i just assumed it was the everything that was inside the dependencies object inside the node_modules.

Known issues/Bugs:

Something that could be an issue later on is if the structure of a package.json or package-lock.json is changed later on
then the code has to be changed also. Currently its very reliant that the structure is the same as the examples given in the homework assignment

Ideas:

1. To add an automatic pipeline so that when the package.json or package-lock.json file is changed then the code automatically runs.
2. Add a review column for each package
3. Develop a GUI.