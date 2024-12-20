# Project Setup and Instructions

## 1. Configure the Environment

Before running the code, ensure you set up your `.env` file with your GPT-4 OpenAI API key:

Make sure to replace `'Your API key'` with your actual OpenAI API key.

## 2. Running the Code

Navigate to the `test_agent.ipynb` notebook and follow these steps:

### **Environment Setup:**
- Run the **first two cells** under the **"Environment Setup"** header to import the necessary Python files.

### **Experiments:**
- Run the **two cells** under the **"Experiments"** section to execute the experiments with and without norms.
  
  The results of the experiments will automatically be saved in:
  - `Norm_dataset.csv` (for experiments using norms)
  - `Without_Norm_dataset.csv` (for experiments without norms)

### **Dataset Information:**
- The `dataset/problems` folder contains grid configurations for 25 problems. The dataset should be automatically loaded by the code in the respective cells.

## 3. Running Individual Commands

- For running individual commands, use the cell under the **"Individual Instruction"** header. 
- You can load different grid configurations and modify the instructions to test various cases and behaviors.

---

**Note:** Make sure all necessary dependencies are installed and configured as per the project requirements.
"""


