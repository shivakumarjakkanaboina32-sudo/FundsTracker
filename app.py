import streamlit as st
from openai import OpenAI
import os

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BrandCraft AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* { font-family: 'Inter', sans-serif; }

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
}

[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.04);
    border-right: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(20px);
}

.brand-header {
    background: linear-gradient(135deg, rgba(138,43,226,0.3), rgba(72,52,212,0.3));
    border: 1px solid rgba(138,43,226,0.4);
    border-radius: 20px;
    padding: 2.5rem;
    text-align: center;
    margin-bottom: 2rem;
    backdrop-filter: blur(10px);
}

.brand-header h1 {
    background: linear-gradient(90deg, #a78bfa, #f472b6, #fb923c);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 3rem;
    font-weight: 800;
    margin: 0;
    letter-spacing: -1px;
}

.brand-header p {
    color: rgba(255,255,255,0.6);
    font-size: 1.1rem;
    margin-top: 0.5rem;
}

.feature-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
}

.feature-card:hover {
    border-color: rgba(167,139,250,0.5);
    background: rgba(255,255,255,0.08);
    transform: translateY(-2px);
}

.result-box {
    background: linear-gradient(135deg, rgba(15,12,41,0.9), rgba(48,43,99,0.9));
    border: 1px solid rgba(167,139,250,0.3);
    border-radius: 16px;
    padding: 1.5rem;
    margin-top: 1rem;
    color: #e2e8f0;
    line-height: 1.8;
    white-space: pre-wrap;
    font-size: 0.95rem;
}

.tab-label {
    font-size: 0.85rem;
    font-weight: 600;
    letter-spacing: 0.5px;
}

.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.6rem 2rem !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    transition: all 0.3s ease !important;
    width: 100%;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #6d28d9, #4338ca) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 25px rgba(124,58,237,0.4) !important;
}

[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stSelectbox"] > div {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}

label, .stMarkdown p {
    color: rgba(255,255,255,0.8) !important;
}

.metric-badge {
    display: inline-block;
    background: rgba(167,139,250,0.2);
    border: 1px solid rgba(167,139,250,0.4);
    border-radius: 20px;
    padding: 0.25rem 0.75rem;
    font-size: 0.8rem;
    color: #a78bfa;
    font-weight: 600;
    margin: 0.2rem;
}

.sidebar-title {
    color: #a78bfa;
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 1rem;
}

div[data-testid="stTabs"] button {
    color: rgba(255,255,255,0.6) !important;
    font-weight: 600 !important;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    color: #a78bfa !important;
    border-bottom-color: #a78bfa !important;
}
</style>
""", unsafe_allow_html=True)

# ── Client Setup ──────────────────────────────────────────────────────────────
@st.cache_resource
def get_client():
    api_key = st.session_state.get("api_key", "")
    return OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
    )

MODEL = "openai/gpt-4o"   # openai/gpt-oss-120b (use exact slug from OpenRouter)

def call_ai(prompt: str, system: str = "You are BrandCraft, an expert AI branding strategist.") -> str:
    api_key = st.session_state.get("api_key", "")
    if not api_key:
        return "⚠️ Please enter your OpenRouter API key in the sidebar."
    client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            max_tokens=1500,
            temperature=0.8,
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-title">⚙️ Configuration</div>', unsafe_allow_html=True)
    api_key = st.text_input("OpenRouter API Key", type="password", placeholder="sk-or-...")
    if api_key:
        st.session_state["api_key"] = api_key

    st.markdown("---")
    st.markdown("""
    <div style='color:rgba(255,255,255,0.5); font-size:0.8rem;'>
    <b style='color:#a78bfa'>Model:</b> openai/gpt-oss-120b<br><br>
    <b style='color:#a78bfa'>Features:</b><br>
    ✨ Brand Name Generation<br>
    🎨 Logo Concept Creation<br>
    ✍️ Content Automation<br>
    💬 Sentiment Analysis<br>
    🤖 Branding Assistant
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<span class="metric-badge">GPT-OSS-120B</span><span class="metric-badge">OpenRouter</span>', unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="brand-header">
    <h1>✨ BrandCraft AI</h1>
    <p>Generative AI–Powered Branding Automation System</p>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tabs = st.tabs(["🏷️ Brand Names", "🎨 Logo Concept", "✍️ Content Writing", "💬 Sentiment Analysis", "🤖 Brand Assistant"])

# ── Tab 1: Brand Name Generation ──────────────────────────────────────────────
with tabs[0]:
    st.markdown("### 🏷️ Brand Name Generator")
    col1, col2 = st.columns(2)
    with col1:
        industry = st.text_input("Industry / Niche", placeholder="e.g. Sustainable Fashion, SaaS, Food Tech")
        keywords = st.text_input("Core Keywords", placeholder="e.g. eco, smart, bold, luxury")
    with col2:
        audience = st.text_input("Target Audience", placeholder="e.g. Gen Z, Entrepreneurs, Parents")
        style = st.selectbox("Brand Style", ["Modern & Minimal", "Playful & Fun", "Professional & Corporate", "Bold & Edgy", "Luxury & Premium"])

    if st.button("✨ Generate Brand Names", key="brand_name"):
        with st.spinner("Crafting unique brand names..."):
            prompt = f"""Generate 10 unique, memorable brand names for a company in the {industry} industry.
Target audience: {audience}
Core keywords: {keywords}
Brand style: {style}

For each name provide:
1. The brand name
2. Why it works (1 line)
3. Domain availability tip
4. A short tagline

Format clearly and make names creative, catchy, and memorable."""
            result = call_ai(prompt)
        st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)

