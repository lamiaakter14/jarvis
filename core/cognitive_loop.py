class CognitiveLoop:
    def __init__(self, memory_manager, planner, teacher, critic, reviewer):
        self.memory_manager = memory_manager
        self.planner = planner
        self.teacher = teacher
        self.critic = critic
        self.reviewer = reviewer

    def run_loop(self):
        # PLAN
        daily_plan = self.planner.generate_plan()
        self.memory_manager.update_working_memory("daily_plan", daily_plan)

        # LEARN
        for task in daily_plan['tasks']:
            self.teacher.teach(task)

        # CRITIQUE
        gaps = self.critic.detect_gaps()
        self.memory_manager.update_knowledge_gaps(gaps)

        # REFLECT
        reflection = self.reviewer.reflect()
        self.memory_manager.update_reflections(reflection)

        # EVOLVE
        evolution_recommendations = self.reviewer.evolve()
        self.memory_manager.update_evolution(evolution_recommendations)
