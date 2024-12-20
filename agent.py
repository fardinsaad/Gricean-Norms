import numpy as np
from llm import get_response
from env_setup import GridEnvironment
class Agent:
    def __init__(self, start_pos):
        self.pos = start_pos  # Agent's initial position (row, col)
        self.keys_collected = []  # List of keys collected (color-coded)
        self.clarification_count = 0  # Track number of clarifications
        self.conversation_history = []  # Track conversation for inference
        self.max_clarifications = 3  # Maximum number of clarifications allowed
        self.previous_symbol = '.'  # Track what was at the agent's previous position
            

    def move(self, direction, grid):
        # Clear the agent's previous position by restoring the previous symbol
        grid[self.pos] = self.previous_symbol

        # Determine the new position based on direction
        new_pos = list(self.pos)
        if direction == 'up':
            new_pos[0] -= 1
        elif direction == 'down':
            new_pos[0] += 1
        elif direction == 'left':
            new_pos[1] -= 1
        elif direction == 'right':
            new_pos[1] += 1

        # Ensure the agent doesn't move through walls (W)
        if grid[new_pos[0], new_pos[1]] != 'W':
            # Update the agent's position
            self.pos = tuple(new_pos)
            # Save the symbol that was on the new position (before placing the agent there)
            self.previous_symbol = grid[self.pos]
            # Mark the agent's new position with 'm'
            grid[self.pos] = 'm'

    def pick_up_key(self, grid):
        # Use the `previous_symbol` to check if the agent was on a key
        if self.previous_symbol in ['r', 'y', 'b']:
            key_color = self.previous_symbol
            print(f"{key_color.capitalize()} key picked up!")
            self.keys_collected.append(key_color)
            self.previous_symbol = '.'  # The key is removed, so the cell becomes empty

    def unlock_door(self, grid):
        # Use the `previous_symbol` to check if the agent was next to a door (R, Y, B)
        if self.previous_symbol == 'R' and 'r' in self.keys_collected:
            print("Red door unlocked!")
            self.previous_symbol = '.'  # The door is removed, so the cell becomes empty
            self.keys_collected.remove('r')

        elif self.previous_symbol == 'Y' and 'y' in self.keys_collected:
            print("Yellow door unlocked!")
            self.previous_symbol = '.'  # The door is removed, so the cell becomes empty
            self.keys_collected.remove('y')

        elif self.previous_symbol == 'B' and 'b' in self.keys_collected:
            print("Blue door unlocked!")
            self.previous_symbol = '.'  # The door is removed, so the cell becomes empty
            self.keys_collected.remove('b')

    def collect_gem(self, grid):
        # Use the `previous_symbol` to check if the agent was on a gem
        if self.previous_symbol == 'g':
            print("Gem collected!")
            self.previous_symbol = '.'  # The gem is removed, so the cell becomes empty

    def chain_of_thought_prompt(self, instruction, grid, grice, object_pos):
        # Generate the prompt with the current grid state and human position
        prompt = self.create_prompt(instruction, grid, grice, object_pos)
        
        # Query the LLM with the prompt
        response = get_response(prompt)
        
        # Log the instruction and response for later reference
        self.conversation_history.append(f"Instruction: {instruction}, Response: {response}")
        
        # Infer whether the LLM is asking for clarification based on response content
        #if self.is_asking_for_clarification(response):
        #    self.clarification_count += 1
        
        # If clarification limit is reached, infer an action
        # if self.clarification_count >= self.max_clarifications:
        #     inferred_action = self.infer_action_from_history()
        #     print(f"Inferred action based on history: {inferred_action}")
        #     return inferred_action
        
        return response  # Returns the LLM's response, either an action or clarification


    
    def create_prompt(self, instruction, grid, grice, object_pos):
        # Full detailed prompt, including the chain-of-thought and few-shot examples
        # Grid context to give the LLM more environmental information
        intro = "You are assisting a human in a cooperative planning domain called Doors, Keys, and Gems, set in a gridworld. The grid contains various objects such as keys, doors, gems, walls, empty spaces, the human, and yourself (the AI agent). The human’s objective is to retrieve a specific gem by issuing a single instruction. Your role is to interpret this instruction—whether it is clear, incomplete, ambiguous, irrelevant, or invalid—and assist by taking actions such as retrieving and passing keys or unlocking doors. Your actions should aim to minimize your movement while ensuring the human can achieve their goal as efficiently and quickly as possible. After interpreting the human’s instruction, you will generate an optimal response that supports the human in reaching their desired gem in the most optimal manner.\n" + \
        "You and the human share a common understanding of the environment and objectives, with the ultimate goal of retrieving a specific gem. Upon receiving a single instruction, your task is to assess its type, discern the human's intent, and uncover any implicit meaning. Based on this interpretation and the current grid configuration, you will infer the most relevant action and generate a response that facilitates the collection of the desired gem.\n" 
        

        grid_context = "\nThe Current Grid Layout for the Keys, Doors, and, Gems: \n" + str(grid) + "\n\nBelow are the locations of all objects on the grid, displayed as (row, column) coordinates, along with their total count:\n" + str(object_pos) + "\n\n"

        #print(str(grid))

        #imp = "\nYour primary objective is to assist the human in collecting a specific gem after receiving an instruction. With common ground between you and the human, you understand the implied goal behind each instruction: to collect a specific gem. The human will provide only one instruction, and you must infer the most relevant action based on the current grid configuration and common ground to identify which particular gem the human wants to retrieve.\n"
        normCOT = "You follow specific communication norms to interpret the instruction and generate a response, ensuring the human successfully achieves their goal of collecting a specific gem after providing an instruction. You adhere to Gricean norms—Quantity, Quality, Relevance, and Manner—when evaluating instructions. If a norm is violated, apply the Action/Inference Norm to infer the most relevant action and generate a response based on the current grid configuration. If no norms are violated, execute the action directly as per the instruction after careful interpretation. Always assess which specific gem the human wants to retrieve, ensuring that your actions enable the human to reach that gem efficiently within the grid.\n"
        
        norms = "\nNorms:\n" + \
                "1. Quantity Norm: The instruction must provide sufficient information for the human to reach the desired gem on the current grid. If the instruction specifies collecting or unlocking the necessary object(s) to retrieve the gem based on the grid configuration, it is considered sufficient. However, if additional actions—such as collecting another key or unlocking another door—are required and these actions aren't mentioned, it results in a Quantity Violation. For example, if the grid has two blue doors, three blue keys, two red keys, and a gem beyond the blue doors, an instruction to pick up only one blue key would be a Quantity Violation. In this case, both blue keys are needed to unlock the doors and reach the gem, so you should collect two blue keys and pass them to the human. Conversely, if the instruction were to \"collect two blue keys\", it would be clear and sufficient. Instructions that involve collecting multiple keys are generally clear when based on the grid configuration or when the human is performing an action and asks you to collect or unlock an object.\n" + \
                "2. Quality Norm: The instruction must be truthful and valid. Verify whether the instruction aligns with the current grid configuration. If the instruction requests an object that does not exist on the grid or contains incorrect information, it results in a Quality Violation. For example, if the instruction tells you to collect a blue key when no blue key is present on the grid, it violates the Quality Norm. In such cases, you should ask the human for clarification.\n" + \
                "3. Relevance Norm: The instruction must be directly related to the goal of collecting the specific gem based on the current grid. Any instruction that does not contribute to this objective results in a Relevance Violation. For example, if the instruction asks something unrelated, such as \"Can you dance?,\" which has no connection to the grid or the game, it violates the Relevance Norm.\n" + \
                "4. Manner Norm: The instruction must be clear and unambiguous. If the instruction is ambiguous or can be interpreted in multiple ways, it results in a Manner Violation. For example, if the instruction is to \"unlock the red door\" but there are two red doors, both equally far from the human with a gem placed beyond them, it creates ambiguity. Since it's unclear which door to unlock and which specific gem the human wants to retrieve, you should ask for clarification to resolve the ambiguity.\n" + \
                "5. Action/Inference Norm: When any of the above norms are violated, infer the most relevant action based on the current grid to help the human collect the desired gem. Begin by interpreting which gem the human intends to retrieve. If no violations occur, execute the instruction as provided. Always generate your response by cross-checking and verifying it against the current grid configuration to ensure accuracy. The inference steps for each violated norm are:\n" + \
                "- 5.1 Quantity Violation Inference: Infer from the instruction which gem the human wants to retrieve. Then analyze the grid to determine the number and color of keys or doors required, minimizing steps to ensure efficient collection of the gem.\n" + \
                "- 5.2 Quality Violation Inference: Ask the human for clarification and provide alternative valid options that could lead to a gem.\n" + \
                "- 5.3 Relevance Violation Inference: Request clarification and suggest relevant key or door options that can help the human retrieve a gem. If the specific gem is ambiguous, treat it as a Manner Norm Violation.\n" + \
                "- 5.4 Manner Violation Inference: Present the human with the most optimal options to resolve the ambiguity, ensuring it leads to their desired gem.\n"
        
                
        key_points = "\nKey Points:\n" + \
                "- The human will provide only one instruction.\n" + \
                "- Infer the specific gem the human wants to retrieve from the instruction.\n" + \
                "- Evaluate the instruction using common ground (shared knowledge), relevance theory (focusing on pertinent details), and theory of mind (considering the human’s perspective), based on the current grid configuration.\n" + \
                "- Always generate a response with the understanding that the implied goal is to collect the specific gem. Keep this objective in mind when interpreting the instruction and determining the most relevant action based on the current grid configuration.\n" + \
                "- Cross-check the instruction against the current grid state, ensuring it provides adequate details, clarity, validity, relevance, and aligns with the intended goal.\n" + \
                "- Always generate your response by cross-checking and verifying it against the current grid configuration to ensure accuracy.\n" + \
                "- Each key can unlock only one door of the corresponding color. A key cannot be reused to unlock multiple doors of the same color.\n" + \
                "- Prioritize collecting keys before unlocking doors. Even if not explicitly mentioned, collect any necessary keys if access through a locked door is required.\n" + \
                "- Once the keys are collected, automatically pass them to the human if the instruction involves passing, finding, or collecting keys.\n" + \
                "- If unable to pass the key due to being blocked by a door, request clarification from the human on how to proceed.\n" + \
                "- Always infer that an instruction involving a key or keys means you should collect them, even if not explicitly stated. Determine which gem the human wants to collect and which key is needed to help them.\n" + \
                "- If explicitly instructed to unlock doors, focus on unlocking them by collecting the necessary keys, without passing them to the human.\n" + \
                "- When traversing the grid, minimize and optimize your path, avoiding collisions with walls (W) or other obstacles.\n" + \
                "- Always prioritize efficient, obstacle-free routes to achieve the human's objective as quickly and effectively as possible.\n"
        
    
        pred = "\nBased on your understanding of the norms, common ground, interpretation strategies, grid layout, and the labeled examples provided below, generate the norm violation type and response for the following human instruction, delimited by triple backticks:\n" 
        pred1 = "\nBased on your understanding of common ground, interpretation strategies, grid layout, and the labeled examples provided below, generate a response for the following human instruction, delimited by triple backticks:\n" 
      
        # Use self.cleaning to clean the instruction
        test_sample = "\nInstruction: " + self.clean_text(str(instruction)) + \
                      "\nNorm: <Identify the norm violation type and provide chain-of-thought reasoning for the violation>" + \
                      "\nResponse: <Generate chain-of-thought reasoning for the response>\n"
        
        # Use self.cleaning to clean the instruction
        test_sample_1 = "\nInstruction: " + self.clean_text(str(instruction)) + \
                        "\nResponse: <Generate chain-of-thought reasoning for the response>\n"


        if grice:
            text = '```' + test_sample + '```\n'
        else:
            text = '```' + test_sample_1 + '```\n'
        

        few_shot = "Use the following examples, delimited by triple quotes, to understand how to generate the appropriate response for each instruction. These examples are based on different grid configurations. Follow the structure and format shown in these examples when generating both the 'Norm' and 'Response'."
        few_shot_1 = "Use the following examples, delimited by triple quotes, to understand how to generate the appropriate response for each instruction. These examples are based on different grid configurations. Follow the structure and format shown in these examples when generating the 'Response'."

        examples = self.get_examples() 

        examples_1 = self.get_examples_1()

        if grice:
            few_shot += "\n" + examples
        else:
            few_shot_1 += "\n" + examples_1    

        if grice:
            prompt = intro + grid_context +  normCOT+ norms + key_points + pred + text + few_shot 
        else:
            prompt = intro + grid_context + key_points + pred1 + text + few_shot_1

        #print(prompt)

        return prompt

    def get_examples(self):
    # You can store your examples here in case of reuse
        return "'''\nInstruction: Can you get the red key?\n" + \
            "Norm: No Violation. Based on the instruction and the grid, I infer that the human wants to collect the gem closest to them at (8,9), which is blocked by a red door. Since only one red key is needed to unlock the door and reach the gem, the instruction is complete and not missing any details.\n" + \
            "Response: There are three red keys and two red doors on the grid. To collect the gem at (8,9), only one red door needs to be unlocked. I will pick up the red key at (3,8) since it is closest to both me and the human, and pass it to the human to unlock the red door at (6,9).\n\n" + \
            "Instruction: Pick up the red key.\n" + \
            "Norm: Quantity Violation. Based on the instruction and the grid, I infer that the human wants to collect the gem at (7,0), which is beyond a red door. However, before reaching the gem, there is also a yellow door blocking the path. Therefore, I must collect both the red and yellow keys, and since the instruction doesn't mention picking up the yellow key, this results in a Quantity Violation.\n" + \
            "Response: There are two yellow doors, one red door, one red key, and one yellow key on the grid. The instruction asks to collect a red key, so the desired gem the human wants to collect is placed beyond the red door at (3,1). However, a yellow door at (6,0) blocks the path to the gem at (7,0). I will collect both the red key at (0,0) and the yellow key at (1,0), then pass them to the human to unlock the doors.\n\n" + \
            "Instruction: Can you get the green key?\n" + \
            "Norm: Quality Violation. Based on the instruction and the grid, there is no green key on the grid, making this an invalid instruction.\n" + \
            "Response: There is no red key on the grid. Do you want me to collect the yellow key, the blue key, or both?\n\n" + \
            "Instruction: Can you dance?\n" + \
            "Norm: Relevance Violation. Based on the instruction and the grid, this request is unrelated to collecting keys or unlocking doors, making it an irrelevant instruction.\n" + \
            "Response: I am an AI and can't dance. This instruction is not relevant to the grid, which contains doors, keys, and gems. Would you like me to pass you a key or unlock a door instead?\n\n"+ \
            "Instruction: Pick up the yellow key.\n" + \
            "Norm: Manner Violation. Based on the instruction and the grid, it is unclear which gem the human wants to collect and which yellow key they are referring to, making this instruction ambiguous.\n" + \
            "Response: There are two yellow keys, one red key, one red door, and two yellow doors on the grid. Could you clarify which key you're referring to? Do you want me to collect the yellow key at (0,4) or (4,6), or do you want me to collect both of them?\n\n" + \
            "Instruction: Get a key there.\n" + \
            "Norm: Manner Violation. Based on the instruction and the grid, it is unclear which gem the human wants to collect and which key they are referring to, making this instruction ambiguous.\n" + \
            "Response: There are two yellow keys, one red key, one red door, and two yellow doors on the grid. Could you clarify which key you're referring to? Do you want me to collect the yellow key(s) or the red key? If I collect the red key, I'll also need to collect the yellow key to unlock both doors and reach the gem.\n\n" + \
            "Instruction: Can you pass me the blue keys?\n" + \
            "Norm: No Violation. Based on the instruction and the grid, I infer that the human wants to collect the gem at (4,8). Two blue doors are blocking the path to the gem, so two blue keys are required, making this a clear instruction with no missing details.\n" + \
            "Response: The grid contains three blue keys, three red keys, two blue doors, and two red doors with gems placed beyond them. The instruction is asking to collect blue keys to retrieve the gem at (4,8). I will collect the two blue keys closest to me at (1,5) and (1,7), and pass them to the human to unlock the blue doors.\n\n" + \
            "Instruction: On my way to pick up the blue key, can you find a yellow key?\n" + \
            "Norm: No Violation. Based on the instruction and the grid, I infer that the human wants to collect the gem at (2,9), which is beyond the yellow door at (3,9) and near the blue door at (3,6). The human will likely unlock the blue door and use the yellow key from me to unlock the yellow door. Since only one yellow key is required to reach the gem, this is a clear instruction with no missing details.\n" + \
            "Response: There are two yellow keys, one red key, one blue key, two red doors, two yellow doors, and three blue doors on the grid. I will collect the yellow key at (7,9), which is closest to the blue door at (3,6) that the human is likely going to unlock. I will then pass the yellow key to the human to unlock the yellow door at (3,9) and retrieve the gem at (2,9).\n\n" + \
            "Instruction: Can you hand me that key?\n" + \
            "Norm: Manner Violation. Based on the instruction and the grid, it is unclear which gem the human wants to collect and which key they are referring to, making this instruction ambiguous.\n" + \
            "Response: There are several keys on the grid. Which key do you want? The red key at (3,8) or the blue key at (2,9)? Both keys are equally distant from your position.\n\n" + \
            "Instruction: Can you come and unlock this door?\n" + \
            "Norm: Manner Violation. Based on the instruction and the grid, it is unclear which gem the human wants to collect and which door they are referring to, making this instruction ambiguous.\n" + \
            "Response: There are two red doors and one blue door. Which door do you want me to unlock: the blue door at (3, 5) or the red door at (4, 6)?\n\n" + \
            "Instruction: Can you come get this yellow door?\n" + \
            "Norm: No Violation. Based on the instruction and the grid, I infer that the human wants to collect the gem at (2,4), which is beyond the yellow door at (3,3). Since only one yellow key is needed to unlock the yellow door, the instruction is clear and complete.\n" + \
            "Response: There is one yellow key, two blue keys, one yellow door, and two blue doors on the grid. I will collect the yellow key at (4,7) and unlock the yellow door at (3,3), allowing the human to reach the desired gem.\n\n" + \
            "Instruction: Can you get the blue door there? I'll pick up the red key.\n" + \
            "Norm: No Violation. Based on the instruction and the grid, I infer that the human wants to collect the gem at (5,9), which is beyond the blue door at (6,7) and the red door at (6,8). Since the human will likely unlock the red door, I only need to unlock the blue door. As unlocking one blue door is sufficient, this is a clear instruction with no missing details.\n" + \
            "Response: There are two blue keys, one red key, two blue doors, and three red doors on the grid. To collect the gem at (5,9), both a blue and a red door need to be unlocked. Since the human is picking up the key for the red door, I will collect the blue key at (4,7), which is closest to the blue door at (6,7), and unlock it. The human will then unlock the red door at (6,8) to reach the gem at (5,9).\n\n" + \
            "Instruction: Can you come and get this red door?\n" + \
            "Norm: Quantity Violation. Based on the instruction and the grid, I infer that the human wants to collect the gem at (5,8), which is beyond the red door at (7,6). However, there is also a blue door at (5,6) blocking the path. Since I need to collect both a red and blue key to unlock the doors, and this isn't mentioned in the instruction, it is incomplete.\n" + \
            "Response: There is one red key, one blue key, two blue doors, and one red door on the grid. The instruction asks to unlock the red door, but there is also a blue door blocking the path to the gem at (5,8). I will collect both the blue key at (2,7) and the red key at (2,8), unlock the blue door at (5,6), and then unlock the red door at (7,6), allowing the human to retrieve the gem.\n\n" + \
            "Instruction: Can you come and get this blue door?\n" + \
            "Norm: Manner Violation. Based on the instruction and the grid, there are two blue doors at (5,5) and (2,1), each with a gem placed beyond them. It's unclear from the instruction which gem the human desires, making the instruction ambiguous.\n" + \
            "Response: There is one blue key, one red key, two blue doors, and one red door on the grid. Should I unlock the blue door at (5,5) or the one at (2,1)? The blue door at (5,5) is blocked by a red door at (7,5) on your path.\n'''"

    
    def get_examples_1(self):
    # You can store your examples here in case of reuse
        return "'''\nInstruction: Can you get the red key?\n" + \
            "Response: There are three red keys and two red doors on the grid. To collect the gem at (8,9), only one red door needs to be unlocked. I will pick up the red key at (3,8) since it is closest to both me and the human, and pass it to the human to unlock the red door at (6,9).\n\n" + \
            "Instruction: Pick up the red key.\n" + \
            "Response: There are two yellow doors, one red door, one red key, and one yellow key on the grid. The instruction asks to collect a red key, so the desired gem the human wants to collect is placed beyond the red door at (3,1). However, a yellow door at (6,0) blocks the path to the gem at (7,0). I will collect both the red key at (0,0) and the yellow key at (1,0), then pass them to the human to unlock the doors.\n\n" + \
            "Instruction: Can you get the green key?\n" + \
            "Response: There is no green key on the grid. Do you want me to collect the yellow key, the blue key, or both?\n\n" + \
            "Instruction: Can you dance?\n" + \
            "Response: I am an AI and can't dance. This instruction is not relevant to the grid, which contains doors, keys, and gems. Would you like me to pass you a key or unlock a door instead?\n\n"+ \
            "Instruction: Pick up the yellow key.\n" + \
            "Response: There are two yellow keys, one red key, one red door, and two yellow doors on the grid. Could you clarify which key you're referring to? Do you want me to collect the yellow key at (0,4) or (4,6), or do you want me to collect both of them?\n\n" + \
            "Instruction: Get a key there.\n" + \
            "Response: There are two yellow keys, one red key, one red door, and two yellow doors on the grid. Could you clarify which key you're referring to? Do you want me to collect the yellow key(s) or the red key? If I collect the red key, I'll also need to collect the yellow key to unlock both doors and reach the gem.\n\n" + \
            "Instruction: Can you pass me the blue keys?\n" + \
            "Response: The grid contains three blue keys, three red keys, two blue doors, and two red doors with gems placed beyond them. The instruction is asking to collect blue keys to retrieve the gem at (4,8). I will collect the two blue keys closest to me at (1,5) and (1,7), and pass them to the human to unlock the blue doors.\n\n" + \
            "Instruction: On my way to pick up the blue key, can you find a yellow key?\n" + \
            "Response: There are two yellow keys, one red key, one blue key, two red doors, two yellow doors, and three blue doors on the grid. I will collect the yellow key at (7,9), which is closest to the blue door at (3,6) that the human is likely going to unlock. I will then pass the yellow key to the human to unlock the yellow door at (3,9) and retrieve the gem at (2,9).\n\n" + \
            "Instruction: Can you hand me that key?\n" + \
            "Response: There are several keys on the grid. Which key do you want? The red key at (3,8) or the blue key at (2,9)? Both keys are equally distant from your position.\n\n" + \
            "Instruction: Can you come and unlock this door?\n" + \
            "Response: There are two red doors and one blue door. Which door do you want me to unlock: the blue door at (3, 5) or the red door at (4, 6)?\n\n" + \
            "Instruction: Can you come get this yellow door?\n" + \
            "Response: There is one yellow key, two blue keys, one yellow door, and two blue doors on the grid. I will collect the yellow key at (4,7) and unlock the yellow door at (3,3), allowing the human to reach the desired gem.\n\n" + \
            "Instruction: Can you get the blue door there? I'll pick up the red key.\n" + \
            "Response: There are two blue keys, one red key, two blue doors, and three red doors on the grid. To collect the gem at (5,9), both a blue and a red door need to be unlocked. Since the human is picking up the key for the red door, I will collect the blue key at (4,7), which is closest to the blue door at (6,7), and unlock it. The human will then unlock the red door at (6,8) to reach the gem at (5,9).\n\n" + \
            "Instruction: Can you come and get this red door?\n" + \
            "Response: There is one red key, one blue key, two blue doors, and one red door on the grid. The instruction asks to unlock the red door, but there is also a blue door blocking the path to the gem at (5,8). I will collect both the blue key at (2,7) and the red key at (2,8), unlock the blue door at (5,6), and then unlock the red door at (7,6), allowing the human to retrieve the gem.\n\n" + \
            "Instruction: Can you come and get this blue door?\n" + \
            "Response: There is one blue key, one red key, two blue doors, and one red door on the grid. Should I unlock the blue door at (5,5) or the one at (2,1)? The blue door at (5,5) is blocked by a red door at (7,5) on your path.\n'''"

    
  
    def clean_text(self, text):
        '''
        Remove new liens / "" in the students response
        remove extra space
        '''
        # print("Before cleaning: ", text)
        text = text.strip()
        text = text.strip('\"')
        text = text.strip('\n')

        return text


    def is_asking_for_clarification(self, response):
        # Check for common phrases that indicate clarification queries
        clarification_phrases = ["Do you mean", "Which", "Could you specify", "I'm not sure"]
        return any(phrase in response for phrase in clarification_phrases)

        
    def infer_action_from_history(self): #Have to edit this
        # Infer the action based on conversation history if clarification limit is reached
        for entry in reversed(self.conversation_history):
            if "Response" in entry and "action" in entry.lower():
                return entry.split("Response: ")[1]
        return "Perform best-guess action based on environment."

