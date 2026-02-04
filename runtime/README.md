# Runtime Directory

This directory contains generated and runtime state that is **NOT** committed to git.

## Structure

- **working/** - Working memory (daily context, plans, task queues, logs)
- **metrics/** - Performance metrics and monitoring data
- **innovations/** - Generated innovations from the innovator agent
- **cache/** - Temporary cache files

## Important

- This directory is **gitignored**
- Each JARVIS instance generates its own runtime state
- Safe to delete for fresh start
- Backed up separately from code
