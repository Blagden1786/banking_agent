from google import genai
import re
from .tools.tools import available_tools

class GenericAgent:
    def __init__(self, model_name: str = "gemini-2.5-flash", main_prompt: str = "", tools: list = []):
        # Initialize the agent with model, prompt, and tools
        # Set model
        self.model_name = model_name
        self.agent = genai.Client()

        # Set the main prompt
        self.main_prompt = main_prompt

        # Initialize tools
        self.tools = tools
        self.tools_regex = self.regex_builder()


    def get_response(self, prompt: str) -> str | None:
        response = self.agent.models.generate_content(model=self.model_name, contents=prompt)
        return response.text

    def prompt_builder(self) -> str:
        return self.main_prompt

    def regex_builder(self) -> str:
        tools_regex = ""

        for tool in self.tools:
            tools_regex += available_tools[tool] + "|"
        tools_regex = self.tools_regex.rstrip("|")

        return tools_regex

    def is_tool_used(self, response: str) -> str:
        match = re.search(self.tools_regex, response)
        if match:
            return match.group()
        return ""
