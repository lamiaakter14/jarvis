
@app.get("/api/money/plan")
async def money_plan_get(target_amount: int = 10000, days: int = 7, skills: str = "graphic_design"):
    """GET version for browser testing"""
    skills_list = [s.strip() for s in skills.split(",")]
    from jarvis_core.agents.money_agent import money_agent
    result = money_agent.plan(
        target_amount=target_amount,
        days=days,
        skills=skills_list
    )
    return {"status": "success", "plan": result}
