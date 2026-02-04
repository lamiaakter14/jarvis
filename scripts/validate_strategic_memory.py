#!/usr/bin/env python3
"""
Validation script for strategic memory files.
This script ensures all strategic memory files are properly populated and accessible.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.memory_manager import MemoryManager


def validate_file_exists_and_populated(file_path: Path, min_lines: int = 10) -> bool:
    """
    Validate that a file exists and has meaningful content.
    
    Args:
        file_path: Path to the file to validate
        min_lines: Minimum number of lines expected
        
    Returns:
        bool: True if validation passes
    """
    if not file_path.exists():
        print(f"❌ File does not exist: {file_path}")
        return False
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    if len(lines) < min_lines:
        print(f"❌ File has insufficient content ({len(lines)} lines): {file_path}")
        return False
    
    print(f"✅ File validated ({len(lines)} lines): {file_path.name}")
    return True


def main():
    """Main validation function."""
    print("=" * 60)
    print("Strategic Memory Validation")
    print("=" * 60)
    
    # Initialize memory manager
    memory_manager = MemoryManager()
    
    # Check strategic memory directory
    strategic_path = memory_manager.strategic_memory_path
    print(f"\nStrategic Memory Path: {strategic_path}")
    print(f"Directory exists: {strategic_path.exists()}")
    
    validation_results = []
    
    # Validate long_term_goal.md
    print("\n1. Validating long_term_goal.md...")
    result = validate_file_exists_and_populated(
        strategic_path / "long_term_goal.md",
        min_lines=50
    )
    validation_results.append(("long_term_goal.md", result))
    
    # Validate milestones.md
    print("\n2. Validating milestones.md...")
    result = validate_file_exists_and_populated(
        strategic_path / "milestones.md",
        min_lines=100
    )
    validation_results.append(("milestones.md", result))
    
    # Validate ADR 001
    print("\n3. Validating ADR 001 (Clean Architecture)...")
    adr_001_path = strategic_path / "architecture_decision_records" / "001-clean-architecture.md"
    result = validate_file_exists_and_populated(adr_001_path, min_lines=100)
    validation_results.append(("001-clean-architecture.md", result))
    
    # Validate ADR 002
    print("\n4. Validating ADR 002 (Schema Validation)...")
    adr_002_path = strategic_path / "architecture_decision_records" / "002-schema-validation.md"
    result = validate_file_exists_and_populated(adr_002_path, min_lines=200)
    validation_results.append(("002-schema-validation.md", result))
    
    # Test MemoryManager methods
    print("\n5. Testing MemoryManager strategic memory methods...")
    
    # Test get_strategic_file
    goal_content = memory_manager.get_strategic_file("long_term_goal.md")
    if goal_content and len(goal_content) > 100:
        print("✅ get_strategic_file('long_term_goal.md') works")
        validation_results.append(("get_strategic_file", True))
    else:
        print("❌ get_strategic_file('long_term_goal.md') failed")
        validation_results.append(("get_strategic_file", False))
    
    # Test list_adrs
    adrs = memory_manager.list_adrs()
    if len(adrs) >= 2 and "001-clean-architecture.md" in adrs:
        print(f"✅ list_adrs() works: Found {len(adrs)} ADRs")
        validation_results.append(("list_adrs", True))
    else:
        print(f"❌ list_adrs() failed: Found {len(adrs)} ADRs")
        validation_results.append(("list_adrs", False))
    
    # Test get_adr
    adr_001_content = memory_manager.get_adr("001")
    if adr_001_content and "Clean Architecture" in adr_001_content:
        print("✅ get_adr('001') works")
        validation_results.append(("get_adr", True))
    else:
        print("❌ get_adr('001') failed")
        validation_results.append(("get_adr", False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Validation Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in validation_results if result)
    total = len(validation_results)
    
    for name, result in validation_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print("\n" + "=" * 60)
    print(f"Results: {passed}/{total} checks passed")
    print("=" * 60)
    
    # Return exit code
    if passed == total:
        print("\n🎉 All validations passed! Strategic memory is properly populated.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} validation(s) failed. Please review the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
