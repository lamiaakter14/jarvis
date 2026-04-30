"""
Cognitive Loop Agent — Analyzes patterns & suggests improvements
Phase 7: Cognitive Loop for Money Mode
"""

from typing import Dict, Any, List
from datetime import datetime

class CognitiveAgent:
    """Learn from income patterns and suggest optimizations"""
    
    def analyze_progress(self, daily_income: List[float], target: float, days_remaining: int) -> Dict[str, Any]:
        """Analyze income patterns and provide insights"""
        
        if not daily_income:
            return {"status": "No data yet", "suggestions": ["Start tracking daily income"]}
        
        total_earned = sum(daily_income)
        avg_daily = total_earned / len(daily_income)
        best_day = max(daily_income) if daily_income else 0
        
        # Calculate projection
        projected = total_earned + (avg_daily * days_remaining)
        
        suggestions = []
        
        if projected < target:
            gap = target - projected
            suggestions.append(f"⚠️ Projected shortfall: ৳{gap:.0f}. Need +{gap/days_remaining:.0f} BDT/day")
            suggestions.append("💡 Try: Higher rate gigs, bundle services, rush delivery fees")
        elif projected > target:
            suggestions.append(f"�� On track to exceed by ৳{projected-target:.0f}!")
            suggestions.append("💡 Consider: Stretch goal or invest surplus in skills")
        
        # Pattern detection
        if len(daily_income) >= 3:
            recent = daily_income[-3:]
            if recent[0] < recent[1] < recent[2]:
                suggestions.append("📈 Momentum building! Keep the streak alive!")
            elif recent[0] > recent[1] > recent[2]:
                suggestions.append("⚠️ Declining trend. Time to push harder!")
        
        return {
            "total_earned": total_earned,
            "average_daily": avg_daily,
            "best_day": best_day,
            "projected_earnings": projected,
            "gap_to_target": max(0, target - projected),
            "suggestions": suggestions,
            "pattern": self._detect_pattern(daily_income)
        }
    
    def _detect_pattern(self, data: List[float]) -> str:
        """Simple pattern detection"""
        if len(data) < 4:
            return "Insufficient data"
        
        increasing = all(data[i] <= data[i+1] for i in range(len(data)-1))
        decreasing = all(data[i] >= data[i+1] for i in range(len(data)-1))
        
        if increasing:
            return "Steady growth 📈"
        elif decreasing:
            return "Declining 📉"
        else:
            return "Fluctuating 🔄"
    
    def suggest_optimizations(self, skills: List[str], platforms: List[str]) -> List[str]:
        """Suggest platform-specific optimizations"""
        suggestions = []
        
        if "Upwork" in platforms:
            suggestions.append("Upwork: Apply within 30 seconds of job posting")
        if "Fiverr" in platforms:
            suggestions.append("Fiverr: Add video intro → 3x conversion")
        if "Facebook" in platforms:
            suggestions.append("Facebook: Join 20+ buy/sell groups")
        
        if "coding" in skills:
            suggestions.append("💻 Premium skill: Charge ৳1000-1500/hour")
        if "graphic_design" in skills:
            suggestions.append("🎨 Bundle: Logo + Banner + Social post = ৳2500")
        
        return suggestions

cognitive_agent = CognitiveAgent()
