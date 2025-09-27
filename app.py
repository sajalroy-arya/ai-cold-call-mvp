import streamlit as st

# --- Initialization and State Management (The Brain's Memory) ---
# Use session_state to manage the conversation flow without a database
if 'step' not in st.session_state:
    st.session_state['step'] = 0
    st.session_state['messages'] = []
    st.session_state['user_name'] = ""

# --- Agent Logic (The Qualifying Script) ---
def get_agent_response(user_input):
    """
    Simulates the core agent logic based on the current step.
    NO external APIs (LLMs, TTS) are called yet, adhering to $0 mandate.
    """
    current_step = st.session_state['step']
    response = ""
    
    if current_step == 0:
        response = "Hello! My name is Riley, and I'm a pre-qualifier agent with [Your Agency Name]. I see you are the [Owner/Manager] at this company. Can you quickly confirm your name for me?"
        st.session_state['step'] = 1
        
    elif current_step == 1:
        # Capture the name and move to the pain point question
        st.session_state['user_name'] = user_input
        response = f"Thank you, {st.session_state['user_name']}. I'm calling because we help solo agencies book more clients. Quick question: are you currently finding it a challenge to consistently generate qualified sales leads?"
        st.session_state['step'] = 2
        
    elif current_step == 2:
        # Check for a positive or neutral response and move to booking
        if any(word in user_input.lower() for word in ['yes', 'yeah', 'challenge', 'struggling', 'maybe']):
            response = f"I thought so. It's tough out there, {st.session_state['user_name']}. Based on that, I can schedule a 10-minute slot with our human specialist, who can share one high-impact tactic. Does **Tuesday at 2 PM** work for you to book that 10-minute meeting?"
            st.session_state['step'] = 3
        else:
            response = "Understood. No problem at all. If anything changes, please feel free to reach out. Have a great day!"
            st.session_state['step'] = 99 # End conversation

    elif current_step == 3:
        # Check for confirmation and finalize the booking
        if any(word in user_input.lower() for word in ['yes', 'confirm', 'book', 'tuesday', 'sure']):
            response = f"Excellent! I've booked that slot for Tuesday at 2 PM. You will receive an email confirmation with the link shortly. Thank you for your time, {st.session_state['user_name']}!"
            st.session_state['step'] = 99 # End conversation
        else:
            response = "No problem. I can check other times, but for the purpose of this demo, let's assume it's booked. Thank you for your time! (END OF DEMO)"
            st.session_state['step'] = 99
            
    elif current_step == 99:
        response = "The call is complete. Thank you for using the qualifier agent demo."
        
    return response


# --- Streamlit UI (The Interface) ---
st.set_page_config(page_title="Riley AI Qualifier Demo", layout="wide")

st.title("📞 Riley AI Lead Qualifier Demo (Simulated Call)")
st.caption("Phase 1 MVP: Test the qualifying script logic before adding real voice APIs.")

# Display all past messages
for role, content in st.session_state['messages']:
    with st.chat_message(role):
        st.markdown(content)

# Initial Agent Message (on first run)
if st.session_state['step'] == 0:
    st.session_state['messages'].append(("assistant", get_agent_response("START")))
    st.experimental_rerun() # Rerun to display the first message immediately

# User Input Form
if st.session_state['step'] != 99:
    user_input = st.chat_input("Type your reply to the agent here:")

    if user_input:
        # 1. Store user message
        st.session_state['messages'].append(("user", user_input))
        
        # 2. Get and store agent response
        agent_response = get_agent_response(user_input)
        st.session_state['messages'].append(("assistant", agent_response))
        
        # 3. Rerun to display new messages
        st.experimental_rerun()
else:
    st.info("Demo complete. You can reset the state below to start a new call.")
    if st.button("Reset Demo"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()
