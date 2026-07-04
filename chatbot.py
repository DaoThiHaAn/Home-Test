"""Helpers for asking OptiBot questions through Gemini File Search."""

from uploader import get_or_create_file_search_store


SYSTEM_PROMPT = """\
You are OptiBot, the customer-support bot for OptiSigns.com.
* Tone: helpful, factual, concise.
* Only answer using the uploaded docs.
* Max 5 bullet points; else link to the doc.
* Cite up to 3 "Article URL:" lines per reply.
"""


def create_chatbot(client, file_search_store_name="OptiSigns Search Store"):
    file_search_store = get_or_create_file_search_store(client, file_search_store_name)
    print(f"File search store ready: {file_search_store.name}")
    return file_search_store


def ask_optibot(client, file_search_store, question):
    interaction = client.interactions.create(
        model="gemini-3.5-flash",
        input=f"{SYSTEM_PROMPT}\n\nUser question: {question}",
        tools=[
            {
                "type": "file_search",
                "file_search_store_names": [file_search_store.name],
            }
        ],
    )

    output = []
    for step in interaction.steps:
        if step.type != "model_output":
            continue
        for content in step.content:
            if content.type == "text":
                output.append(content.text)
                for annotation in content.annotations or []:
                    if annotation.type == "file_citation":
                        output.append(f"Article URL: {annotation.source}")

    return "\n".join(output)


def sanity_check(file_search_store, client):
    question = "How do I add a YouTube video?"
    response = ask_optibot(client, file_search_store, question)
    print("Question: ", question)
    print("\n[OptiBot Response]:\n", response)
