from openai import OpenAI
import streamlit as st
import requests
from datetime import datetime
# scratched the clipboard thing but might come back to it
# from st_copy_to_clipboard import st_copy_to_clipboard
from supabase import create_client

# setup supabase
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# setup page
st.set_page_config(page_title="Fay's Bible", page_icon="☻", layout="centered")


# to do: make login for saved verses
def clear_login_inputs():
    """Callback to clear login inputs"""
    st.session_state.login_username = ""
    st.session_state.login_password = ""

@st.dialog("Sign in to your Bible")
def login_modal():
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Let's go!", on_click=clear_login_inputs):
        # add database stuff
        if username and password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.error("Please enter a valid username and password.")
            # st.rerun()
            # add locigc!! lol. its just for shwo rn btw
        else:
            st.error("Please enter a valid username and password.")
            

# setup gpt wrapper
SYSTEM_PROMPT = {
    "role": "system",
    "content": """You are a scholarly educator on the Bible.

Rules:
- Do not provide spiritual guidance
- Provide context, clarification and insight into bible verses
- Always cite specific Bible verses (Book Chapter:Verse) when relevant
- Provide historical and cultural context when helpful
- Be respectful of all Christian denominations as well as other religions
- Keep responses clear and accessible
- If unsure, say so rather than making things up

Tone: Warm, thoughtful, and encouraging."""
}

# css styling changes
st.markdown("""
<style>
    /*hide the AI profile pictures too corny LOL*/
    [data-testid="stChatMessageAvatarUser"],
    [data-testid="stChatMessageAvatarAssistant"],
    .stChatMessage img,
    .stChatMessage svg {
        display: none !important;
    }
    
    /*hide the text inside the feedback form (too crowded)*/
    .stForm [data-testid="stFormSubmitButton"]::after {
        display: none !important;
    }
    .stForm small {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# init
if "verse_results" not in st.session_state:
    st.session_state.verse_results = None
 
 
# title and header of page
st.write("**welcome!** open sidebar for more.")
st.markdown("""<style>h1 { color: #1866cc }</style> <h1>lookup a chapter or verse:</h1>""", unsafe_allow_html=True)
# note: want this color #1866cc


# sidebar!
with st.sidebar:
    # full date and time
    now = datetime.now()
    #st.markdown(f"**{now.strftime('%A, %B %d')}** {now.strftime('%I:%M %p').lstrip('0')}")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f":blue[helping you get your **daily bread**, even at {now.strftime('%I:%M%p').lstrip('0').lower()} on a random {now.strftime('%A').lower()}.]")
    with col2:
        if st.button("Log in", on_click=clear_login_inputs):
            login_modal()

    st.markdown("---")
    st.header("Search Instructions")
    st.markdown("""
    - Search an `entire chapter` like :red[**Philippians 4**]
    
    - Search a `single verse` like :red[**Jeremiah 29:11**]
    
    - Search for a `range of verses` like :red[**Matthew 6:25-34**]
    
    - Search for `multiple chapters` like :red[**John 3:16-4:10**]
    
    """)
    
    # mini feedback bar for funsies
    st.markdown("---")
    with st.form(key="feedback_form", clear_on_submit=True):
        name = st.text_input(label="Send me feedback!", placeholder="Your name")
        message = st.text_input(label="", placeholder="Your message here", label_visibility="collapsed")
        submitted = st.form_submit_button("Send")

        if submitted and name and message:
            supabase.table("feedback").insert({"name":name, "message":message}).execute()
            st.success(f"Thanks for the feedback, {name}!")
            
    # footer
    st.markdown("---")
    st.markdown("""
                <div style='text-align: center; color: gray;'>
                <small>Made with ❤️ by Fay</small>
                </div>
                """, unsafe_allow_html=True)
    
    

# front page columns (search tool)
col1, col2, col3, col4 = st.columns([1, 0.5, 0.5, 0.5])
with col1:
    TRANSLATIONS = {
        "kjv": "King James Version",
        "web": "World English Bible",
        "bbe": "Bible in Basic English",
        "asv": "American Standard Version", 
    }
    translation = st.selectbox(
        "Select Translation",
        options=TRANSLATIONS.keys(),
        format_func=lambda x: TRANSLATIONS[x]
    )

with col2:
    book = st.text_input("Book Name", placeholder="Genesis")

with col3:
    verse = st.text_input("Chapter + Verse", placeholder="1:1")

with col4:
    st.markdown("<br>", unsafe_allow_html=True)
    search_button = st.button("Search", type="secondary")


# get the verse with bible api
def get_verse(book, verse, translation):
    url = f'https://bible-api.com/{book}+{verse}?translation={translation}'
    try:
        response = requests.get(url)
        if response.status_code == 404:
            st.error("Error! Please enter a valid book and verse.")
            return None
        elif response.status_code == 200: # if successful
            return response.json()
        else:
            # catch errors
            st.warning(f"Unexpected error. (Status code: {response.status_code})")
            return None
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

# logic to show the bible vers
def display_verse(bible_content):
    if bible_content:
        st.markdown("---")
        st.badge(f"{bible_content['reference']}", color="blue")

        reference = bible_content['reference']
    
        base_ref = reference.split(':')[0] if ':' in reference else reference
        base_book = base_ref.split(" ")[0]
        base_chapter = base_ref.split(" ")[1]

        for v in bible_content["verses"]:
            # col_text = st.columns(1)
            # with col_text:
            st.write(f'`{v["verse"]}` {v["text"]}')
            # with col_copy:
            #     full_verse = f"{base_ref}:{v['verse']} - {v['text'].strip()}"
            #     st_copy_to_clipboard(full_verse, before_copy_label="ᴄᴏᴘʏ", after_copy_label="✓")
            
        # add  a link to enduring word bible commentary
        # + bibleref while im at it lol.
        st.markdown("---")
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown(f'**Read commentary on {base_ref}:**')
        with col2:
            # note bug: in enduring word they call it"psalm" without  the s.
            if base_book == "Psalms":
                base_book = "Psalm"
            st.page_link(label=f':blue[from **Enduring Word**]',
                        page=f'https://enduringword.com/bible-commentary/{base_book}-{base_chapter}/')
        with col3:
            # lol there has to be a more effecient way to resolve this
            if base_book == "Psalm":
                base_book = "Psalms"
            st.page_link(label=f':blue[from **BibleRef**]',
                        page=f'https://www.bibleref.com/{base_book}/{base_chapter}/{base_book}-chapter-{base_chapter}.html')


# trigger with the search btn
if search_button:
    if book and verse:
        with st.spinner("..."):
            result = get_verse(book, verse, translation)
            if result:
                st.session_state.verse_results = result
    elif book and not verse:
        st.warning("Please enter a chapter and verse.")
    else:
        st.warning("Please enter both a book name and verse.")

display_verse(st.session_state.verse_results)


# implement large language model ------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = [SYSTEM_PROMPT]

for message in st.session_state.messages:
    if message["role"] != "system":  
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("need more context or clarification?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        # providing current verse or chapter for context if available
        messages_to_send = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]
        if st.session_state.verse_results:
            verse_text = "\n".join(
                f'{v["verse"]}. {v["text"]}' for v in st.session_state.verse_results["verses"]
            )
            verse_context = {
                "role": "system",
                "content": f"The user is currently viewing {st.session_state.verse_results['reference']}:\n{verse_text}"
            }
            messages_to_send.insert(1, verse_context)

        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=messages_to_send,
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
    



        
        
        
        
    
