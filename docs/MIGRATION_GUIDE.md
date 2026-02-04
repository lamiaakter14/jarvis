# Migration Guide: Monorepo Restructure

This guide explains the changes made in the monorepo restructure and how to update your code.

## 🔄 What Changed

JARVIS has been restructured from a single-directory layout to a modern monorepo architecture:

### Old Structure
```
jarvis/
├── src/
│   ├── domain/
│   ├── application/
│   ├── infrastructure/
│   ├── presentation/
│   │   ├── api/
│   │   └── cli/
│   ├── bridge/
│   └── shared/
├── frontend/
└── memory/
```

### New Structure
```
jarvis/
├── apps/                   # Applications
│   ├── api/jarvis_api/    # FastAPI application
│   ├── cli/jarvis_cli/    # CLI application
│   └── web/               # React frontend
├── packages/              # Shared packages
│   └── jarvis_core/       # Core business logic
│       ├── domain/
│       ├── application/
│       ├── infrastructure/
│       ├── bridge/
│       └── shared/
├── memory/                # Curated knowledge (version controlled)
└── runtime/               # Generated state (gitignored)
```

## 📦 Import Changes

All imports from `src.*` have been changed to `jarvis_core.*`:

### Before
```python
from src.domain.entities.task import Task
from src.application.use_cases.generate_daily_plan import GenerateDailyPlan
from src.infrastructure.agents.strategist_agent import StrategistAgent
from src.bridge.agent_bridge import StrategistBridge
from src.shared.constants import TASK_STATUS
```

### After
```python
from jarvis_core.domain.entities.task import Task
from jarvis_core.application.use_cases.generate_daily_plan import GenerateDailyPlan
from jarvis_core.infrastructure.agents.strategist_agent import StrategistAgent
from jarvis_core.bridge.agent_bridge import StrategistBridge
from jarvis_core.shared.constants import TASK_STATUS
```

## 🚀 Running Applications

### API Application

**Old:**
```bash
python -m src.presentation.api.main
# or
uvicorn src.presentation.api.main:app --reload
```

**New:**
```bash
export PYTHONPATH=/path/to/jarvis/packages:/path/to/jarvis/apps/api:/path/to/jarvis/apps/cli
python -m jarvis_api.main
# or
uvicorn jarvis_api.main:app --reload
```

### CLI Application

**Old:**
```bash
python -m src.presentation.cli.main --help
python -m src.presentation.cli.main run
```

**New:**
```bash
export PYTHONPATH=/path/to/jarvis/packages:/path/to/jarvis/apps/api:/path/to/jarvis/apps/cli
python -m jarvis_cli.main --help
python -m jarvis_cli.main run
```

### Web Dashboard

**Old:**
```bash
cd frontend
npm run dev
```

**New:**
```bash
cd apps/web
npm run dev
```

## 🐳 Docker Changes

### Dockerfile

The Dockerfile has been updated to work with the new structure:

**Key Changes:**
- Copies `packages/` and `apps/` separately
- Sets `PYTHONPATH` to include both locations
- Uses module imports (`python -m jarvis_api.main`)

### docker-compose.yml

**Old:**
```yaml
command: python src/presentation/api/main.py
```

**New:**
```yaml
command: python -m uvicorn jarvis_api.main:app --host 0.0.0.0 --port 8000
volumes:
  - ./runtime:/app/runtime  # New: runtime directory
```

## 🧪 Testing

### Test Configuration

**pytest.ini** has been updated:

**Old:**
```ini
--cov=src
```

**New:**
```ini
--cov=packages/jarvis_core
--cov=apps
```

### Running Tests

```bash
export PYTHONPATH=/path/to/jarvis/packages:/path/to/jarvis/apps/api:/path/to/jarvis/apps/cli
pytest tests/
```

## 📁 Memory vs Runtime

### Memory Directory (✅ Version Controlled)

The `memory/` directory contains curated knowledge that should be committed:

- Strategic plans and goals
- Learning roadmaps
- Architecture decision records (ADRs)
- Innovation templates

### Runtime Directory (❌ Gitignored)

A new `runtime/` directory has been added for generated state:

```
runtime/
├── working/              # Daily context, plans, task queue
├── metrics/             # Performance metrics
├── innovations/         # Generated innovations
└── cache/              # Temporary cache
```

This directory is gitignored and each JARVIS instance creates its own runtime state.

## 🔧 Configuration Updates

### pyproject.toml

Updated to support the monorepo structure:

```toml
[project]
name = "jarvis"
version = "1.0.0"

[project.scripts]
jarvis-api = "jarvis_api.main:main"
jarvis-cli = "jarvis_cli.main:app"

[tool.setuptools.packages.find]
where = ["packages", "apps"]
```

### Environment Variables

Add `PYTHONPATH` to your environment:

```bash
# Linux/Mac
export PYTHONPATH=/path/to/jarvis/packages:/path/to/jarvis/apps/api:/path/to/jarvis/apps/cli

# Windows (PowerShell)
$env:PYTHONPATH = "/path/to/jarvis/packages;/path/to/jarvis/apps/api;/path/to/jarvis/apps/cli"

# Or add to .bashrc/.zshrc for permanent setup
echo 'export PYTHONPATH=/path/to/jarvis/packages:/path/to/jarvis/apps/api:/path/to/jarvis/apps/cli' >> ~/.bashrc
```

## 🔍 Migration Checklist

If you have custom code or scripts:

- [ ] Update all `from src.*` imports to `from jarvis_core.*`
- [ ] Update module execution commands (e.g., `python -m src.presentation.cli.main` → `python -m jarvis_cli.main`)
- [ ] Update Docker commands if using Docker
- [ ] Set `PYTHONPATH` environment variable
- [ ] Move any runtime-generated files to `runtime/` directory
- [ ] Update any CI/CD pipeline configurations
- [ ] Update documentation references

## 💡 Benefits of New Structure

1. **Clear Separation** - Apps vs Core business logic vs Runtime state
2. **Better Scalability** - Easy to add new applications
3. **Improved Testing** - Isolated test environments
4. **Cleaner Git** - No runtime state in commits
5. **Docker Friendly** - Better volume management
6. **Industry Standard** - Follows modern monorepo patterns

## 🆘 Troubleshooting

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'jarvis_core'`

**Solution:** Set `PYTHONPATH`:
```bash
export PYTHONPATH=/path/to/jarvis/packages:/path/to/jarvis/apps/api:/path/to/jarvis/apps/cli
```

### API Won't Start

**Problem:** `ModuleNotFoundError: No module named 'jarvis_api'`

**Solution:** Ensure `PYTHONPATH` includes the apps directory:
```bash
export PYTHONPATH=$PYTHONPATH:/path/to/jarvis/apps/api
```

### Tests Failing

**Problem:** Tests can't find modules

**Solution:** Run tests with PYTHONPATH set:
```bash
PYTHONPATH=/path/to/jarvis/packages:/path/to/jarvis/apps/api:/path/to/jarvis/apps/cli pytest tests/
```

## 📞 Getting Help

If you encounter issues:

1. Check that `PYTHONPATH` is set correctly
2. Verify all imports use `jarvis_core.*` instead of `src.*`
3. Ensure you're running commands from the project root
4. Check the updated README.md for latest instructions
5. Open an issue on GitHub with details about your problem

## 🎉 Summary

The monorepo restructure improves JARVIS's architecture while maintaining backward compatibility through the bridge layer. All existing functionality works the same way - only the internal organization has changed for better maintainability and scalability.
