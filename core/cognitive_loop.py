class CognitiveLoop:
    def __init__(self, memory_manager, strategist, mentor, executor, innovator, amplifier):
        """
        Initialize the CognitiveLoop with agents and memory manager.
        Args:
            memory_manager: A MemoryManager instance for loading and saving memory files.
            strategist: The Strategist Agent for planning.
            mentor: The Mentor Agent for diagnostics and feedback.
            executor: The Executor Agent for task implementation.
            innovator: The Innovator Agent for creative synthesis.
            amplifier: The Amplifier Agent for performance optimization.
        """
        self.memory_manager = memory_manager
        self.strategist = strategist
        self.mentor = mentor
        self.executor = executor
        self.innovator = innovator
        self.amplifier = amplifier

    def run_loop(self):
        """
        Main loop to execute all agents in the cognitive framework sequentially.
        """
        # Step 1: Planning with STRATEGIST
        print("---- Step 1: Planning with Strategist ----")
        daily_plan = self.strategist.generate_plan()
        print(f"Generated Plan: {daily_plan}")

        # Step 2: Reviewing Tasks with MENTOR
        print("\n---- Step 2: Reviewing Tasks with Mentor ----")
        updated_gaps = self.mentor.analyze_execution_logs()
        print(f"Updated Gaps: {updated_gaps}")

        for task in daily_plan.get("tasks", []):
            mentorship_feedback = self.mentor.mentor_task(task)
            print(f"Mentorship Feedback for Task: {mentorship_feedback}")
            # Save feedback for each task
            self.memory_manager.save_working_memory("execution_logs/feedback.json", mentorship_feedback)

        # Step 3: Executing Tasks with EXECUTOR
        print("\n---- Step 3: Executing Tasks with Executor ----")
        self.executor.run_tasks()

        # Step 4: Innovating with INNOVATOR
        print("\n---- Step 4: Innovator Generating Creative Suggestions ----")
        innovations = self.innovator.create_innovations()
        print(f"Innovator Suggestions: {innovations}")

        # Step 5: Optimizing System with AMPLIFIER
        print("\n---- Step 5: Amplifier Optimizing System ----")
        amplifier_results = self.amplifier.amplify()
        print(f"Amplifier Results: {amplifier_results}")
