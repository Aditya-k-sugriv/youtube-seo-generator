import streamlit as st
from openai import OpenAI

# Page Configuration
st.set_page_config(
    page_title="ViralAI - Multi-Platform Video SEO Generator",
    page_icon="🚀",
    layout="wide"
)

# App Header
st.title("🚀 ViralAI: Multi-Platform Video SEO & Metadata Generator")
st.markdown(
    "Turn rough video ideas or scripts into viral-optimized **YouTube Titles, Descriptions, Tags, Hashtags, and Short Hooks** instantly using advanced LLM prompting."
)

# Sidebar for API Key & Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key_input = st.text_input("Enter your OpenAI API Key", type="password")
    
    st.markdown("---")
    st.markdown("### 💡 Mentor's Tip")
    st.info(
        "This tool uses the prompt engineering principles you learned from DeepLearning.AI—structuring system instructions to parse unstructured text into high-conversion social assets."
    )

# Main Application Form
with st.form("seo_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        video_topic = st.text_input(
            "Video Title / Core Subject",
            placeholder="e.g., How I built a passive income stream using AI in 30 days"
        )
        
    with col2:
        target_audience = st.selectbox(
            "Target Audience / Niche",
            ["Tech & AI Beginners", "Entrepreneurs & Freelancers", "Students & Learners", "General Creators", "Fitness & Lifestyle"]
        )

    video_content = st.text_area(
        "Paste your video script, rough notes, or key bullet points here:",
        placeholder="Paste details about what happens in the video...",
        height=150
    )
    
    submitted = st.form_submit_button("🔥 Generate Viral Metadata")

# Processing Form Submission
if submitted:
    if not api_key_input:
        st.error("⚠️ Please enter your OpenAI API key in the sidebar to proceed.")
    elif not video_topic or not video_content:
        st.warning("⚠️ Please fill in both the video subject and the core content/script.")
    else:
        client = OpenAI(api_key=api_key_input)
        
        system_prompt = (
            "You are an elite Social Media Growth & SEO Expert specializing in multi-platform optimization "
            "for YouTube, YouTube Shorts, Instagram Reels, and Facebook Reels. Your job is to take a creator's rough "
            "video concept or script and output high-converting metadata designed for maximum Click-Through Rate (CTR) "
            "and algorithmic discovery."
        )
        
        user_prompt = f"""
        Video Topic/Title: {video_topic}
        Target Audience: {target_audience}
        Video Script/Notes: {video_content}
        
        Please generate the following structured output:
        1. **YouTube Titles (3 Options):** Under 60 characters, highly clickable, front-loaded with primary keywords, and utilizing curiosity loops.
        2. **Optimized Description:** A 3-line high-retention hook using the primary keyword, followed by clear timestamp structure placeholders, and a strong call-to-action.
        3. **Strategic Tags:** 10 to 15 precise tags (primary, secondary, and long-tail variations) under 500 characters total.
        4. **Hashtags:** 3 high-impact hashtags tailored for YouTube/Shorts, and 5 for Instagram/Facebook Reels.
        5. **Short-Form Hook Suggestions:** A 3-second visual/verbal hook specifically for the first 3 seconds of a Short or Reel to kill drop-off.
        """

        with st.spinner("🤖 Analyzing trends, keywords, and crafting viral metadata..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.7
                )
                
                result_text = response.choices[0].message.content
                
                st.success("✨ Metadata successfully generated!")
                st.markdown("---")
                st.markdown(result_text)
                
            except Exception as e: