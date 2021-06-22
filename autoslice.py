import subprocess
import tempfile

import numpy as np
from octorest import OctoRest
from stl import Mesh


class AutoSlicer:
    # Program/config locations
    slicerPath = "C:\\Program Files\\Prusa3D\\PrusaSlicer\\prusa-slicer-console.exe"
    configPath = "C:\\Users\\vinja\\Downloads\\MK3Sconf.ini"
    tweakerPath = "C:\\Users\\vinja\\OneDrive\\Documents\\VSCode\\Python\\Tweaker 3\\Tweaker-3"

    inputFile = ""

    def __tweakFile(self, inputFile, dir):
        try:
            outputFile = dir + "\\tweaked.stl"
            subprocess.run(["python", self.tweakerPath + "\\Tweaker.py", "-i", inputFile, "-o", outputFile, "-x"])
            print(outputFile)
            return outputFile
        except:
            print("Couldn't run tweaker on file " + self.inputFile)


    def __adjustHeight(self, inputFile, dir):
        try:
            outputFile = dir + "\\translated.stl"
            myMesh = Mesh.from_file(inputFile)
            print("Z min:", myMesh.z.min())
            print("Z max:", myMesh.z.max())
            translation = np.array([0, 0, -myMesh.z.min()])
            myMesh.translate(translation)
            print("Translated, new Z min:", myMesh.z.min())
            myMesh.save(outputFile)
            return outputFile
        except:
            print("Couldn't adjust height of file " + self.inputFile)


    def __runSlicer(self, inputFile, dir, initialName):
        [filename, extension] = initialName.split(".")
        outputFile = dir + "\\" + filename + ".gcode"
        try:
            subprocess.run([self.slicerPath, "--load", self.configPath
                            , "-g", "-o", outputFile, inputFile])
        except:
            print("Couldn't slice file " + self.inputFile)

    def slice(self, input, outputPath, initialName):
        self.inputFile = input
        with tempfile.TemporaryDirectory() as tempDirectory:
            print(tempDirectory)
            tweakedFile = self.__tweakFile(self.inputFile, tempDirectory)
            translatedFile = self.__adjustHeight(tweakedFile, tempDirectory)
            self.__runSlicer(translatedFile, outputPath, initialName)
        




# inFile = "C:\\Users\\vinja\\Downloads\\BagClip_65.stl
# tweakedFile = "C:\\Users\\vinja\\Downloads\\tweakedMesh.stl"
# translatedFile = "C:\\Users\\vinja\\Downloads\\movedMesh.stl"
# finishedFile = "C:\\Users\\vinja\\Downloads\\output.gcode"

# subprocess.run(["python", tweakerPath + "\\Tweaker.py", "-i", inFile, "-o", tweakedFile, "-x"])

# myMesh = Mesh.from_file(tweakedFile)
# print("Z min:", myMesh.z.min())
# print("Z max:", myMesh.z.max())
# translation = np.array([0, 0, -myMesh.z.min()])
# myMesh.translate(translation)
# print("Translated, new Z min:", myMesh.z.min())
# myMesh.save(translatedFile)

# subprocess.run([slicerPath, "--load", "C:\\Users\\vinja\\Downloads\\MK3Sconf.ini", "-g", "-o", finishedFile, translatedFile])

# client = OctoRest(url="http://octopi05.local", apikey="9159AB574FE84EB39B8C6760C23CDF2E")
# state = client.state()
# if (state == "Operational"):
#     client.upload(finishedFile)
#     client.select("output.gcode", print=True)
#     print("Print started on printer 05")
# else:
#     print("Printer not available, finished")
