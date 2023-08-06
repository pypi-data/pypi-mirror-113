# Stuff to help my memory

"""

### FILE MANAGEMENT ###

Write - Writes things but will repeat.
Append - Delets all file contents and updates with new.
Delete - Deletes given file.
ContentDelete - Deletes content in given file.
Create - Creates given filename.
Duplicate - Duplicates given filename, along with makes new filename for duplicated file.
Rename - Renames file given to new file name.

"""

# Import Shitz
import os
import shutil

# FruityScript

class fileM():
        ## WRITE

        ## WARNING ##
        # The write function will automatically repeat writing what you put inside everytime you run your project, please use with caution.

    def write(filename, data=None):
        if data is None:
            DataError = 'ERROR: Data not supplied!'
            
            return print(DataError)

        with open(filename, 'a+') as fs:
            fs.write(data)
            fs.close()

    ## APPEND

    ## WARNING ##
    # This will delete all file contents and update it with the file contents you wanted it to update with, use with caution.

    def append(fileName, toAppend=None):
        if toAppend is None:
            AppendError = 'ERROR: toAppend not supplied!'

            return print(AppendError)

        with open(fileName, 'w') as fs:
            fs.write(toAppend)
            fs.close()

    ## DELETE

    ## WARNING ##
    # This will delete the given file, use with caution.

    def delete(toDelete=None):
        if toDelete is None:
            DeleteError = 'ERROR: toDelete not supplied!'

            return print(DeleteError)
        
        os.remove(toDelete)

    ## CONTENTDELETE
    ## WARNING ##
    # This will delete all content in your file, use with caution.

    def contentDelete(file=None):
        if file is None:
            ContentError = 'ERROR: file not supplied!'

            return print(ContentError)

        with open(file, 'w') as fs:
            fs.flush()

    ## CREATE
    # No warnings lol

    def create(filename=None):
        if filename is None:
            FileError = 'ERROR: filename not supplied!'

            return print(FileError)
        
        with open(filename, 'w+') as fs:
            return

    ## COPY

    ## WARNING ##
    # This may be a cool feature but looping this could really hurt your computer, especially lag of some sort, just use it with caution.

    def duplicate(filename=None, duplicateName=None):
        if filename is None:
            FileError = 'ERROR: filename not supplied!'

            return print(FileError)
        
        if duplicateName is None:
            duplicateError = 'ERROR: duplicateName not supplied!'

            return print(duplicateError)

        shutil.copy(filename, duplicateName)

    ## RENAME
    # No warnings lol (Do not recommend looping ig idk)

    def rename(filename, newName=None):
        if newName is None:
            newNameError = 'ERROR: newName not supplied!'

            return print(newNameError)

        os.rename(filename, newName)

    def compressDir(nameOfZip=None):
        if nameOfZip is None:
            ZipNameError = 'ERROR: nameOfZip not supplied!'

            return print(ZipNameError)
        
        shutil.make_archive(nameOfZip, 'zip')
    
class script():

    ## MUSH
    ## Warnings ##
    # This will mush anything you put inside together, try it lol.

    def mush(input1=None, input2=None):
        if input1 is None:
            InputError = 'ERROR: Input1 not supplied!'

            return print(InputError)
        if input2 is None:
            InputError = 'ERROR: Input2 not supplied!'

            return print(InputError)
        
        return (input1 + input2)

    ## EXECUTE
    
    ## WARNINGS ##
    # This will execute ANYTHING you put inside, use with caution.

    def execute(input):
        if input is not str():
            pass

        if input is None:
            InputError = 'ERROR: Input not supplied!'

            return print(InputError)
        
        if input is TypeError:
            return

        return exec(input)