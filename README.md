# AI Code Explainer

An LLM-based tool that explains source code in plain natural language for beginners. Paste a snippet, pick a language, and get a step-by-step explanation written for someone who is new to programming.

**Live demo:** https://ai-code-explainer-gqyl.onrender.com
**Repository:** https://github.com/Siddhirai/AI-Code-Explainer

> The demo runs on a free hosting tier, so the first request after a period of inactivity can take about a minute while the server wakes up.

## Features

- Web interface for pasting code and reading the explanation
- REST API for using the explainer from other programs
- Supports Python, Java, JavaScript, C and C++
- Dataset of curated beginner code snippets with reference explanations
- Every request is stored, so the history grows into a second dataset
- Django admin panel for managing the data
- Automatic retry when the LLM service is temporarily busy

## Tech Stack

| Part | Technology |
|---|---|
| Language | Python 3.13 |
| Web framework | Django |
| API | Django REST Framework |
| LLM | Google Gemini (`gemini-3.8-flash`) through the `google-genai` SDK |
| Database | SQLite (local), configurable through `DATABASE_URL` |
| Static files | WhiteNoise |
| Server | Gunicorn |
| Hosting | Render |

## How It Works

```
User (browser or API client)
        |
        v
Django view / DRF API  -->  services.explain_code()  -->  Gemini API
        |                                                    |
        v                                                    v
 ExplanationLog (database)  <------------ explanation text -+
```

1. The user submits code and a language, through the web form or `POST /api/explain/`.
2. The request is validated.
3. `services.py` builds a prompt around the code and sends it to the Gemini model.
4. The explanation is saved in the `ExplanationLog` table and returned to the user.

## Prompt Design

The model is given the role of a friendly programming teacher for complete beginners, plus these rules:

1. Start with a one-line summary of what the code does.
2. Explain the code step by step in plain English.
3. Avoid jargon, and define any technical term that must be used.
4. End with a small example of input and output when useful.
5. Use plain text only, with no markdown symbols, so the output displays cleanly on the page.

## Dataset

The project includes two datasets, both stored in the database and visible in the admin panel.

**1. Curated samples (`CodeSample`)**
Beginner and intermediate snippets, each with a title, language, difficulty level, the code, and a human-written reference explanation. The source file is `explainer/data/samples.csv`, loaded with:

```bash
python manage.py load_samples
```

The current dataset contains [NUMBER] samples covering [loops, functions, conditionals, lists, recursion, etc.]. It is served at `GET /api/samples/`.

**2. Usage history (`ExplanationLog`)**
Every code snippet submitted and the explanation generated for it, with a timestamp. The latest 50 entries are served at `GET /api/history/`.

## API Reference

### `POST /api/explain/`

Request body (JSON):

```json
{
  "code": "for i in range(3): print(i)",
  "language": "python"
}
```

Response:

```json
{
  "language": "python",
  "explanation": "This code counts from 0 to 2 and prints each number..."
}
```

Example:

```bash
curl -X POST https://ai-code-explainer-gqyl.onrender.com/api/explain/ \
  -H "Content-Type: application/json" \
  -d '{"code":"print(1+1)","language":"python"}'
```

Errors: `400` for invalid input, `502` if the LLM service fails.

### `GET /api/samples/`
Returns the curated dataset as JSON.

### `GET /api/history/`
Returns the 50 most recent explanations.

## Project Structure

```
AI-Code-Explainer/
├── config/                  # Django project settings and URLs
├── explainer/               # Main app
│   ├── data/samples.csv     # Dataset source
│   ├── management/commands/load_samples.py
│   ├── templates/explainer/index.html
│   ├── models.py            # CodeSample, ExplanationLog
│   ├── services.py          # LLM call and prompt
│   ├── serializers.py
│   ├── api.py               # REST endpoints
│   ├── views.py             # Web page
│   └── urls.py
├── build.sh                 # Deployment build script
├── requirements.txt
└── manage.py
```

## Run Locally

1. Clone the repository and create a virtual environment:

```bash
git clone https://github.com/Siddhirai/AI-Code-Explainer.git
cd AI-Code-Explainer
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Get a free Gemini API key from https://aistudio.google.com/apikey and create a `.env` file in the project root:

```
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-3.8-flash
SECRET_KEY=any-long-random-string
DEBUG=True
```

3. Set up the database, load the dataset, and start the server:

```bash
python manage.py migrate
python manage.py load_samples
python manage.py createsuperuser
python manage.py runserver
```

4. Open http://127.0.0.1:8000/ for the web page, or http://127.0.0.1:8000/admin/ for the admin panel.

## Deployment

The project is deployed on Render as a web service.

- **Build command:** `./build.sh` (installs packages, collects static files, migrates the database, loads the dataset)
- **Start command:** `gunicorn config.wsgi`
- **Environment variables:** `GEMINI_API_KEY`, `GEMINI_MODEL`, `SECRET_KEY`, `DEBUG=False`, `PYTHON_VERSION`

## Limitations

- On the free hosting tier the SQLite database resets on each redeploy, so the usage history does not persist. The curated dataset is reloaded on every build. A hosted PostgreSQL database would fix this.
- Explanation quality depends on the LLM and can occasionally be inaccurate. Beginners should verify important details.
- The free LLM tier has rate limits, and the service can be temporarily busy.
- Input is limited to 5,000 characters per request.

## Future Improvements

- Explanation levels (absolute beginner, intermediate)
- Line-by-line highlighting alongside the code
- Automatic evaluation of generated explanations against the reference explanations in the dataset
- User accounts and saved history
- Support for more programming languages

## Author

[Siddhi Rai], [B.Tech / 5th Semester], [ABES Engineering College]