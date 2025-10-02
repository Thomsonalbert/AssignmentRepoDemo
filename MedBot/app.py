import os, gradio as gr
from dotenv import load_dotenv
from openai import OpenAI

# ---- Load API key ----
load_dotenv("med_storage")
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ OPENAI_API_KEY not found in med_storage")
client = OpenAI(api_key=api_key)

# ---- System prompts ----
SYS_GENERAL = "You are a helpful, concise assistant."
SYS_MEDICAL = (
    "You are a cautious medical information assistant for education only. "
    "Provide general information, avoid diagnosis, prescriptions, or dosing. "
    "When appropriate, advise consulting a licensed clinician."
)

# ---- Safety terms ----
EMERGENCY_TERMS = {"chest pain","shortness of breath","stroke","unconscious",
                   "suicidal","overdose","severe bleeding","anaphylaxis",
                   "cant breathe","can't breathe", "kill myself", "computer science student"}
DOSING_TERMS = {"dose","dosage","mg","milligram","prescribe","prescription","titrate"}
MEDICAL_KEYWORDS = {"side effect","contraindication","symptom","diagnosis","medication","drug",
                    "hypertension","diabetes","asthma","antibiotic","antihistamine","statin",
                    "interaction","blood pressure","fever","rash","allergy"}

# ---- Safety + routing ----
def safety_gate(text: str) -> str | None:
    t = text.lower()
    if any(k in t for k in EMERGENCY_TERMS):
        return " Emergency detected. Call 911 or seek immediate medical help."
    if any(k in t for k in DOSING_TERMS):
        return " Dosing/prescription request detected. Consult a licensed clinician."
    return None

def route(text: str) -> str:
    return "medical" if any(k in text.lower() for k in MEDICAL_KEYWORDS) else "general"

# ---- OpenAI call ----
def openai_generate(system_prompt: str, user_text: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text}
        ],
        max_tokens=256,
        temperature=0.2
    )
    return response.choices[0].message.content.strip()

def generate_general(user_text: str) -> str:
    return openai_generate(SYS_GENERAL, user_text)

def generate_medical(user_text: str) -> str:
    return openai_generate(SYS_MEDICAL, user_text)

def respond(user_text, history):
    guard = safety_gate(user_text)
    if guard:
        reply, used = guard, "safety"
    else:
        if route(user_text) == "medical":
            reply, used = generate_medical(user_text), "medical"
        else:
            reply, used = generate_general(user_text), "general"
    history = history + [(user_text, f"[{used}] {reply}")]
    return history, ""

# ---- Login validation ----
def validate_login(username, password):
    if not username or not password:
        return False, "All fields are required."
    if not username.endswith("@vcu.edu"):
        return False, "Username must be a valid vcu.edu email."
    if password != "admin":
        return False, "Invalid password."
    return True, "Login successful."

# ---- Build UI ----
def build_app():
    with gr.Blocks(css=".footer{color:#64748b;font-size:12px;text-align:center;margin-top:12px}") as app:
        state = gr.State("login")  # tracks current screen

        # LOGIN SCREEN
        with gr.Group(visible=True) as login_screen:
            gr.Markdown("## 🔐 Login to MedBot")
            user = gr.Textbox(label="Username", placeholder="you@vcu.edu")
            pw = gr.Textbox(label="Password", type="password", placeholder="admin")
            login_btn = gr.Button("Confirm")
            cancel_btn = gr.Button("Cancel")
            login_msg = gr.Markdown("")

        # HOME SCREEN
        with gr.Group(visible=False) as home_screen:
            gr.Markdown("## 🏠 MedBot Home")
            start_btn = gr.Button("Start Conversation")
            res_btn = gr.Button("View Resources")
            logout_btn = gr.Button("Logout")
            home_msg = gr.Markdown("Welcome! Choose an option.")

        # CHATBOT SCREEN
        with gr.Group(visible=False) as chat_screen:
            gr.Markdown("### ⚠️ Disclaimer: MedBot is for educational purposes only. Not medical advice. Always consult a licensed clinician.")
            chat = gr.Chatbot(height=460, label="Conversation")
            box = gr.Textbox(placeholder="Ask a question…")
            send = gr.Button("Send")
            back_btn = gr.Button("Back to Home")

        # RESOURCES SCREEN
        with gr.Group(visible=False) as res_screen:
            gr.Markdown("### 📚 Resources\n- [CDC Health Topics](https://www.cdc.gov)\n- [NIH MedlinePlus](https://medlineplus.gov)\n")
            back_home = gr.Button("Back to Home")

        # ----- Actions -----
        def do_login(u, p):
            ok, msg = validate_login(u, p)
            if ok:
                return gr.update(visible=False), gr.update(visible=True), msg
            return gr.update(), gr.update(), f"❌ {msg}"

        login_btn.click(do_login, [user, pw], [login_screen, home_screen, login_msg])
        cancel_btn.click(lambda: ("", "", "Cancelled."), outputs=[user, pw, login_msg])

        start_btn.click(lambda: (gr.update(visible=False), gr.update(visible=True)),
                        outputs=[home_screen, chat_screen])
        res_btn.click(lambda: (gr.update(visible=False), gr.update(visible=True)),
                      outputs=[home_screen, res_screen])
        logout_btn.click(lambda: (gr.update(visible=True), gr.update(visible=False), ""),
                         outputs=[login_screen, home_screen, login_msg])

        send.click(respond, [box, chat], [chat, box])
        box.submit(respond, [box, chat], [chat, box])
        back_btn.click(lambda: (gr.update(visible=False), gr.update(visible=True)),
                       outputs=[chat_screen, home_screen])
        back_home.click(lambda: (gr.update(visible=False), gr.update(visible=True)),
                        outputs=[res_screen, home_screen])

        gr.HTML('<div class="footer">Built for demo • MedBot with login</div>')

    return app

if __name__ == "__main__":
    build_app().launch(share=True)
