"""Seed database with test data."""
import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


async def seed_database():
    """Seed database with test data."""
    print("Seeding database with test data...")
    
    # Add your seeding logic here
    # Example:
    # - Create test users
    # - Create sample tasks
    # - Create sample plans
    
    print("✅ Database seeding complete!")


if __name__ == "__main__":
    asyncio.run(seed_database())
