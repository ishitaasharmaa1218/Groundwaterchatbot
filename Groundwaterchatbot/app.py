import streamlit as st
import pandas as pd
from chatbot import ask_bot

st.set_page_config(
    page_title="Groundwater AI Chatbot",
    page_icon="💧",
    layout="wide"
)

# Initialize session history
if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar (Chat History)
st.sidebar.title("💬 Chat History")

if st.session_state.history:
    for i, item in enumerate(st.session_state.history):
        st.sidebar.write(f"**Q{i+1}:** {item['question']}")
else:
    st.sidebar.write("No questions asked yet.")

st.sidebar.markdown("---")

if st.sidebar.button("Clear History"):
    st.session_state.history = []

# Main Title
st.title("💧 Groundwater AI Chatbot")

st.markdown(
"""
Welcome! This AI assistant helps analyze **groundwater trends** from the dataset.

You can ask questions about:

• Groundwater level trends  
• Impact of precipitation  
• Pumping rate effects  
• Seasonal groundwater changes  
"""
)

# Suggested Questions
st.subheader("Suggested Questions")

suggestions = [
    "What is the groundwater level trend?",
    "How does precipitation affect groundwater level?",
    "Which month has the lowest groundwater level?",
    "Does pumping rate impact groundwater level?"
]

cols = st.columns(2)

for i, q in enumerate(suggestions):
    if cols[i % 2].button(q):
        st.session_state.user_question = q

# Input box
question = st.text_input(
    "Ask a question about groundwater data",
    value=st.session_state.get("user_question", "")
)

if st.button("Ask"):

    if question:

        answer, context = ask_bot(question)

        # Save history
        st.session_state.history.append({
            "question": question,
            "answer": answer
        })

        # Show Answer
        st.subheader("AI Explanation")
        st.write(answer)

        # Extract data for chart
        levels = []
        months = []

        for row in context.split("\n"):

            if "Groundwater_Level" in row:

                try:
                    parts = row.split("|")

                    for p in parts:

                        if "Groundwater_Level" in p:
                            levels.append(float(p.split(":")[1]))

                        if "Month" in p:
                            months.append(int(p.split(":")[1]))

                except:
                    pass

        # Visualization
        if len(levels) > 0:

            df = pd.DataFrame({
                "Month": months,
                "Groundwater_Level": levels
            })

            st.subheader("📈 Groundwater Level Trend")

            st.line_chart(df.set_index("Month"))

        # Source Data
        st.subheader("📄 Source Data Used")

        st.code(context)

# Display previous chat in main page
if st.session_state.history:

    st.markdown("---")
    st.subheader("Conversation")

    for item in reversed(st.session_state.history):

        st.markdown(f"**🧑 Question:** {item['question']}")
        st.markdown(f"**🤖 Answer:** {item['answer']}")
        st.markdown("---")