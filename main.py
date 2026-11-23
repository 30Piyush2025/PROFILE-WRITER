import os
from dotenv import load_dotenv
from src.graph import build_profile_graph

load_dotenv()

MENU = """
======================================================
  🤖 Agentic Profile & Bio Writer (LangGraph + Groq)
======================================================
Choose content to generate:
  1) GitHub Profile / Project README
  2) LinkedIn Post (High-Engagement Hook)
  3) LinkedIn About Section (Conversational & Punchy)
  4) LinkedIn Headline (Under 220 chars + Tips)
  5) Custom Content Type (Describe your need)
  0) Exit
"""

CONTENT_MAP = {
    "1": "readme",
    "2": "linkedin_post",
    "3": "linkedin_about",
    "4": "linkedin_headline",
}

def get_context():
    print("\nEnter your background / project context (press Enter twice when done):\n")
    lines = []
    while True:
        try:
            line = input()
            if line == "" and (not lines or lines[-1] == ""):
                break
            lines.append(line)
        except EOFError:
            break
    return "\n".join(lines).strip()

def main():
    if not os.environ.get("GROQ_API_KEY"):
        print("⚠️ Warning: GROQ_API_KEY environment variable is not set.")
        key = input("Enter your Groq API Key (or press enter if set in .env): ").strip()
        if key:
            os.environ["GROQ_API_KEY"] = key

    app = build_profile_graph()

    while True:
        print(MENU)
        choice = input("Enter option [0-5]: ").strip()
        if choice == "0":
            print("Exiting. Have a great day!")
            break

        state = {"num_variations": 3}

        if choice in CONTENT_MAP:
            state["content_type"] = CONTENT_MAP[choice]
            state["context"] = get_context()
        elif choice == "5":
            state["request"] = input("\nDescribe what you need written: ").strip()
            state["context"] = get_context()
        else:
            print("Invalid choice, please select again.")
            continue

        print("\n⏳ Routing request through LangGraph state machine & invoking Llama 3.3...\n")
        try:
            result = app.invoke(state)
            outputs = result.get("outputs", [])
            for i, text in enumerate(outputs, 1):
                print(f"\n{'='*60}\n✨ VARIATION {i}\n{'='*60}\n{text}\n")
        except Exception as e:
            print(f"❌ Error during generation: {e}")

if __name__ == "__main__":
    main()
