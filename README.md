<h1>BANK ACCOUNT AGENT</h1>

<h2>What is it?</h2>
The bank account agent is a LLM based multi agent system which finds the user the best relevant savings accounts and credit cards based on their needs which are inferred through natural conversation.
<h3>The agents</h3>
<h4>Orchestrator</h4>
The orchestrator agent moves the user around the agents after determining what the user is looking for.

<h4>Savings Agent</h4>
This agent is split into a triage agent and a search agent. It finds out what specific account the user wants and then finds it by searching the given websites

<h4>Credit Card Agent</h4>
This agent is split into a triage agent and a search agent. It finds out what specific account the user wants and then finds it by searching the given websites

<h4>LLM Judge</h4>
LLM-as-a-judge is used to evaluate the responses of the agents. It can then feedback to the agent if it thinks the response needs to be redone.

<h3>Result</h3>
These agents work together to produce a fully functional system that finds the best rate account satisfying the user requirements.

<h2>Running the Agent</h2>
<h3>Libraries</h3>
<ul>
  <li>Google Genai</li>
  <li>Requests</li>
  <li>BeautifulSoup</li>
  <li>re</li>
  <li>sys</li>
</ul>

You will also need to get a google API key from [this site](https://aistudio.google.com/api-keys) and replace all instances of ```client = genai.Client()``` with ```client = genai.Client(api_key="YOUR_API_KEY")```. These instances are spread across the files in agent_code and agent_code/tools.

<h3>In the terminal</h3>
Run the file main.py in te terminal. Add the parameter True if you want to see the workings of the agents.

<h2>How it works</h2>
As opposed to using the built in tool-use features within gemini, this project has focused on building the agent functionality from the ground up. The code alternates between receiving user input and running the LLM. When the LLM decides to use a tool, external code runs the function and then the LLM is run again with the answer so it can use the result in its decision making.
