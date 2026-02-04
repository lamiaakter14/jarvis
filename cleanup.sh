#!/bin/bash

echo "🧹 Starting JARVIS Repository Cleanup..."

# Navigate to repository root
cd "$(git rev-parse --show-toplevel)"

echo "📁 Current directory: $(pwd)"

# 1. Remove redundant setup.sh
if [ -f "setup.sh" ]; then
    echo "❌ Removing redundant setup.sh..."
    git rm setup.sh
fi

# 2. Clean Python artifacts
echo "🐍 Cleaning Python artifacts..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete
find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null

# 3. Clean test artifacts
echo "🧪 Cleaning test artifacts..."
find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null
find . -type f -name ".coverage" -delete
find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null
find . -type d -name ".tox" -exec rm -rf {} + 2>/dev/null

# 4. Clean macOS files
echo "🍎 Cleaning macOS files..."
find . -name ".DS_Store" -delete
find . -name ".AppleDouble" -delete 2>/dev/null
find . -name ".LSOverride" -delete 2>/dev/null

# 5. Clean log files
echo "📜 Cleaning log files..."
find . -name "*.log" -type f -delete 2>/dev/null

# 6. Clean temporary files
echo "🗑️  Cleaning temporary files..."
find . -name "*.tmp" -type f -delete 2>/dev/null
find . -name "*.temp" -type f -delete 2>/dev/null
find . -name "*.bak" -type f -delete 2>/dev/null
find . -name "*.swp" -type f -delete 2>/dev/null
find . -name "*~" -type f -delete 2>/dev/null

# 7. Clean build artifacts
echo "🏗️  Cleaning build artifacts..."
find . -type d -name "dist" -exec rm -rf {} + 2>/dev/null
find . -type d -name "build" -exec rm -rf {} + 2>/dev/null
find . -type d -name ".eggs" -exec rm -rf {} + 2>/dev/null

# 8. Verify runtime/ is in .gitignore and not tracked
echo "📦 Verifying runtime/ directory..."
if git ls-files runtime/ | grep -q .; then
    echo "⚠️  WARNING: runtime/ has tracked files. They should be gitignored."
fi

# 9. Show git status
echo ""
echo "✅ Cleanup complete! Git status:"
git status

echo ""
echo "📋 Summary of actions:"
echo "  - Removed setup.sh (redundant)"
echo "  - Cleaned Python cache files"
echo "  - Cleaned test artifacts"
echo "  - Cleaned macOS system files"
echo "  - Cleaned log and temporary files"
echo "  - Cleaned build artifacts"
echo ""
echo "💡 Next steps:"
echo "  1. Review changes: git status"
echo "  2. Commit changes: git commit -m 'chore: clean up repository'"
echo "  3. Push changes: git push"