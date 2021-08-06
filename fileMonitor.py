import time
import os
import configparser
import autoslice

# Set working directory to allow running autoslicer from another process

autoslicer_location = os.path.dirname(__file__)
print("Autoslicer location:", autoslicer_location)
if autoslicer_location != "":
    os.chdir(autoslicer_location)

config = configparser.ConfigParser()
config.read("./Config/config.ini")

class Watcher:
    DIRECTORY_TO_WATCH = config["PATHS"]["inputDirectory"]
    autoslicer = autoslice.AutoSlicer()

    def __init__(self):
        print("Watching", self.DIRECTORY_TO_WATCH)

    def __getValidFiles(self):
        # Get list of all files and directories in monitored directory
        allFiles = os.listdir(self.DIRECTORY_TO_WATCH)
        validFiles = []

        # Check all files for type, store all STL files in validFiles
        # TODO: Handle æøå, spaces - they don't work after uploading to octoprint
        # Force ASCII?
        for file in allFiles:
            try:
                # Separate file name and extension
                [name, extension] = file.rsplit(".", 1)
                if extension.lower() == "stl" or extension.lower() == "3mf":
                    #print("Valid STL file found")
                    validFiles.append(file)
            except:
                print("Invalid file found: ", file)

        return validFiles

    def run(self):
        try:
            while True:
                # Get list of STL/3MF files in input folder
                validFiles = self.__getValidFiles()
                for file in validFiles:
                    inputFilePath = os.path.join(self.DIRECTORY_TO_WATCH, file)

                    try:
                        self.autoslicer.slice(inputFilePath, config, file)
                    except:
                        print("Couldn't slice file " + file)

                    try:
                        # Clean folder to avoid endless loops on file
                        os.remove(inputFilePath)
                    except:
                        print("Couldn't delete file " + file)

                # Delay between checks
                time.sleep(2)
        except:
            print ("Error")

if __name__ == '__main__':
    w = Watcher()
    w.run()