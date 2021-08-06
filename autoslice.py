import subprocess
import tempfile

import numpy as np
import os
from stl import Mesh

class AutoSlicer:
    config = "" # will get from fileMonitor.py
    inputFile = "" 

    # Select slicer parameters based on unprintability > treshold
    treshold_supports = 1.0
    treshold_brim = 2.0


    def __tweakFile(self, input_file, dir):
        try:
            outputFile = os.path.join(dir, "tweaked.stl")
            print(outputFile)
            if os.name == "nt":
                python_path = os.path.join(os.getcwd(), "venv", "Scripts", "python")
            else:
                python_path = os.path.join(os.getcwd(), "venv", "bin", "python")
            tweaker_path = os.path.join(
                os.getcwd(),
                self.config["PATHS"]["tweaker"], 
                "Tweaker.py"
            )
            result = subprocess.run([python_path, tweaker_path, "-i", input_file, "-o", outputFile, "-x", "-vb"]
                                    , capture_output=True, text=True).stdout
            _, temp = result.splitlines()[-5].split(":")
            unprintability = str(round(float(temp.strip()), 2))
            print("Unprintability: " + unprintability)
            print(result)
            print(outputFile)
            return outputFile, unprintability
        except:
            print("Couldn't run tweaker on file " + self.input_file)


    def __adjustHeight(self, input_file, dir):
        try:
            output_file = os.path.join(dir, "translated.stl")
            my_mesh = Mesh.from_file(input_file)
            print("Z min:", my_mesh.z.min())
            print("Z max:", my_mesh.z.max())
            translation = np.array([0, 0, -my_mesh.z.min()])
            my_mesh.translate(translation)
            print("Translated, new Z min:", my_mesh.z.min())
            my_mesh.save(output_file)
            return output_file
        except:
            print("Couldn't adjust height of file " + self.input_file)


    def __runSlicer(self, input_file, initial_name, unprintability):
        filename, _ = initial_name.split(".")
        filename = filename.replace(" ", "_") # Remove spaces

        cwd = os.getcwd()

        input_file = os.path.join(
            cwd,
            input_file
        )
        output_file = os.path.join(
            cwd,
            self.config["PATHS"]["outputDirectory"],
            (filename + "_U" + str(unprintability) + "_{print_time}" ".gcode")
            )
        slicer_loc = os.path.join(
            cwd,
            self.config["PATHS"]["slicer"]
        )
        config_loc = os.path.join(
            cwd,
            self.config["PATHS"]["slicerConfig"]
        )

        cmd = [slicer_loc, "--load", config_loc]

        if float(unprintability) > self.treshold_brim:
            cmd.extend(["--brim-width", "5", "--skirt-distance", "6"])
        if float(unprintability) > self.treshold_supports:
            cmd.append("--support-material")

        cmd.extend(["-g", "-o", output_file, input_file])
        print(cmd)
        try:
            subprocess.run(cmd)
        except:
            print("Couldn't slice file " + self.input_file)


    def slice(self, input, config_parsed, initial_name):
        self.input_file = input
        self.config = config_parsed
        with tempfile.TemporaryDirectory() as temp_directory:
            print(temp_directory)
            tweakedFile, unprintability = self.__tweakFile(self.input_file, temp_directory)
            translatedFile = self.__adjustHeight(tweakedFile, temp_directory)
            self.__runSlicer(translatedFile, initial_name, unprintability)