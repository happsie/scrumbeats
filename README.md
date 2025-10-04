# ScrumBeats

ScrumBeats turns the past 24 hours of engineering activity into a song. A director agent gathers updates from developer tools, lyricist agents compete to write the best verses, and the Suno API produces the final track.

# Important note: 
Due to confidential information and different environment setups, only a mock lives inside the integrations for internal data. 
Replace the mocking agents with actual integrations. 

## Features
- Multi-agent orchestration built on `openai-agents`, including a summary director and three specialized lyricists
- Example integrations for Bitbucket pull requests, Jira issues, and Jenkins builds to simulate daily activity
- Suno API tool that converts chosen lyrics into an audio generation request
- Environment-driven configuration so you can swap prompts, genres, and data sources to fit your team

## Prerequisites
- Python 3.12 or newer
- `uv` (https://github.com/astral-sh/uv)
- Access to the OpenAI API (the agents default to `gpt-4o-mini`)
- SunoAPI account with credentials for the `generate` endpoints

## Setup
1. Resolve dependencies and create the virtual environment managed by `uv`:
   ```bash
   uv sync
   ```
   This installs the packages defined in `pyproject.toml` (including `openai-agents`, `python-dotenv`, and `requests`) into `.venv`.
2. Create a `.env` file at the repository root with your credentials:
   ```env
   OPENAI_API_KEY=your-openai-key
   SUNOAPI_API_KEY=your-suno-key
   ```
   Never commit real keys to version control.

## Running
1. Ensure `.env` is populated with valid API keys.
2. Launch the workflow with `uv`:
   ```bash
   uv run main.py
   ```
   The app loads environment variables, gathers data through the Bitbucket, Jira, and Jenkins integrations, crafts a summary, generates competing lyrics, and submits the winning lyrics to Suno for song creation.
3. Watch the terminal output for progress logs from each agent and the status of the Suno request.

## Customizing
- Update the prompt in `main.py` to change the theme or level of detail in the summary.
- Modify the sample data in `scrumbeats/integrations/*` to reflect real tool responses or connect to live APIs.
- Adjust the lyric agents in `scrumbeats/directors/song_director.py` to experiment with different styles or model selections.
