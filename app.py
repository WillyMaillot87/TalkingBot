import streamlit as st
from transformers import BlenderbotTokenizerFast, BlenderbotForConditionalGeneration
import time

st.title("Local ChatBot")

checkpoint = "facebook/blenderbot-400M-distill"

#Tokenizer
tokenizer = BlenderbotTokenizerFast.from_pretrained(checkpoint)

# Model
model = BlenderbotForConditionalGeneration.from_pretrained(checkpoint)


if "blenderbot_model" not in st.session_state:
    st.session_state["blenderbot_model"] = "facebook/blenderbot-400M-distill"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What's Up ?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # Generate response based on the chat history
        inputs = tokenizer([prompt], return_tensors="pt", max_length=1024, padding='longest')
        response = model.generate(**inputs)

        # Décoder la réponse
        output_text = tokenizer.decode(response[0], skip_special_tokens=True)

        # Simulate stream of response with milliseconds delay
        for chunk in output_text.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Display sidebar
with st.sidebar :
    #Link to the githupb repo
    st.link_button("Go to GitHub Repository", "https://github.com/WillyMaillot87/my_llm_project")

    # Add button to clear the chat history
    if st.button('Clear Chat History', type="primary"):
        st.write('Chat history erased')
        st.session_state.messages = []
    else:
        st.write(f"History size : {len(st.session_state.messages)}")