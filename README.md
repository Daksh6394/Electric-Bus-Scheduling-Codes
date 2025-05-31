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
### Integration of CPLEX and DOcplex

- **Python Installation**: 
  - Installed Python version 3.10.

- **DOcplex Library Setup**: 
  - Installed the DOcplex library in Jupyter Notebook.

- **Jupyter Lab Integration**: 
  - Integrated Jupyter Lab with the CPLEX environment using the following commands:
    ```python
    import sys
    sys.path.append(r"C:\Program Files\IBM\ILOG\CPLEX_Studio_22.1.1\cplex\python\3.10\x64_win64")
    import cplex
    from docplex.mp.model import Model
    ```

- **Virtual Environment Creation**: 
  - Created a virtual environment named `cplex_env` using:
    ```bash
    py -3.10 -m venv cplex_env
    ```

- **Activating Virtual Environment**: 
  - Activated the virtual environment with:
    ```bash
    cplex_env\Scripts\activate
    ```

- **CPLEX Setup Installation**: 
  - Navigated to the CPLEX Python directory:
    ```bash
    cd "C:\Program Files\IBM\ILOG\CPLEX_Studio_22.1.1\cplex\python\3.10\x64_win64"
    ```
  - Installed CPLEX using:
    ```bash
    python setup.py install
    ```

### Conversion of Visnu Sir’s CPLEX Code into Python DOcplex

- **Data Preparation**: 
  - Obtained values of V through Python code (pre-processing) in the form of a `.dat` file.

- **Edge Calculation**: 
  - Derived E from V using a for loop.

- **Output Generation**: 
  - Generated output, although it was not fully accurate.

27/06/25

1.Created a st.plot for the model with n = 3 vehicles 
2.Watched the videos of maxflow
3.Added extra comments in the code and understood the code 
4.Went through kulkarni research paper ( tsnf formulation)  and
the constraints .

28/06/2025

1. went through the kulkarni paper and worked on the code
2. understood the various approaches followed in vehicle scheduling

29/06/2025
1.solved the bug in the code
2.created a st.plot 
3. understood the code properly with various parameters of model fucntions

30/06/2025 
1. Solved the entire code , earlier it was not giving the complete schedule of the vehicle now it's giving complete schedule of single vehicle
2. Although still the vehicle is not showing the exact time difference , so need to make changes in it .
3. change the arc according to the frequency
4. make changes in the miimization fucntion
   
