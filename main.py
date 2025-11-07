import agents.savings_agent as s
import agents.triage_agent as t
import agents.orchestrator_agent as o

if __name__ == "__main__":
    orces = o.Orchestrator()

    while True:
        orces.current_agent()
