from core.cognitive_loop import CognitiveLoop
from core.memory_manager import MemoryManager
from agents.strategist import Strategist
from agents.mentor import Mentor
from agents.executor import Executor
from agents.innovator import Innovator
from agents.amplifier import Amplifier


def test_cognitive_loop():
    # Initialize Memory Manager
    memory_manager = MemoryManager()

    # Initialize Agents
    strategist = Strategist(memory_manager)
    mentor = Mentor(memory_manager)
    executor = Executor(memory_manager)
    innovator = Innovator(memory_manager)
    amplifier = Amplifier(memory_manager)

    # Initialize and run the cognitive loop
    jarvis = CognitiveLoop(memory_manager, strategist, mentor, executor, innovator, amplifier)
    jarvis.run_loop()


if __name__ == "__main__":
    print("Testing the Cognitive Loop...")
    test_cognitive_loop()
