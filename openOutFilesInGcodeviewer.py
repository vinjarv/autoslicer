import subprocess, os
slicerPath = "C:\\Program Files\\Prusa3D\\PrusaSlicer\\prusa-slicer-console.exe"
outFilesPath = "C:\\Users\\vinja\\OneDrive\\Documents\\VSCode\\Python\\Autoslicer_testing\\outputFiles"


files = os.listdir(".\\outputFiles")
for file in files:
    print(file)
    subprocess.run([slicerPath, "--gcodeviewer", outFilesPath + "\\" + file])