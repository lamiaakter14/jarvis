#!/bin/bash

echo "🔄 Reorganizing memory/ and runtime/ directories..."

cd "$(git rev-parse --show-toplevel)"

# 1. Move database files to runtime
echo "📦 Moving database files..."
mv memory/test_tasks.db runtime/ 2>/dev/null || true

# 2. Move working directory to runtime
echo "📁 Moving working directory..."
mkdir -p runtime/working
cp -r memory/working/* runtime/working/ 2>/dev/null || true
rm -rf memory/working

# 3. Move amplifier data to runtime
echo "📊 Moving amplifier data..."
mkdir -p runtime/amplifier
mv memory/amplifier/performance_summary.json runtime/amplifier/ 2>/dev/null || true
rm -rf memory/amplifier

# 4. Move innovator generated data to runtime
echo "💡 Moving innovator data..."
mkdir -p runtime/innovator
mv memory/innovator/innovations.json runtime/innovator/ 2>/dev/null || true

# 5. Keep innovator template in memory
echo "📝 Creating innovator template..."
mkdir -p memory/innovator
cat > memory/innovator/innovation_template.json << 'EOF'
{
  "innovation_id": "",
  "title": "",
  "description": "",
  "category": "",
  "impact_score": 0.0,
  "effort_estimate": "",
  "status": "proposed",
  "created_at": "",
  "tags": []
}
EOF

# 6. Create memory templates
echo "📋 Creating memory templates..."

cat > memory/working_template.json << 'EOF'
{
  "date": "",
  "focus_areas": [],
  "active_tasks": [],
  "context_notes": "",
  "energy_level": "",
  "priorities": []
}
EOF

cat > memory/gaps_template.json << 'EOF'
{
  "gaps": [],
  "resolved_gaps": [],
  "learning_priorities": [],
  "last_updated": ""
}
EOF

cat > memory/reflections_template.md << 'EOF'
# Daily Reflections Template

## Date: [YYYY-MM-DD]

### What Went Well
- 

### What Could Be Improved
- 

### Key Learnings
- 

### Tomorrow's Focus
- 

### Productivity Score
- **Score**: /10
- **Reason**: 
EOF

# 7. Ensure .gitignore is correct
echo "🔒 Updating .gitignore..."
grep -q "^runtime/" .gitignore || echo "runtime/" >> .gitignore
grep -q "*.db" .gitignore || echo "*.db" >> .gitignore

# 8. Remove runtime from git tracking
echo "🗑️  Removing runtime from git..."
git rm -r --cached runtime/ 2>/dev/null || true
git rm --cached memory/test_tasks.db 2>/dev/null || true

# 9. Show git status
echo ""
echo "✅ Reorganization complete!"
echo ""
echo "📊 Git status:"
git status

echo ""
echo "📋 Memory structure (curated, committed):"
tree memory/ -L 2

echo ""
echo "📦 Runtime structure (generated, gitignored):"
tree runtime/ -L 2

echo ""
echo "💡 Next steps:"
echo "  1. Review changes: git status"
echo "  2. Add changes: git add ."
echo "  3. Commit: git commit -m 'refactor: reorganize memory/ and runtime/'"
echo "  4. Push: git push"