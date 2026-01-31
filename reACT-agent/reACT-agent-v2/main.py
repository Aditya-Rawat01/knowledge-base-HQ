from langchain.messages import SystemMessage, HumanMessage
import uuid
from src.agent import graph
from src.prompts import get_system_prompt
def main():
    # Create a unique thread_id for this session
    thread_id = str(uuid.uuid4())

    print("🚀 Code-Zero-Agent Initialized. Type 'q'/ 'quit' / 'exit' to quit.")
    print("--------------------------------------------------")

    # Initial System Prompt to set the persona
    sys_prompt = get_system_prompt()
    
    # Seed the history
    graph.invoke({"messages": [SystemMessage(content=sys_prompt)]}, config={"configurable": {"thread_id": thread_id}})

    while True:
        try:
            user_input = input("\n👤 You: ")
            if user_input.lower() in ['q', 'quit', 'exit']:
                print("👋 Bye!")
                break
            
            # Streaming events allows the user to see Tool calls in real-time
            print("🤖 Agent is working...")
            events = graph.stream(
                {"messages": [HumanMessage(content=user_input)]}, 
                config={"configurable": {"thread_id": thread_id}}, 
                stream_mode="updates"
            )
            
            for event in events:
                # event keys are node names (e.g., "agent", "toolCallFnNode")
                for node_name, values in event.items():
                    # values is the dictionary returned by that node (e.g., {"messages": [...]})
                    if "messages" in values:
                        last_msg = values["messages"][-1]
                        
                        # Print AI response
                        if last_msg.type == "ai" and last_msg.content:
                            print(f"🤖 Code-Zero: {last_msg.content}")
                        
                        # Print Tool execution
                        elif last_msg.type == "tool":
                            # Try to get the tool name; fallback if missing
                            tool_name = getattr(last_msg, 'name', 'Unknown Tool')
                            print(f"   🛠️  Executed: {tool_name}")

        except KeyboardInterrupt:
            print("\n\n⚠️ Interrupted by user. Session ended.")
            break
        except Exception as e:
            print(f"❌ Critical Error: {e}")

if __name__ == "__main__":
    main()


# v1



# cannot find the files and folders , throws error.
# not intelligent enough to understand the commands.
# will need shit ton on improvement.