from generic_agent import GenericAgent



class TriageAgent(GenericAgent):
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        super().__init__(model_name=model_name)
    # Additional methods specific to TriageAgent can be added here
