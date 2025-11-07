from .generic_agent import GenericAgent
from .tools.tools import *
from .tools.web_scraper_llm import web_search



# The savings account agent finds the savings which match the query

SAVINGS_PROMPT = """TASK: Your main goal is to find the best savings account based on the given requirements and perform any other calculations when asked.
ALWAYS use the following exact format:

Question: the input question you must answer
Thought: you should always think about one action to take. Only one action at a time in this format:
Action:$Python Function Call

Now begin, remember to use the EXACT format as above.
Once you have sufficient information to provide an answer give a natural answer to the question.

Requirments: """
SAVINGS_URLS = ['https://www.natwest.com/savings.html', 'https://www.hsbc.co.uk/savings/products/']

class SearchAgent(GenericAgent):
    def __init__(self, main_prompt, available_sites, tools=[], model_name: str = "gemini-2.5-flash"):
        # The urls available to the agent
        self.urls = available_sites

        super().__init__(model_name=model_name, main_prompt=main_prompt, tools=tools + ['search_tool'])

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

    def search_tool(self, search=""):
        """Search tool for the search agent to use. It access the urls given in the init

        Args:
            search (str, optional): String describing what to get the LLM to find in the pages. Defaults to "".

        Returns:
            str: A string of relevant accounts in the JSON format
        """
        # Get HTML source code of the webpage
        response = web_search(self.urls, search)

        return response

class SavingsAgent(SearchAgent):
    def __init__(self):
        super().__init__(SAVINGS_PROMPT, SAVINGS_URLS, ["interest_calc"])
