class CognitiveLoop:
    def __init__(self, memory_manager, planner, teacher, critic, reviewer):
        """
        Initialize the Primary Cognitive Loop with memory manager and agents.
        Args:
            memory_manager: Instance of MemoryManager to handle memory operations.
            planner: Planner Agent for generating the daily task plan.
            teacher: Teacher Agent for executing the learning tasks.
            critic: Critic Agent for identifying knowledge gaps.
            reviewer: Reviewer Agent for reflecting on learning and improving strategy.
        """
        self.memory_manager = memory_manager
        self.planner = planner
        self.teacher = teacher
        self.critic = critic
        self.reviewer = reviewer

    def run_loop(self):
        """
        Run the full cognitive loop:
        PLAN -> LEARN -> CRITIQUE -> REFLECT -> EVOLVE
        """
        print("Starting Cognitive Loop...")
        
        # Step 1: PLAN
        print("[PLAN] Generating Daily Learning Plan...")
        daily_plan = self.planner.generate_plan()
        print(f"Planned Tasks for {daily_plan['date']}:", daily_plan["tasks"])

        # Step 2: LEARN
        print("[LEARN] Executing Daily Learning Plan...")
        for task in daily_plan["tasks"]:
            concept = task["task"]
            print(f"Learning Task: {concept}")
            explanation = self.teacher.explain_concept(concept)
            print(f"Generated Explanation: {explanation}")

        # Step 3: CRITIQUE
        print("[CRITIQUE] Analyzing Outcomes and Identifying Knowledge Gaps...")
        gaps = self.critic.detect_gaps()
        print("Detected Gaps:", gaps)

        # Step 4: REFLECT
        print("[REFLECT] Summarizing Learning and Generating Recommendations...")
        reflection = self.reviewer.reflect()
        print("Daily Reflection Summary:", reflection)

        # Step 5: EVOLVE
        print("[EVOLVE] Updating Strategy and Evolving Learning Plan...")
        recommendations = reflection["evolution_recommendations"]
        for rec in recommendations:
            print(f"Recommendation: {rec}")

        print("Cognitive Loop Complete!")
