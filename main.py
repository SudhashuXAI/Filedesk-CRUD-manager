from pathlib import Path
import os

def createfile():
    try:
        name = input("please tell your file name :-")
        path = Path(name)
        if not path.exists():
            with open(path , "w") as fs:
                data = input("what you want write")
                fs.write(data)
                print("file successfully created")
        else:
            print("file already exists ")    
    except Exception as err:
        print(f"An {err} has occured ")

def readfile():
        try:
                
            name = input("please tell your file name :-")
            path = Path(name)
            if path.exists():
                with open(path,"r") as fs:
                    content = fs.read()
                    print(f"your file content is \n {content} ")
            else:
                print(" Error! No such files is exists ")        
                    
        except Exception as err:
            print(f"An {err} has occured there !")

def updatefile():
        name = input("please tell your file name :-")
        path = Path(name)

        if path.exists():
            print("1. Renaming the  file ")
            print("2. Erasing the content inside the file ")
            print("3. Appending content in the  file ")
            print("4. Overwritting  the file ")

            choice = int(input("Choose the one of the options to update the file :- "))

            if choice ==1:
                try:
                    New_name = input("New name of the file ")
                    New_path = Path(New_name)
                    if not New_path.exists():
                        path.rename(New_name)
                    else:
                        print("!! Sorry !! this file is already exists.")

                except Exception as err:
                    print(F"An {err} has occured ")

            elif choice == 2:
                try:
                    name = input("please tell your file name :-")
                    path = Path(name)
                    with open(path, "w") as fs:
                        fs.write("") 
                    print("file cleared successfully")

                except Exception as err:
                    print(f"An {err} has occured ")
                
            elif choice == 3:
                try:
                    name = input("please tell your file name :-")
                    path = Path(name)
                    with open(path,"a") as fs:
                        data = input(" write the content you want to add in a file\n :- ")
                        fs.write("\n "+data)
                    print(" Added successfully  ")    
                except Exception as err:
                    print(f"An {err} has ocurred ")

            elif choice == 4:
                try:
                    name = input("please tell your file name :-")
                    path = Path(name)
                    with open(path,"a") as fs:
                        data = input(" what do you want to overwrite\n :- ")
                        fs.write(" "+data)
                        print("Successfully overwriten  ")    
                except Exception as err:
                        print(f"An {err} has ocurred ")

def deletefile():
    try:
        name = input("please tell your file name :-")
        path = Path(name)
        if path.exists():
            path.unlink()
            print(" Deleted Successfully ")
        else:
            print(" !! Error !! file not exixts ")
    except Exception as err:
        print(f"An {err} has ocurred ")    

  
print("press 1 for creating a file ")
print("press 2 for reading a file ")
print("press 3 for updating a file ")
print("press 4 for deleting a file ")

a = int(input("tell your response :-"))

if a ==1:
    createfile()

if a == 2:
    readfile()

if a == 3:
    updatefile()

if a == 4:
    deletefile()  