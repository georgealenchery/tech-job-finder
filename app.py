import streamlit as st
from database import init_db, get_all_jobs, update_job_status
from webbscraper import scrape_remoteok

init_db()

st.set_page_config(page_title="Tech Job Hunter", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Exo+2:wght@300;400;500;600&display=swap');

/* ===== XBOX 360 NXE THEME ===== */

html, body, [class*="css"] {
    font-family: 'Exo 2', sans-serif;
    background-color: #080D08;
    color: #FFFFFF;
}

.stApp {
    background:
        radial-gradient(ellipse at 25% 15%, rgba(127,186,0,0.10) 0%, transparent 50%),
        radial-gradient(ellipse at 78% 80%, rgba(16,124,16,0.07) 0%, transparent 50%),
        #080D08;
    min-height: 100vh;
}

/* ===== HEADER ===== */
.xbox-header {
    padding: 2rem 0 0 0;
    margin-bottom: 2rem;
}

.xbox-brand {
    display: flex;
    align-items: center;
    gap: 1.2rem;
    margin-bottom: 1.2rem;
}

.xbox-orb {
    width: 58px;
    height: 58px;
    border-radius: 50%;
    background: radial-gradient(circle at 35% 35%, #C8FF50 0%, #7FBA00 40%, #4A8A00 70%, #1A4A00 100%);
    border: 2px solid rgba(173,255,47,0.55);
    box-shadow:
        0 0 28px rgba(127,186,0,0.75),
        0 0 55px rgba(127,186,0,0.30),
        inset 0 0 16px rgba(255,255,255,0.15);
    flex-shrink: 0;
}

.xbox-brand-text h1 {
    font-family: 'Rajdhani', sans-serif;
    font-size: 2.7rem;
    font-weight: 700;
    color: #FFFFFF;
    letter-spacing: 4px;
    text-transform: uppercase;
    line-height: 1;
    text-shadow: 0 0 30px rgba(127,186,0,0.30);
    margin: 0;
    padding: 0;
}

.xbox-brand-text p {
    font-family: 'Exo 2', sans-serif;
    font-size: 0.70rem;
    color: #7FBA00;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin: 0.25rem 0 0 0;
    padding: 0;
}

/* ===== BLADE NAV BAR ===== */
.blade-bar {
    display: flex;
    align-items: stretch;
    border-bottom: 2px solid #7FBA00;
    box-shadow: 0 2px 18px rgba(127,186,0,0.22);
    gap: 0;
}

.blade {
    padding: 0.55rem 2rem;
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.76rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #3A6A3A;
    background: #0D120D;
    border-top: 1px solid #1A3A1A;
    border-right: 1px solid #1A3A1A;
    border-left: 1px solid #1A3A1A;
    cursor: default;
}

.blade.active {
    background: linear-gradient(180deg, #9ACA3C 0%, #5A9A1A 60%, #3D7510 100%);
    color: #000000;
    font-weight: 700;
    border-color: #7FBA00;
    box-shadow: 0 0 14px rgba(127,186,0,0.40);
    position: relative;
    z-index: 1;
}

/* ===== SEARCH SECTION ===== */
.search-section {
    background: linear-gradient(135deg, #111A11 0%, #0A120A 100%);
    border: 1px solid #2A4A2A;
    border-left: 4px solid #7FBA00;
    border-radius: 2px;
    padding: 1.2rem 1.6rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 0 20px rgba(0,0,0,0.5), inset 0 1px 0 rgba(127,186,0,0.08);
}

.section-label {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.66rem;
    text-transform: uppercase;
    letter-spacing: 3px;
    color: #7FBA00;
    margin-bottom: 0.7rem;
    font-weight: 700;
}

/* ===== NXE STAT TILES ===== */
.stat-row {
    display: flex;
    gap: 0.7rem;
    margin-bottom: 2rem;
}

.stat-tile {
    flex: 1;
    background: linear-gradient(145deg, #9ACA3C 0%, #6EAE18 45%, #4A8A08 100%);
    border-radius: 5px;
    padding: 1rem 1.3rem 1.2rem;
    position: relative;
    overflow: hidden;
    box-shadow:
        0 6px 22px rgba(0,0,0,0.60),
        0 0 14px rgba(127,186,0,0.13),
        inset 0 1px 0 rgba(255,255,255,0.22);
}

.stat-tile::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 44%;
    background: linear-gradient(180deg, rgba(255,255,255,0.18) 0%, transparent 100%);
    border-radius: 5px 5px 0 0;
    pointer-events: none;
}

.tile-label {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.60rem;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: rgba(0,0,0,0.62);
    font-weight: 700;
    position: relative;
    z-index: 1;
}

.tile-value {
    font-family: 'Rajdhani', sans-serif;
    font-size: 3.1rem;
    font-weight: 700;
    color: #000000;
    line-height: 1.05;
    margin-top: 0.1rem;
    position: relative;
    z-index: 1;
    text-shadow: 0 2px 4px rgba(0,0,0,0.18);
}

.stat-tile.offers {
    background: linear-gradient(145deg, #FFD700 0%, #FFA500 45%, #CC7000 100%);
}

/* ===== JOB EXPANDERS ===== */
[data-testid="stExpander"] {
    border: none !important;
    margin-bottom: 0.4rem !important;
}

.streamlit-expanderHeader {
    background: linear-gradient(135deg, #121C12 0%, #0A120A 100%) !important;
    border: 1px solid #253525 !important;
    border-left: 3px solid #5A9A1A !important;
    border-radius: 3px !important;
    color: #FFFFFF !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
}

.streamlit-expanderHeader:hover {
    border-left-color: #ADFF2F !important;
    box-shadow: 0 0 14px rgba(127,186,0,0.14) !important;
}

.streamlit-expanderContent {
    background: #0F180F !important;
    border: 1px solid #1A2A1A !important;
    border-top: none !important;
    border-radius: 0 0 3px 3px !important;
}

/* ===== STATUS BADGES ===== */
.status-badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 2px;
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

.badge-New       { background: #0F1A0F; color: #7FBA00; border: 1px solid #2A4A2A; }
.badge-Applied   { background: #1A2A0F; color: #ADFF2F; border: 1px solid #3A6A1A; }
.badge-Interview { background: #0F1A2A; color: #60A0FF; border: 1px solid #1A3A6A; }
.badge-Rejected  { background: #2A0F0F; color: #FF6060; border: 1px solid #6A1A1A; }
.badge-Offer     { background: #2A1F00; color: #FFD700; border: 1px solid #6A5000; }

/* ===== INPUTS ===== */
.stTextInput input {
    background: #111A11 !important;
    border: 1px solid #2A4A2A !important;
    border-radius: 2px !important;
    color: #FFFFFF !important;
    font-family: 'Exo 2', sans-serif !important;
    font-size: 0.95rem !important;
    caret-color: #7FBA00 !important;
}

.stTextInput input:focus {
    border-color: #7FBA00 !important;
    box-shadow: 0 0 0 1px #7FBA00, 0 0 14px rgba(127,186,0,0.22) !important;
}

.stTextInput input::placeholder { color: #2A4A2A !important; }

.stSelectbox > div > div {
    background: #111A11 !important;
    border: 1px solid #2A4A2A !important;
    color: #FFFFFF !important;
    border-radius: 2px !important;
}

.stTextArea textarea {
    background: #111A11 !important;
    border: 1px solid #2A4A2A !important;
    color: #FFFFFF !important;
    font-family: 'Exo 2', sans-serif !important;
    border-radius: 2px !important;
}

/* ===== BUTTONS ===== */
.stButton > button {
    background: linear-gradient(180deg, #92CC3F 0%, #5EA018 100%) !important;
    color: #000000 !important;
    border: none !important;
    border-radius: 3px !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.86rem !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    padding: 0.45rem 1.2rem !important;
    box-shadow: 0 3px 10px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.25) !important;
    transition: all 0.15s !important;
}

.stButton > button:hover {
    background: linear-gradient(180deg, #ADFF2F 0%, #7FBA00 100%) !important;
    box-shadow: 0 0 20px rgba(127,186,0,0.55), 0 3px 10px rgba(0,0,0,0.4) !important;
}

.stFormSubmitButton > button {
    background: linear-gradient(180deg, #92CC3F 0%, #5EA018 100%) !important;
    color: #000000 !important;
    border: none !important;
    border-radius: 3px !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.86rem !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    width: 100% !important;
    box-shadow: 0 3px 10px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.25) !important;
}

.stFormSubmitButton > button:hover {
    background: linear-gradient(180deg, #ADFF2F 0%, #7FBA00 100%) !important;
    box-shadow: 0 0 20px rgba(127,186,0,0.55) !important;
}

/* ===== MISC ===== */
hr { border-color: #1A2A1A !important; margin: 1.5rem 0 !important; }
a { color: #7FBA00 !important; text-decoration: none !important; }
a:hover { color: #ADFF2F !important; }

.stMarkdown p { color: #CCDDCC; }

::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #080D08; }
::-webkit-scrollbar-thumb { background: #2A4A2A; border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: #7FBA00; }

/* Alert / toast overrides */
[data-testid="stAlert"] { border-radius: 2px !important; }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="xbox-header">
    <div class="xbox-brand">
        <div class="xbox-orb"></div>
        <div class="xbox-brand-text">
            <h1>Tech Job Hunter</h1>
            <p>George Alenchery &nbsp;&middot;&nbsp; Remote OK</p>
        </div>
    </div>
    <div class="blade-bar">
        <div class="blade active">My Jobs</div>
        <div class="blade">Marketplace</div>
        <div class="blade">Achievements</div>
        <div class="blade">System</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Session state ---
if "keyword" not in st.session_state:
    st.session_state["keyword"] = "software"

# --- Search / Scrape ---
st.markdown('<div class="search-section"><div class="section-label">Search &amp; Fetch Listings</div>', unsafe_allow_html=True)

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
    <div class="stat-tile">
        <div class="tile-label">Total Listings</div>
        <div class="tile-value">{total}</div>
    </div>
    <div class="stat-tile">
        <div class="tile-label">Applied</div>
        <div class="tile-value">{applied}</div>
    </div>
    <div class="stat-tile">
        <div class="tile-label">Interviews</div>
        <div class="tile-value">{interviews}</div>
    </div>
    <div class="stat-tile offers">
        <div class="tile-label">Offers</div>
        <div class="tile-value">{offers}</div>
    </div>
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

st.markdown(
    f"<p style='font-family:Rajdhani,sans-serif; font-size:0.78rem; color:#3A6A3A; "
    f"letter-spacing:1.5px; text-transform:uppercase; margin-bottom:1rem;'>"
    f"{len(jobs)} listings found</p>",
    unsafe_allow_html=True
)

STATUSES = ["New", "Applied", "Interview", "Rejected", "Offer"]

for job in jobs:
    job_id, title, company, location, url, date_posted, source, date_scraped, status, notes = job
    badge_class = f"badge-{status}" if status in STATUSES else "badge-New"

    with st.expander(f"{title}  ·  {company}"):
        st.markdown(f"""
        <div style='margin-bottom:0.8rem;'>
            <span class='status-badge {badge_class}'>{status}</span>
            <span style='color:#3A6A3A; font-family:"Exo 2",sans-serif; font-size:0.78rem;
                         margin-left:0.8rem; letter-spacing:0.5px;'>
                {location} &nbsp;&middot;&nbsp; {source} &nbsp;&middot;&nbsp; {date_posted[:10] if date_posted else "—"}
            </span>
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
