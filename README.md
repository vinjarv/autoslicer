# autoslicer
Python script for automatic slicing of STL files with PrusaSlicer

autoslicer.py works either as a python module or a command line tool
Usage:

Python:
```python
import autoslice

autoslicer = AutoSlicer(slicer_path="C:/Program Files/Prusa3D/PrusaSlicer/prusa-slicer-console.exe" config_path="Config/MK3Sconf.ini")
autoslicer.slice("inputFiles/input.stl", "outputFiles")
```

Or from command line:
```bash
python autoslice.py inputFiles/input.stl Config/MK3Sconf.ini "C:/Program Files/Prusa3D/PrusaSlicer/prusa-slicer-console.exe" -o outputFiles
```