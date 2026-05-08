import streamlit as st
from database import init_db, get_all_jobs, update_job_status
from webbscraper import scrape_remoteok

init_db()

st.set_page_config(page_title="Tech Job Hunter", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600&family=Source+Sans+3:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Source Sans 3', sans-serif;
    background-color: #0a1628;
    color: #f0f4ff;
}

.stApp {
    background-color: #0a1628;
}

.header-block {
    text-align: center;
    padding: 2.5rem 0 1.5rem 0;
    border-bottom: 1px solid #1e3a5f;
    margin-bottom: 2rem;
}

.header-block h1 {
    font-family: 'Playfair Display', serif;
    font-size: 3.2rem;
    font-weight: 600;
    color: #ffffff;
    letter-spacing: -0.5px;
    margin-bottom: 0.3rem;
}

.header-block p {
    font-size: 1rem;
    font-weight: 300;
    color: #7a9cc4;
    letter-spacing: 1px;
}

.search-section {
    background: #0f2040;
    border: 1px solid #1e3a5f;
    border-radius: 10px;
    padding: 1.4rem 1.8rem;
    margin-bottom: 2rem;
}

.section-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #7a9cc4;
    margin-bottom: 0.6rem;
}

.stat-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
}

.stat-card {
    flex: 1;
    background: #0f2040;
    border: 1px solid #1e3a5f;
    border-radius: 8px;
    padding: 1.2rem 1.5rem;
}

.stat-card .label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #7a9cc4;
    margin-bottom: 0.4rem;
}

.stat-card .value {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    color: #ffffff;
}

.stat-card.accent .value {
    color: #f0c060;
}

.stTextInput input {
    background: #162d4a !important;
    border: 1px solid #1e3a5f !important;
    border-radius: 6px !important;
    color: #f0f4ff !important;
    font-family: 'Source Sans 3', sans-serif !important;
    font-size: 1rem !important;
}

.stTextInput input::placeholder {
    color: #4a6a8a !important;
}

.stSelectbox > div > div {
    background: #162d4a !important;
    border: 1px solid #1e3a5f !important;
    color: #f0f4ff !important;
}

.stTextArea textarea {
    background: #162d4a !important;
    border: 1px solid #1e3a5f !important;
    color: #f0f4ff !important;
    font-family: 'Source Sans 3', sans-serif !important;
}

.stButton > button {
    background: #1a5276 !important;
    color: #ffffff !important;
    border: 1px solid #2471a3 !important;
    border-radius: 6px !important;
    font-family: 'Source Sans 3', sans-serif !important;
    font-weight: 500 !important;
    padding: 0.4rem 1.2rem !important;
    transition: background 0.2s !important;
}

.stButton > button:hover {
    background: #2471a3 !important;
}

.stFormSubmitButton > button {
    background: #1a5276 !important;
    color: #ffffff !important;
    border: 1px solid #2471a3 !important;
    border-radius: 6px !important;
    font-family: 'Source Sans 3', sans-serif !important;
    font-weight: 500 !important;
    width: 100% !important;
    transition: background 0.2s !important;
}

.stFormSubmitButton > button:hover {
    background: #2471a3 !important;
}

.status-badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

