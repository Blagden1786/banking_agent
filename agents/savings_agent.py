from .generic_agent import GenericAgent
from .tools.tools import *



# The savings account agent finds the savings which match the query

SAVINGS_PROMPT = """TASK: Your main goal is to find the best savings account based on the given requirements and perform any other calculations when asked.
ALWAYS use the following exact format:

Question: the input question you must answer
Thought: you should always think about one action to take. Only one action at a time in this format:
Action:$Python Function Call

Now begin, remember to use the EXACT format as above.
Once you have sufficient information to provide an answer give a natural answer to the question.

Requirments: """

class SavingsAgent(GenericAgent):
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        super().__init__(model_name=model_name, main_prompt=SAVINGS_PROMPT, tools=["account_finder_tool", "interest_calc"])
    # Additional methods specific to SavingsAgent can be added here

    def run_agent(self, task:str, trace: bool = False) -> str:
        """Run the savings agent. It loops through the logic, producing tool calls until creating a final answer

        Args:
            task (str): The type of savings account the user wants to find
            trace (bool, optional): Whether to show the debug code during execution. Defaults to False.

        Returns:
            str: Final recommendation from the agent
        """
        prompt = self.prompt_builder() + task

        while True:
            # Get response from the model
            response = self.get_response(prompt)
            if response is None:
                return "Error: No response from model."

            if trace:
                print("\n\n----------------------AGENT RESPONSE----------------------")
                print(response)


            tool_call = self.tool_use(response)
            if tool_call != "":
                # Execute the tool call
                try:
                    tool_result = str(eval(tool_call))
                except Exception as e:
                    tool_result = f"Error executing tool: {e}"

                if trace:
                    print("\n----------------------TOOL RESPONSE----------------------")
                    print(f"Tool call: {tool_call}")
                    print(f"Tool result: {tool_result}")

                # Append the tool result to the prompt for the next iteration
                prompt += f"\nAgent response: {response}\nThe outcome of the usage of the tool use was {tool_result}"
            else:
                # No tool used, return the final answer
                return response
