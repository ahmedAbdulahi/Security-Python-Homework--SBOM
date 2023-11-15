from sbom import create_sbom
import os
def test_create_sbom():
    passed = 0
    create_sbom('/Users/ahmedabdulahiahmed/Documents/IN3110')
    if not os.path.exists('/Users/ahmedabdulahiahmed/Documents/IN3110/sbom.json') and not os.path.exists('/Users/ahmedabdulahiahmed/Documents/IN3110/sbom.csv'):
        print("Test 1 failed")
    else:
        print("------------Test 1 passed------------")
        passed+=1
    with open('/Users/ahmedabdulahiahmed/Documents/IN3110/sbom.csv') as f:
        
        if not f.readline() == 'Name,Version,Type,Path,Git commit,Last updated':
            print(f.read(100))
            print('Test 2 failed')
        else:
            print("------------Test 2 passed------------")
            passed+=1
    if passed == 2:
        print("Congratulations, the code passed every tested")




if __name__== '__main__':
    test_create_sbom()