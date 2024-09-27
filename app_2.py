import streamlit as st
import ollama

# Set page configuration
#st.set_page_config(page_title="LLaMA 3 AI Generator", layout="wide")


# Load CSS styles
def load_css():
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()



# Add logo
logo_path = "logo.gif"  # Change this to your logo file path
st.image(logo_path, width=100)  # Adjust the width as needed

#st.title("LLaMA 3 AI Generator")

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
if prompt := st.chat_input(placeholder="Escribe tu historia de usuario"):
    gherkin_prompt = f'Escribe tu historia de usuario para "{prompt}" en formato Gherkin. Ejemplo: Como un [tipo de usuario], quiero [objetivo] para que [razón]. La historia de usuario debe estar completa en español.'
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user", avatar="🧑‍💻").write(prompt)
    
    st.session_state["full_message"] = ""
    st.chat_message("assistant", avatar="🤖").write_stream(generate_response(gherkin_prompt))
    st.session_state.messages.append({"role": "assistant", "content": st.session_state["full_message"]})

# Second input for improvements or feedback on the original answer
if "messages" in st.session_state and len(st.session_state["messages"]) > 1:
    improvement_input = st.text_input("¿Quieres mejorar la historia de usuario? Escribe tu sugerencia:")
    
    if improvement_input:
        # Get the last assistant's response to reference
        last_response = st.session_state["messages"][-1]["content"]
        
        # Format the improvement request with reference to the previous answer
        gherkin_improvement_prompt = f'Basado en la siguiente historia de usuario: "{last_response}". Mejora esta historia de usuario según la siguiente sugerencia: "{improvement_input}".'
        
        st.session_state.messages.append({"role": "user", "content": improvement_input})
        st.chat_message("user", avatar="🧑‍💻").write(improvement_input)
        
        st.session_state["full_message"] = ""
        st.chat_message("assistant", avatar="🤖").write_stream(generate_response(gherkin_improvement_prompt))
        st.session_state.messages.append({"role": "assistant", "content": st.session_state["full_message"]})
