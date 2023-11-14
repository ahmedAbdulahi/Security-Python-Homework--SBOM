# Security-Python-Homework--SBOM
Command line tool for finding and documenting dependencies and their versions



Assumptions:

1. I assume that if its a requirements.txt then the type is pip and if its a package.json file then the type is npm.

2. I assume that if the file does not have a name value then the it is not a valid dependency and therefore is not needed in the sbom.