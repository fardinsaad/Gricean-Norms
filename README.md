# Gricean Norms as a Basis for Effective Collaboration
![Static Badge](https://img.shields.io/badge/LLM--agent-Lamoid-Green?logo=chatbot)
![Static Badge](https://img.shields.io/badge/Norms-Cooperative%20Principle-blue?logo=python&logoColor=white)

This project enhances human-agent collaboration by incorporating Gricean norms such as Quantity, Quality, Relation, and Manner into Lamoid, a GPT-4-powered agent, enabling it to interpret ambiguous, incomplete, irrelevant, invlaid and clear instructions in the Doors, Keys, and Gems grid world. Leveraging principles of common ground, relevance theory, and Theory of Mind (ToM), Lamoid aligns its responses with human intentions by inferring implicit goals and addressing norm violations through few-shot chain-of-thought demonstrations. 

This approach adhering to the Gricean nroms improves task accuracy, response clarity, and relevance, demonstrating the potential of structured norms and pragmatic reasoning in creating effective AI collaborators and cooperative assistants. 

For more details, see [our paper](https://www.not_availablenow.com):
>Fardin Saad, Pradeep Murukannaiah, Munindar P. Singh. 2025. Gricean Norms as a Basis for Effective Collaboration. In Proc. of the 24th International Conference on Autonomous Agents and Multiagent Systems (AAMAS 2025).


## Setup
This repository contains:
- `.env`: Contains the API key.
- `llm.py`: Loads the API key.
- `env_setup`: Loads the dataset for different grid configurations.
- `agent.py`: Contains the agent's framework and prompting techniques.
- `test_agent.ipynb`: Contains code for running the experiments across the norm and non-norm condition.

## 1. Configure the Environment

Before running the code, **ensure you set up your `.env` file** with ***your GPT-4 OpenAI API key***:

Make sure to replace `'Your API key'` with your **actual OpenAI API key**.

## 2. Running the Code

Navigate to the `test_agent.ipynb` notebook and follow these steps:

### **Environment Setup:**
- Run the **first two cells** under the **"Environment Setup"** header to import the necessary Python files.

### **Experiments:**
- Run the **two cells** under the **"Experiments"** section to execute the experiments with and without norms.
  
  The results of the experiments will automatically be saved in:
  - `Norm_dataset.csv` (for experiments ***using norms***)
  - `Without_Norm_dataset.csv` (for experiments ***without norms***)

### **Dataset Information:**
- The `dataset/problems` folder contains grid configurations for 25 problems. The dataset will be automatically loaded by the code in the respective cells.

## 3. Running Individual Commands

- For running individual commands, use the cell under the **"Individual Instruction"** header. 
- You can load different grid configurations and modify the instructions to test various cases and behaviors.

---

>**Note:** Make sure all necessary dependencies are installed and configured as per the project requirements.



