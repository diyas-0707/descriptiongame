import streamlit as st
from openai import OpenAI
client = OpenAI()

def get_hint():
    """Generate a descriptive hint for a random object using OpenAI."""
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a psychologist."},
            {
                "role": "user",
                "content": (
                    "You are testing high school students for cognitive abilities. "
                    "Give a hint for a random object and also provide the correct answer. The correct answer must only be one word. "
                    "Format your response as 'HINT:  ANSWER: '. "
                    "Be descriptive, but not too revealing in the hint. "
                    "Only use two sentences for the hint. The difficulty level should be a 5 out of 10."
                ),
            },
        ],
    )
    response = completion.choices[0].message.content
    hint_part = response.split("ANSWER:")[0].replace("HINT:", "").strip()
    answer_part = response.split("ANSWER:")[1].strip().lower()
    return hint_part, answer_part

def advance_level():
    """Advance to the next level and get a new hint."""
    st.session_state.level += 1
    if st.session_state.level <= 4:
        hint, answer = get_hint()
        st.session_state.hint = hint
        st.session_state.answer = answer
        st.session_state.solved = False
        st.session_state.current_guess = ""
    else:
        st.session_state.game_complete = True

# Initialize session state
if 'level' not in st.session_state:
    st.session_state.level = 0
    st.session_state.hint = None
    st.session_state.answer = None
    st.session_state.solved = False
    st.session_state.current_guess = ""
    st.session_state.game_complete = False
    advance_level()

# Streamlit UI
st.title("Description Game")

if not st.session_state.game_complete:
    st.write(f"Test your cognitive abilities! You are currently on **Level {st.session_state.level}/4**.")

    # Display hint
    st.subheader("Here's your hint:")
    st.write(st.session_state.hint)

    # Input field and submit button
    guess_input = st.text_input(
        "What's your guess?", 
        value="",
        key=f"guess_input_{st.session_state.level}"
    )
    print(st.session_state.answer)
    if st.button("Submit Guess"):
        if guess_input.strip():  # Only process non-empty input
            if guess_input.lower() == st.session_state.answer:
                st.success("🎉 Congratulations! That's correct!")
                if st.session_state.level < 4:
                    advance_level()
                    st.rerun()
                else:
                    st.session_state.game_complete = True
                    st.rerun()
            else:
                st.error("Not quite right. Try again!")
else:
    st.success("🎉 Congratulations! You have completed all 4 levels!")