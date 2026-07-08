import streamlit as st

st.set_page_config(
    page_title="Tourist Recommendation System",
    page_icon="🌍",
    layout="wide"
)

# ── 1. ALL CSS (ticker, navbar, hero, modal, stats, footer) ──────────────────
# Using st.html, not st.markdown: st.markdown runs content through a
# markdown-to-HTML pipeline first, which is unreliable for large blocks of
# raw HTML/CSS (tags can get mangled or dumped as literal text after a
# certain point). st.html renders raw HTML directly into the page, no
# markdown parsing, no iframe.
st.html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;0,700;1,300;1,400&family=Inter:wght@300;400;500;600&display=swap');

*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}

html,body,[data-testid="stAppViewContainer"],[data-testid="stMain"],.main{
  background:#fafaf8 !important;
  font-family:'Inter',sans-serif;
  color:#1a1814;
}

#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stDecoration"],
[data-testid="stSidebar"],[data-testid="collapsedControl"]{display:none !important;}

.block-container{padding:0 !important;max-width:100% !important;}
[data-testid="stVerticalBlock"],[data-testid="stVerticalBlockBorderWrapper"]{gap:0 !important;}

/* push page content down so it isn't hidden under the fixed ticker+navbar */
.page-spacer{height:100px;}

/* TICKER */
.ticker-wrap{
  position:fixed;top:0;left:0;right:0;z-index:2000;
  background:linear-gradient(90deg,#1a1410,#2d2218,#1a1410);
  height:34px;display:flex;align-items:center;overflow:hidden;
  border-bottom:1px solid rgba(201,169,110,0.3);
}
.ticker-track{display:flex;white-space:nowrap;animation:tickerScroll 30s linear infinite;}
.ticker-track:hover{animation-play-state:paused;}
.ticker-item{
  display:inline-flex;align-items:center;gap:0.5rem;padding:0 2.2rem;
  font-size:0.7rem;font-weight:500;letter-spacing:0.1em;text-transform:uppercase;
  color:rgba(201,169,110,0.85);
}
.ticker-sep{color:rgba(255,255,255,0.25);}
@keyframes tickerScroll{0%{transform:translateX(0);}100%{transform:translateX(-50%);}}

/* NAVBAR shell + brand (fixed, sits below ticker) */
.navbar-shell{
  position:fixed;top:34px;left:0;right:0;z-index:1500;height:66px;
  background:rgba(250,250,248,0.96);
  backdrop-filter:blur(20px) saturate(160%);
  border-bottom:1px solid rgba(201,169,110,0.18);
}
.nav-brand{
  position:fixed;top:34px;left:4rem;z-index:1600;height:66px;
  display:flex;align-items:center;gap:0.65rem;
}
.nav-logo{font-size:1.55rem;line-height:1;}
.nav-name{
  font-family:'Cormorant Garamond',serif;
  font-size:1.18rem;font-weight:600;color:#1a1814;letter-spacing:0.03em;
}

/* Streamlit nav buttons floated into navbar.
   This page has only one st.columns() call, so targeting
   stHorizontalBlock directly (no JS, no class tag) is safe here. */
div[data-testid="stHorizontalBlock"]{
  position:fixed !important;top:34px !important;right:3rem !important;
  height:66px !important;width:auto !important;display:flex !important;
  align-items:center !important;gap:0.6rem !important;z-index:1600 !important;
  background:transparent !important;padding:0 !important;margin:0 !important;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]{
  width:auto !important;flex:none !important;min-width:0 !important;padding:0 !important;
}
div[data-testid="stHorizontalBlock"] div.stButton > button{
  display:inline-flex !important;align-items:center !important;justify-content:center !important;
  height:38px !important;padding:0 1.2rem !important;border-radius:8px !important;
  font-family:'Inter',sans-serif !important;font-size:0.81rem !important;font-weight:500 !important;
  cursor:pointer !important;white-space:nowrap !important;
  transition:all 0.22s ease !important;box-shadow:none !important;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(1) div.stButton > button{
  background:rgba(30,20,10,0.05) !important;color:#4a3d2a !important;
  border:1.5px solid rgba(60,40,20,0.15) !important;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(1) div.stButton > button:hover{
  background:rgba(30,20,10,0.1) !important;transform:translateY(-2px) !important;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(2) div.stButton > button{
  background:transparent !important;color:#6b5a3e !important;
  border:1.5px solid rgba(201,169,110,0.5) !important;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(2) div.stButton > button:hover{
  background:rgba(201,169,110,0.1) !important;transform:translateY(-2px) !important;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(3) div.stButton > button{
  background:linear-gradient(135deg,#c9a96e,#a87828) !important;
  color:#fff !important;border:none !important;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(3) div.stButton > button:hover{
  transform:translateY(-2px) !important;
}

/* ── MODAL ── */
#modal-toggle{display:none;}
#modal-toggle:not(:checked) ~ .modal-overlay{
  opacity:1;pointer-events:all;animation:overlayIn 0.4s ease both;
}
#modal-toggle:checked ~ .modal-overlay{
  opacity:0;pointer-events:none;transition:opacity 0.35s ease;
}
@keyframes overlayIn{from{opacity:0;}to{opacity:1;}}
.modal-overlay{
  position:fixed;inset:0;z-index:3000;
  background:rgba(20,15,8,0.55);backdrop-filter:blur(8px);
  display:flex;align-items:center;justify-content:center;
}
.modal-box{
  background:#fff;border-radius:20px;
  padding:2.5rem 2.8rem;max-width:420px;width:90%;
  box-shadow:0 30px 80px rgba(0,0,0,0.18),0 0 0 1px rgba(201,169,110,0.18);
  animation:popIn 0.45s cubic-bezier(0.34,1.56,0.64,1) 0.1s both;
  text-align:center;
}
@keyframes popIn{from{opacity:0;transform:scale(0.8) translateY(24px);}to{opacity:1;transform:scale(1) translateY(0);}}
.modal-icon{font-size:3rem;margin-bottom:1rem;}
.modal-title{
  font-family:'Cormorant Garamond',serif;font-size:1.85rem;font-weight:700;
  color:#1a1814;margin-bottom:0.5rem;
}
.modal-desc{font-size:0.87rem;color:#7a6a52;line-height:1.65;margin-bottom:1.6rem;}
.modal-close{
  display:inline-flex;align-items:center;justify-content:center;gap:0.4rem;
  padding:0.65rem 2.2rem;border-radius:10px;
  background:linear-gradient(135deg,#c9a96e,#a87828);
  color:#fff;font-size:0.88rem;font-weight:500;cursor:pointer;
  box-shadow:0 4px 14px rgba(180,130,40,0.28);
  transition:all 0.2s ease;user-select:none;border:none;
}
.modal-close:hover{transform:translateY(-2px);}

/* ── SPLIT HERO ── */
.hero-split{
  display:flex;
  min-height:80vh;
}

/* LEFT panel */
.hero-left{
  width:52%;
  background:#fafaf8;
  display:flex;flex-direction:column;justify-content:center;
  padding:4rem 3.5rem 4rem 4.5rem;
  position:relative;overflow:hidden;
}
.hero-left::before{
  content:'';position:absolute;inset:0;pointer-events:none;
  background-image:radial-gradient(circle,rgba(201,169,110,0.1) 1px,transparent 1px);
  background-size:28px 28px;
}
.hero-left::after{
  content:'';position:absolute;left:0;top:20%;bottom:20%;width:3px;
  background:linear-gradient(180deg,transparent,#c9a96e,transparent);
  border-radius:0 2px 2px 0;
}
.hero-left-inner{position:relative;z-index:2;max-width:500px;}

.split-eyebrow{
  display:inline-flex;align-items:center;gap:0.5rem;
  background:rgba(201,169,110,0.1);border:1px solid rgba(201,169,110,0.32);
  border-radius:100px;padding:0.35rem 1rem;
  font-size:0.7rem;font-weight:600;color:#8a6730;
  letter-spacing:0.14em;text-transform:uppercase;
  margin-bottom:1.6rem;
}
.edot{
  width:6px;height:6px;border-radius:50%;background:#c9a96e;
  display:inline-block;
  animation:edotPulse 2s ease-in-out infinite;
}
@keyframes edotPulse{0%,100%{opacity:1;transform:scale(1);}50%{opacity:0.4;transform:scale(0.6);}}

.split-title{
  font-family:'Cormorant Garamond',serif;
  font-size:clamp(2.6rem,4vw,4.4rem);
  font-weight:300;line-height:1.06;color:#1a1814;
  letter-spacing:-0.02em;margin-bottom:0.9rem;
}
.split-title strong{
  font-weight:700;display:block;
  background:linear-gradient(135deg,#c9a96e 0%,#7a5420 50%,#c9a96e 100%);
  background-size:200% auto;
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  animation:shimmer 4s linear 1s infinite;
}
@keyframes shimmer{0%{background-position:0% center;}100%{background-position:200% center;}}

.split-sub{
  font-family:'Cormorant Garamond',serif;
  font-size:1.22rem;font-weight:300;font-style:italic;
  color:#6b5a3e;margin-bottom:0.8rem;
}
.split-desc{
  font-size:0.92rem;line-height:1.78;color:#5a4d3a;margin-bottom:1.8rem;
}

.split-cta-note{
  display:flex;align-items:center;gap:0.6rem;
  background:rgba(201,169,110,0.08);border:1px solid rgba(201,169,110,0.28);
  border-radius:10px;padding:0.7rem 1rem;margin-bottom:1.8rem;
  font-size:0.82rem;color:#7a6244;
}

.split-feat-row{display:flex;flex-wrap:wrap;gap:0.55rem;margin-bottom:2rem;}
.split-feat{
  display:inline-flex;align-items:center;gap:0.4rem;
  background:#fff;border:1px solid rgba(201,169,110,0.25);
  border-radius:100px;padding:0.3rem 0.85rem;
  font-size:0.74rem;font-weight:500;color:#6b5a3e;
  box-shadow:0 1px 4px rgba(0,0,0,0.04);
}

.trust-row{display:flex;align-items:center;gap:1.1rem;}
.trust-avatars{display:flex;}
.trust-avatar{
  width:32px;height:32px;border-radius:50%;border:2px solid #fff;
  background:linear-gradient(135deg,#c9a96e,#8a5f20);
  margin-left:-9px;display:flex;align-items:center;justify-content:center;
  font-size:0.65rem;font-weight:600;color:#fff;
}
.trust-avatar:first-child{margin-left:0;}
.trust-text{font-size:0.76rem;color:#7a6a52;line-height:1.45;}
.trust-text strong{color:#1a1814;font-weight:600;}

/* RIGHT panel */
.hero-right{
  width:48%;position:relative;overflow:hidden;min-height:500px;
  border-radius:0;
}
.hero-photo{
  position:absolute;inset:0;
  background:url('https://images.unsplash.com/photo-1524492412937-b28074a5d7da?w=1200&q=85') center/cover no-repeat;
}
.hero-photo::before{
  content:'';position:absolute;inset:0;
  background:linear-gradient(90deg,rgba(250,250,248,0.25) 0%,transparent 25%),
             linear-gradient(0deg,rgba(10,8,5,0.35) 0%,transparent 50%);
}

.dest-badge{
  position:absolute;bottom:2rem;left:1.8rem;
  background:rgba(255,255,255,0.93);backdrop-filter:blur(12px);
  border-radius:14px;padding:0.85rem 1.1rem;
  box-shadow:0 8px 30px rgba(0,0,0,0.15);
  border:1px solid rgba(201,169,110,0.22);min-width:190px;
}
.dest-badge-loc{
  font-size:0.65rem;font-weight:600;color:#c9a96e;
  letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.2rem;
}
.dest-badge-name{
  font-family:'Cormorant Garamond',serif;font-size:1.1rem;
  font-weight:600;color:#1a1814;margin-bottom:0.3rem;
}
.dest-badge-row{display:flex;align-items:center;gap:0.5rem;}
.dest-badge-tag{
  font-size:0.65rem;font-weight:500;padding:0.15rem 0.5rem;border-radius:100px;
  background:rgba(201,169,110,0.12);color:#7a5820;border:1px solid rgba(201,169,110,0.28);
}
.dest-badge-rating{font-size:0.73rem;font-weight:600;color:#1a1814;margin-left:auto;}

.photo-pill{
  position:absolute;top:1.8rem;right:1.8rem;
  background:rgba(255,255,255,0.9);backdrop-filter:blur(10px);
  border-radius:100px;padding:0.42rem 0.9rem;
  font-size:0.7rem;font-weight:600;color:#6b5a3e;
  border:1px solid rgba(201,169,110,0.25);
  box-shadow:0 4px 16px rgba(0,0,0,0.1);
  display:flex;align-items:center;gap:0.4rem;
}
.photo-dot{
  width:7px;height:7px;border-radius:50%;background:#c9a96e;
  display:inline-block;
  animation:edotPulse 2s ease-in-out infinite;
}

/* ── STATS ── */
.stats-bar{
  background:#fff;
  border-top:1px solid rgba(201,169,110,0.18);
  border-bottom:1px solid rgba(201,169,110,0.18);
  padding:2.2rem 0;
}
.stats-inner{
  max-width:860px;margin:0 auto;
  display:flex;justify-content:center;align-items:center;flex-wrap:wrap;padding:0 2rem;
}
.stat-item{flex:1;min-width:160px;text-align:center;padding:0.5rem 1.5rem;}
.stat-item+.stat-item{border-left:1px solid rgba(201,169,110,0.2);}
.stat-n{
  font-family:'Cormorant Garamond',serif;font-size:2.4rem;font-weight:700;
  color:#c9a96e;line-height:1;margin-bottom:0.25rem;
}
.stat-l{
  font-size:0.73rem;font-weight:500;color:rgba(80,65,42,0.55);
  letter-spacing:0.1em;text-transform:uppercase;
}

/* ── FOOTER ── */
.site-footer{
  background:#f2ede4;border-top:1px solid rgba(201,169,110,0.22);
  padding:1.8rem 4rem;display:flex;align-items:center;
  justify-content:space-between;flex-wrap:wrap;gap:1rem;
}
.footer-brand{font-family:'Cormorant Garamond',serif;font-size:1rem;font-weight:600;color:#6b5a3e;}
.footer-links{display:flex;gap:1.5rem;}
.footer-link{font-size:0.76rem;color:rgba(107,90,62,0.58);text-decoration:none;}
.footer-link:hover{color:#c9a96e;}
.footer-copy{font-size:0.73rem;color:rgba(100,80,50,0.45);letter-spacing:0.06em;}

/* responsive: stack hero on narrow screens */
@media (max-width: 900px){
  .hero-split{flex-direction:column;}
  .hero-left,.hero-right{width:100%;}
  .hero-right{min-height:320px;}
  div[data-testid="stHorizontalBlock"]{right:1rem !important;}
  .nav-brand{left:1.2rem !important;}
}
</style>
""")


# ── 2. TICKER + NAVBAR SHELL + BRAND (fixed, always on top) ──────────────────
st.html("""
<div class="ticker-wrap">
  <div class="ticker-track">
    <span class="ticker-item">🗺️ 120+ Destinations <span class="ticker-sep">·</span></span>
    <span class="ticker-item">💰 Budget-Smart Planning <span class="ticker-sep">·</span></span>
    <span class="ticker-item">🌤️ Climate Matched Travel <span class="ticker-sep">·</span></span>
    <span class="ticker-item">📅 Personalised Itineraries <span class="ticker-sep">·</span></span>
    <span class="ticker-item">⭐ 4.9 Star Rated <span class="ticker-sep">·</span></span>
    <span class="ticker-item">✈️ 50,000+ Happy Travellers <span class="ticker-sep">·</span></span>
    <span class="ticker-item">🏨 Curated Stays <span class="ticker-sep">·</span></span>
    <span class="ticker-item">🌍 AI-Powered Recommendations <span class="ticker-sep">·</span></span>
    <span class="ticker-item">🗺️ 120+ Destinations <span class="ticker-sep">·</span></span>
    <span class="ticker-item">💰 Budget-Smart Planning <span class="ticker-sep">·</span></span>
    <span class="ticker-item">🌤️ Climate Matched Travel <span class="ticker-sep">·</span></span>
    <span class="ticker-item">📅 Personalised Itineraries <span class="ticker-sep">·</span></span>
    <span class="ticker-item">⭐ 4.9 Star Rated <span class="ticker-sep">·</span></span>
    <span class="ticker-item">✈️ 50,000+ Happy Travellers <span class="ticker-sep">·</span></span>
    <span class="ticker-item">🏨 Curated Stays <span class="ticker-sep">·</span></span>
    <span class="ticker-item">🌍 AI-Powered Recommendations <span class="ticker-sep">·</span></span>
  </div>
</div>
<div class="navbar-shell"></div>
<div class="nav-brand">
  <span class="nav-logo">🌍</span>
  <span class="nav-name">Smart Travel Planner</span>
</div>
""")


# ── 3. NAV BUTTONS (real Streamlit) ───────────────────────────────────────────
# This page has exactly one st.columns() call, so it's safe to target
# div[data-testid="stHorizontalBlock"] directly in CSS (see step 1) without
# needing a JS-based class tag. If you ever add another st.columns() block
# to this same page, give this one a wrapper class instead (e.g. via
# st.container) so the CSS doesn't accidentally target the wrong block.
nav_col1, nav_col2, nav_col3 = st.columns([1, 1, 1])
with nav_col1:
    if st.button("📝  Register", key="nav_register"):
        st.switch_page("pages/home.py")
with nav_col2:
    if st.button("👤  Login", key="nav_login"):
        st.switch_page("pages/login.py")
with nav_col3:
    if st.button("🔐  Admin", key="nav_admin"):
        st.switch_page("pages/adminreg.py")


# ── 4. PAGE SPACER (clears the fixed ticker + navbar) ────────────────────────
st.html('<div class="page-spacer"></div>')


# ── 5. MAIN PAGE BODY — raw HTML via st.html, no markdown parsing, no iframe ──
st.html("""
<input type="checkbox" id="modal-toggle">
<div class="modal-overlay">
  <div class="modal-box">
    <div class="modal-icon">🌍</div>
    <div class="modal-title">Welcome, Explorer!</div>
    <div class="modal-desc">
      Your personalised travel journey starts here.<br>
      Discover destinations crafted around your budget, climate, and travel style.
    </div>
    <label class="modal-close" for="modal-toggle">✨  Let's Explore</label>
  </div>
</div>

<section class="hero-split">

  <div class="hero-left">
    <div class="hero-left-inner">

      <div class="split-eyebrow">
        <span class="edot"></span>&nbsp; AI-Powered Travel Intelligence
      </div>

      <h1 class="split-title">
        Discover Your<br>
        <strong>Perfect Journey</strong>
      </h1>

      <p class="split-sub">Curated destinations, built around you</p>
      <p class="split-desc">
        Tell us your budget, preferred climate, and travel style —
        we'll craft recommendations that feel handpicked by a local expert.
      </p>

      <div class="split-cta-note">
        👆&nbsp; Use the <strong>Register</strong> or <strong>Login</strong> buttons at the top right to get started
      </div>

      <div class="split-feat-row">
        <span class="split-feat">🗺️ Destinations</span>
        <span class="split-feat">💰 Budget Match</span>
        <span class="split-feat">🌤️ Climate Filter</span>
        <span class="split-feat">📅 Trip Planner</span>
        <span class="split-feat">🤖 ML Powered</span>
      </div>

      <div class="trust-row">
        <div class="trust-avatars">
          <div class="trust-avatar">AR</div>
          <div class="trust-avatar">PK</div>
          <div class="trust-avatar">SM</div>
          <div class="trust-avatar">+</div>
        </div>
        <div class="trust-text">
          <strong>50,000+ travellers</strong> found their perfect trip<br>
          ⭐⭐⭐⭐⭐&nbsp; 4.9 average rating
        </div>
      </div>

    </div>
  </div>

  <div class="hero-right">
    <div class="hero-photo"></div>
    <div class="dest-badge">
      <div class="dest-badge-loc">📍 Featured Destination</div>
      <div class="dest-badge-name">Taj Mahal, Agra</div>
      <div class="dest-badge-row">
        <span class="dest-badge-tag">🌤️ Moderate</span>
        <span class="dest-badge-tag">💰 Medium</span>
        <span class="dest-badge-rating">⭐ 4.9</span>
      </div>
    </div>
    <div class="photo-pill">
      <span class="photo-dot"></span>&nbsp; 120+ destinations available
    </div>
  </div>

</section>

<div class="stats-bar">
  <div class="stats-inner">
    <div class="stat-item"><div class="stat-n">120+</div><div class="stat-l">Destinations</div></div>
    <div class="stat-item"><div class="stat-n">50K+</div><div class="stat-l">Happy Travellers</div></div>
    <div class="stat-item"><div class="stat-n">4.9 ★</div><div class="stat-l">Average Rating</div></div>
    <div class="stat-item"><div class="stat-n">24/7</div><div class="stat-l">AI Support</div></div>
  </div>
</div>

<footer class="site-footer">
  <div class="footer-brand">🌍 Smart Travel Planner</div>
  <div class="footer-links">
    <a class="footer-link" href="#">About</a>
    <a class="footer-link" href="#">Privacy</a>
    <a class="footer-link" href="#">Contact</a>
  </div>
  <span class="footer-copy">© 2025 Smart Travel Planner · All rights reserved</span>
</footer>
""")