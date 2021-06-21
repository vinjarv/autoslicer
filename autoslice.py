import numpy as np
from stl import Mesh
import subprocess
from octorest import OctoRest

slicerPath = "C:\\Program Files\\Prusa3D\\PrusaSlicer\\prusa-slicer-console.exe"
tweakerPath = "C:\\Users\\vinja\\OneDrive\\Documents\\VSCode\\Python\\Tweaker 3\\Tweaker-3"

inFile = "C:\\Users\\vinja\\Downloads\\BagClip_65.stl"
tweakedFile = "C:\\Users\\vinja\\Downloads\\tweakedMesh.stl"
translatedFile = "C:\\Users\\vinja\\Downloads\\movedMesh.stl"
finishedFile = "C:\\Users\\vinja\\Downloads\\output.gcode"

subprocess.run(["python", tweakerPath + "\\Tweaker.py", "-i", inFile, "-o", tweakedFile, "-x"])

myMesh = Mesh.from_file(tweakedFile)
print("Z min:", myMesh.z.min())
print("Z max:", myMesh.z.max())
translation = np.array([0, 0, -myMesh.z.min()])
myMesh.translate(translation)
print("Translated, new Z min:", myMesh.z.min())
myMesh.save(translatedFile)

subprocess.run([slicerPath, "--load", "C:\\Users\\vinja\\Downloads\\MK3Sconf.ini", "-g", "-o", finishedFile, translatedFile])

# client = OctoRest(url="http://octopi05.local", apikey="9159AB574FE84EB39B8C6760C23CDF2E")
# state = client.state()
# if (state == "Operational"):
#     client.upload(finishedFile)
#     client.select("output.gcode", print=True)
#     print("Print started on printer 05")
# else:
#     print("Printer not available, finished")