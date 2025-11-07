import agents.savings_agent as s
import agents.triage_agent as t
import agents.orchestrator_agent as o

if __name__ == "__main__":
    agent = s.SavingsAgent()

    agent.run_agent("Best savings account with no access and fixed interest rate", True)

    """
    orca = o.Orchestrator()
    triage = t.SavingsTriageAgent()
    agent = s.SavingsAgent()

    agent_choice = orca.run_agent()

    match agent_choice:
        case "savings_agent()":
            prompt = triage.run_agent()
            output = agent.run_agent(prompt, True)
        case _:
            output = "This agent has yet to be built"

    print(output)
    """
