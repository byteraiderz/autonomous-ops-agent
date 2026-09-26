import streamlit as st
from agent import app as agent_app
from email_reader import fetch_latest_customer_email


st.set_page_config(page_title="Operations Command Center", page_icon="⚙️", layout="wide")

st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
      .stApp { background: radial-gradient(ellipse at 85% 0%, #eaf1ff 0, transparent 34%), #f5f7fb; color:#182438; font-family:'DM Sans',sans-serif; }
      [data-testid="stHeader"] { background:transparent; }
      [data-testid="stSidebar"] { background:#111c2e; border-right:1px solid rgba(255,255,255,.08); }
      [data-testid="stSidebar"] * { color:#e9eff9; }
      [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color:#9baac0; }
      [data-testid="stSidebar"] hr { border-color:rgba(255,255,255,.12); }
      .block-container { max-width:1250px; padding-top:2.4rem; padding-bottom:3rem; }
      .main-header { padding:.3rem 0 1.6rem; }
      .eyebrow { color:#536de5; font-size:.72rem; font-weight:700; letter-spacing:.14em; text-transform:uppercase; margin-bottom:.55rem; }
      .main-header h1 { color:#152238; font-family:'Manrope',sans-serif; font-size:2.35rem; letter-spacing:-.045em; line-height:1.12; margin:0 0 .45rem; }
      .main-header p { color:#718096; font-size:1rem; margin:0; }
      div[data-testid="stVerticalBlockBorderWrapper"] { background:rgba(255,255,255,.92); border:1px solid #e6ebf3; border-radius:18px; padding:1.15rem 1.3rem; box-shadow:0 10px 30px rgba(26,43,71,.055); }
      h2,h3 { color:#1d2c43; font-family:'Manrope',sans-serif !important; letter-spacing:-.025em; }
      h3 { font-size:1.05rem !important; }
      .stButton button[kind="primary"] { background:linear-gradient(100deg,#4e63d8,#6879ed); border:0; border-radius:11px; min-height:3.2rem; font-size:1rem; font-weight:700; box-shadow:0 5px 12px rgba(78,99,216,.2); transition:transform .15s,box-shadow .15s; }
      .stButton button[kind="primary"]:hover { background:linear-gradient(100deg,#4358cb,#5d70e4); box-shadow:0 8px 18px rgba(78,99,216,.26); transform:translateY(-1px); }
      .status-row { display:flex; align-items:center; gap:.55rem; margin-top:.25rem; }
      .status-dot { width:8px; height:8px; border-radius:50%; background:#3bd18c; box-shadow:0 0 0 4px rgba(59,209,140,.13); }
      .status-pill { display:inline-flex; align-items:center; gap:.5rem; background:rgba(44,190,125,.12); color:#80e0b0; border:1px solid rgba(97,220,160,.2); border-radius:999px; padding:.4rem .72rem; font-size:.82rem; font-weight:700; }
      .decision-badge { display:inline-block; background:#eef1ff; border:1px solid #dce2ff; border-radius:10px; color:#4d5fc7; font-family:'Manrope',sans-serif; font-size:1.15rem; font-weight:800; letter-spacing:.02em; padding:.6rem .85rem; }
      [data-testid="stAlert"] { border-radius:12px; }
      @media(max-width:700px) { .block-container{padding:1.4rem 1rem 2rem;} .main-header h1{font-size:1.8rem;} }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.title("Operations")
    st.caption("COMMAND CENTER  /  AI OPERATOR")
    st.divider()
    st.markdown("**SYSTEM STATUS**")
    st.markdown(
        '<div class="status-row"><span class="status-dot"></span><span class="status-pill">Online</span></div>',
        unsafe_allow_html=True,
    )
    st.divider()
    st.caption("Track 6 · Human-in-the-Loop")

st.markdown(
    '<div class="main-header"><div class="eyebrow">Customer operations · Live workspace</div>'
    '<h1>Operations Command Center</h1>'
    '<p>Fetch a new customer email and let the operations agent handle the next step.</p></div>',
    unsafe_allow_html=True,
)

with st.container(border=True):
    st.subheader("Live Gmail Inbox")
    st.write("Fetch the latest unread customer email and send it to the agent.")
    fetch_clicked = st.button("Fetch Live Customer Email", type="primary", use_container_width=True)

if fetch_clicked:
    try:
        with st.spinner("Connecting to Gmail and fetching the latest unread email…"):
            fetched_data = fetch_latest_customer_email()

        if fetched_data is None:
            st.info("No unread emails found in the inbox.")
        else:
            live_email = fetched_data["body"]
            with st.container(border=True):
                st.subheader("Fetched Customer Email")
                st.text(live_email)

            with st.spinner("The agent is analyzing the email and preparing actions…"):
                result = agent_app.invoke(
                    {
                        "email_content": live_email,
                        "customer_email": fetched_data["sender"],
                        "decision": "",
                        "issue_summary": "",
                        "refund_amount": "",
                        "missing_info": [],
                        "action_result": "",
                    }
                )

            st.success("Workflow complete")
            reasoning_col, actions_col = st.columns(2, gap="large")
            with reasoning_col:
                with st.container(border=True):
                    st.subheader("Agent Reasoning")
                    st.caption("Routing decision")
                    decision = result.get("decision", "UNKNOWN")
                    if decision == "REFUND":
                        st.markdown("Refund / Replacement request accepted waiting for approval from the team")
                    else:
                        st.markdown(f'<span class="decision-badge">{decision}</span>', unsafe_allow_html=True)
            with actions_col:
                with st.container(border=True):
                    st.subheader("Actions Executed")
                    st.markdown(result.get("action_result", "No actions recorded."))
    except Exception as error:
        st.error(f"Could not complete the email workflow: {error}")