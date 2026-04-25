"""End-to-end API validation tests.

These tests exercise every public endpoint of the JARVIS API using FastAPI's
built-in ``TestClient`` (which runs the ASGI app in-process, no live server
required) and validate:

  1. Backend reachability (root + health check)
  2. All agent-bridge read endpoints (cognitive-loop, plans, gaps,
     innovations, performance)
  3. Full task user-flow: list → create → fetch → update → complete → delete

Response shapes are asserted against the TypeScript contracts used by the
frontend so that a passing test suite guarantees "UI renders expected data".
"""

import sys
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Path wiring (mirrors conftest.py but scoped to this module so the test
# can be run in isolation with: pytest tests/e2e/test_api_validation.py)
# ---------------------------------------------------------------------------
ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT / "packages"))
sys.path.insert(0, str(ROOT / "apps" / "api"))

from fastapi.testclient import TestClient  # noqa: E402
from jarvis_api.main import app, _tasks   # noqa: E402


@pytest.fixture(autouse=True)
def clear_task_store():
    """Reset the in-memory task store before every test to ensure isolation."""
    _tasks.clear()
    yield
    _tasks.clear()


@pytest.fixture(scope="module")
def client():
    """Shared TestClient for the module (app is stateless except _tasks)."""
    with TestClient(app, raise_server_exceptions=True) as c:
        yield c


# ===========================================================================
# 1. Backend reachability
# ===========================================================================


@pytest.mark.e2e
class TestBackendReachability:
    """Verify the server is reachable and reports itself as healthy."""

    def test_root_endpoint_returns_200(self, client):
        """GET / must return 200 with basic API info."""
        resp = client.get("/")
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "running"
        assert "version" in body
        assert "JARVIS" in body["message"]

    def test_health_check_returns_healthy(self, client):
        """GET /health must report healthy status and list all 5 agents."""
        resp = client.get("/health")
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "healthy"
        expected_agents = {"strategist", "mentor", "executor", "innovator", "amplifier"}
        assert expected_agents == set(body["agents"])

    def test_unknown_route_returns_404(self, client):
        """Unknown routes must return 404 with structured error body."""
        resp = client.get("/api/does-not-exist")
        assert resp.status_code == 404
        body = resp.json()
        assert "error" in body or "detail" in body  # either FastAPI or custom handler


# ===========================================================================
# 2. Agent-bridge read endpoints
# ===========================================================================


@pytest.mark.e2e
class TestCognitiveLoopEndpoint:
    """POST /api/cognitive-loop – orchestrates all 5 agents."""

    def test_cognitive_loop_returns_success(self, client):
        resp = client.post("/api/cognitive-loop")
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "success"

    def test_cognitive_loop_includes_all_agents(self, client):
        body = client.post("/api/cognitive-loop").json()
        for agent in ("strategist", "mentor", "executor", "innovator", "amplifier"):
            assert agent in body, f"Agent '{agent}' missing from cognitive-loop response"

    def test_strategist_plan_has_tasks_list(self, client):
        body = client.post("/api/cognitive-loop").json()
        plan = body["strategist"]["plan"]
        assert "tasks" in plan
        assert isinstance(plan["tasks"], list)
        assert len(plan["tasks"]) > 0

    def test_mentor_gaps_is_list(self, client):
        body = client.post("/api/cognitive-loop").json()
        gaps = body["mentor"]["gaps"]
        assert isinstance(gaps, list)

    def test_mentor_task_feedback_is_list(self, client):
        body = client.post("/api/cognitive-loop").json()
        feedback = body["mentor"]["task_feedback"]
        assert isinstance(feedback, list)

    def test_innovator_innovations_is_list(self, client):
        body = client.post("/api/cognitive-loop").json()
        innovations = body["innovator"]["innovations"]
        assert isinstance(innovations, list)

    def test_amplifier_performance_has_required_keys(self, client):
        body = client.post("/api/cognitive-loop").json()
        perf = body["amplifier"]["performance"]
        required = {
            "productivity_score",
            "completion_rate",
            "task_completion_trend",
            "task_distribution",
            "optimization_suggestions",
        }
        missing = required - set(perf.keys())
        assert not missing, f"Performance missing keys: {missing}"


