import agents.savings_agent as s
import agents.triage_agent as t
import agents.orchestrator_agent as o

if __name__ == "__main__":
    orces = o.Orchestrator()

    print(orces.current_agent(None))
    while True:
        inp = input("Answer: ")
        print(orces.current_agent(inp))
