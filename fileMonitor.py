import subprocess
import time
import os
import ntpath
import autoslice

class Watcher:
    DIRECTORY_TO_WATCH = ".\\inputFiles"
    DIRECTORY_OUT = ".\\outputFiles"
    autoslicer = autoslice.AutoSlicer()

    def __init__(self):
        print("Watching", self.DIRECTORY_TO_WATCH)

    def __getValidFiles(self):
        # Get list of all files and directories in monitored directory
        allFiles = os.listdir(self.DIRECTORY_TO_WATCH)
        validFiles = []

        # Check all files for type, store all STL files in validFiles
        for file in allFiles:
            try:
                # Separate file name and extension
                [name, extension] = file.split(".", 2)
                #print("File name:", name)
                #print("File extension:", extension)
                if extension.lower() == "stl":
                    #print("Valid STL file found")
                    validFiles.append(file)
            except:
                print("Invalid file found: ", file)

        #print("Current folder content:")
        #print(validFiles)
        return validFiles

    def run(self):
        try:
            while True:
                # Get list of STL files in input folder
                validFiles = self.__getValidFiles()
                for file in validFiles:
                    inputFile = self.DIRECTORY_TO_WATCH + "\\" + file

                    try:
                        self.autoslicer.slice(inputFile, self.DIRECTORY_OUT, file)
                    except:
                        print("Couldn't slice file " + file)

                    try:
                        os.remove(inputFile)
                    except:
                        print("Couldn't delete file " + file)

                # Delay between checks
                time.sleep(2)
        except:
            print ("Error")

if __name__ == '__main__':
    w = Watcher()
    w.run()