if __name__ == "__main__":
    # Example grid setup
    grid = np.array([
        ['r', '.', '.', '.', 'm', 'W', 'W', 'g'],
        ['y', '.', 'W', 'W', '.', 'W', 'W', '.'],
        ['W', 'W', 'W', 'W', '.', 'W', 'W', '.'],
        ['.', 'R', '.', '.', '.', '.', 'h', '.'],
        ['.', 'W', '.', 'W', 'W', 'W', 'W', '.'],
        ['.', 'W', '.', 'W', 'W', 'W', 'W', 'Y'],
        ['Y', 'W', '.', 'W', 'W', 'W', 'W', '.'],
        ['g', 'W', 'g', 'W', 'W', 'W', 'W', 'g']
    ])

    # Define positions
    agent_start_pos = (0, 4)  # Starting position of the agent (m)
    human_pos = (3, 6)  # Position of the human (h)

    # Initialize the agent
    agent = Agent(agent_start_pos)

    # Define the instruction
    instruction = "Can you pass me the blue key?."

    env = GridEnvironment()
    name = "5.txt" 
    grid_file_path = env.get_grid_file_path(name)
    env.load_grid_from_file(grid_file_path)

    pos = env.get_all_object_positions()
    # Get agent and object positions
    agent_pos = env.get_agent_position()
    human_pos = env.get_human_position()
    grice = True
    object_pos = env. get_all_object_positions()

    #print(pos)

    # Generate the prompt
    prompt = agent.create_prompt(instruction, grid, grice, object_pos)


    # Print the generated prompt
    print(prompt)

