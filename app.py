import streamlit as st
from groq import Groq

# ---------------- Page Configuration ----------------
st.set_page_config(
    page_title="ViralAI | Social Media SEO Studio",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------- Styling ----------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #0b1020 0%, #111827 48%, #0b1020 100%);
        color: #f8fafc;
    }
    [data-testid="stSidebar"] {
        background: #111827;
        border-right: 1px solid #263247;
    }
    .hero {
        padding: 1.6rem 1.8rem;
        border-radius: 22px;
        background: linear-gradient(120deg, #172554, #312e81 55%, #4c1d95);
        border: 1px solid #4338ca;
        margin-bottom: 1.25rem;
    }
    .hero h1 { color: #ffffff; margin-bottom: .35rem; }
    .hero p { color: #dbeafe; font-size: 1.03rem; margin-bottom: 0; }
    .small-note { color: #a5b4fc; font-size: .9rem; }
    div[data-testid="stForm"] {
        background: rgba(17, 24, 39, .78);
        padding: 1.2rem;
        border: 1px solid #334155;
        border-radius: 18px;
    }
    div.stButton > button, div.stFormSubmitButton > button {
        border-radius: 10px;
        min-height: 2.8rem;
        font-weight: 650;
    }
    div[data-testid="stTextArea"] textarea,
    div[data-testid="stTextInput"] input {
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- Header ----------------
st.markdown(
    """
    <div class="hero">
        <h1>🚀 ViralAI</h1>
        <p>Your AI studio for video titles, descriptions, tags, hashtags and scroll-stopping hooks.</p>
        <p class="small-note">Create smarter metadata for YouTube, Shorts, Instagram Reels and Facebook Reels.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------- Sidebar ----------------
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    st.caption("Your API key is read from Streamlit Secrets.")
    st.markdown("---")
    st.markdown("### ✨ What you can create")
    st.markdown(
        "- Click-worthy title ideas\n"
        "- Search-friendly descriptions\n"
        "- Relevant tags and hashtags\n"
        "- Short-form opening hooks"
    )
    st.markdown("---")
    st.caption("Tip: Use a specific topic and include the main points covered in your video.")
    st.caption("Never put your API key in public source code.")

# ---------------- Input Form ----------------
left, right = st.columns([1.35, 0.85], gap="large")

with left:
    st.subheader("🎬 Create your metadata")
    with st.form("seo_form"):
        video_topic = st.text_input(
            "Video topic or working title *",
            placeholder="e.g. 5 free AI tools every student should know",
        )
        video_content = st.text_area(
            "Video script, rough notes or key points *",
            placeholder="What happens in the video? Add key ideas, steps, facts or story beats...",
            height=190,
        )
        col_a, col_b = st.columns(2)
        with col_a:
            platform = st.selectbox(
                "Platform",
                [
                    "YouTube (Long Video)",
                    "YouTube Shorts",
                    "Instagram Reels",
                    "Facebook Reels",
                    "All Platforms",
                ],
            )
            language = st.selectbox("Output language", ["English", "Hindi", "Hinglish"])
        with col_b:
            target_audience = st.selectbox(
                "Target audience",
                [
                    "Tech & AI Beginners",
                    "Entrepreneurs & Freelancers",
                    "Students & Learners",
                    "General Creators",
                    "Fitness & Lifestyle",
                    "Education & Exam Preparation",
                    "Bhakti & Spirituality",
                    "Entertainment & Comedy",
                    "Other",
                ],
            )
            tone = st.selectbox(
                "Content style",
                ["Informative", "Curiosity-driven", "Funny", "Emotional", "Professional", "Devotional"],
            )
        submitted = st.form_submit_button("✨ Generate SEO Metadata", type="primary", use_container_width=True)

with right:
    st.subheader("💡 Get better results")
    st.info(
        "Be specific. Instead of “AI tools”, try “5 free AI tools for students preparing for exams”."
    )
    st.markdown("#### A useful brief includes")
    st.markdown(
        "1. **Main subject** — what the video is about\n"
        "2. **Audience** — who should watch it\n"
        "3. **Value** — what viewers will learn or feel\n"
        "4. **Proof/details** — steps, examples or story points"
    )
    st.markdown("#### Built for creators")
    st.markdown("- Multiple title options\n- Platform-aware hashtags\n- Hooks for the opening seconds\n- Easy-to-copy output")

# ---------------- Generation ----------------
if submitted:
    if not video_topic.strip() or not video_content.strip():
        st.warning("Please fill in both the video topic and the script/notes.")
    else:
        try:
            api_key = st.secrets.get("GROQ_API_KEY", "")
            if not api_key:
                st.error(
                    "Groq API key not configured. Open your Streamlit app settings → Secrets "
                    "and add GROQ_API_KEY = \"your_key_here\"."
                )
                st.stop()

            client = Groq(api_key=api_key)

            system_prompt = (
                "You are ViralAI, a practical social media SEO strategist. "
                "Create truthful, relevant metadata based only on the user's supplied topic and notes. "
                "Do not promise virality or invent facts, statistics, timestamps, or claims. "
                "Make output specific to the selected platform and audience."
            )

            user_prompt = f"""
Create a complete video SEO package.

Topic/title: {video_topic}
Audience: {target_audience}
Platform: {platform}
Output language: {language}
Tone: {tone}
Script/notes: {video_content}

Return clear headings and the following:
1. Three distinct title options. Aim for concise, compelling titles and keep YouTube titles under about 60 characters where possible.
2. One searchable description with a strong opening, a concise summary, and a relevant call to action. Do not invent timestamps; use timestamp placeholders only if useful.
3. 10–15 relevant tags, comma-separated and focused on the actual content.
4. Relevant hashtags for the selected platform. Avoid unrelated trending tags.
5. Three short-form hooks suitable for the first 3 seconds, including a visual suggestion where appropriate.
6. One recommended title and a short explanation of why it fits the audience.
7. A brief accuracy reminder if the supplied notes do not support a claim.

Use {language} for the output. Keep the result easy to scan and copy.
"""

            with st.spinner("✨ Creating your metadata..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    temperature=0.7,
                    max_tokens=1800,
                )
                result_text = response.choices[0].message.content or ""

            st.success("Your metadata is ready.")
            st.markdown("---")
            st.subheader("📦 Your SEO package")
            st.text_area("Generated result — select and copy", value=result_text, height=430)
            st.download_button(
                "⬇️ Download result as TXT",
                data=result_text,
                file_name="viralai_metadata.txt",
                mime="text/plain",
                use_container_width=True,
            )

        except st.errors.StreamlitSecretNotFoundError:
            st.error('Streamlit Secrets are not configured. Add GROQ_API_KEY in your app settings.')
        except Exception as exc:
            st.error("Generation failed. Check your API key, model availability, usage limits, and app logs.")
            with st.expander("Technical details"):
                st.code(str(exc))

st.markdown("---")
st.caption("ViralAI helps draft metadata. Actual reach depends on content quality, audience response and platform algorithms.")
