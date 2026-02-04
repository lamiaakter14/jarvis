"""Test script for cognitive loop.

This script demonstrates the cognitive loop functionality using the new
Clean Architecture with backward compatibility through the bridge layer.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.cognitive_loop import CognitiveLoop
from core.memory_manager import MemoryManager

try:
    # Try to use new architecture through bridge
    from src.bridge.agent_bridge import (
        StrategistBridge,
        MentorBridge,
        ExecutorBridge,
        InnovatorBridge,
        AmplifierBridge
    )
    use_bridge = True
    print("✓ Using new Clean Architecture through bridge layer")
except ImportError as e:
    # Fallback to old agents if bridge not available
    print(f"⚠ Bridge not available, using old agents: {e}")
    from agents.strategist import Strategist
    from agents.mentor import Mentor
    from agents.executor import Executor
    from agents.innovator import Innovator
    from agents.amplifier import Amplifier
    use_bridge = False


def test_cognitive_loop():
    """Test the cognitive loop with all five agents."""
    print("\n" + "=" * 60)
    print("JARVIS Cognitive Loop Test")
    print("=" * 60 + "\n")
    
    # Initialize Memory Manager
    memory_manager = MemoryManager()
    print("✓ Memory Manager initialized")

    # Initialize Agents
    if use_bridge:
        strategist = StrategistBridge(memory_manager)
        mentor = MentorBridge(memory_manager)
        executor = ExecutorBridge(memory_manager)
        innovator = InnovatorBridge(memory_manager)
        amplifier = AmplifierBridge(memory_manager)
        print("✓ Agents initialized (using bridge layer)")
    else:
        strategist = Strategist(memory_manager)
        mentor = Mentor(memory_manager)
        executor = Executor(memory_manager)
        innovator = Innovator(memory_manager)
        amplifier = Amplifier(memory_manager)
        print("✓ Agents initialized (using old implementation)")

    # Initialize and run the cognitive loop
    print("\n" + "-" * 60)
    print("Running Cognitive Loop...")
    print("-" * 60 + "\n")
    
    jarvis = CognitiveLoop(memory_manager, strategist, mentor, executor, innovator, amplifier)
    jarvis.run_loop()
    
    print("\n" + "=" * 60)
    print("Cognitive Loop Test Complete")
    print("=" * 60)


if __name__ == "__main__":
    try:
        test_cognitive_loop()
    except Exception as e:
        print(f"\n❌ Error during cognitive loop execution: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
