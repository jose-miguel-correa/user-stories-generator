import streamlit as st
import ollama

# Set page configuration
st.set_page_config(page_title="LLaMA 3 AI Generator", layout="wide")

# Add logo
logo_path = "logo.gif"  # Change this to your logo file path
st.image(logo_path, width=100)  # Adjust the width as needed

# Function to clear chat history
def clear_chat():
    st.session_state["messages"] = [{"role": "IT Engineer / Scrum Master", "content": "Escribe tu historia de usuario"}]
    st.session_state["full_message"] = ""

# Add a button to clear history
if st.button("🗑️ Limpiar Inputs"):
    clear_chat()

# Initialize messages if not present in session state
if "messages" not in st.session_state:
    clear_chat()

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message(msg["role"], avatar="🧑‍💻").write(msg["content"])
    else:
        st.chat_message(msg["role"], avatar="🤖").write(msg["content"])

# Generate response based on prompt
def generate_response(gherkin_prompt):
    response = ollama.chat(model='llama3', stream=True, messages=[{"role": "user", "content": gherkin_prompt}])
    for partial_resp in response:
        token = partial_resp["message"]["content"]
        st.session_state["full_message"] += token
        yield token

# First input for initial user story
if user_input := st.chat_input(placeholder="Escribe el objetivo de la historia de usuario"):
    gherkin_prompt = (
        f'Escribe una historia de usuario en formato Gherkin para {user_input}. '
        f'La historia de usuario debe incluir detalles relevantes y contexto específico:\n'
        f'- Scenario: Describe el contexto general del escenario.\n'
        f'- Given: Proporciona el estado inicial del sistema o del usuario.\n'
        f'- When: Explica la acción que el usuario realiza.\n'
        f'- Then: Criterio de aceptación.\n'
        f'La historia debe estar completa en español, incluyendo cualquier caso de uso adicional que sea relevante.'
    )
    
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user", avatar="🧑‍💻").write(user_input)
    
    st.session_state["full_message"] = ""
    st.chat_message("assistant", avatar="🤖").write_stream(generate_response(gherkin_prompt))
    st.session_state.messages.append({"role": "assistant", "content": st.session_state["full_message"]})

# Second input for improvements or feedback on the original answer
if "messages" in st.session_state and len(st.session_state["messages"]) > 1:
    improvement_input = st.text_input("¿Quieres mejorar la historia de usuario? Escribe tu sugerencia:")
    
    if improvement_input:
        last_response = st.session_state["messages"][-1]["content"]
        gherkin_improvement_prompt = (
            f'Basado en la siguiente historia de usuario:\n'
            f'"{last_response}". Mejora esta historia de usuario según la siguiente sugerencia:\n'
            f'"{improvement_input}".'
        )
        
        st.session_state.messages.append({"role": "user", "content": improvement_input})
        st.chat_message("user", avatar="🧑‍💻").write(improvement_input)
        
        st.session_state["full_message"] = ""
        st.chat_message("assistant", avatar="🤖").write_stream(generate_response(gherkin_improvement_prompt))
        st.session_state.messages.append({"role": "assistant", "content": st.session_state["full_message"]})
