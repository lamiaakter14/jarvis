"""
Context-Aware Planner — Auto-loads local contexts for project planning
Phase 7.5: Full integration with Master Chat
"""

import re
from typing import List, Dict, Any
from jarvis_core.memory.context_store import context_store

class ContextPlanner:
    """Plan projects using local Bangladesh/Sakhipur contexts"""
    
    # Project type detection
    PROJECT_TYPES = {
        "juice_bar": ["জুস বার", "জুসের দোকান", "juice bar", "juice shop", "ফলের জুস"],
        "restaurant": ["রেস্টুরেন্ট", "হোটেল", "restaurant", "hotel", "খাবারের দোকান"],
        "grocery": ["কিরানা", "মুদি", "grocery", "দোকান"],
        "construction": ["বাড়ি", "ঘর", "house", "building", "নির্মাণ", "construction"],
        "renovation": ["রিনোভেশন", "সংস্কার", "renovation", "repair"],
    }
    
    # Budget ranges by project type (BDT)
    BUDGET_RANGES = {
        "juice_bar": {"min": 25000, "max": 40000, "description": "Construction + Equipment"},
        "restaurant": {"min": 50000, "max": 150000, "description": "Full setup"},
        "grocery": {"min": 30000, "max": 80000, "description": "Shop + Inventory"},
        "construction": {"min": 80000, "max": 200000, "description": "Per 1000 sq ft"},
        "renovation": {"min": 20000, "max": 60000, "description": "Room renovation"},
    }
    
    def detect_project_type(self, user_input: str) -> str:
        """Detect project type from user input"""
        user_lower = user_input.lower()
        for project_type, keywords in self.PROJECT_TYPES.items():
            for keyword in keywords:
                if keyword in user_lower:
                    return project_type
        return "general"
    
    def extract_keywords(self, user_input: str) -> List[str]:
        """Extract relevant keywords from user input"""
        user_lower = user_input.lower()
        keywords = []
        
        # Location keywords
        if "সখীপুর" in user_lower or "sakhipur" in user_lower:
            keywords.append("সখীপুর")
        
        # Material keywords
        material_keywords = ["কাঠ", "timber", "সিমেন্ট", "cement", "ইট", "brick"]
        for kw in material_keywords:
            if kw in user_lower:
                keywords.append(kw)
        
        # Labour keywords
        if "শ্রমিক" in user_lower or "labour" in user_lower or "মিস্ত্রি" in user_lower:
            keywords.append("labour")
        
        # Business keywords
        if "দোকান" in user_lower or "shop" in user_lower or "ব্যবসা" in user_lower:
            keywords.append("shop")
        
        return keywords[:5]
    
    def load_relevant_contexts(self, keywords: List[str], project_type: str) -> List[Dict[str, Any]]:
        """Load contexts matching keywords and project type"""
        all_contexts = []
        
        # Always load base contexts for Sakhipur
        base_contexts = context_store.get_by_keyword("সখীপুর")
        all_contexts.extend(base_contexts)
        
        # Load contexts by keywords
        for keyword in keywords:
            contexts = context_store.get_by_keyword(keyword)
            all_contexts.extend(contexts)
        
        # Project-specific contexts
        if project_type == "juice_bar":
            # Load shop-related contexts
            shop_contexts = context_store.get_by_keyword("দোকান")
            all_contexts.extend(shop_contexts)
        
        # Remove duplicates by id
        seen = set()
        unique_contexts = []
        for ctx in all_contexts:
            if ctx["id"] not in seen:
                seen.add(ctx["id"])
                unique_contexts.append(ctx)
        
        return unique_contexts[:10]
    
    def generate_context_summary(self, contexts: List[Dict[str, Any]]) -> str:
        """Generate formatted summary of loaded contexts"""
        if not contexts:
            return ""
        
        summary = "\n📍 **Local Context Loaded!**\n"
        for ctx in contexts[:5]:  # Show top 5
            icon = "🏪" if ctx["category"] == "market_price" else "👷" if ctx["category"] == "labour" else "🚗" if ctx["category"] == "transport" else "��"
            summary += f"   {icon} **{ctx['key']}**: {ctx['value']}\n"
        
        if len(contexts) > 5:
            summary += f"   ... and {len(contexts)-5} more contexts\n"
        
        return summary
    
    def get_budget_estimate(self, project_type: str) -> str:
        """Get budget estimate for project type"""
        budget = self.BUDGET_RANGES.get(project_type, {"min": 10000, "max": 50000, "description": "General"})
        
        estimate = f"\n💰 **Budget Estimate:**\n"
        estimate += f"   - **{budget['description']}:** ৳{budget['min']:,} - ৳{budget['max']:,}\n"
        
        # Add monthly costs if applicable
        if project_type in ["juice_bar", "restaurant", "grocery"]:
            estimate += f"   - **Monthly rent:** ৳5,000 - ৳15,000\n"
            estimate += f"   - **Labour (daily):** ৳500/day\n"
        
        return estimate
    
    def generate_action_plan(self, project_type: str) -> str:
        """Generate action plan based on project type"""
        plans = {
            "juice_bar": """
📋 **Action Plan:**
   1. 🔲 Find shop location (100-200 sq ft)
   2. 🔲 Setup furniture (৳10,000-15,000)
   3. 🔲 Buy equipment (juicer, refrigerator) 
   4. 🔲 Purchase raw materials (fruits, ice)
   5. 🔲 Hire 1-2 staff (৳500/day each)
   6. 🔲 Marketing (local banners, Facebook)
""",
            "restaurant": """
📋 **Action Plan:**
   1. 🔲 Location scouting (300-500 sq ft)
   2. 🔲 Kitchen setup (৳50,000-80,000)
   3. 🔲 Dining furniture (৳30,000-50,000)
   4. 🔲 Staff hiring (cook + helper)
   5. 🔲 License & permissions
""",
            "general": """
📋 **Action Plan:**
   1. 🔲 Detailed requirement analysis
   2. 🔲 Get multiple quotes from locals
   3. 🔲 Create timeline (7-14 days)
   4. 🔲 Execute with local labour
"""
        }
        return plans.get(project_type, plans["general"])
    
    def process_query(self, user_input: str) -> Dict[str, Any]:
        """Main method - process user query and return full response"""
        project_type = self.detect_project_type(user_input)
        keywords = self.extract_keywords(user_input)
        contexts = self.load_relevant_contexts(keywords, project_type)
        context_summary = self.generate_context_summary(contexts)
        budget_estimate = self.get_budget_estimate(project_type)
        action_plan = self.generate_action_plan(project_type)
        
        # Generate friendly response
        if project_type == "juice_bar":
            main_response = f"🍹 **জুস বার খুলতে চান? Great idea!**\n\n{context_summary}{budget_estimate}{action_plan}\n\n**Ready to plan details?** বলুন কিভাবে সাহায্য করি! 🚀"
        elif contexts:
            main_response = f"{context_summary}{budget_estimate}{action_plan}\n\n**কিভাবে এগোতে চান?** বলুন! 💪"
        else:
            main_response = f"আমি আপনার জন্য লোকাল কনটেক্স লোড করেছি।{budget_estimate}\n\nআরও বিস্তারিত জানালে better plan দিতে পারব! 🎯"
        
        return {
            "response": main_response,
            "contexts_loaded": contexts,
            "keywords_detected": keywords,
            "project_type": project_type,
            "budget": self.BUDGET_RANGES.get(project_type, {}),
            "has_contexts": len(contexts) > 0
        }

context_planner = ContextPlanner()
