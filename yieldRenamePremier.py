import os, glob, re, time
import zipfile, shutil

#matches how premier exports yield files
fileRegex = re.compile(r"SciMax Solutions_SciMax_Christians Farms_(.*)_(\w*)_Yield20(\d\d) PT(\.)(\w*)")
#for loop to go through current directory. Program needs to be saved in current directory
#def renameFiles():
for path, subdirs, files in os.walk(os.getcwd()):
    #creates a list of filename. Need to iterate through that list
    for fileName in files:
        mo = fileRegex.search(fileName)
        #skip if it is not a match object
        if mo == None:
            print('This file does not match naming system')
            continue
        #replace field name without spaces
        fieldName = mo.group(1)
        fieldName = fieldName.replace(' ', '')
        #should convert to field name year plus file ext.
        newName = fieldName+mo.group(3)+mo.group(4)+mo.group(5)
        #rename file
        os.rename(fileName, newName)



time.sleep(10)

newFileRegex = re.compile(r"(.*)\.(.*)")
for path, subdirs, files in os.walk(os.getcwd()):
    fileNameList = []
    for fileName in files:
        mo = newFileRegex.search(fileName)
        if mo == None:
            print('This object does not match naming system')
            continue
        if mo.group(2) != ('shp' or 'dbf' or 'shx'):
            continue
        fieldName = mo.group(1)
        if fieldName not in fileNameList:
            fileNameList.append(fieldName)


zippedFilesList = []
for fileName in fileNameList: 
    with zipfile.ZipFile(f'{fileName}.zip', 'w') as zipF:
        zippedFilesList.append(f'{fileName}.zip')
        zipFileNames = [f'{fileName}.shp', f'{fileName}.dbf', f'{fileName}.shx']
        for file in zipFileNames:
            zipF.write(file, compress_type=zipfile.ZIP_DEFLATED)


if 'zippedFiles' not in os.listdir():
    os.mkdir('zippedFiles')

for i in zippedFilesList:
    shutil.move(i, 'zippedFiles')




