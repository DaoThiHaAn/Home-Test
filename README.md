This is a coding home test that requires to implement a mini chatbot supporting users in an app guidance

Deployment:

Gemini File Search: 
**Setup**
This project uses Gemini API for file search.
1. Clone the repository
2. Install dependencies using
    ```bash
    pip install -r requirements.txt
    ```
3. Create a free [Google AI Studio](https://aistudio.google.com/) account
4. Create a new API key for the new project
5. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) (if not already installed) and ensure it is running

**How To Run Locally**
1. Create a `.env` file in the root directory of the project in the same format as `.env.example` and fill in the required values
2. Build the Docker image using the command:
   ```bash
    docker build -t opti-bot
    ```

3. Run the Docker container using the command:
   ```bash
    docker run -e GEMINI_API_KEY="YourActualAPIKeyHere" opti-bot
    ```

**Link To Daily Job Logs**

**Sample Run**
Sample question: "How do I add a YouTube video?"
Result:


**Approach Explained**
1. Markdown conversion
- Articles from [support.optisigns.com](https://support.optisigns.com/en/) are retrieved using the [Zendesk Articles API](https://developer.zendesk.com/api-reference/help_center/help-center-api/articles/).
- The retrieved articles are converted to Markdown format using the [markdownify](https://pypi.org/project/markdownify/) library.
- The converted Markdown files are stored within the `articles_markdown` folder.
  
2. Build AI assistant
- The converted Markdown files are indexed using the [Gemini File Search API](https://ai.google.dev/gemini-api/docs/file-search
).
- The embedded files are chunked automatically by default.
- 