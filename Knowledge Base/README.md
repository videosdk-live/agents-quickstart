# Knowledge Base

This example demonstrates how to integrate a custom Knowledge Base with your agent, allowing it to answer questions based on documents you provide.

## Key Features

- **Custom Knowledge Base**: Use a knowledge base created from your own documents.
- **Contextual Responses**: The agent uses information from the knowledge base to provide more accurate and relevant answers.
- **Customizable Logic**: Implement custom logic for when and how to query the knowledge base.

## How It Works

The `knowledge_base.py` script shows how to use a `KnowledgeBase`. 

First, you need to create a Knowledge Base through the VideoSDK Dashboard. You can go to the [Knowledge Base section](https://app.videosdk.live/agents/knowledge-base), click on "Add Knowledge Base", provide a name, and upload your documents (Supported formats: Word, PDF, Text, Excel. Max size: 5 MB).

After a successful upload, you will get a `KNOWLEDGE_BASE_ID`. This ID should be set as an environment variable.

The script defines a `CustomKnowledgeBase` class that inherits from `KnowledgeBase`. This allows for custom logic to:
- decide when to search the knowledge base (`allow_retrieval`),
- how to clean up the user's query (`pre_process_query`), 
- and how to format the retrieved information (`format_context`).

The `KnowledgeBaseConfig` is used to configure the knowledge base with its ID.

## How to Run

1.  **Install the required dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

2.  **Create a Knowledge Base in the VideoSDK Dashboard and get your `KNOWLEDGE_BASE_ID`**.

3.  **Set up your environment variables**:

    Create a `.env` file in the root of the project and add the following:

    ```
    KNOWLEDGE_BASE_ID=<your_knowledge_base_id>
    GOOGLE_API_KEY=<your_google_api_key>
    SARVAMAI_API_KEY=<your_sarvamai_api_key>
    VIDEOSDK_AUTH_TOKEN=<your_videosdk_auth_token>
    ```

4.  **Run the agent**:
    ```bash
    python "Knowledge Base/knowledge_base.py"
    ```
