# BLAST Project (Airblas Parameters By Distance, By NEQ, By TNT Equivalence)
# author: Ilmo Koo (johnnykoo84@gmail.com)
# project: 2018-02 2 weeks

## files

### source files
- param.py: for airburst & surface sub-calculation (e.g. getting Ps, Is, Pr, Ir ...etc)
- eval_param.py: for evaluating intermediate results (e.g. f(U), f(U^2), Y, Anti-log Y ... etc)
- render.py: to render a GUI screen which runs on windows or OSX. It has input features and rendering figures based on the calculations in eval_param.py

### static files
- dimension.png: provided by the client. This picture is positioned in the program

### spec files
- BLC.spec: this is a config file for creating execuatable program (e.g. *.exe) instead of running python source code. This works with pyinstaller.

### libraries used
- math: for calculation
- numpy: for calculation
- matplotlib: for plots
- tkinter: GUI helper
- pyinstaller: to create OS dependent executable program

### environment info
- python v3.6.4 used

### general strategy
1. in param.py we define all the reusable methods to get all the params
2. in eval_param.py we have actual slopes data and plug them in into all the methods to get blas parameters in param.py
3. Here, we make a window program and render some input boxes, and also plot the results.


## Source Code (explained)

### general overview
1. render.py calls eval_param.py
2. eval_param.py calls param.py
Therefore, param.py runs first, eval_param.py runs second, lastly, render.py code runs and execute the window-like program

3. how class (OOP works here)
class someClassName
  someInitialValues1=...
  someInitialValues2=...
  someInitialValues3=...

  when this class is called, below __init__ is executed with class inputs (arguments)
  def __init__(self, input1, input 2, ...):

  def otherMethods...
  ...
  def otherMethods...
  ...


## Q&A
1. in some files, we find
if __name__ == "__main__"
  ...
  ...
what the heck is this?
answer) if there are some codes under if __name__ == "__main__", this means that the code under this statement only runs when this file was run directly

## how to bundle and publish window or osx program
### VERY IMPORTANT! this program runs depending on which Operating System you use

go to BLC.spec file, you need to update the following two lines based on your directory
1. line 7 pathex => your project directory
2. line 17 image_files => your image, dimension.png directory


save BLC.spec

in terminal or command line run below
pyinstaller .\BLC.spec
