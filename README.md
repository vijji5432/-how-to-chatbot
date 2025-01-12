# Chatbot Documentation Fetcher

This project fetches and processes dynamic documentation from multiple platforms (Segment, mParticle, Lytics, Zeotap) and uses it to provide relevant answers to user queries in a chatbot.

## Features
- Fetches documentation from the web for various platforms.
- Processes the content dynamically and answers user queries.
- Supports multiple platforms: Segment, mParticle, Lytics, and Zeotap.

## Requirements
To run this project, you need to have Python 3.x installed.

### Install Dependencies
Install the required Python libraries using `pip`:

```bash
pip install -r requirements.txt
```

This will install the following dependencies:
- `requests`
- `beautifulsoup4`
- `flask`
- `openai`
- `langchain`

### Optional: Docker Setup
If you want to containerize the application using Docker, you can use the provided `Dockerfile`. Build the Docker image with:

```bash
docker build -t chatbot-docs-fetcher .
```

To run the container:

```bash
docker run -p 5000:5000 chatbot-docs-fetcher
```

## Usage

1. **Fetching Documentation**:
   To fetch documentation from a specified platform, run the script:

   ```bash
   python fetch_docs.py
   ```

   The script fetches documentation dynamically from the URLs for Segment, mParticle, Lytics, and Zeotap.

2. **Running the Chatbot API**:
   To start the Flask application that interacts with the chatbot:

   ```bash
   python app.py
   ```

   The Flask app will be accessible on `http://localhost:5000`.

3. **Making API Requests**:
   You can send a `POST` request to the `/ask` endpoint with the platform and query. Here’s an example using `curl`:

   ```bash
   curl -X POST -H "Content-Type: application/json" \
   -d '{"platform": "Segment", "query": "How do I set up a new source in Segment?"}' \
   http://127.0.0.1:5000/ask
   ```

   The chatbot will return an answer based on the fetched documentation.

## Testing

This project uses **pytest** to run tests for the functionality of fetching and processing documentation.

To run the tests, first install `pytest`:

```bash
pip install pytest
```

Then, run the tests with:

```bash
pytest
```

## Contributing

1. Fork the repository.
2. Clone your forked repository:
   ```bash
   git clone https://github.com/your-username/chatbot-docs-fetcher.git
   ```
3. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
4. Make changes, then commit them:
   ```bash
   git add .
   git commit -m "Description of the changes"
   ```
5. Push to your fork:
   ```bash
   git push origin feature-name
   ```
6. Open a Pull Request to the main repository.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements
- This project uses [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing.
- [Flask](https://flask.palletsprojects.com/) is used for creating the API.
- [OpenAI GPT-4](https://openai.com/) is used to process queries and generate responses.


