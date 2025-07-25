# main.py
from langchain_core.messages import HumanMessage
from core.graph_builder import graph
from tools.zerodha_client import initialize_zerodha_client

from tools.zerodha_tools import set_client as set_zerodha_tools_client

def main():
    # --- Interactive Zerodha Login ---

    client = initialize_zerodha_client()
    if not client:
        return # Exit if connection fails
    
    set_zerodha_tools_client(client)
        
    print("🤖 Finance Bot is ready. Ask me anything about your portfolio or the market.")
    print("Type 'exit' to quit.")

    # Stateful conversation loop
    conversation_history = []
    
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                break


            conversation_history.append(HumanMessage(content=user_input))

            result = graph.invoke({"messages": conversation_history})

            final_response = result['messages'][-1]
            
            conversation_history.append(final_response)
            
            print(f"Bot: {final_response.content}")

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
