import streamlit as st

st.set_page_config(page_title="AI Assistant", layout="wide")

# Check login
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.error("Please login first")
    st.stop()

st.title("AI Assistant")
st.write(f"User: {st.session_state.username} | Role: {st.session_state.role}")

# Simple chat interface
st.write("This is a simulated AI Assistant. For real implementation, add OpenAI API.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your AI Assistant. How can I help you today?"}
    ]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("Type your question here..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Simulate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Simple responses based on keywords
            if "security" in prompt.lower() or "cyber" in prompt.lower():
                response = """
**Security Recommendation:**
1. Regularly update your software
2. Use strong, unique passwords
3. Enable two-factor authentication
4. Be cautious of suspicious emails
5. Backup your data regularly
                """
            elif "it" in prompt.lower() or "ticket" in prompt.lower():
                response = """
**IT Support Tips:**
1. Prioritize high-priority tickets
2. Document all solutions
3. Communicate clearly with users
4. Follow up on unresolved issues
5. Maintain knowledge base
                """
            else:
                response = f"I understand you're asking about '{prompt}'. For detailed analysis, please integrate the OpenAI API."
            
            st.write(response)
    
    # Add AI response to history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Clear chat button
if st.button("Clear Chat"):
    st.session_state.messages = [
        {"role": "assistant", "content": "Chat cleared. How can I help you?"}
    ]
    st.rerun()

# Navigation
st.markdown("---")
if st.button("← Back to Home"):
    st.switch_page("app.py")