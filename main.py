import agents.search_agent as s
import agents.triage_agent as t
import agents.orchestrator_agent as o

import re
import sys


def run(debug):
    orces = o.Orchestrator()

    print(orces.current_agent(None, debug))
    while True:
        inp = input("Answer: ")
        output = orces.current_agent(inp, debug)

        if output == 'ENDCHAT' or output.endswith("COMPLETE"):
            print(output.removesuffix("COMPLETE"))
            print("Thanks for using this service today!! Hope to see you soon.")
            break

        print(output)

"""Run the code. first it checks for whether debug mode is on using a sys.arg. The it Runs a while loop of: The agent, Input from user etc
"""
if __name__ == "__main__":
    # Check if Debug mode is on
    debug = False
    if len(sys.argv) > 1:
        if sys.argv[1] == "True":
            debug = True
            print("DEBUG MODE\nPrinting all agent outputs...")

    run(debug)
    #credit = s.CreditAgent()
    #print(credit.run_agent("Find me a best credit card with good rates on balance transfers", debug))
