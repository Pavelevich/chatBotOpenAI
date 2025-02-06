# Chat Project
![image](https://github.com/user-attachments/assets/ad9d9625-74d1-4f73-8598-495c41478ebb)


## Description
This project is a FastAPI-based web application designed to serve an AI assistant. The AI assistant analyzes user-provided data and answers queries based on predefined reference data (`qa_data.txt`). It leverages FastAPI to handle HTTP routes, integrates with Chainlit for conversational support, and communicates with the OpenAI API for generating intelligent responses.

The project also serves a static HTML file (`index.html`) and has middleware configured to enable CORS for specific origins.

## Features
- **FastAPI Framework**: Handles HTTP requests and middleware integration.
- **Chainlit Integration**: Supports enhanced conversational experiences with Chainlit.
- **CORS Support**: Configured CORS (Cross-Origin Resource Sharing) middleware for specific domains.
- **Static File Hosting**: Serves files through the `/public` route.
- **OpenAI API Integration**: Communicates with the OpenAI GPT model for dynamic query handling.

## Project Structure
- `index.html`: The landing page of the web application.
- `app.py`: The main backend script including API endpoint definitions, middleware setup, and AI assistant configuration.
- `qa_data.txt`: A reference data file for answering queries based on a predefined dataset.
- `/public/`: Directory for hosting static files.

## How to Run
1. Ensure you have Python 3.7+ installed.
2. Install necessary dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the server by running:
   ```bash
   python app.py
   ```
4. Access the application in your web browser:
   ```
   http://127.0.0.1:8000
   ```

## License
This project is licensed under a standard open-source license. Replace this section with the actual license information for your project.
