# Teach Me This

Teach Me This is an interactive learning chatbot that helps users master new topics through personalized Q&A sessions.

## Features

- Upload learning material for the AI to analyze
- Engage in interactive conversations to learn the material
- Real-time progress tracking
- Adaptive teaching based on user responses
- Final evaluation and mastery assessment

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/teach-me-this.git
   cd teach-me-this
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up your environment variables:
   Create a `.env` file in the root directory and add your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```

## Usage

1. Start the Flask server:
   ```
   python app.py
   ```

2. Open your web browser and navigate to `http://localhost:5000`

3. Enter your learning material in the provided text area and click "Start Learning Session"

4. Engage in the interactive Q&A session with the AI tutor

## Development

The main components of the application are:

- `app.py`: Flask server and Socket.IO setup
- `learning_chatbot.py`: Core logic for the AI tutor
- `system_prompt.py`: Defines the system prompt for the AI
- `templates/index.html`: Frontend interface

## Deployment

The application is configured for deployment on Render.