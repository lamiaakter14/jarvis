from jarvis.core.cognitive_loop import CognitiveLoop
from jarvis.core.memory_manager import MemoryManager
from jarvis.agents.planner import Planner
from jarvis.agents.teacher import Teacher
from jarvis.agents.critic import Critic
from jarvis.agents.reviewer import Reviewer


def test_cognitive_loop():
    # Initialize Memory Manager
    memory_manager = MemoryManager()

    # Initialize Agents
    planner = Planner(memory_manager)
    teacher = Teacher(memory_manager)
    critic = Critic(memory_manager)
    reviewer = Reviewer(memory_manager)

    # Initialize and run the cognitive loop
    jarvis = CognitiveLoop(memory_manager, planner, teacher, critic, reviewer)
    jarvis.run_loop()


if __name__ == "__main__":
    print("Testing the Cognitive Loop...")
    test_cognitive_loop()