@pytest.mark.e2e
class TestPlanEndpoints:
    """Plan endpoints used by the Plans page."""

    def _assert_plan_shape(self, plan: dict):
        assert "date" in plan
        assert "tasks" in plan
        assert isinstance(plan["tasks"], list)
        if plan["tasks"]:
            task = plan["tasks"][0]
            # Must have fields the Plans page renders
            assert "title" in task
            assert "priority" in task
            assert "status" in task

    def test_get_today_plan(self, client):
        resp = client.get("/api/plan/today")
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "success"
        self._assert_plan_shape(body["plan"])

    def test_generate_plan(self, client):
        resp = client.post("/api/plan/generate")
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "success"
        self._assert_plan_shape(body["plan"])

    def test_plan_tasks_have_estimated_hours(self, client):
        plan = client.get("/api/plan/today").json()["plan"]
        for task in plan["tasks"]:
            assert "estimated_hours" in task, "Task missing estimated_hours"
            assert isinstance(task["estimated_hours"], (int, float))


@pytest.mark.e2e
class TestGapsEndpoint:
    """GET /api/gaps – knowledge gap analysis."""

    def test_gaps_returns_list(self, client):
        resp = client.get("/api/gaps")
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "success"
        assert isinstance(body["gaps"], list)

    def test_gaps_have_required_fields(self, client):
        gaps = client.get("/api/gaps").json()["gaps"]
        required = {"id", "title", "description", "severity", "status"}
        for gap in gaps:
            missing = required - set(gap.keys())
            assert not missing, f"Gap missing fields: {missing}"

    def test_gap_severity_values_are_valid(self, client):
        valid = {"low", "medium", "high", "critical"}
        for gap in client.get("/api/gaps").json()["gaps"]:
            assert gap["severity"] in valid


@pytest.mark.e2e
class TestInnovationsEndpoint:
    """GET /api/innovations – innovation list."""

    def test_innovations_returns_list(self, client):
        resp = client.get("/api/innovations")
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "success"
        assert isinstance(body["innovations"], list)

    def test_innovations_have_required_fields(self, client):
        innovations = client.get("/api/innovations").json()["innovations"]
        required = {"id", "title", "description", "category", "impact_score",
                    "implementation_status", "created_at"}
        for innov in innovations:
            missing = required - set(innov.keys())
            assert not missing, f"Innovation missing fields: {missing}"

    def test_innovation_impact_score_in_range(self, client):
        for innov in client.get("/api/innovations").json()["innovations"]:
            assert 0.0 <= innov["impact_score"] <= 1.0

    def test_innovation_status_values_are_valid(self, client):
        valid = {"proposed", "in_progress", "implemented"}
        for innov in client.get("/api/innovations").json()["innovations"]:
            assert innov["implementation_status"] in valid


@pytest.mark.e2e
class TestPerformanceEndpoint:
    """GET /api/performance – amplifier metrics."""

    def test_performance_returns_200(self, client):
        resp = client.get("/api/performance")
        assert resp.status_code == 200
        assert resp.json()["status"] == "success"

    def test_performance_has_numeric_scores(self, client):
        perf = client.get("/api/performance").json()["performance"]
        for field in ("productivity_score", "completion_rate", "average_roi",
                      "time_utilization", "success_rate"):
            assert field in perf, f"Missing field: {field}"
            assert 0.0 <= perf[field] <= 1.0, f"{field} out of [0,1] range"

    def test_performance_has_trend_data(self, client):
        perf = client.get("/api/performance").json()["performance"]
        trend = perf["task_completion_trend"]
        assert isinstance(trend, list)
        assert len(trend) > 0
        assert "date" in trend[0]
        assert "count" in trend[0]

    def test_performance_has_distribution_data(self, client):
        perf = client.get("/api/performance").json()["performance"]
        dist = perf["task_distribution"]
        assert isinstance(dist, list)
        assert len(dist) > 0
        assert "priority" in dist[0]
        assert "count" in dist[0]

    def test_performance_has_optimization_suggestions(self, client):
        perf = client.get("/api/performance").json()["performance"]
        suggestions = perf["optimization_suggestions"]
        assert isinstance(suggestions, list)
        assert len(suggestions) > 0
        assert all(isinstance(s, str) for s in suggestions)