.badge-New       { background: #162d4a; color: #7a9cc4; border: 1px solid #1e3a5f; }
.badge-Applied   { background: #0d3320; color: #5dbb8a; border: 1px solid #1a5c3a; }
.badge-Interview { background: #0d1f40; color: #6b9fdb; border: 1px solid #1a3a6e; }
.badge-Rejected  { background: #3a0d0d; color: #db6b6b; border: 1px solid #6e1a1a; }
.badge-Offer     { background: #3a2a0d; color: #f0c060; border: 1px solid #6e4e1a; }

.streamlit-expanderHeader {
    background: #0f2040 !important;
    border: 1px solid #1e3a5f !important;
    border-radius: 8px !important;
    color: #f0f4ff !important;
    font-family: 'Source Sans 3', sans-serif !important;
}

.streamlit-expanderContent {
    background: #0f2040 !important;
    border: 1px solid #1e3a5f !important;
    border-top: none !important;
    border-radius: 0 0 8px 8px !important;
}

hr { border-color: #1e3a5f !important; margin: 1.5rem 0 !important; }

a { color: #6baed6 !important; text-decoration: none; }
a:hover { text-decoration: underline; }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="header-block">
    <h1>Tech Job Hunter</h1>
    <p>George Alenchery</p>
</div>
""", unsafe_allow_html=True)

# --- Session state ---
if "keyword" not in st.session_state:
    st.session_state["keyword"] = "software"

# --- Search / Scrape ---
st.markdown('<div class="search-section"><div class="section-label">Search & Fetch Listings</div>', unsafe_allow_html=True)

with st.form(key="search_form", clear_on_submit=False):
    col1, col2 = st.columns([4, 1])
    with col1:
        keyword = st.text_input("", value=st.session_state["keyword"],
            placeholder="Enter keyword (e.g. engineer, cloud, data)...",
            label_visibility="collapsed")
    with col2:
        scrape = st.form_submit_button("Fetch Jobs", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

if scrape:
    st.session_state["keyword"] = keyword
    count = scrape_remoteok(keyword=keyword)
    if count == 0:
        st.warning(f"No new jobs found for '{keyword}' — try: engineer, developer, cloud, data.")
    else:
        st.success(f"{count} new jobs added.")
    st.rerun()

# --- Stats ---
all_jobs = get_all_jobs()
total = len(all_jobs)
applied = sum(1 for j in all_jobs if j[9] == "Applied")
interviews = sum(1 for j in all_jobs if j[9] == "Interview")
offers = sum(1 for j in all_jobs if j[9] == "Offer")

st.markdown(f"""
<div class="stat-row">
    <div class="stat-card"><div class="label">Total Listings</div><div class="value">{total}</div></div>
    <div class="stat-card"><div class="label">Applied</div><div class="value">{applied}</div></div>
    <div class="stat-card"><div class="label">Interviews</div><div class="value">{interviews}</div></div>
    <div class="stat-card accent"><div class="label">Offers</div><div class="value">{offers}</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# --- Filter + Jobs ---
st.markdown('<div class="section-label">Your Listings</div>', unsafe_allow_html=True)
status_filter = st.selectbox("", ["All", "New", "Applied", "Interview", "Rejected", "Offer"],
    label_visibility="collapsed")

keyword_filter = st.session_state.get("keyword", "").lower()
jobs = [j for j in get_all_jobs() if not keyword_filter or keyword_filter in (j[1] or "").lower()]

if status_filter != "All":
    jobs = [j for j in jobs if j[9] == status_filter]

st.markdown(f"<p style='color:#4a6a8a; font-size:0.85rem; margin-bottom:1rem;'>{len(jobs)} listings</p>",
    unsafe_allow_html=True)

STATUSES = ["New", "Applied", "Interview", "Rejected", "Offer"]

for job in jobs:
    job_id, title, company, location, url, date_posted, source, date_scraped, status, notes = job
    badge_class = f"badge-{status}" if status in STATUSES else "badge-New"

    with st.expander(f"{title}  ·  {company}"):
        st.markdown(f"""
        <div style='margin-bottom:0.8rem;'>
            <span class='status-badge {badge_class}'>{status}</span>
            <span style='color:#4a6a8a; font-size:0.8rem; margin-left:0.8rem;'>{location} · {source} · {date_posted[:10] if date_posted else "—"}</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"[View listing →]({url})")
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

        c1, c2 = st.columns([1, 2])
        with c1:
            new_status = st.selectbox("Status", STATUSES,
                index=STATUSES.index(status) if status in STATUSES else 0,
                key=f"status_{job_id}")
        with c2:
            new_notes = st.text_area("Notes", value=notes or "", key=f"notes_{job_id}", height=80)

        if st.button("Save changes", key=f"save_{job_id}"):
            update_job_status(job_id, new_status, new_notes)
            st.success("Saved.")
            st.rerun()