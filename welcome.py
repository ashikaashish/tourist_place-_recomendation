import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(
    page_title="Tourist Recommendation System",
    page_icon="🌍",
    layout="wide"
)

# ── ALL STYLES + STATIC HTML ─────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;0,700;1,300;1,400&family=Inter:wght@300;400;500;600&display=swap');

*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}

html,body,[data-testid="stAppViewContainer"],[data-testid="stMain"],.main{
  background:#fafaf8 !important;
  font-family:'Inter',sans-serif;
  color:#1a1814;
  overflow-x:hidden;
}

#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stDecoration"],
[data-testid="stSidebar"],[data-testid="collapsedControl"]{display:none !important;}

.block-container{
  padding:0 !important;
  max-width:100% !important;
}

[data-testid="stVerticalBlock"],[data-testid="stVerticalBlockBorderWrapper"]{
  gap:0 !important;
}

/* ══════════════════════════════════
   TICKER
══════════════════════════════════ */
.ticker-wrap{
  position:fixed;top:0;left:0;right:0;z-index:2000;
  background:linear-gradient(90deg,#1a1410,#2d2218,#1a1410);
  height:34px;display:flex;align-items:center;overflow:hidden;
  border-bottom:1px solid rgba(201,169,110,0.3);
}
.ticker-track{
  display:flex;white-space:nowrap;
  animation:tickerScroll 30s linear infinite;
}
.ticker-track:hover{animation-play-state:paused;}
.ticker-item{
  display:inline-flex;align-items:center;gap:0.5rem;
  padding:0 2.2rem;
  font-size:0.7rem;font-weight:500;letter-spacing:0.1em;text-transform:uppercase;
  color:rgba(201,169,110,0.85);
}
.ticker-sep{color:rgba(255,255,255,0.25);}
@keyframes tickerScroll{0%{transform:translateX(0);}100%{transform:translateX(-50%);}}

/* ══════════════════════════════════
   NAVBAR SHELL  (brand only — buttons injected by Streamlit below)
══════════════════════════════════ */
.navbar-shell{
  position:fixed;top:34px;left:0;right:0;z-index:1500;
  height:66px;
  background:rgba(250,250,248,0.93);
  backdrop-filter:blur(20px) saturate(160%);
  border-bottom:1px solid rgba(201,169,110,0.18);
  animation:navDown 0.7s cubic-bezier(0.16,1,0.3,1) 0.1s both;
  pointer-events:none;
}
@keyframes navDown{from{opacity:0;transform:translateY(-100%);}to{opacity:1;transform:translateY(0);}}

.nav-brand{
  position:fixed;top:34px;left:4rem;z-index:1600;
  height:66px;display:flex;align-items:center;gap:0.65rem;
  animation:fadeR 0.7s ease 0.5s both;
  pointer-events:none;
}
@keyframes fadeR{from{opacity:0;transform:translateX(-10px);}to{opacity:1;transform:translateX(0);}}
.nav-logo{font-size:1.55rem;line-height:1;}
.nav-name{
  font-family:'Cormorant Garamond',serif;
  font-size:1.18rem;font-weight:600;color:#1a1814;letter-spacing:0.03em;
}

/* ── Streamlit columns positioned into navbar ── */
[data-testid="stHorizontalBlock"]{
  position:fixed !important;
  top:34px !important;
  right:3rem !important;
  height:66px !important;
  width:auto !important;
  display:flex !important;
  align-items:center !important;
  gap:0.6rem !important;
  z-index:1600 !important;
  background:transparent !important;
  padding:0 !important;
  margin:0 !important;
}

[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]{
  width:auto !important;
  flex:none !important;
  min-width:0 !important;
  padding:0 !important;
}

/* ── ALL THREE nav buttons base ── */
[data-testid="stHorizontalBlock"] div.stButton > button {
  display:inline-flex !important;
  align-items:center !important;
  justify-content:center !important;
  height:38px !important;
  padding:0 1.2rem !important;
  border-radius:8px !important;
  font-family:'Inter',sans-serif !important;
  font-size:0.81rem !important;
  font-weight:500 !important;
  letter-spacing:0.03em !important;
  cursor:pointer !important;
  white-space:nowrap !important;
  transition:all 0.22s cubic-bezier(0.34,1.56,0.64,1) !important;
  box-shadow:none !important;
}

/* Register — ghost */
[data-testid="stHorizontalBlock"] [data-testid="stColumn"]:nth-child(1) div.stButton > button{
  background:rgba(30,20,10,0.05) !important;
  color:#4a3d2a !important;
  border:1.5px solid rgba(60,40,20,0.15) !important;
}
[data-testid="stHorizontalBlock"] [data-testid="stColumn"]:nth-child(1) div.stButton > button:hover{
  background:rgba(30,20,10,0.1) !important;
  border-color:rgba(60,40,20,0.32) !important;
  transform:translateY(-2px) !important;
}

/* Login — outlined gold */
[data-testid="stHorizontalBlock"] [data-testid="stColumn"]:nth-child(2) div.stButton > button{
  background:transparent !important;
  color:#6b5a3e !important;
  border:1.5px solid rgba(201,169,110,0.5) !important;
}
[data-testid="stHorizontalBlock"] [data-testid="stColumn"]:nth-child(2) div.stButton > button:hover{
  background:rgba(201,169,110,0.1) !important;
  border-color:#c9a96e !important;
  transform:translateY(-2px) !important;
}

/* Admin — filled gold */
[data-testid="stHorizontalBlock"] [data-testid="stColumn"]:nth-child(3) div.stButton > button{
  background:linear-gradient(135deg,#c9a96e 0%,#a87828 100%) !important;
  color:#fff !important;
  border:none !important;
  box-shadow:0 2px 12px rgba(180,130,40,0.3) !important;
}
[data-testid="stHorizontalBlock"] [data-testid="stColumn"]:nth-child(3) div.stButton > button:hover{
  background:linear-gradient(135deg,#d4b47a,#c09030) !important;
  transform:translateY(-2px) !important;
  box-shadow:0 6px 20px rgba(180,130,40,0.42) !important;
}

/* ══════════════════════════════════
   MODAL — pure CSS checkbox
══════════════════════════════════ */
#modal-toggle{display:none;}
#modal-toggle:not(:checked) ~ .modal-overlay{
  opacity:1;pointer-events:all;
  animation:overlayIn 0.4s ease both;
}
#modal-toggle:checked ~ .modal-overlay{
  opacity:0;pointer-events:none;
  transition:opacity 0.35s ease;
}
@keyframes overlayIn{from{opacity:0;}to{opacity:1;}}
.modal-overlay{
  position:fixed;inset:0;z-index:3000;
  background:rgba(20,15,8,0.52);
  backdrop-filter:blur(8px);
  display:flex;align-items:center;justify-content:center;
}
.modal-box{
  background:#fff;border-radius:20px;
  padding:2.5rem 2.8rem;max-width:420px;width:90%;
  box-shadow:0 30px 80px rgba(0,0,0,0.18),0 0 0 1px rgba(201,169,110,0.18);
  animation:popIn 0.45s cubic-bezier(0.34,1.56,0.64,1) 0.1s both;
  text-align:center;position:relative;z-index:1;
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
  color:#fff;font-size:0.88rem;font-weight:500;
  cursor:pointer;
  box-shadow:0 4px 14px rgba(180,130,40,0.28);
  transition:all 0.2s ease;user-select:none;
}
.modal-close:hover{background:linear-gradient(135deg,#d4b47a,#c09030);transform:translateY(-2px);}

/* ══════════════════════════════════
   HERO
══════════════════════════════════ */
.hero{
  min-height:100vh;
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  padding:160px 2rem 100px;
  position:relative;overflow:hidden;
  background-image:url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e');
  background-size:cover;
  background-position:center;
  background-repeat:no-repeat;
}
.hero::before{
  content:'';position:absolute;inset:0;
  background:
    radial-gradient(ellipse 65% 55% at 50% -5%,rgba(201,169,110,0.13) 0%,transparent 65%),
    radial-gradient(ellipse 45% 35% at 88% 75%,rgba(160,210,185,0.09) 0%,transparent 60%),
    radial-gradient(ellipse 40% 30% at 5%  80%,rgba(190,180,230,0.07) 0%,transparent 55%);
  animation:auraPulse 9s ease-in-out infinite alternate;pointer-events:none;
}
@keyframes auraPulse{0%{opacity:0.6;transform:scale(1);}100%{opacity:1;transform:scale(1.05);}}
.hero::after{
  content:'';position:absolute;inset:0;
  background-image:radial-gradient(circle,rgba(201,169,110,0.1) 1px,transparent 1px);
  background-size:36px 36px;pointer-events:none;
  mask-image:radial-gradient(ellipse 75% 65% at 50% 50%,black 20%,transparent 80%);
  -webkit-mask-image:radial-gradient(ellipse 75% 65% at 50% 50%,black 20%,transparent 80%);
}
.hero-inner{position:relative;z-index:5;text-align:center;max-width:780px;margin:0 auto;}

.orb-wrap{width:140px;height:140px;position:relative;margin:0 auto 2.2rem;animation:fadeUp 0.8s ease 0.9s both;}
.orb-ring{position:absolute;border-radius:50%;border:1px solid rgba(201,169,110,0.22);top:50%;left:50%;transform:translate(-50%,-50%);}
.orb-ring:nth-child(1){width:162px;height:162px;animation:ringOut 3s ease-in-out infinite;}
.orb-ring:nth-child(2){width:196px;height:196px;animation:ringOut 3s ease-in-out 0.7s infinite;}
@keyframes ringOut{0%,100%{opacity:0.45;transform:translate(-50%,-50%) scale(1);}50%{opacity:0;transform:translate(-50%,-50%) scale(1.12);}}
.orb-core{
  position:absolute;inset:0;border-radius:50%;
  background:radial-gradient(circle at 35% 32%,rgba(255,255,255,0.95) 0%,rgba(245,233,210,0.9) 40%,rgba(201,169,110,0.6) 80%,rgba(160,118,55,0.45) 100%);
  box-shadow:0 0 0 1px rgba(201,169,110,0.3),0 20px 50px rgba(180,135,60,0.25),inset 0 4px 16px rgba(255,255,255,0.6),inset 0 -4px 12px rgba(140,95,30,0.15);
  display:flex;align-items:center;justify-content:center;font-size:3.8rem;
  animation:orbFloat 5.5s ease-in-out infinite;
}
@keyframes orbFloat{0%,100%{transform:translateY(0) rotate(0deg);}50%{transform:translateY(-13px) rotate(4deg);}}

.eyebrow{
  display:inline-flex;align-items:center;gap:0.5rem;
  background:rgba(201,169,110,0.1);border:1px solid rgba(201,169,110,0.32);
  border-radius:100px;padding:0.35rem 1rem;
  font-size:0.7rem;font-weight:600;color:#8a6730;
  letter-spacing:0.14em;text-transform:uppercase;
  margin-bottom:1.6rem;animation:fadeUp 0.8s ease 1.05s both;
}
.edot{width:6px;height:6px;border-radius:50%;background:#c9a96e;animation:edotPulse 2s ease-in-out infinite;}
@keyframes edotPulse{0%,100%{opacity:1;transform:scale(1);}50%{opacity:0.4;transform:scale(0.6);}}

.htitle{
  font-family:'Cormorant Garamond',serif;
  font-size:clamp(3rem,7.5vw,5.8rem);
  font-weight:300;line-height:1.08;color:#1a1814;letter-spacing:-0.02em;
  margin-bottom:0.15rem;animation:titleUp 1s cubic-bezier(0.16,1,0.3,1) 1.2s both;
}
.htitle strong{
  font-weight:700;
  background:linear-gradient(135deg,#c9a96e 0%,#7a5420 55%,#c9a96e 100%);
  background-size:200% auto;
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  animation:shimmer 4s linear 2.5s infinite;
}
@keyframes shimmer{0%{background-position:0% center;}100%{background-position:200% center;}}
@keyframes titleUp{from{opacity:0;transform:translateY(32px);}to{opacity:1;transform:translateY(0);}}

.hsub{
  font-family:'Cormorant Garamond',serif;
  font-size:clamp(1.2rem,2.5vw,1.85rem);font-weight:300;font-style:italic;
  color:#ffffff;margin-bottom:1.5rem;text-shadow:1px 1px 8px rgba(0,0,0,0.8);
  animation:fadeUp 0.8s ease 1.45s both;
}
.hdesc{
  font-size:0.97rem;line-height:1.76;color:#f5f5f5;text-shadow:1px 1px 6px rgba(0,0,0,0.8);
  max-width:490px;margin:0 auto 2.8rem;animation:fadeUp 0.8s ease 1.6s both;
}
.feat-row{display:flex;justify-content:center;align-items:center;flex-wrap:wrap;margin-bottom:3rem;animation:fadeUp 0.8s ease 1.75s both;}
.feat-item{display:flex;align-items:center;gap:0.45rem;padding:0 1.3rem;font-size:0.83rem;font-weight:500;color:#ffffff;text-shadow:1px 1px 6px rgba(0,0,0,0.8);}
.feat-item:not(:last-child){border-right:1px solid rgba(201,169,110,0.28);}
@keyframes fadeUp{from{opacity:0;transform:translateY(18px);}to{opacity:1;transform:translateY(0);}}

/* ══════════════════════════════════
   STATS
══════════════════════════════════ */
.stats-bar{background:#fff;border-top:1px solid rgba(201,169,110,0.18);border-bottom:1px solid rgba(201,169,110,0.18);padding:2.2rem 0;}
.stats-inner{max-width:860px;margin:0 auto;display:flex;justify-content:center;align-items:center;flex-wrap:wrap;padding:0 2rem;}
.stat-item{flex:1;min-width:160px;text-align:center;padding:0.5rem 1.5rem;}
.stat-item:not(:last-child){border-right:1px solid rgba(201,169,110,0.2);}
.stat-n{font-family:'Cormorant Garamond',serif;font-size:2.4rem;font-weight:700;color:#c9a96e;line-height:1;margin-bottom:0.25rem;}
.stat-l{font-size:0.73rem;font-weight:500;color:rgba(80,65,42,0.52);letter-spacing:0.1em;text-transform:uppercase;}

/* ══════════════════════════════════
   FOOTER
══════════════════════════════════ */
.site-footer{
  background:#f2ede4;border-top:1px solid rgba(201,169,110,0.22);
  padding:1.8rem 4rem;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:1rem;
}
.footer-brand{font-family:'Cormorant Garamond',serif;font-size:1rem;font-weight:600;color:#6b5a3e;}
.footer-links{display:flex;gap:1.5rem;}
.footer-link{font-size:0.76rem;color:rgba(107,90,62,0.58);text-decoration:none;transition:color 0.2s;}
.footer-link:hover{color:#c9a96e;}
.footer-copy{font-size:0.73rem;color:rgba(100,80,50,0.45);letter-spacing:0.06em;}

</style>

<!-- TICKER -->
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

<!-- NAVBAR SHELL + BRAND -->
<div class="navbar-shell"></div>
<div class="nav-brand">
  <span class="nav-logo">🌍</span>
  <span class="nav-name">Smart Travel Planner</span>
</div>

<!-- MODAL -->
<input type="checkbox" id="modal-toggle">
<div class="modal-overlay">
  <div class="modal-box">
    <div class="modal-icon">🌍</div>
    <div class="modal-title">Welcome, Explorer!</div>
    <div class="modal-desc">
      Your personalised travel journey starts here.<br>
      Discover destinations crafted around your budget, climate, and travel style.
    </div>
    <label class="modal-close" for="modal-toggle">✨ &nbsp;Let's Explore</label>
  </div>
</div>

<!-- HERO -->
<section class="hero">
  <div class="hero-inner">
    <div class="orb-wrap">
      <div class="orb-ring"></div>
      <div class="orb-ring"></div>
      <div class="orb-core">🌍</div>
    </div>
    <div class="eyebrow"><span class="edot"></span> AI-Powered Travel Intelligence</div>
    <h1 class="htitle">Discover Your<br><strong>Perfect Journey</strong></h1>
    <p class="hsub">Curated destinations, built around you</p>
    <p class="hdesc">Tell us your budget, preferred climate, and travel style — and we'll craft recommendations that feel handpicked by a local expert.</p>
    <div class="feat-row">
      <div class="feat-item">🗺️ Destinations</div>
      <div class="feat-item">💰 Budget Match</div>
      <div class="feat-item">🌤️ Climate Filter</div>
      <div class="feat-item">📅 Trip Planner</div>
    </div>
  </div>
</section>

<!-- STATS -->
<div class="stats-bar">
  <div class="stats-inner">
    <div class="stat-item"><div class="stat-n">120+</div><div class="stat-l">Destinations</div></div>
    <div class="stat-item"><div class="stat-n">50K+</div><div class="stat-l">Happy Travellers</div></div>
    <div class="stat-item"><div class="stat-n">4.9 ★</div><div class="stat-l">Average Rating</div></div>
    <div class="stat-item"><div class="stat-n">24/7</div><div class="stat-l">AI Support</div></div>
  </div>
</div>

<!-- FOOTER -->
<footer class="site-footer">
  <div class="footer-brand">🌍 Smart Travel Planner</div>
  <div class="footer-links">
    <a class="footer-link" href="#">About</a>
    <a class="footer-link" href="#">Privacy</a>
    <a class="footer-link" href="#">Contact</a>
  </div>
  <span class="footer-copy">© 2025 Smart Travel Planner · All rights reserved</span>
</footer>
""", unsafe_allow_html=True)


# ── REAL Streamlit buttons — CSS positions them into the navbar ───────────────
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("📝  Register"):
        st.switch_page("pages/home.py")
with col2:
    if st.button("👤  Login"):
        st.switch_page("pages/login.py")
with col3:
    if st.button("🔐  Admin"):
        st.switch_page("pages/adminreg.py")