# ===========================================================================
# 3. Full task user flow: list → create → fetch → update → complete → delete
# ===========================================================================


@pytest.mark.e2e
class TestTaskUserFlow:
    """Simulate the complete task user flow expected by the frontend UI."""

    # -----------------------------------------------------------------------
    # Step 1 – list tasks (empty store)
    # -----------------------------------------------------------------------

    def test_01_list_tasks_initially_empty(self, client):
        """GET /api/tasks on a fresh store must return an empty list."""
        resp = client.get("/api/tasks")
        assert resp.status_code == 200
        assert resp.json() == []

    # -----------------------------------------------------------------------
    # Step 2 – create a task
    # -----------------------------------------------------------------------

    def test_02_create_task_returns_201(self, client):
        """POST /api/tasks must return HTTP 201 with the created task."""
        payload = {
            "title": "Write validation tests",
            "description": "Cover all API endpoints end-to-end",
            "priority": "high",
            "status": "todo",
            "roi": 0.9,
            "cognitive_load": 3,
            "estimated_hours": 2.0,
            "tags": ["testing", "qa"],
        }
        resp = client.post("/api/tasks", json=payload)
        assert resp.status_code == 201
        task = resp.json()
        assert task["title"] == payload["title"]
        assert task["description"] == payload["description"]
        assert task["priority"] == "high"
        assert task["status"] == "todo"
        assert task["roi"] == 0.9
        assert task["estimated_hours"] == 2.0
        assert set(task["tags"]) == {"testing", "qa"}
        assert "id" in task
        assert "created_at" in task
        assert task["completed_at"] is None

    def test_03_create_task_missing_title_returns_422(self, client):
        """Requests with no title must be rejected with HTTP 422."""
        resp = client.post("/api/tasks", json={"description": "no title here"})
        assert resp.status_code == 422

    def test_04_create_task_empty_title_returns_422(self, client):
        """Requests with an empty title must be rejected with HTTP 422."""
        resp = client.post("/api/tasks", json={"title": ""})
        assert resp.status_code == 422

    # -----------------------------------------------------------------------
    # Step 3 – fetch (verify the created task appears in list)
    # -----------------------------------------------------------------------

    def test_05_created_task_appears_in_list(self, client):
        """After creation, GET /api/tasks must include the new task."""
        client.post("/api/tasks", json={"title": "Fetch me"})
        tasks = client.get("/api/tasks").json()
        assert len(tasks) == 1
        assert tasks[0]["title"] == "Fetch me"

    def test_06_multiple_tasks_all_appear_in_list(self, client):
        """All created tasks must be returned by GET /api/tasks."""
        titles = ["Task Alpha", "Task Beta", "Task Gamma"]
        for t in titles:
            client.post("/api/tasks", json={"title": t})
        tasks = client.get("/api/tasks").json()
        assert len(tasks) == 3
        assert {t["title"] for t in tasks} == set(titles)

    # -----------------------------------------------------------------------
    # Step 4 – update a task
    # -----------------------------------------------------------------------

    def test_07_update_task_title(self, client):
        """PATCH /api/tasks/{id} must update the specified field."""
        task_id = client.post("/api/tasks", json={"title": "Old title"}).json()["id"]
        resp = client.patch(f"/api/tasks/{task_id}", json={"title": "New title"})
        assert resp.status_code == 200
        assert resp.json()["title"] == "New title"

    def test_08_update_task_priority(self, client):
        task_id = client.post("/api/tasks", json={"title": "Priority test"}).json()["id"]
        resp = client.patch(f"/api/tasks/{task_id}", json={"priority": "critical"})
        assert resp.status_code == 200
        assert resp.json()["priority"] == "critical"

    def test_09_update_nonexistent_task_returns_404(self, client):
        resp = client.patch("/api/tasks/no-such-id", json={"title": "x"})
        assert resp.status_code == 404

    # -----------------------------------------------------------------------
    # Step 5 – complete a task (status → done, completed_at is set)
    # -----------------------------------------------------------------------

    def test_10_completing_task_sets_status_done(self, client):
        """PATCH status=done must set status to 'done'."""
        task_id = client.post("/api/tasks", json={"title": "Complete me"}).json()["id"]
        resp = client.patch(f"/api/tasks/{task_id}", json={"status": "done"})
        assert resp.status_code == 200
        task = resp.json()
        assert task["status"] == "done"

    def test_11_completing_task_records_completed_at(self, client):
        """PATCH status=done must populate completed_at timestamp."""
        task_id = client.post("/api/tasks", json={"title": "Timestamp test"}).json()["id"]
        task = client.patch(f"/api/tasks/{task_id}", json={"status": "done"}).json()
        assert task["completed_at"] is not None

    def test_12_completed_task_persists_in_list(self, client):
        """Completed task must still appear in GET /api/tasks."""
        task_id = client.post("/api/tasks", json={"title": "Persist check"}).json()["id"]
        client.patch(f"/api/tasks/{task_id}", json={"status": "done"})
        tasks = client.get("/api/tasks").json()
        done_tasks = [t for t in tasks if t["status"] == "done"]
        assert len(done_tasks) == 1

    # -----------------------------------------------------------------------
    # Step 6 – delete a task
    # -----------------------------------------------------------------------

    def test_13_delete_task_returns_204(self, client):
        task_id = client.post("/api/tasks", json={"title": "Delete me"}).json()["id"]
        resp = client.delete(f"/api/tasks/{task_id}")
        assert resp.status_code == 204

    def test_14_deleted_task_absent_from_list(self, client):
        task_id = client.post("/api/tasks", json={"title": "Gone soon"}).json()["id"]
        client.delete(f"/api/tasks/{task_id}")
        tasks = client.get("/api/tasks").json()
        assert all(t["id"] != task_id for t in tasks)

    def test_15_delete_nonexistent_task_returns_404(self, client):
        resp = client.delete("/api/tasks/ghost-id")
        assert resp.status_code == 404

    # -----------------------------------------------------------------------
    # Step 7 – full sequential user flow in a single test
    # -----------------------------------------------------------------------

    def test_16_full_create_fetch_update_complete_delete_flow(self, client):
        """Simulate the exact user flow visible in the UI screenshots."""
        # 1. List is empty
        assert client.get("/api/tasks").json() == []

        # 2. Create task
        task = client.post("/api/tasks", json={
            "title": "End-to-end flow task",
            "description": "Full lifecycle validation",
            "priority": "high",
            "estimated_hours": 1.5,
        }).json()
        task_id = task["id"]
        assert task["status"] == "todo"

        # 3. Fetch: task appears in list
        tasks = client.get("/api/tasks").json()
        assert len(tasks) == 1
        assert tasks[0]["id"] == task_id

        # 4. Update to in_progress
        updated = client.patch(f"/api/tasks/{task_id}",
                               json={"status": "in_progress"}).json()
        assert updated["status"] == "in_progress"

        # 5. Complete it
        completed = client.patch(f"/api/tasks/{task_id}",
                                 json={"status": "done"}).json()
        assert completed["status"] == "done"
        assert completed["completed_at"] is not None

        # 6. Task still visible (not auto-deleted)
        assert len(client.get("/api/tasks").json()) == 1

        # 7. Delete it
        del_resp = client.delete(f"/api/tasks/{task_id}")
        assert del_resp.status_code == 204

        # 8. List is empty again
        assert client.get("/api/tasks").json() == []
