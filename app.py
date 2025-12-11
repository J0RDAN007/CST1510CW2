import streamlit as st

# Set page config
st.set_page_config(
    page_title="Intelligence Platform",
    layout="wide"
)

def main():
    st.title("Multi-Domain Intelligence Platform")
    st.write("Welcome to the Intelligence Platform Dashboard")
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Cybersecurity")
        st.write("Monitor security incidents")
        if st.button("Go to Cybersecurity Dashboard"):
            st.switch_page("pages/2.Cybersecurity_Dashboard.py")
    
    with col2:
        st.subheader("IT Operations")
        st.write("Manage IT service desk")
        if st.button("Go to IT Operations Dashboard"):
            st.switch_page("pages/3.IT_Operations_Dashboard.py")
    
    with col3:
        st.subheader("AI Assistant")
        st.write("Get AI-powered insights")
        if st.button("Go to AI Assistant"):
            st.switch_page("pages/4.AI_Assistant.py")
    
    # Login/Logout
    st.markdown("---")
    
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        st.info("Please login from the Login page")
        if st.button("Go to Login Page"):
            st.switch_page("pages/1.Login.py")
    else:
        st.success(f"Welcome, {st.session_state.get('username', 'User')}!")
        if st.button("Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

if __name__ == "__main__":
    main()