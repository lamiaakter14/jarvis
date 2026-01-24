class Mentor:
    def __init__(self, memory_manager):
        """
        Initialize the Mentor Agent.
        Args:
            memory_manager: Instance of the Memory Manager to interact with system memory.
        """
        self.memory_manager = memory_manager

    def analyze_execution_logs(self):
        """
        Analyze execution logs to identify errors and prioritize knowledge gaps.

        Returns:
            list: Prioritized knowledge gaps with remediation suggestions.
        """
        # Fetch execution logs
        execution_logs = self.memory_manager.get_working_memory("execution_logs/")
        gaps = self.memory_manager.get_knowledge("gaps.md")

        # Collect and analyze recurring errors or notes from execution logs
        for log_file in execution_logs:
            log_content = self.memory_manager.load_file(log_file)
            errors = log_content.get("errors", [])
            for error in errors:
                # Check if the error exists in current gaps, otherwise add it
                if not self.is_gap_recorded(error, gaps):
                    new_gap = {
                        "id": f"gap_{len(gaps['unresolved_gaps']) + 1}",
                        "description": error.get("description"),
                        "evidence": [error.get("details")],
                        "suggested_remediation": ["Revisit concepts and practice exercises."]
                    }
                    gaps["unresolved_gaps"].append(new_gap)

        # Save the updated gaps
        self.memory_manager.save_knowledge("gaps.md", gaps)
        return gaps

    def provide_feedback(self, task):
        """
        Provide feedback for a completed task.
        
        Args:
            task (dict): Task information from the execution logs.

        Returns:
            dict: Feedback with comments and recommendations.
        """
        task_name = task.get("task")
        errors = task.get("errors", [])
        feedback = {
            "task": task_name,
            "feedback": [],
        }

        if not errors:
            feedback["feedback"].append("Great work! No errors detected.")
        else:
            for error in errors:
                feedback["feedback"].append(f"Error in task '{task_name}': {error['message']}")
            feedback["feedback"].append("Consider revisiting similar exercises to strengthen your understanding.")

        return feedback

    def assess_knowledge_depth(self, topic):
        """
        Assess the depth of knowledge on a specific topic.
        
        Args:
            topic (str): The topic to assess.

        Returns:
            dict: Assessment results including a depth score.
        """
        # Sample conditions to calculate understanding depth (Score = 0-100)
        reflections = self.memory_manager.get_knowledge("reflections.md")
        all_tasks = [r for r in reflections.get("reflections", []) if topic in r.get("learning_summary", {}).get("facts_learned", [])]

        if all_tasks:
            success_rate = len([task for task in all_tasks if not task.get("error_analysis", [])]) / len(all_tasks)
            depth_score = int(success_rate * 100)
        else:
            depth_score = 0

        return {
            "topic": topic,
            "depth_score": depth_score,
            "status": "Good" if depth_score > 70 else "Needs Improvement",
        }

    def socratic_questioning(self, topic):
        """
        Generate a thought-provoking question to increase topic understanding.

        Args:
            topic (str): The topic to discuss.

        Returns:
            str: A Socratic question to stimulate deeper understanding.
        """
        questions = [
            f"What is the essence of {topic}? Can you explain it to a 10-year-old?",
            f"Can you think of areas where {topic} can be practically applied?",
            f"What underlying assumptions do we make about {topic}? Are they always valid?",
            f"Can you think of an example that contradicts common beliefs about {topic}?",
        ]
        from random import choice
        return choice(questions)

    def mentor_task(self, task):
        """
        Mentor the learner for a specific task in the daily plan.

        Args:
            task (dict): A specific task from the daily learning plan.

        Returns:
            dict: Mentorship feedback and recommendations for the task.
        """
        feedback = self.provide_feedback(task)
        socratic_question = self.socratic_questioning(task.get("task"))
        feedback["socratic_question"] = socratic_question
        feedback["recommendations"] = self.provide_learning_suggestions(task)

        return feedback

    def provide_learning_suggestions(self, task):
        """
        Generate learning suggestions based on the task.
        
        Args:
            task (dict): A specific task from the daily learning plan.

        Returns:
            list: A list of actionable learning suggestions.
        """
        task_topic = task.get("task")
        recommendations = [
            f"Revisit {task_topic} in your roadmap.",
            f"Check the associated knowledge gaps for {task_topic}.",
            "Try available quizzes or exercises to improve your skills.",
            "Ask a peer or mentor for additional insights."
        ]

        return recommendations

    def execute(self, daily_plan):
        """
        Execute the mentorship tasks for a daily plan, looping through each task to provide individualized feedback.

        Args:
            daily_plan (dict): The daily task plan generated by the Strategist.

        Returns:
            None
        """
        for task in daily_plan.get("tasks", []):
            print(f"Mentoring on task: {task['task']}")
            feedback = self.mentor_task(task)
            print("\nFeedback:\n", feedback)
