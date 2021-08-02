import subprocess
import tempfile

import numpy as np
from stl import Mesh

class AutoSlicer:
    config = "" # will get from fileMonitor.py
    inputFile = "" 

    # Select slicer parameters based on unprintability > treshold
    treshold_supports = 1.0
    treshold_brim = 2.0


    def __tweakFile(self, inputFile, dir):
        try:
            outputFile = dir + "\\tweaked.stl"
            result = subprocess.run(["python", self.config["PATHS"]["tweaker"] + "\\Tweaker.py", "-i", inputFile, "-o", outputFile, "-x", "-vb"]
                                    , capture_output=True, text=True).stdout
            _, temp = result.splitlines()[-5].split(":")
            unprintability = str(round(float(temp.strip()), 2))
            print("Unprintability: " + unprintability)
            print(result)
            print(outputFile)
            return outputFile, unprintability
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


    def __runSlicer(self, inputFile, initialName, unprintability):
        filename, _ = initialName.split(".")
        filename = filename.replace(" ", "_") # Remove spaces
        outputFile = self.config["PATHS"]["outputDirectory"] + "\\" + filename + "_U" + str(unprintability) + "_{print_time}" ".gcode"

        cmd = [self.config["PATHS"]["slicer"], "--load", self.config["PATHS"]["slicerConfig"]]

        if float(unprintability) > self.treshold_brim:
            cmd.extend(["--brim-width", "5", "--skirt-distance", "6"])
        if float(unprintability) > self.treshold_supports:
            cmd.append("--support-material")

        cmd.extend(["-g", "-o", outputFile, inputFile])
        print(cmd)
        try:
            subprocess.run(cmd)
        except:
            print("Couldn't slice file " + self.inputFile)


    def slice(self, input, configParsed, initialName):
        self.inputFile = input
        self.config = configParsed
        with tempfile.TemporaryDirectory() as tempDirectory:
            print(tempDirectory)
            tweakedFile, unprintability = self.__tweakFile(self.inputFile, tempDirectory)
            translatedFile = self.__adjustHeight(tweakedFile, tempDirectory)
            self.__runSlicer(translatedFile, initialName, unprintability)