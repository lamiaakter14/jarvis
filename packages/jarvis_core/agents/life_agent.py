"""Long-term Life System Agent - Phase 8"""

from datetime import datetime
from typing import Dict, Any, List
from pathlib import Path
import json

class LifeAgent:
    def __init__(self):
        self.storage_path = Path.home() / ".jarvis" / "life_data.json"
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.data = self._load()

    def _load(self) -> Dict[str, Any]:
        if self.storage_path.exists():
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self._get_default()

    def _get_default(self) -> Dict[str, Any]:
        return {
            "mp_election_2036": {
                "target_year": 2036,
                "target_role": "জাতীয় সংসদ সদস্য",
                "constituency": "Sakhipur/Tangail",
                "progress": 25,
                "milestones": [
                    {"year": 2024, "title": "Start business/venture", "completed": True},
                    {"year": 2025, "title": "Build local network", "completed": True},
                    {"year": 2026, "title": "Community service projects", "completed": False},
                    {"year": 2028, "title": "Join local politics", "completed": False},
                    {"year": 2030, "title": "Union Parishad level", "completed": False},
                    {"year": 2032, "title": "Upazila level recognition", "completed": False},
                    {"year": 2034, "title": "District level campaign", "completed": False},
                    {"year": 2036, "title": "MP Election 🎯", "completed": False}
                ]
            },
            "skills": {
                "web_development": {"current": 80, "required": 90, "priority": "medium"},
                "public_speaking": {"current": 20, "required": 85, "priority": "high"},
                "leadership": {"current": 50, "required": 90, "priority": "high"},
                "networking": {"current": 60, "required": 85, "priority": "high"},
                "bangla_writing": {"current": 40, "required": 70, "priority": "medium"},
                "political_knowledge": {"current": 30, "required": 80, "priority": "high"},
                "fundraising": {"current": 25, "required": 75, "priority": "high"}
            },
            "network": {"political": 3, "social": 5, "business": 4, "total": 12, "target": 50},
            "islamic_practice": {
                "daily_prayers": {"fajr": False, "dhuhr": False, "asr": False, "maghrib": False, "isha": False},
                "quran_pages_today": 0, "quran_completion": 0, "fasting": {"ramadan": 0, "nafl": 0},
                "last_updated": datetime.now().isoformat()
            },
            "daily_accountability": [],
            "financial": {
                "campaign_budget_target": 10000000, "current_savings": 0, "monthly_saving_goal": 50000,
                "funding_sources": {"personal": 0, "donors": 0, "party": 0, "other": 0},
                "expenses": {"advertising": 0, "rallies": 0, "transport": 0, "staff": 0, "materials": 0},
                "monthly_tracking": [], "last_updated": datetime.now().isoformat()
            },
            "created_at": datetime.now().isoformat()
        }

    def _save(self):
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def get_dashboard(self) -> Dict[str, Any]:
        mp = self.data["mp_election_2036"]
        skills = self.data["skills"]
        completed = sum(1 for m in mp["milestones"] if m["completed"])
        avg_current = sum(s["current"] for s in skills.values()) / len(skills)
        avg_required = sum(s["required"] for s in skills.values()) / len(skills)
        return {
            "mp_election_2036": mp,
            "mp_progress": mp["progress"],
            "milestones": {"completed": completed, "total": len(mp["milestones"]), "percentage": (completed / len(mp["milestones"])) * 100},
            "skills": skills,
            "skill_gap": {"average_current": avg_current, "average_required": avg_required, "gap": avg_required - avg_current},
            "network": self.data["network"],
            "islamic_practice": self.data["islamic_practice"],
            "daily_accountability": self.data["daily_accountability"][:7],
            "financial": self.data["financial"]
        }

    def update_skill(self, skill_name: str, current_level: int) -> Dict[str, Any]:
        if skill_name in self.data["skills"]:
            self.data["skills"][skill_name]["current"] = min(current_level, 100)
            self._save()
            return {"status": "updated", "skill": skill_name, "current": current_level}
        return {"error": "Skill not found"}

    def update_prayer(self, prayer_name: str, completed: bool) -> Dict[str, Any]:
        if prayer_name in self.data["islamic_practice"]["daily_prayers"]:
            self.data["islamic_practice"]["daily_prayers"][prayer_name] = completed
            self._save()
            return {"status": "updated", "prayer": prayer_name, "completed": completed}
        return {"error": "Prayer not found"}

    def update_quran(self, pages: int) -> Dict[str, Any]:
        total = self.data["islamic_practice"].get("total_pages_read", 0) + pages
        self.data["islamic_practice"]["total_pages_read"] = total
        self.data["islamic_practice"]["quran_completion"] = (total / 604) * 100
        self._save()
        return {"status": "updated", "pages_today": pages, "completion": self.data["islamic_practice"]["quran_completion"]}

    def add_contact(self, category: str, name: str, role: str) -> Dict[str, Any]:
        if "contacts" not in self.data["network"]:
            self.data["network"]["contacts"] = []
        self.data["network"]["contacts"].append({"name": name, "role": role, "category": category, "added_at": datetime.now().isoformat()})
        self.data["network"][category] = self.data["network"].get(category, 0) + 1
        self.data["network"]["total"] = len(self.data["network"]["contacts"])
        self._save()
        return {"status": "added", "contact": {"name": name, "role": role, "category": category}}

    def add_accountability(self, task: str) -> Dict[str, Any]:
        entry = {"date": datetime.now().strftime("%Y-%m-%d"), "task": task, "completed": True, "timestamp": datetime.now().isoformat()}
        self.data["daily_accountability"].append(entry)
        self._save()
        return {"status": "recorded", "entry": entry}

    def update_milestone(self, milestone_index: int, completed: bool) -> Dict[str, Any]:
        milestones = self.data["mp_election_2036"]["milestones"]
        if 0 <= milestone_index < len(milestones):
            milestones[milestone_index]["completed"] = completed
            completed_count = sum(1 for m in milestones if m["completed"])
            self.data["mp_election_2036"]["progress"] = (completed_count / len(milestones)) * 100
            self._save()
            return {"status": "updated", "milestone": milestones[milestone_index]["title"], "completed": completed}
        return {"error": "Milestone not found"}

    def update_savings(self, amount: int) -> Dict[str, Any]:
        self.data["financial"]["current_savings"] += amount
        self._save()
        progress = (self.data["financial"]["current_savings"] / self.data["financial"]["campaign_budget_target"]) * 100
        return {
            "status": "updated",
            "current_savings": self.data["financial"]["current_savings"],
            "target": self.data["financial"]["campaign_budget_target"],
            "progress": progress,
            "remaining": self.data["financial"]["campaign_budget_target"] - self.data["financial"]["current_savings"]
        }

    def get_financial_goals(self) -> Dict[str, Any]:
        return self.data["financial"]

life_agent = LifeAgent()
