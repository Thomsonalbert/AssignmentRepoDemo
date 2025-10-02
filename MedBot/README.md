🖥️ Getting Started (For Beginners)

These instructions assume you do not already have Python installed. Follow them step by step.

1. Install Python

Go to the official download page: https://www.python.org/downloads/

Download the latest version of Python 3 (3.9 or higher recommended).

During installation, check the box that says “Add Python to PATH.”

Verify installation: open your terminal (Command Prompt on Windows, or Terminal on Mac) and type:

python --version


You should see something like Python 3.11.x.

2. Install GitHub Desktop

Download GitHub Desktop: https://desktop.github.com

Sign in with your GitHub account.

Clone our project repository:

In GitHub Desktop, go to File ▸ Clone Repository.

Paste this URL:

https://github.com/Thomsonalbert/AssignmentRepoDemo.git


Choose a folder where you want the project saved.

Click Clone.

3. Set Up the Project Environment

Open the cloned folder in your computer’s file explorer.

In GitHub Desktop, click Open in Terminal (or open a terminal manually in that folder).

Create a virtual environment (this keeps dependencies clean):

python -m venv venv


Activate the environment:

On Windows:

venv\Scripts\activate


On Mac/Linux:

source venv/bin/activate

4. Install Required Packages

With the virtual environment active, run:

pip install -r requirements.txt


This installs everything the project needs (Gradio, OpenAI, dotenv, etc.).

5. Add Your OpenAI API Key

This app needs an OpenAI API key to work. Each team member should use their own key.

Just ask Aaron for his unless you seriously want to pay.

Log in at https://platform.openai.com/account/api-keys
.

Click + Create new secret key and copy it.

In the project folder, create a file called:

med_storage


Inside it, paste:

OPENAI_API_KEY=sk-yourapikeyhere


Save the file.
✅ Don’t worry — this file is ignored by GitHub, so your key will stay private.

6. Run the Application

In your terminal (with the virtual environment active):

python app.py


If everything is correct, you’ll see:

Running on http://127.0.0.1:7860


Click the link (or copy it into your browser) to open the chatbot.

💬 Usage Guide

Login: Use your VCU email + password.

Chat Modes:

General Mode → Standard assistant conversation.

Medical Mode → Educational information only (no diagnoses, no prescriptions).

Therapy Mode → Keywords like panic or anxiety trigger grounding techniques and, if needed, direct to VCU therapy resources.

🔧 Troubleshooting

pip not recognized: Make sure you checked Add Python to PATH during install. Reinstall Python if needed.

venv folder missing: Make sure you ran python -m venv venv inside the project folder.

API key not found: Double-check that med_storage is in the project folder, with the line OPENAI_API_KEY=....

Port already in use: If Gradio says the port is in use, rerun with:

python app.py --server.port 7861
