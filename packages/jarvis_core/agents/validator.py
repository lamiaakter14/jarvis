"""Phase 11: Validator Agent - Feasibility check, risk analysis, missing requirements."""

from typing import Dict, List

class ValidatorAgent:
    """Validates plans before execution - catches impossible requests."""
    
    def __init__(self):
        self.name = "Validator"
        self.version = "1.0.0"
    
    def validate(self, strategy: Dict, intent: Dict) -> Dict:
        checks = []
        risks = []
        missing = []
        score = 10.0
        
        # Budget check
        if intent.get("entities", {}).get("amount"):
            budget = intent["entities"]["amount"]
            if budget < 1000:
                checks.append({"check": "budget", "status": "fail", "message": f"Budget ৳{budget} too low for any project"})
                risks.append("Budget unrealistic")
                score -= 3
            elif budget < 5000:
                checks.append({"check": "budget", "status": "warning", "message": f"Budget ৳{budget} may be tight"})
                score -= 1
        
        # Timeline check
        if intent.get("entities", {}).get("days"):
            days = intent["entities"]["days"]
            if days < 3:
                checks.append({"check": "timeline", "status": "fail", "message": f"{days} days too short"})
                risks.append("Timeline impossible")
                score -= 3
            elif days < 7:
                checks.append({"check": "timeline", "status": "warning", "message": f"{days} days aggressive"})
                score -= 1
        
        # Missing critical info
        if intent.get("domain") == "business":
            if not any(kw in str(strategy).lower() for kw in ["budget", "customer", "competition"]):
                missing.append("Business details (budget, customers, competition)")
                score -= 1
        
        if intent.get("domain") == "coding":
            if not any(kw in str(strategy).lower() for kw in ["tech", "stack", "hosting"]):
                missing.append("Technical requirements (stack, hosting)")
                score -= 1
        
        # Phase count sanity
        phases = strategy.get("phases", [])
        if len(phases) < 2:
            checks.append({"check": "structure", "status": "warning", "message": "Very few phases"})
            score -= 1
        if len(phases) > 10:
            checks.append({"check": "structure", "status": "warning", "message": "Too many phases, consider merging"})
            score -= 1
        
        return {
            "feasible": score >= 5.0,
            "score": max(0, score),
            "checks": checks,
            "risks": risks,
            "missing_requirements": missing,
            "recommendation": "proceed" if score >= 7 else "review" if score >= 5 else "revise"
        }
