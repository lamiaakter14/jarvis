"""
Money Mode Agent — Survival Income Planner
v5.3.0 | Phase 6: Money Mode
"""

from typing import List, Dict, Any
from datetime import datetime, timedelta
import random


class MoneyAgent:
    """Plan daily income goals based on skills & platforms"""
    
    def __init__(self):
        self.platform_mapping = {
            "Fiverr": {
                "min_rate": 500,
                "max_rate": 5000,
                "setup_time": 2,  # hours
                "earning_potential": "High"
            },
            "Upwork": {
                "min_rate": 800,
                "max_rate": 8000,
                "setup_time": 3,
                "earning_potential": "Very High"
            },
            "Facebook": {
                "min_rate": 300,
                "max_rate": 3000,
                "setup_time": 1,
                "earning_potential": "Medium"
            },
            "Local": {
                "min_rate": 1000,
                "max_rate": 10000,
                "setup_time": 4,
                "earning_potential": "Immediate"
            }
        }
        
        self.skill_platforms = {
            "graphic_design": ["Fiverr", "Upwork", "Facebook"],
            "content_writing": ["Fiverr", "Upwork"],
            "video_editing": ["Fiverr", "Upwork", "Facebook"],
            "web_development": ["Upwork", "Fiverr"],
            "data_entry": ["Fiverr", "Facebook", "Local"],
            "virtual_assistant": ["Upwork", "Facebook", "Local"],
            "social_media": ["Facebook", "Fiverr"],
            "coding": ["Upwork", "Fiverr"],
            "teaching": ["Local", "Facebook"],
            "photography": ["Facebook", "Local", "Fiverr"]
        }
    
    def plan(self, target_amount: int, days: int, skills: List[str]) -> Dict[str, Any]:
        """
        Generate survival plan for target amount in given days
        
        Args:
            target_amount: Total money needed (BDT)
            days: Number of days to achieve
            skills: List of user skills
        
        Returns:
            dict: Complete plan with daily tasks, platform matches
        """
        
        daily_target = target_amount / days
        hourly_rate = self._estimate_hourly_rate(skills)
        hours_needed = daily_target / hourly_rate if hourly_rate > 0 else 8
        
        # Match skills to platforms
        recommended_platforms = self._match_platforms(skills)
        
        # Generate daily action plan
        daily_plan = self._generate_daily_plan(
            days, daily_target, hourly_rate, hours_needed, recommended_platforms
        )
        
        # Calculate total hours needed
        total_hours = hours_needed * days
        
        return {
            "goal": {
                "amount": target_amount,
                "days": days,
                "daily_target": round(daily_target, 2),
                "hourly_rate": hourly_rate,
                "hours_needed_per_day": round(hours_needed, 1),
                "total_hours_needed": round(total_hours, 1)
            },
            "skills": skills,
            "recommended_platforms": recommended_platforms,
            "platform_details": {
                p: self.platform_mapping[p] for p in recommended_platforms if p in self.platform_mapping
            },
            "daily_plan": daily_plan,
            "tips": self._generate_tips(skills, recommended_platforms),
            "survival_quote": self._get_survival_quote()
        }
    
    def track_progress(self, current_income: float, target_amount: float) -> Dict[str, Any]:
        """Track income progress against target"""
        percentage = (current_income / target_amount) * 100 if target_amount > 0 else 0
        
        if percentage >= 100:
            status = "ACHIEVED 🎉"
            message = "Goal unlocked! Party time!"
        elif percentage >= 75:
            status = "ALMOST THERE 🔥"
            message = f"{100-percentage:.1f}% left — keep pushing!"
        elif percentage >= 50:
            status = "HALFWAY 💪"
            message = "Good progress! Double the hustle!"
        elif percentage >= 25:
            status = "ON TRACK 📈"
            message = "Building momentum! Stay consistent!"
        else:
            status = "STARTING 🚀"
            message = "First step taken! Keep grinding!"
        
        return {
            "current": current_income,
            "target": target_amount,
            "percentage": round(percentage, 1),
            "remaining": target_amount - current_income,
            "status": status,
            "message": message
        }
    
    def _estimate_hourly_rate(self, skills: List[str]) -> float:
        """Estimate hourly rate in BDT based on skills"""
        rates = {
            "graphic_design": 500,
            "content_writing": 400,
            "video_editing": 600,
            "web_development": 800,
            "data_entry": 300,
            "virtual_assistant": 350,
            "social_media": 450,
            "coding": 1000,
            "teaching": 400,
            "photography": 500
        }
        
        if not skills:
            return 350  # Default rate
        
        total_rate = sum(rates.get(skill.lower(), 350) for skill in skills)
        return total_rate / len(skills)
    
    def _match_platforms(self, skills: List[str]) -> List[str]:
        """Match skills to best platforms"""
        all_platforms = set()
        
        for skill in skills:
            skill_lower = skill.lower().replace(" ", "_")
            platforms = self.skill_platforms.get(skill_lower, ["Fiverr", "Facebook"])
            all_platforms.update(platforms)
        
        # Prioritize platforms by earning potential
        priority = ["Local", "Upwork", "Fiverr", "Facebook"]
        matched = [p for p in priority if p in all_platforms]
        
        return matched[:3]  # Top 3 platforms
    
    def _generate_daily_plan(self, days: int, daily_target: float, 
                            hourly_rate: float, hours_needed: float, 
                            platforms: List[str]) -> List[Dict[str, Any]]:
        """Generate day-by-day action plan"""
        plan = []
        
        # Day 1-2: Setup & Profile
        plan.append({
            "day": 1,
            "title": "🛠️ Platform Setup",
            "tasks": [
                f"Create/optimize profiles on {', '.join(platforms[:2])}",
                "Write compelling bio highlighting your skills",
                "Upload portfolio samples (at least 3)",
                f"Set hourly rate: {hourly_rate} BDT/hour",
                "Research top 10 gigs in your niche"
            ],
            "estimated_earnings": 0,
            "time_needed": 3
        })
        
        # Day 2-3: First clients
        if days >= 2:
            plan.append({
                "day": 2,
                "title": "🎯 Active Bidding",
                "tasks": [
                    f"Send proposals to 5+ projects on {platforms[0]}",
                    "Respond to 10+ Facebook group requests",
                    "Create 3 service listing variations",
                    f"Target: {int(daily_target/2)} BDT mini projects",
                    "Ask previous clients for testimonials"
                ],
                "estimated_earnings": daily_target * 0.5,
                "time_needed": 5
            })
        
        # Daily earning tasks
        for day in range(3, min(days + 1, 8)):
            plan.append({
                "day": day,
                "title": f"💼 Day {day}: Hustle Mode",
                "tasks": [
                    f"Complete {int(hours_needed)} hours of paid work",
                    f"Send 3+ new proposals on {platforms[0]}",
                    "Follow up on pending offers",
                    "Deliver completed work within 4 hours",
                    "Ask for reviews after each delivery"
                ],
                "estimated_earnings": daily_target,
                "time_needed": round(hours_needed, 1)
            })
        
        # Final days strategy
        if days > 7:
            plan.append({
                "day": days,
                "title": "🏁 Final Push",
                "tasks": [
                    "Complete all pending deliveries",
                    "Request immediate payment from clients",
                    "Offer express delivery (50% extra fee)",
                    f"Target remaining: {daily_target * 1.5} BDT",
                    "Update progress tracker"
                ],
                "estimated_earnings": daily_target * 1.5,
                "time_needed": round(hours_needed * 1.2, 1)
            })
        
        return plan[:min(days, 10)]  # Max 10 days plan
    
    def _generate_tips(self, skills: List[str], platforms: List[str]) -> List[str]:
        """Generate actionable tips"""
        tips = [
            "🔥 Start with small gigs (500-1000 BDT) to build reviews",
            "📱 Keep phone notifications ON for instant replies",
            "💬 Always ask 'Budget koto?' before starting work",
            "⭐ Deliver 30 min early for bonus ratings",
            "🔄 Bundle services: 'Logo + Banner = 1500 BDT'",
            "🎯 Target weekend clients (pay faster)",
            "📸 Before/after screenshots = social proof"
        ]
        
        if "Fiverr" in platforms:
            tips.append("🚀 Fiverr: 7 gig images + video intro = 3x clicks")
        if "Upwork" in platforms:
            tips.append("�� Upwork: Apply within 5 minutes of job post")
        if "Facebook" in platforms:
            tips.append("📢 Facebook: Join 10+ buy/sell groups NOW")
        if "Local" in platforms:
            tips.append("🏪 Local: Visit 5 shops tomorrow with rate card")
        
        return tips[:6]
    
    def _get_survival_quote(self) -> str:
        """Motivational quote for survival mode"""
        quotes = [
            "7 din e 10,000 Taka — Possible? Hustle korle YES! 💪",
            "Bidai din e taka khamu? Na, ajkei start! 🚀",
            "Skill thakle income r distance kom! 🎯",
            "Freelancing = apnar time er value fixed kora! ⏰",
            "10 offers pathaben, 1 ta paiben — eta law! 📊"
        ]
        return random.choice(quotes)

# Singleton instance
money_agent = MoneyAgent()
