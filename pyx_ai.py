class PyxAI:
    def __init__(self):
        self.conversation_history = []  # Initialize conversation history
        self.gaming_keywords = ["game", "minecraft", "roblox", "fortnite", "respawn", "restart", "level", "player", "character", "play", "gaming", "stream", "boss fight", "checkpoint", "stuck", "lava", "spawn", "died", "health", "lives"]  # Define gaming keywords

    def score(self, text: str) -> float:
        # Base scoring logic
        pass

    def score_with_context(self, text: str) -> float:
        base_score = self.score(text)  # Calculate base score
        recent_context = " ".join(self.conversation_history[-5:]).lower()  # Get recent context
        has_gaming_context = any(keyword in recent_context for keyword in self.gaming_keywords)  # Check for gaming context

        # Adjust score based on context
        if has_gaming_context and any(word in text.lower() for word in ["die", "kill", "dead", "death", "respawn", "restart"]):
            base_score *= 0.4  # Reduce severity

        self.conversation_history.append(text)  # Update conversation history
        if len(self.conversation_history) > 10:
            self.conversation_history.pop(0)  # Remove oldest message if limit exceeded

        return base_score  # Return adjusted score


def main():
    while True:
        command = input("Enter command:")
        if command.startswith("context "):
            text = command[len("context "):]
            regular_score = score(text)  # Get regular score
            context_aware_score = score_with_context(text)  # Get context-aware score
            print(f"Regular Score: {regular_score}, Context-Aware Score: {context_aware_score}")  # Show both scores
        # Handle other commands

# Clear comments explaining the context-aware feature
# The context-aware score adjusts the base score based on the recent conversation context to provide a more relevant response.