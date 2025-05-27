Progress Update:
• Installed CPLEX and configured the environment.
• Successfully solved Vishnu’s code using CPLEX.
• Understood the structure and generation of .dat files.
• Analysed and understood the constraint definitions and the objective function in
the model.
• Developed an initial version of a Python script to generate inputs for .dat files.

25 May, 2025 updates

• We had a meeting with Vishnu.
• Understood the logic behind the code.
• Wrote a preprocessing code to prepare a list of possible node that a bus can
take.

26/06/2025

INTEGRATION OF CPLEX AND DOCPLEX 
1.installed python 3.10
2. Installed docplex library in jupyter 
3.through commands we integrated jupyter lab with cplex environment 
import sys
sys.path.append(r"C:\Program Files\IBM\ILOG\CPLEX_Studio_22.1.1\cplex\python\3.10\x64_win64")
import cplex
from docplex.mp.model import Model
4. py -3.10 -m venv cplex_env
5. cplex_env\Scripts\activate
6.cd "C:\Program 7.Files\IBM\ILOG\CPLEX_Studio2211\cplex\python\3.10\x64_win64"
python setup.py install
CONVERSION OF VISNU SIR ‘S CPLEX CODE INTO PYTHON DOCPLEX
1.Obtained the values of V  through python code (pre- processing)in the form of dat.file
2. Then obtained E through V via  for loop
3.got the output (although not accurate
