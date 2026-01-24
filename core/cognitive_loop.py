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

        # STEP 1: PLAN - Generate the day's learning plan
        print("[PLAN] Generating Daily Learning Plan...")
        daily_plan = self.planner.generate_plan()
        print(f"Planned Tasks for {daily_plan['date']}:", daily_plan["tasks"])

        # STEP 2: LEARN - Execute the Learning Plan
        print("[LEARN] Executing Daily Learning Plan...")
        for task in daily_plan["tasks"]:
            task_description = task["task"]
            print(f"Learning Task: {task_description}")
            explanation = self.teacher.explain_concept(task_description)
            print(f"Generated Explanation: {explanation}")
        
        # STEP 3: CRITIQUE - Analyze Outcomes and Identify Knowledge Gaps
        print("[CRITIQUE] Analyzing Outcomes and Identifying Knowledge Gaps...")
        knowledge_gaps = self.critic.detect_gaps()
        print("Detected Knowledge Gaps:", knowledge_gaps)

        # STEP 4: REFLECT - Generate Summary and Strategy Recommendations
        print("[REFLECT] Summarizing Learning and Generating Recommendations...")
        reflections = self.reviewer.reflect()
        print("Daily Reflection Summary:", reflections)

        # STEP 5: EVOLVE - Adapt Learning Strategy
        print("[EVOLVE] Updating Strategy and Evolving Learning Plan...")
        recommendations = reflections["evolution_recommendations"]
        for recommendation in recommendations:
            print(f"Recommendation for Evolution: {recommendation}")

        print("Cognitive Loop Complete!")
