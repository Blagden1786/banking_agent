import agents.savings_agent as s
import agents.triage_agent as t
import agents.orchestrator_agent as o

if __name__ == "__main__":
    orca = o.Orchestrator()
    triage = t.SavingsTriageAgent()
    agent = s.SavingsAgent()

    agent_choice = orca.run_agent()
    prompt = triage.run_agent()
    print(prompt)
    agent.run_agent(prompt, True)
