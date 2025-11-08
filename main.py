import agents.search_agent as s
import agents.triage_agent as t
import agents.orchestrator_agent as o

import sys

if __name__ == "__main__":
    orces = o.Orchestrator()

    debug = False
    if len(sys.argv) > 1:
        if sys.argv[1] == "True":
            debug = True
            print("DEBUG MODE\nPrinting all agent outputs...")


    print(orces.current_agent(None, debug))
    while True:
        inp = input("Answer: ")
        print(orces.current_agent(inp, debug))