# ── Tab 2: Logo Concept ───────────────────────────────────────────────────────
with tabs[1]:
    st.markdown("### 🎨 Logo Concept Creator")
    col1, col2 = st.columns(2)
    with col1:
        brand_name = st.text_input("Brand Name", placeholder="e.g. NovaSpark")
        brand_values = st.text_input("Brand Values", placeholder="e.g. innovation, trust, speed")
    with col2:
        color_pref = st.selectbox("Color Palette Preference", ["Vibrant & Bold", "Pastel & Soft", "Dark & Moody", "Monochrome", "Earth Tones", "Neon & Electric"])
        logo_style = st.selectbox("Logo Style", ["Wordmark", "Lettermark", "Pictorial Mark", "Abstract Mark", "Mascot", "Combination Mark"])

    if st.button("🎨 Generate Logo Concept", key="logo"):
        with st.spinner("Designing your logo concept..."):
            prompt = f"""Create a detailed logo design brief and concept for brand: {brand_name}
Brand values: {brand_values}
Color palette preference: {color_pref}
Logo style: {logo_style}

Include:
1. Visual Concept Description (detailed)
2. Color Palette (with hex codes)
3. Typography Recommendation (font families)
4. Symbol/Icon Description
5. Design Rationale
6. Variations (primary, secondary, icon-only)
7. Usage Guidelines
8. Figma/Design Tool Tips

Be specific and detailed so a designer can execute this."""
            result = call_ai(prompt)
        st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)

# ── Tab 3: Content Writing ────────────────────────────────────────────────────
with tabs[2]:
    st.markdown("### ✍️ Content Automation")
    content_type = st.selectbox("Content Type", [
        "Brand Story / About Us",
        "Social Media Posts (7-day plan)",
        "Email Newsletter",
        "Product Description",
        "Press Release",
        "Website Homepage Copy",
        "Ad Copy (Google/Meta)",
    ])
    col1, col2 = st.columns(2)
    with col1:
        brand_info = st.text_area("Brand Description", placeholder="Tell us about your brand, product, or service...", height=120)
    with col2:
        tone = st.selectbox("Tone of Voice", ["Professional", "Conversational", "Inspirational", "Humorous", "Authoritative", "Friendly"])
        word_count = st.selectbox("Length", ["Short (150-250 words)", "Medium (300-500 words)", "Long (600-900 words)"])

    if st.button("✍️ Generate Content", key="content"):
        with st.spinner("Writing your content..."):
            prompt = f"""Write {content_type} for a brand with the following info:
{brand_info}

Tone: {tone}
Length: {word_count}

Make it compelling, on-brand, and ready to publish. Include any relevant CTAs, hashtags, or formatting as appropriate for the content type."""
            result = call_ai(prompt, system="You are an expert brand copywriter and content strategist. Write compelling, conversion-focused content.")
        st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)

