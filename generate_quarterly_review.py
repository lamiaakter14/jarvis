#!/usr/bin/env python3
"""
Quarterly Review Generation Script for JARVIS
Automatically summarizes key tasks, lessons learned, unresolved gaps,
and plans for the next quarter based on daily logs.

This script:
1. Analyzes reflections.json and gaps.json from the past quarter
2. Generates a comprehensive quarterly review report
3. Identifies key achievements, challenges, and learnings
4. Creates actionable plans for the next quarter
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from typing import Dict, List, Any


class QuarterlyReviewGenerator:
    """Generates quarterly review reports from JARVIS logs."""
    
    def __init__(self, memory_dir: str = "memory", quarter: str = None):
        """
        Initialize the Quarterly Review Generator.
        
        Args:
            memory_dir: Root directory for memory storage
            quarter: Quarter to review (e.g., 'Q1', 'Q2'). If None, uses current.
        """
        self.memory_dir = Path(memory_dir)
        self.working_memory_path = self.memory_dir / "working"
        self.knowledge_memory_path = self.memory_dir / "knowledge"
        self.reflections_file = self.working_memory_path / "reflections.json"
        self.gaps_file = self.working_memory_path / "gaps.json"
        self.quarter = quarter
        
        self.reflections_data = self._load_json(self.reflections_file)
        self.gaps_data = self._load_json(self.gaps_file)
    
    def _load_json(self, file_path: Path) -> Dict:
        """Load JSON data from file."""
        if not file_path.exists():
            print(f"Warning: {file_path} does not exist")
            return {}
        
        with open(file_path, 'r') as f:
            return json.load(f)
    
    def _save_json(self, file_path: Path, data: Dict):
        """Save data to JSON file."""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _filter_by_quarter(self, reflections: List[Dict]) -> List[Dict]:
        """Filter reflections by quarter."""
        if not self.quarter:
            return reflections
        
        return [r for r in reflections if r.get("quarter") == self.quarter]
    
    def summarize_key_tasks(self) -> Dict[str, Any]:
        """
        Summarize key tasks completed during the quarter.
        
        Returns:
            Dictionary containing task summary
        """
        if not self.reflections_data:
            return {"error": "No reflection data available"}
        
        daily_reflections = self.reflections_data.get("daily_reflections", [])
        quarter_reflections = self._filter_by_quarter(daily_reflections)
        
        all_completed_tasks = []
        total_hours = 0
        difficulty_distribution = Counter()
        
        for reflection in quarter_reflections:
            completed_tasks = reflection.get("tasks_completed", [])
            for task in completed_tasks:
                all_completed_tasks.append(task)
                total_hours += task.get("time_spent_hours", 0)
                difficulty = task.get("difficulty")
                if difficulty:
                    difficulty_distribution[difficulty] += 1
        
        # Sort tasks by time spent to identify major tasks
        major_tasks = sorted(
            all_completed_tasks,
            key=lambda x: x.get("time_spent_hours", 0),
            reverse=True
        )[:10]
        
        return {
            "total_tasks_completed": len(all_completed_tasks),
            "total_hours_invested": round(total_hours, 2),
            "difficulty_distribution": dict(difficulty_distribution),
            "major_tasks": [
                {
                    "title": task.get("title"),
                    "hours": task.get("time_spent_hours", 0),
                    "difficulty": task.get("difficulty")
                }
                for task in major_tasks
            ],
            "average_hours_per_task": round(total_hours / max(len(all_completed_tasks), 1), 2)
        }
    
    def summarize_lessons_learned(self) -> Dict[str, Any]:
        """
        Summarize lessons learned during the quarter.
        
        Returns:
            Dictionary containing lessons summary
        """
        if not self.reflections_data:
            return {"error": "No reflection data available"}
        
        daily_reflections = self.reflections_data.get("daily_reflections", [])
        quarter_reflections = self._filter_by_quarter(daily_reflections)
        
        all_lessons = []
        all_wins = []
        areas_for_improvement = []
        
        for reflection in quarter_reflections:
            all_lessons.extend(reflection.get("lessons_learned", []))
            all_wins.extend(reflection.get("wins", []))
            areas_for_improvement.extend(reflection.get("areas_for_improvement", []))
        
        # Group similar lessons (simple keyword-based grouping)
        lesson_themes = self._extract_themes(all_lessons)
        improvement_themes = self._extract_themes(areas_for_improvement)
        
        return {
            "total_lessons": len(all_lessons),
            "key_lessons": all_lessons[-20:] if all_lessons else [],  # Most recent 20
            "lesson_themes": lesson_themes,
            "total_wins": len(all_wins),
            "major_wins": all_wins[-10:] if all_wins else [],  # Most recent 10
            "areas_for_improvement": improvement_themes,
            "improvement_count": len(areas_for_improvement)
        }
    
    def _extract_themes(self, items: List[str], top_n: int = 5) -> Dict[str, int]:
        """Extract common themes from text items."""
        keyword_counts = defaultdict(int)
        common_words = {'the', 'a', 'an', 'is', 'to', 'for', 'of', 'and', 'in', 'on', 'at', 'be'}
        
        for item in items:
            words = item.lower().split()
            for word in words:
                if len(word) > 3 and word not in common_words:
                    keyword_counts[word] += 1
        
        top_themes = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
        return dict(top_themes)
    
    def summarize_unresolved_gaps(self) -> Dict[str, Any]:
        """
        Summarize unresolved gaps from the quarter.
        
        Returns:
            Dictionary containing unresolved gaps summary
        """
        if not self.gaps_data:
            return {"error": "No gap data available"}
        
        unresolved_gaps = self.gaps_data.get("unresolved_gaps", [])
        resolved_gaps = self.gaps_data.get("resolved_gaps", [])
        
        # Filter by quarter if specified
        if self.quarter:
            quarter_unresolved = [
                gap for gap in unresolved_gaps
                if self._is_in_quarter(gap.get("date"))
            ]
        else:
            quarter_unresolved = unresolved_gaps
        
        # Group by category and priority
        category_distribution = Counter(gap.get("category") for gap in quarter_unresolved)
        priority_distribution = Counter(gap.get("priority") for gap in quarter_unresolved)
        
        # Identify critical gaps
        critical_gaps = [
            gap for gap in quarter_unresolved
            if gap.get("priority") in ["critical", "high"]
        ]
        
        return {
            "total_unresolved_gaps": len(quarter_unresolved),
            "total_resolved_in_quarter": len(resolved_gaps),
            "category_distribution": dict(category_distribution),
            "priority_distribution": dict(priority_distribution),
            "critical_gaps": [
                {
                    "title": gap.get("title"),
                    "category": gap.get("category"),
                    "priority": gap.get("priority"),
                    "description": gap.get("description")
                }
                for gap in critical_gaps[:10]
            ]
        }
    
    def _is_in_quarter(self, date_str: str) -> bool:
        """Check if a date falls within the specified quarter."""
        if not self.quarter or not date_str:
            return True
        
        try:
            date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            quarter_num = int(self.quarter[1])  # Extract number from 'Q1', 'Q2', etc.
            quarter_start_month = (quarter_num - 1) * 3 + 1
            quarter_end_month = quarter_start_month + 2
            
            return quarter_start_month <= date.month <= quarter_end_month
        except (ValueError, IndexError):
            return True
    
    def generate_next_quarter_plan(self) -> Dict[str, Any]:
        """
        Generate recommendations for the next quarter.
        
        Returns:
            Dictionary containing next quarter recommendations
        """
        # Analyze patterns to make recommendations
        task_summary = self.summarize_key_tasks()
        lessons_summary = self.summarize_lessons_learned()
        gaps_summary = self.summarize_unresolved_gaps()
        
        recommendations = []
        
        # Based on unresolved gaps
        if gaps_summary.get("critical_gaps"):
            recommendations.append({
                "priority": "high",
                "category": "knowledge_gaps",
                "recommendation": f"Address {len(gaps_summary['critical_gaps'])} critical knowledge gaps",
                "details": "Focus on resolving high-priority gaps to improve overall performance"
            })
        
        # Based on improvement areas
        if lessons_summary.get("areas_for_improvement"):
            top_improvements = list(lessons_summary["areas_for_improvement"].keys())[:3]
            recommendations.append({
                "priority": "medium",
                "category": "process_improvement",
                "recommendation": "Focus on identified improvement areas",
                "details": f"Key themes: {', '.join(top_improvements)}"
            })
        
        # Based on task difficulty
        if task_summary.get("difficulty_distribution"):
            easy_tasks = task_summary["difficulty_distribution"].get("easy", 0)
            hard_tasks = task_summary["difficulty_distribution"].get("hard", 0)
            total = sum(task_summary["difficulty_distribution"].values())
            
            if hard_tasks / max(total, 1) < 0.2:
                recommendations.append({
                    "priority": "low",
                    "category": "skill_development",
                    "recommendation": "Take on more challenging tasks",
                    "details": "Increase exposure to difficult problems for skill growth"
                })
        
        return {
            "next_quarter": self._get_next_quarter(),
            "recommendations": recommendations,
            "focus_areas": [
                "Address critical knowledge gaps",
                "Implement process improvements",
                "Continue successful patterns",
                "Develop new skills"
            ]
        }
    
    def _get_next_quarter(self) -> str:
        """Get the next quarter identifier."""
        if not self.quarter:
            # Determine current quarter
            current_month = datetime.now().month
            current_quarter = (current_month - 1) // 3 + 1
            self.quarter = f"Q{current_quarter}"
        
        quarter_num = int(self.quarter[1])
        next_quarter_num = (quarter_num % 4) + 1
        return f"Q{next_quarter_num}"
    
    def generate_quarterly_review(self) -> Dict[str, Any]:
        """
        Generate complete quarterly review.
        
        Returns:
            Dictionary containing complete quarterly review
        """
        review = {
            "quarter": self.quarter or self._get_next_quarter(),
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "tasks": self.summarize_key_tasks(),
                "lessons_learned": self.summarize_lessons_learned(),
                "unresolved_gaps": self.summarize_unresolved_gaps()
            },
            "next_quarter_plan": self.generate_next_quarter_plan()
        }
        
        return review
    
    def print_review(self):
        """Print formatted quarterly review."""
        review = self.generate_quarterly_review()
        
        print("=" * 80)
        print(f"QUARTERLY REVIEW - {review['quarter']}")
        print("=" * 80)
        print(f"Generated at: {review['generated_at']}")
        print()
        
        # Tasks Summary
        print("-" * 80)
        print("TASKS SUMMARY")
        print("-" * 80)
        tasks = review['summary']['tasks']
        if 'error' not in tasks:
            print(f"Total Tasks Completed: {tasks['total_tasks_completed']}")
            print(f"Total Hours Invested: {tasks['total_hours_invested']}")
            print(f"Average Hours per Task: {tasks['average_hours_per_task']}")
            print(f"Difficulty Distribution: {tasks['difficulty_distribution']}")
            print("\nMajor Tasks:")
            for i, task in enumerate(tasks['major_tasks'][:5], 1):
                print(f"  {i}. {task['title']} ({task['hours']} hours, {task['difficulty']})")
        print()
        
        # Lessons Learned
        print("-" * 80)
        print("LESSONS LEARNED")
        print("-" * 80)
        lessons = review['summary']['lessons_learned']
        if 'error' not in lessons:
            print(f"Total Lessons: {lessons['total_lessons']}")
            print(f"Total Wins: {lessons['total_wins']}")
            print(f"\nKey Lesson Themes: {list(lessons['lesson_themes'].keys())[:5]}")
            print("\nRecent Key Lessons:")
            for lesson in lessons['key_lessons'][-5:]:
                print(f"  • {lesson}")
            print("\nMajor Wins:")
            for win in lessons['major_wins'][-5:]:
                print(f"  ✓ {win}")
        print()
        
        # Unresolved Gaps
        print("-" * 80)
        print("UNRESOLVED GAPS")
        print("-" * 80)
        gaps = review['summary']['unresolved_gaps']
        if 'error' not in gaps:
            print(f"Total Unresolved Gaps: {gaps['total_unresolved_gaps']}")
            print(f"Resolved in Quarter: {gaps['total_resolved_in_quarter']}")
            print(f"Category Distribution: {gaps['category_distribution']}")
            print(f"Priority Distribution: {gaps['priority_distribution']}")
            print("\nCritical Gaps to Address:")
            for gap in gaps['critical_gaps'][:5]:
                print(f"  ⚠ [{gap['priority'].upper()}] {gap['title']}")
                print(f"    Category: {gap['category']}")
        print()
        
        # Next Quarter Plan
        print("-" * 80)
        print(f"PLAN FOR {review['next_quarter_plan']['next_quarter']}")
        print("-" * 80)
        plan = review['next_quarter_plan']
        print("\nRecommendations:")
        for rec in plan['recommendations']:
            print(f"  [{rec['priority'].upper()}] {rec['recommendation']}")
            print(f"    {rec['details']}")
        print("\nFocus Areas:")
        for area in plan['focus_areas']:
            print(f"  • {area}")
        print()
        
        print("=" * 80)
    
    def save_review(self, output_file: str = None):
        """
        Save quarterly review to file.
        
        Args:
            output_file: Path to output file. If None, auto-generates name.
        """
        review = self.generate_quarterly_review()
        
        if not output_file:
            quarter = review['quarter']
            timestamp = datetime.now().strftime("%Y%m%d")
            output_file = f"quarterly_review_{quarter}_{timestamp}.json"
        
        output_path = Path(output_file)
        
        with open(output_path, 'w') as f:
            json.dump(review, f, indent=2)
        
        print(f"\nQuarterly review saved to: {output_path.absolute()}")
        
        # Also update reflections.json with quarterly summary
        self._update_reflections_with_summary(review)
    
    def _update_reflections_with_summary(self, review: Dict[str, Any]):
        """Add quarterly summary to reflections.json."""
        if not self.reflections_data:
            return
        
        quarterly_summaries = self.reflections_data.get("quarterly_summaries", [])
        
        # Create summary entry
        summary_entry = {
            "quarter": review["quarter"],
            "generated_at": review["generated_at"],
            "total_tasks_completed": review["summary"]["tasks"].get("total_tasks_completed", 0),
            "total_hours_worked": review["summary"]["tasks"].get("total_hours_invested", 0),
            "total_lessons_learned": review["summary"]["lessons_learned"].get("total_lessons", 0),
            "unresolved_gaps": review["summary"]["unresolved_gaps"].get("total_unresolved_gaps", 0),
            "next_quarter_focus": review["next_quarter_plan"].get("focus_areas", [])
        }
        
        # Remove existing summary for this quarter if present
        quarterly_summaries = [s for s in quarterly_summaries if s.get("quarter") != review["quarter"]]
        quarterly_summaries.append(summary_entry)
        
        self.reflections_data["quarterly_summaries"] = quarterly_summaries
        self._save_json(self.reflections_file, self.reflections_data)
        
        print(f"Updated reflections.json with {review['quarter']} summary")


def main():
    """Main function to generate quarterly review."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate JARVIS quarterly review")
    parser.add_argument(
        "--quarter",
        type=str,
        help="Quarter to review (e.g., Q1, Q2, Q3, Q4). Defaults to current quarter."
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output file path. If not specified, auto-generates filename."
    )
    
    args = parser.parse_args()
    
    print("JARVIS Quarterly Review Generator")
    print("=" * 80)
    print()
    
    # Initialize generator
    generator = QuarterlyReviewGenerator(quarter=args.quarter)
    
    # Print review
    generator.print_review()
    
    # Save review
    generator.save_review(args.output)


if __name__ == "__main__":
    main()
