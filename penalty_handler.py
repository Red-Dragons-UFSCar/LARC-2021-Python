import asyncio

class PenaltyHandler:
    def __init__(self):
        self.defensive_penalty_tactics = ['spin', 'spin-v', 'direct']
        self.offensive_penalty_tactics = ['spin', 'direct', 'switch']
        self.timer = 0
        self.current_offensive_tactic = 0
        self.current_defensive_tactic = 0

    async def handle_offensive_penalty(self, goals_recieved):
        pass

    async def handle_defensive_penalty(self, goals_recieved):
        pass
