class Strategist:
    def __init__(self, memory_manager):
        """
        Initialize the Strategist Agent.
        Args:
            memory_manager: Instance of the MemoryManager to interact with system memory.
        """
        self.memory_manager = memory_manager

    def generate_plan(self):
        """
        Generate a strategic learning and task plan for the day, based on the learning roadmap,
        knowledge gaps, and daily context.
        
        Returns:
            dict: A structured daily plan with prioritized tasks and time allocations.
        """
        # Load roadmap and memory data
        roadmap = self.memory_manager.get_knowledge("roadmap.md")
        gaps = self.memory_manager.get_knowledge("gaps.md")
        context = self.memory_manager.get_working_memory("daily_context.json")

        # Perform task prioritization, filtering, and scheduling
        prioritized_tasks = self.prioritize_tasks(roadmap, gaps, context)
        schedule = self.create_schedule(prioritized_tasks, context)

        # Save the generated daily plan into working memory
        daily_plan = {
            "date": context.get("date"),  # Ensure today's date is in the plan
            "tasks": schedule
        }
        self.memory_manager.save_working_memory("daily_plan.json", daily_plan)
        return daily_plan

    def prioritize_tasks(self, roadmap, gaps, context):
        """
        Prioritize tasks based on ROI and knowledge gaps.
        
        Args:
            roadmap (dict): Roadmap milestones and deadlines.
            gaps (dict): List of unresolved knowledge gaps.
            context (dict): The current daily context.

        Returns:
            List[Dict]: List of prioritized tasks.
        """
        tasks = []

        # Prioritize tasks from knowledge gaps based on gap severity
        for gap in gaps.get("unresolved_gaps", []):
            tasks.append({
                "task": f"Review material on: {gap['description']}",
                "priority": "high",
                "cognitive_load": "medium",
                "evidence": gap.get("evidence", []),
                "roi": self.calculate_learning_roi(gap)
            })

        # Add tasks from roadmap milestones
        for milestone in roadmap.get("milestones", []):
            tasks.append({
                "task": f"Work on milestone: {milestone['title']}",
                "priority": "medium",
                "cognitive_load": "high",
                "due_date": milestone.get("due_date"),
                "roi": self.calculate_execution_roi(milestone)
            })

        # Include focus on recent topics from context
        for topic in context.get("current_focus", []):
            tasks.append({
                "task": f"Revisit recent topic: {topic}",
                "priority": "low",
                "cognitive_load": "low",
                "roi": 0.2  # Low priority task with minimal impact
            })

        # Sort tasks based on ROI (descending order)
        return sorted(tasks, key=lambda x: x["roi"], reverse=True)

    def calculate_learning_roi(self, gap):
        """
        Calculate ROI for learning tasks based on knowledge gap data.
        
        Args:
            gap (dict): A specific knowledge gap data.

        Returns:
            float: Calculated learning ROI.
        """
        # Assume a simple formula for now: prioritize recurring critical gaps first
        severity = len(gap.get("evidence", []))  # More evidence indicates higher severity
        # Customize to reflect your scoring preference
        return severity * 1.5

    def calculate_execution_roi(self, milestone):
        """
        Calculate ROI for execution tasks based on milestones.

        Args:
            milestone (dict): A specific milestone from the roadmap.

        Returns:
            float: Calculated execution ROI.
        """
        # Example: Prioritize based on proximity to deadline
        due_date = milestone.get("due_date")
        if due_date:
            days_remaining = (self.parse_date(due_date) - self.current_date()).days
            return max(1, 100 / (days_remaining + 1))  # Higher ROI for sooner deadlines
        return 0.5  # Default value for milestones without a due date

    def create_schedule(self, tasks, context):
        """
        Create a time-blocked schedule for tasks.

        Args:
            tasks (list): Prioritized tasks list.
            context (dict): The learner's current execution context.

        Returns:
            List[Dict]: A schedule with tasks and estimated time allocations.
        """
        schedule = []
        available_hours = 8  # Assuming 8 hours of productive time per day

        for task in tasks:
            # Simple heuristic for time blocking based on cognitive load
            time_required = {
                "low": 1,   # 1 hour
                "medium": 2,  # 2 hours
                "high": 3   # 3 hours
            }[task["cognitive_load"]]

            if available_hours - time_required >= 0:
                task["time_allocated"] = f"{time_required} hours"
                schedule.append(task)
                available_hours -= time_required

        return schedule

    @staticmethod
    def parse_date(date_str):
        """
        Parse a date string from the roadmap data.
        
        Args:
            date_str (str): Date string (YYYY-MM-DD).
        
        Returns:
            date: Parsed date object.
        """
        from datetime import datetime
        return datetime.strptime(date_str, "%Y-%m-%d").date()

    @staticmethod
    def current_date():
        """
        Get the current system date.
        
        Returns:
            date: Today's date.
        """
        from datetime import date
        return date.today()
