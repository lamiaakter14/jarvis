#!/usr/bin/env python3
"""
Log Analysis Tool for JARVIS
Analyzes logs from reflections.json and gaps.json to generate insights.

This tool provides:
- Frequently encountered gaps analysis
- Most common lessons learned
- Trends in task execution (time spent, completion rates)
- Productivity patterns
- Challenge analysis
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from collections import Counter, defaultdict
from typing import Dict, List, Any
import statistics


class LogAnalyzer:
    """Analyzes JARVIS reflection and gap logs to generate insights."""
    
    def __init__(self, memory_dir: str = "memory"):
        """
        Initialize the Log Analyzer.
        
        Args:
            memory_dir: Root directory for memory storage
        """
        self.memory_dir = Path(memory_dir)
        self.working_memory_path = self.memory_dir / "working"
        self.reflections_file = self.working_memory_path / "reflections.json"
        self.gaps_file = self.working_memory_path / "gaps.json"
        
        self.reflections_data = self._load_json(self.reflections_file)
        self.gaps_data = self._load_json(self.gaps_file)
    
    def _load_json(self, file_path: Path) -> Dict:
        """Load JSON data from file."""
        if not file_path.exists():
            print(f"Warning: {file_path} does not exist")
            return {}
        
        with open(file_path, 'r') as f:
            return json.load(f)
    
    def analyze_gaps(self) -> Dict[str, Any]:
        """
        Analyze knowledge gaps.
        
        Returns:
            Dictionary containing gap analysis insights
        """
        if not self.gaps_data:
            return {"error": "No gap data available"}
        
        unresolved_gaps = self.gaps_data.get("unresolved_gaps", [])
        resolved_gaps = self.gaps_data.get("resolved_gaps", [])
        
        # Category distribution
        category_counts = Counter(gap.get("category") for gap in unresolved_gaps)
        
        # Priority distribution
        priority_counts = Counter(gap.get("priority") for gap in unresolved_gaps)
        
        # Resolution time analysis
        resolution_times = []
        for gap in resolved_gaps:
            if gap.get("date") and gap.get("resolved_date"):
                try:
                    start = datetime.fromisoformat(gap["date"].replace('Z', '+00:00'))
                    end = datetime.fromisoformat(gap["resolved_date"].replace('Z', '+00:00'))
                    days = (end - start).days
                    resolution_times.append(days)
                except (ValueError, KeyError):
                    continue
        
        avg_resolution_time = statistics.mean(resolution_times) if resolution_times else 0
        median_resolution_time = statistics.median(resolution_times) if resolution_times else 0
        
        return {
            "total_unresolved_gaps": len(unresolved_gaps),
            "total_resolved_gaps": len(resolved_gaps),
            "category_distribution": dict(category_counts),
            "priority_distribution": dict(priority_counts),
            "avg_resolution_time_days": round(avg_resolution_time, 2),
            "median_resolution_time_days": median_resolution_time,
            "most_common_category": category_counts.most_common(1)[0][0] if category_counts else None,
            "most_common_priority": priority_counts.most_common(1)[0][0] if priority_counts else None
        }
    
    def analyze_lessons_learned(self) -> Dict[str, Any]:
        """
        Analyze lessons learned from daily reflections.
        
        Returns:
            Dictionary containing lessons learned insights
        """
        if not self.reflections_data:
            return {"error": "No reflection data available"}
        
        daily_reflections = self.reflections_data.get("daily_reflections", [])
        
        # Collect all lessons
        all_lessons = []
        for reflection in daily_reflections:
            lessons = reflection.get("lessons_learned", [])
            all_lessons.extend(lessons)
        
        # Find common patterns in lessons (simple keyword matching)
        lesson_keywords = defaultdict(int)
        common_words = {'the', 'a', 'an', 'is', 'to', 'for', 'of', 'and', 'in', 'on', 'at'}
        
        for lesson in all_lessons:
            words = lesson.lower().split()
            for word in words:
                if len(word) > 3 and word not in common_words:
                    lesson_keywords[word] += 1
        
        top_keywords = sorted(lesson_keywords.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            "total_lessons": len(all_lessons),
            "unique_lessons": len(set(all_lessons)),
            "top_lesson_keywords": dict(top_keywords),
            "recent_lessons": all_lessons[-10:] if all_lessons else [],
            "lessons_per_day_avg": round(len(all_lessons) / max(len(daily_reflections), 1), 2)
        }
    
    def analyze_task_execution(self) -> Dict[str, Any]:
        """
        Analyze task execution trends.
        
        Returns:
            Dictionary containing task execution insights
        """
        if not self.reflections_data:
            return {"error": "No reflection data available"}
        
        daily_reflections = self.reflections_data.get("daily_reflections", [])
        
        total_tasks = 0
        total_time = 0
        difficulty_counts = Counter()
        completion_rates = []
        productivity_scores = []
        energy_levels = []
        focus_qualities = []
        
        for reflection in daily_reflections:
            # Completed tasks
            completed_tasks = reflection.get("tasks_completed", [])
            in_progress_tasks = reflection.get("tasks_in_progress", [])
            
            total_tasks += len(completed_tasks)
            
            # Time tracking
            for task in completed_tasks:
                time_spent = task.get("time_spent_hours", 0)
                total_time += time_spent
                
                difficulty = task.get("difficulty")
                if difficulty:
                    difficulty_counts[difficulty] += 1
            
            # Completion rate (tasks completed vs in progress)
            total_day_tasks = len(completed_tasks) + len(in_progress_tasks)
            if total_day_tasks > 0:
                completion_rate = len(completed_tasks) / total_day_tasks * 100
                completion_rates.append(completion_rate)
            
            # Productivity metrics
            if reflection.get("productivity_score"):
                productivity_scores.append(reflection["productivity_score"])
            if reflection.get("energy_level"):
                energy_levels.append(reflection["energy_level"])
            if reflection.get("focus_quality"):
                focus_qualities.append(reflection["focus_quality"])
        
        return {
            "total_tasks_completed": total_tasks,
            "total_hours_worked": round(total_time, 2),
            "avg_task_completion_rate": round(statistics.mean(completion_rates), 2) if completion_rates else 0,
            "avg_productivity_score": round(statistics.mean(productivity_scores), 2) if productivity_scores else 0,
            "avg_energy_level": round(statistics.mean(energy_levels), 2) if energy_levels else 0,
            "avg_focus_quality": round(statistics.mean(focus_qualities), 2) if focus_qualities else 0,
            "difficulty_distribution": dict(difficulty_counts),
            "avg_hours_per_task": round(total_time / max(total_tasks, 1), 2),
            "total_reflection_days": len(daily_reflections)
        }
    
    def analyze_challenges(self) -> Dict[str, Any]:
        """
        Analyze challenges faced and their resolutions.
        
        Returns:
            Dictionary containing challenge analysis
        """
        if not self.reflections_data:
            return {"error": "No reflection data available"}
        
        daily_reflections = self.reflections_data.get("daily_reflections", [])
        
        all_challenges = []
        total_time_lost = 0
        resolution_methods = []
        
        for reflection in daily_reflections:
            challenges = reflection.get("challenges_faced", [])
            for challenge in challenges:
                all_challenges.append(challenge.get("challenge"))
                total_time_lost += challenge.get("time_lost_hours", 0)
                if challenge.get("resolution"):
                    resolution_methods.append(challenge["resolution"])
        
        # Find common challenge patterns
        challenge_keywords = defaultdict(int)
        common_words = {'the', 'a', 'an', 'is', 'to', 'for', 'of', 'and', 'in', 'on', 'at'}
        
        for challenge in all_challenges:
            if challenge:
                words = challenge.lower().split()
                for word in words:
                    if len(word) > 3 and word not in common_words:
                        challenge_keywords[word] += 1
        
        top_challenge_keywords = sorted(challenge_keywords.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            "total_challenges": len(all_challenges),
            "total_time_lost_hours": round(total_time_lost, 2),
            "avg_time_lost_per_challenge": round(total_time_lost / max(len(all_challenges), 1), 2),
            "top_challenge_keywords": dict(top_challenge_keywords),
            "total_resolutions_documented": len(resolution_methods)
        }
    
    def analyze_productivity_trends(self) -> Dict[str, Any]:
        """
        Analyze productivity trends over time.
        
        Returns:
            Dictionary containing productivity trend insights
        """
        if not self.reflections_data:
            return {"error": "No reflection data available"}
        
        daily_reflections = self.reflections_data.get("daily_reflections", [])
        
        if not daily_reflections:
            return {"error": "No daily reflections available"}
        
        # Sort by day number
        sorted_reflections = sorted(daily_reflections, key=lambda x: x.get("day_number", 0))
        
        productivity_trend = []
        energy_trend = []
        focus_trend = []
        
        for reflection in sorted_reflections:
            day = reflection.get("day_number", 0)
            productivity_trend.append({
                "day": day,
                "score": reflection.get("productivity_score", 0)
            })
            energy_trend.append({
                "day": day,
                "level": reflection.get("energy_level", 0)
            })
            focus_trend.append({
                "day": day,
                "quality": reflection.get("focus_quality", 0)
            })
        
        # Calculate trends (simple moving average)
        window_size = min(7, len(sorted_reflections))  # 7-day moving average
        
        def moving_average(data, window):
            if len(data) < window:
                return []
            return [
                sum(data[i:i+window]) / window
                for i in range(len(data) - window + 1)
            ]
        
        productivity_scores = [r.get("productivity_score", 0) for r in sorted_reflections]
        energy_levels = [r.get("energy_level", 0) for r in sorted_reflections]
        focus_qualities = [r.get("focus_quality", 0) for r in sorted_reflections]
        
        productivity_ma = moving_average(productivity_scores, window_size)
        energy_ma = moving_average(energy_levels, window_size)
        focus_ma = moving_average(focus_qualities, window_size)
        
        return {
            "productivity_trend": productivity_trend,
            "energy_trend": energy_trend,
            "focus_trend": focus_trend,
            "productivity_moving_avg": [round(x, 2) for x in productivity_ma],
            "energy_moving_avg": [round(x, 2) for x in energy_ma],
            "focus_moving_avg": [round(x, 2) for x in focus_ma],
            "trend_improving": productivity_ma[-1] > productivity_ma[0] if len(productivity_ma) > 1 else None
        }
    
    def generate_comprehensive_report(self) -> Dict[str, Any]:
        """
        Generate a comprehensive analysis report.
        
        Returns:
            Dictionary containing all analysis insights
        """
        return {
            "report_generated_at": datetime.now().isoformat(),
            "gap_analysis": self.analyze_gaps(),
            "lessons_learned_analysis": self.analyze_lessons_learned(),
            "task_execution_analysis": self.analyze_task_execution(),
            "challenge_analysis": self.analyze_challenges(),
            "productivity_trends": self.analyze_productivity_trends()
        }
    
    def print_summary(self):
        """Print a formatted summary of the analysis."""
        report = self.generate_comprehensive_report()
        
        print("=" * 80)
        print("JARVIS LOG ANALYSIS REPORT")
        print("=" * 80)
        print(f"Generated at: {report['report_generated_at']}")
        print()
        
        # Gap Analysis
        print("-" * 80)
        print("GAP ANALYSIS")
        print("-" * 80)
        gap_analysis = report['gap_analysis']
        if 'error' not in gap_analysis:
            print(f"Total Unresolved Gaps: {gap_analysis['total_unresolved_gaps']}")
            print(f"Total Resolved Gaps: {gap_analysis['total_resolved_gaps']}")
            print(f"Average Resolution Time: {gap_analysis['avg_resolution_time_days']} days")
            print(f"Most Common Category: {gap_analysis['most_common_category']}")
            print(f"Most Common Priority: {gap_analysis['most_common_priority']}")
            print(f"Category Distribution: {gap_analysis['category_distribution']}")
        else:
            print(gap_analysis['error'])
        print()
        
        # Lessons Learned
        print("-" * 80)
        print("LESSONS LEARNED ANALYSIS")
        print("-" * 80)
        lessons_analysis = report['lessons_learned_analysis']
        if 'error' not in lessons_analysis:
            print(f"Total Lessons: {lessons_analysis['total_lessons']}")
            print(f"Lessons per Day (Avg): {lessons_analysis['lessons_per_day_avg']}")
            print(f"Top Keywords: {list(lessons_analysis['top_lesson_keywords'].keys())[:5]}")
            print("\nRecent Lessons:")
            for lesson in lessons_analysis['recent_lessons'][-5:]:
                print(f"  • {lesson}")
        else:
            print(lessons_analysis['error'])
        print()
        
        # Task Execution
        print("-" * 80)
        print("TASK EXECUTION ANALYSIS")
        print("-" * 80)
        task_analysis = report['task_execution_analysis']
        if 'error' not in task_analysis:
            print(f"Total Tasks Completed: {task_analysis['total_tasks_completed']}")
            print(f"Total Hours Worked: {task_analysis['total_hours_worked']}")
            print(f"Average Completion Rate: {task_analysis['avg_task_completion_rate']}%")
            print(f"Average Productivity Score: {task_analysis['avg_productivity_score']}/10")
            print(f"Average Energy Level: {task_analysis['avg_energy_level']}/10")
            print(f"Average Focus Quality: {task_analysis['avg_focus_quality']}/10")
            print(f"Average Hours per Task: {task_analysis['avg_hours_per_task']}")
        else:
            print(task_analysis['error'])
        print()
        
        # Challenge Analysis
        print("-" * 80)
        print("CHALLENGE ANALYSIS")
        print("-" * 80)
        challenge_analysis = report['challenge_analysis']
        if 'error' not in challenge_analysis:
            print(f"Total Challenges Faced: {challenge_analysis['total_challenges']}")
            print(f"Total Time Lost: {challenge_analysis['total_time_lost_hours']} hours")
            print(f"Average Time Lost per Challenge: {challenge_analysis['avg_time_lost_per_challenge']} hours")
            print(f"Resolutions Documented: {challenge_analysis['total_resolutions_documented']}")
            print(f"Top Challenge Keywords: {list(challenge_analysis['top_challenge_keywords'].keys())[:5]}")
        else:
            print(challenge_analysis['error'])
        print()
        
        # Productivity Trends
        print("-" * 80)
        print("PRODUCTIVITY TRENDS")
        print("-" * 80)
        trend_analysis = report['productivity_trends']
        if 'error' not in trend_analysis and trend_analysis['trend_improving'] is not None:
            trend_direction = "IMPROVING ↗" if trend_analysis['trend_improving'] else "DECLINING ↘"
            print(f"Overall Trend: {trend_direction}")
            if trend_analysis['productivity_moving_avg']:
                print(f"Recent 7-Day Productivity Avg: {trend_analysis['productivity_moving_avg'][-1]}/10")
                print(f"Recent 7-Day Energy Avg: {trend_analysis['energy_moving_avg'][-1]}/10")
                print(f"Recent 7-Day Focus Avg: {trend_analysis['focus_moving_avg'][-1]}/10")
        else:
            print("Insufficient data for trend analysis")
        print()
        
        print("=" * 80)
    
    def save_report(self, output_file: str = "log_analysis_report.json"):
        """
        Save the comprehensive report to a JSON file.
        
        Args:
            output_file: Path to the output file
        """
        report = self.generate_comprehensive_report()
        output_path = Path(output_file)
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"Report saved to: {output_path.absolute()}")


def main():
    """Main function to run log analysis."""
    # Add parent directory to path for imports
    sys.path.insert(0, str(Path(__file__).parent.parent))
    
    print("JARVIS Log Analysis Tool")
    print("=" * 80)
    print()
    
    # Initialize analyzer
    analyzer = LogAnalyzer()
    
    # Print summary
    analyzer.print_summary()
    
    # Save report
    analyzer.save_report("log_analysis_report.json")


if __name__ == "__main__":
    main()
