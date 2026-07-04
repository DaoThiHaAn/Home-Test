"""Create a RAG chatbot"""

from uploader import create_file_search_store


def create_chatbot(client, file_search_store_name):
    file_search_store = create_file_search_store(client, file_search_store_name)
        
    optibot_agent = client.agents.create(
        model="gemini-3.5-flash",
        config={
            "system_instruction": """
            You are OptiBot, the customer-support bot for OptiSigns.com.
            • Tone: helpful, factual, concise.
            • Only answer using the uploaded docs.
            • Max 5 bullet points; else link to the doc.
            • Cite up to 3 "Article URL:" lines per reply.
            """,
            "tools": [{
                "type": "file_search",
                "file_search_store_names": [file_search_store.name] 
            }]
        }
    )
    
    print(f"OptiBot agent created")
    return optibot_agent
    

def sanity_check(optibot_agent, client):
    session = client.agents.create_session(agent=optibot_agent.id)
    question = "How do I add a YouTube video?"
    response = session.send_message(question)
    print("Question: ", question)
    print("\n[OptiBot Response]:")
    print(response.text)
