import streamlit as st
import requests


st.set_page_config(page_title="Bible Search", page_icon="☻", layout="wide")

# Title and description
st.title("Search a Bible Verse ☻")
st.markdown("**Read the Bible, King James Version**")

# Sidebar with instructions
with st.sidebar:
    st.header("HOW TO SEARCH")
    st.markdown("""
    **Enter a book and verse in these formats:**
    
    - `John 3` for an entire chapter
    - `John 3:16` for a single verse
    - `John 3:16-20` for a range of verses
    - `John 3:16-4:10` for multiple chapters
    
    **For example:**
    - Genesis 1:1
    - Psalm 23
    - Romans 8:28-39
    """)

# Main input area
col1, col2 = st.columns([3, 1])

with col1:
    book = st.text_input("Name of book:", placeholder="e.g., John")
    
with col2:
    verse = st.text_input("Chapter & verse:", placeholder="e.g., 3:16")

search_button = st.button("Search", use_container_width=True, type="primary")


def get_verse(book, verse):
    url = f'https://bible-api.com/{book}+{verse}?translation=kjv'
    try:
        response = requests.get(url)
        if response.status_code == 404:
            st.error("Error! Please enter a valid book and verse.")
            return
        elif response.status_code == 200: # if successful
            bible_content = response.json()
            st.success(f"Let's read {bible_content['reference']}!")
        
            st.markdown("---")
            verses = bible_content["verses"]
            
            for v in verses:
                # thsi makes sections which is not good i dont want
                with st.container():
                    # st.markdown(v{['verse']})
                    # what is difference between markdown and write
                    st.write(f':red[{v['verse']}] {v['text']}')
                    # st.markdown("") 
        
        else:
            st.warning(f"⚠️ unexpected error (Status code: {response.status_code})")
            # wha does this do?
            # like catching the errors
    except Exception as e:
        st.error(f"an error occurred: {str(e)}")

# searching stuff
if search_button:
    if book and verse:
        with st.spinner("searching..."):
            get_verse(book, verse)
    elif book and not verse:
        st.warning("⚠️ please enter a chapter and verse.")
    else:
        st.warning("⚠️ please enter both a book name and verse.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <small>Data provided by <a href='https://bible-api.com/' target='_blank'>Bible API</a></small>
</div>
""", unsafe_allow_html=True)