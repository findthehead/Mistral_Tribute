import os
from dotenv import load_dotenv
from mistralai import Mistral
import streamlit as st
load_dotenv()


st.title("How may I help you?")
api_key = os.getenv("MISTRAL_API_KEY")
client = Mistral(api_key=api_key)
if not api_key:
    raise RuntimeError(
        "Environment variable MISTRAL_API_KEY is not set. "
        "Set it and retry (e.g. `export MISTRAL_API_KEY=your_key`)."
    )

# def main():
if "Mistral_model" not in st.session_state:
    st.session_state["Mistral_model"] = "mistral-small-latest"
if "messages" not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        res = client.chat.complete(
            model=st.session_state.get("Mistral_model", "mistral-small-latest"),
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=False,
        )
        # extract the assistant text, display it, and append the actual string to session state
        assistant_text = None
        try:
            assistant_text = res.choices[0].message.content
        except Exception:
            assistant_text = getattr(res.choices[0].message, "content", None) or str(res)
        if assistant_text is None:
            assistant_text = ""
        st.markdown(assistant_text)
    st.session_state.messages.append({"role": "assistant", "content": assistant_text})
