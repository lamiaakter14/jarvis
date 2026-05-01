"""Phase 11: Output Composer - Structured JSON output with UI components."""

from typing import Dict, List, Any
from datetime import datetime, timezone

class OutputComposer:
    """Composes structured output with UI component instructions."""
    
    @staticmethod
    def compose(intent: Dict, strategy: Dict = None, validation: Dict = None, 
                execution: Dict = None, memory: List[str] = None) -> Dict:
        return {
            "status": "success",
            "version": "11.0.0",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "intent": intent,
            "strategy": strategy,
            "validation": validation,
            "approval_required": validation["recommendation"] != "proceed" if validation else True,
            "execution_plan": execution.get("tasks", []) if execution else [],
            "ui_components": OutputComposer._build_ui(strategy, validation, intent),
            "memory_updates": memory or []
        }
    
    @staticmethod
    def _build_ui(strategy: Dict, validation: Dict, intent: Dict) -> List[Dict]:
        components = []
        
        if strategy:
            components.append({
                "type": "project_card",
                "data": {
                    "id": strategy.get("project_id"),
                    "title": strategy.get("title"),
                    "phases_count": len(strategy.get("phases", [])),
                    "tasks_count": len(strategy.get("tasks", [])),
                    "domain": strategy.get("domain", "general")
                }
            })
            
            components.append({
                "type": "phase_list",
                "data": strategy.get("phases", [])
            })
            
            components.append({
                "type": "task_list",
                "data": strategy.get("tasks", [])[:10]
            })
        
        if validation:
            if not validation.get("feasible"):
                components.append({
                    "type": "warning_card",
                    "data": {
                        "title": "⚠️ Validation Issues",
                        "risks": validation.get("risks", []),
                        "missing": validation.get("missing_requirements", []),
                        "score": validation.get("score", 0)
                    }
                })
            
            components.append({
                "type": "approval_buttons",
                "data": {
                    "can_approve": validation.get("feasible", False),
                    "needs_review": validation.get("recommendation") == "review"
                }
            })
        
        return components
