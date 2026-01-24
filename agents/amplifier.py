import statistics

class Amplifier:
    def __init__(self, memory_manager):
        """
        Initialize the Amplifier Agent.
        Args:
            memory_manager: An instance of the MemoryManager.
        """
        self.memory_manager = memory_manager

    def analyze_performance(self):
        """
        Analyze overall system performance by aggregating logs and feedback.

        Returns:
            dict: A performance summary with key metrics and insights.
        """
        # Load relevant files
        feedback_logs = self.memory_manager.get_working_memory("execution_logs/feedback.json")
        reflections = self.memory_manager.get_knowledge("reflections.md")
        gaps = self.memory_manager.get_knowledge("gaps.md")

        results = {
            "performance_metrics": {},
            "insights": []
        }

        # Calculate task completion metrics
        task_statuses = [log.get("status") for log in feedback_logs.values()]
        results["performance_metrics"]["tasks_completed"] = task_statuses.count("success")
        results["performance_metrics"]["tasks_failed"] = task_statuses.count("failed")
        results["performance_metrics"]["tasks_pending"] = task_statuses.count("manual_pending")
        results["performance_metrics"]["total_tasks"] = len(task_statuses)

        # Calculate error types and frequency
        all_errors = [error for log in feedback_logs.values() for error in log.get("errors", [])]
        results["performance_metrics"]["total_errors"] = len(all_errors)
        if all_errors:
            most_common_error = statistics.mode(all_errors)
            results["performance_metrics"]["most_common_error"] = most_common_error

        # Incorporate reflections and identify recurring patterns
        recommendations = []
        for reflection in reflections.get("reflections", []):
            recommendations.extend(reflection.get("evolution_recommendations", []))
        results["performance_metrics"]["recommendation_count"] = len(recommendations)

        # Insights for overall system analysis
        if results["performance_metrics"]["tasks_failed"] > 0:
            results["insights"].append("High task failure rate detected, consider improving error handling or task dependencies.")

        if len(gaps.get("unresolved_gaps", [])) > 5:
            results["insights"].append(f"System is managing {len(gaps['unresolved_gaps'])} unresolved gaps. Consider focusing on addressing them.")

        return results

    def propose_optimizations(self, performance_summary):
        """
        Propose system-level optimizations based on performance analysis.
        
        Args:
            performance_summary (dict): Summary of system performance.

        Returns:
            dict: Proposed optimizations and changes to improve system flow.
        """
        optimizations = []

        # Address high failure rates
        failure_rate = performance_summary["performance_metrics"].get("tasks_failed", 0)
        total_tasks = performance_summary["performance_metrics"].get("total_tasks", 1)
        if failure_rate / total_tasks > 0.3:
            optimizations.append(
                "Consider reducing task difficulty or increasing Mentor Agent's preparation efforts before execution."
            )

        # Address unresolved gaps
        unresolved_gaps = performance_summary["performance_metrics"].get("recommendation_count", 0)
        if unresolved_gaps > 5:
            optimizations.append(
                f"There are {unresolved_gaps} unresolved gaps. Focus on learning the most critical gaps first to minimize task failure risks."
            )

        # Inter-agent communication analysis
        optimizations.append("Ensure better communication between Strategist and Mentor Agents for clear task planning.")

        # Output final system-level recommendations
        return {"proposed_optimizations": optimizations}

    def amplify(self):
        """
        Perform system analysis and propose optimizations.
        
        Returns:
            dict: System performance summary and optimization proposals.
        """
        print("Analyzing system performance...")
        performance_summary = self.analyze_performance()
        print(f"Performance Summary: {performance_summary}")

        print("Proposing system optimizations...")
        optimizations = self.propose_optimizations(performance_summary)

        # Save performance and optimizations to a summary file
        results = {
            "performance_summary": performance_summary,
            "optimizations": optimizations
        }
        self.memory_manager.save_working_memory("amplifier/performance_summary.json", results)
        print("Performance and optimization report saved to 'amplifier/performance_summary.json'.")

        return results
