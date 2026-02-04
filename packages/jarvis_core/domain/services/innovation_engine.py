"""Innovation engine domain service."""

from typing import List, Dict, Any

from jarvis_core.domain.entities.task import Task
from jarvis_core.domain.entities.context import Context
from jarvis_core.domain.entities.innovation import Innovation
from jarvis_core.shared.utils import generate_id
from jarvis_core.shared.exceptions import DomainException


class InnovationEngine:
    """Service for identifying innovations and suggesting improvements.
    
    The InnovationEngine analyzes patterns in tasks, performance data,
    and context to generate novel ideas and improvement suggestions.
    """
    
    def analyze_patterns(
        self,
        tasks: List[Task],
        context: Context
    ) -> List[Innovation]:
        """Analyze task patterns to identify innovation opportunities.
        
        Looks for recurring patterns, inefficiencies, and optimization
        opportunities in task execution.
        
        Args:
            tasks: List of tasks to analyze
            context: Current execution context
            
        Returns:
            List of identified innovations
        """
        if not tasks:
            return []
        
        innovations = []
        
        # Pattern 1: Identify frequently repeated task types
        task_titles = [t.title.lower() for t in tasks]
        title_counts = {}
        for title in task_titles:
            # Extract key terms (first 3 words)
            key = " ".join(title.split()[:3])
            title_counts[key] = title_counts.get(key, 0) + 1
        
        # Suggest automation for repeated tasks
        for key, count in title_counts.items():
            if count >= 3:  # Threshold for repetition
                innovations.append(Innovation(
                    title=f"Automate '{key}' tasks",
                    description=f"Consider automating this task type which appears {count} times",
                    category="process",
                    impact_score=0.6 + min(count * 0.05, 0.3),
                    created_by="pattern_analyzer"
                ))
        
        # Pattern 2: Identify high-effort, low-ROI tasks
        inefficient_tasks = [
            t for t in tasks
            if t.cognitive_load.estimated_hours > 2.0 and t.roi.is_low_value()
        ]
        
        if inefficient_tasks:
            innovations.append(Innovation(
                title="Optimize or eliminate low-ROI tasks",
                description=f"Found {len(inefficient_tasks)} high-effort, low-ROI tasks",
                category="strategic",
                impact_score=0.7,
                created_by="efficiency_analyzer"
            ))
        
        # Pattern 3: Suggest learning based on gaps in context
        if context.gaps:
            high_severity_gaps = [g for g in context.gaps if g.get("severity") in ["high", "critical"]]
            if high_severity_gaps:
                innovations.append(Innovation(
                    title="Implement structured learning program",
                    description=f"Address {len(high_severity_gaps)} critical knowledge/skill gaps",
                    category="learning",
                    impact_score=0.8,
                    created_by="gap_analyzer"
                ))
        
        # Pattern 4: Suggest strategic alignment improvements
        if context.strategic_goals and len(tasks) > 5:
            # Count tasks aligned with strategic goals
            aligned_count = 0
            for task in tasks:
                task_terms = set(task.title.lower().split())
                for goal in context.strategic_goals:
                    goal_terms = set(goal.lower().split())
                    if task_terms.intersection(goal_terms):
                        aligned_count += 1
                        break
            
            alignment_rate = aligned_count / len(tasks)
            if alignment_rate < 0.5:  # Less than 50% aligned
                innovations.append(Innovation(
                    title="Improve strategic alignment of tasks",
                    description=f"Only {alignment_rate*100:.0f}% of tasks align with strategic goals",
                    category="strategic",
                    impact_score=0.75,
                    created_by="alignment_analyzer"
                ))
        
        return innovations
    
    def suggest_improvements(
        self,
        performance_data: Dict[str, Any]
    ) -> List[Innovation]:
        """Suggest improvements based on performance metrics.
        
        Analyzes execution metrics to identify areas for improvement.
        
        Args:
            performance_data: Dictionary containing performance metrics
            
        Returns:
            List of improvement suggestions as innovations
        """
        innovations = []
        
        # Check success rate
        success_rate = performance_data.get("success_rate", 1.0)
        if success_rate < 0.8:  # Below 80% success
            innovations.append(Innovation(
                title="Improve agent reliability",
                description=f"Current success rate is {success_rate*100:.1f}% - investigate failures",
                category="technical",
                impact_score=0.85,
                created_by="performance_analyzer"
            ))
        
        # Check execution time
        avg_time = performance_data.get("average_execution_time", 0.0)
        if avg_time > 300:  # More than 5 minutes average
            innovations.append(Innovation(
                title="Optimize execution performance",
                description=f"Average execution time is {avg_time:.0f}s - identify bottlenecks",
                category="technical",
                impact_score=0.7,
                created_by="performance_analyzer"
            ))
        
        # Check task completion rate
        completed = performance_data.get("completed_tasks", 0)
        total = performance_data.get("total_tasks", 1)
        completion_rate = completed / total if total > 0 else 0
        
        if completion_rate < 0.7:  # Less than 70% completion
            innovations.append(Innovation(
                title="Improve task completion rate",
                description=f"Only {completion_rate*100:.0f}% of tasks completed - review blockers",
                category="process",
                impact_score=0.8,
                created_by="completion_analyzer"
            ))
        
        # Check for idle time
        utilized_hours = performance_data.get("utilized_hours", 0.0)
        available_hours = performance_data.get("available_hours", 8.0)
        utilization = utilized_hours / available_hours if available_hours > 0 else 0
        
        if utilization < 0.6:  # Less than 60% utilization
            innovations.append(Innovation(
                title="Improve time utilization",
                description=f"Only {utilization*100:.0f}% of available time utilized",
                category="process",
                impact_score=0.65,
                created_by="utilization_analyzer"
            ))
        
        return innovations
    
    def score_innovation(self, innovation: Innovation) -> float:
        """Calculate a comprehensive score for an innovation.
        
        Considers impact, category, age, and status to determine
        overall innovation value.
        
        Args:
            innovation: Innovation to score
            
        Returns:
            Score from 0.0 to 1.0
        """
        # Base score from impact
        score = innovation.impact_score
        
        # Adjust for category (strategic and learning are valued higher)
        category_weights = {
            "strategic": 1.2,
            "learning": 1.15,
            "process": 1.1,
            "technical": 1.0,
            "general": 0.9
        }
        category_weight = category_weights.get(innovation.category, 1.0)
        score *= category_weight
        
        # Penalize older innovations (decreasing relevance)
        age_days = innovation.get_age_in_days()
        if age_days > 30:
            age_penalty = 1.0 - min((age_days - 30) * 0.01, 0.3)  # Max 30% penalty
            score *= age_penalty
        
        # Bonus for approved innovations
        if innovation.is_approved():
            score *= 1.1
        
        # Penalty for rejected innovations
        if innovation.is_rejected():
            score *= 0.5
        
        # Normalize to 0-1 range
        return min(max(score, 0.0), 1.0)
    
    def rank_innovations(
        self,
        innovations: List[Innovation]
    ) -> List[Innovation]:
        """Rank innovations by their comprehensive score.
        
        Args:
            innovations: List of innovations to rank
            
        Returns:
            Sorted list of innovations (highest score first)
        """
        if not innovations:
            return []
        
        # Score each innovation and sort
        scored = [(self.score_innovation(inn), inn) for inn in innovations]
        scored.sort(reverse=True, key=lambda x: x[0])
        
        return [inn for _, inn in scored]
    
    def filter_actionable_innovations(
        self,
        innovations: List[Innovation],
        min_score: float = 0.6
    ) -> List[Innovation]:
        """Filter innovations to only those worth acting on.
        
        Args:
            innovations: List of innovations to filter
            min_score: Minimum score threshold (default 0.6)
            
        Returns:
            Filtered list of high-value innovations
            
        Raises:
            DomainException: If min_score is invalid
        """
        if not 0.0 <= min_score <= 1.0:
            raise DomainException("Minimum score must be between 0.0 and 1.0")
        
        if not innovations:
            return []
        
        actionable = [
            inn for inn in innovations
            if self.score_innovation(inn) >= min_score and 
            (inn.is_proposed() or inn.is_approved())
        ]
        
        return self.rank_innovations(actionable)