# ── Tab 4: Sentiment Analysis ─────────────────────────────────────────────────
with tabs[3]:
    st.markdown("### 💬 Brand Sentiment Analysis")
    st.info("Paste customer reviews, social media comments, or any brand-related text to analyze sentiment and extract brand insights.", icon="ℹ️")
    user_text = st.text_area("Customer Feedback / Social Media Text", placeholder="Paste reviews, tweets, comments, feedback here...", height=200)
    brand_context = st.text_input("Brand/Product Name (optional)", placeholder="e.g. NovaSpark App")

    if st.button("💬 Analyze Sentiment", key="sentiment"):
        with st.spinner("Analyzing sentiment and brand perception..."):
            prompt = f"""Perform a comprehensive brand sentiment analysis on the following text{f' about {brand_context}' if brand_context else ''}:

TEXT:
{user_text}

Provide:
1. Overall Sentiment Score (0-100, with label: Very Negative / Negative / Neutral / Positive / Very Positive)
2. Sentiment Breakdown (% Positive, Neutral, Negative)
3. Key Themes Identified (positive themes & pain points)
4. Most Impactful Phrases (exact quotes)
5. Customer Emotion Tags (e.g. frustrated, delighted, confused)
6. Brand Perception Summary
7. Actionable Recommendations for the brand team
8. Priority Issues to Address

Format as a structured report."""
            result = call_ai(prompt, system="You are an expert brand analyst and consumer psychology specialist specializing in sentiment analysis and brand perception.")
        st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)

# ── Tab 5: Branding Assistant ──────────────────────────────────────────────────
with tabs[4]:
    st.markdown("### 🤖 AI Branding Assistant")
    st.markdown('<p style="color:rgba(255,255,255,0.5); font-size:0.9rem;">Your personal AI branding expert. Ask anything about brand strategy, positioning, identity, or marketing.</p>', unsafe_allow_html=True)

    if "brand_chat" not in st.session_state:
        st.session_state.brand_chat = []

    # Chat display
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.brand_chat:
            if msg["role"] == "user":
                st.markdown(f"""<div style="background:rgba(124,58,237,0.2);border:1px solid rgba(124,58,237,0.3);border-radius:12px;padding:0.75rem 1rem;margin:0.5rem 0;color:#e2e8f0;">
                <b style="color:#a78bfa">You:</b> {msg['content']}</div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""<div style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:12px;padding:0.75rem 1rem;margin:0.5rem 0;color:#e2e8f0;">
                <b style="color:#f472b6">BrandCraft AI:</b> {msg['content']}</div>""", unsafe_allow_html=True)

    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input("Ask your branding question...", placeholder="e.g. How do I position my brand against competitors?", key="chat_input", label_visibility="collapsed")
    with col2:
        send = st.button("Send →", key="send_chat")

    if send and user_input:
        st.session_state.brand_chat.append({"role": "user", "content": user_input})
        history_prompt = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state.brand_chat[-6:]])
        with st.spinner("Thinking..."):
            response = call_ai(
                history_prompt,
                system="You are BrandCraft, a world-class AI branding strategist with expertise in brand identity, positioning, visual identity, content strategy, and brand growth. Provide actionable, expert advice."
            )
        st.session_state.brand_chat.append({"role": "assistant", "content": response})
        st.rerun()

    if st.button("🗑️ Clear Chat", key="clear_chat"):
        st.session_state.brand_chat = []
        st.rerun()

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:rgba(255,255,255,0.3); font-size:0.8rem; padding:1rem 0;">
    ✨ BrandCraft AI — Powered by <b style="color:#a78bfa">openai/gpt-oss-120b</b> via OpenRouter &nbsp;|&nbsp; Built with Streamlit
</div>
""", unsafe_allow_html=True)
