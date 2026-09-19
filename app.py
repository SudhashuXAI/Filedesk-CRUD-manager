"""
File Desk - a CRUD file manager with a Streamlit UI.
Run:  pip install streamlit  &&  streamlit run app.py
All files live inside a local ./workspace folder, so nothing outside it is touched.
"""
import html
import time
from datetime import datetime
from pathlib import Path

import streamlit as st

WORKSPACE = Path("workspace")
WORKSPACE.mkdir(exist_ok=True)

st.set_page_config(page_title="File Desk", page_icon="🗂️", layout="wide")


# ------------------------------------------------------------------ helpers
def block(s: str) -> str:
    """Strip indentation/blank lines so Markdown never mistakes HTML for a code block."""
    return "\n".join(line.strip() for line in s.splitlines() if line.strip())


def safe_path(name: str):
    """Keep every file inside the workspace (drops any folder parts of the name)."""
    name = Path(name.strip()).name
    return WORKSPACE / name if name else None


def list_files():
    files = [p for p in WORKSPACE.iterdir() if p.is_file()]
    return sorted(files, key=lambda p: p.stat().st_mtime, reverse=True)


def fmt_size(n: int) -> str:
    for unit in ("B", "KB", "MB"):
        if n < 1024:
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} GB"


def ago(ts: float) -> str:
    s = int(time.time() - ts)
    if s < 60:
        return "just now"
    if s < 3600:
        return f"{s // 60} min ago"
    if s < 86400:
        return f"{s // 3600} h ago"
    return f"{s // 86400} d ago"


def log(action: str, text: str):
    st.session_state.setdefault("log", []).insert(
        0, (datetime.now().strftime("%H:%M"), action, text)
    )


def flash(msg: str, icon: str = "✅"):
    st.session_state["flash"] = (msg, icon)


def empty_state(text: str):
    st.markdown(f'<div class="empty">{text}</div>', unsafe_allow_html=True)


# ------------------------------------------------------------------ styling
st.markdown(
    block(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=DM+Sans:wght@400;500;700&display=swap');
:root{--bg:#0D1526;--panel:#141F36;--line:#263553;--text:#E8EEF9;--muted:#8C9BB8;
--create:#3DDC97;--read:#5B9DFF;--update:#FFB547;--delete:#FF5C7A;}
html,body,.stApp,[data-testid="stAppViewContainer"]{background:var(--bg)!important;color:var(--text);font-family:'DM Sans',sans-serif;}
[data-testid="stHeader"]{background:transparent;}
#MainMenu,footer{visibility:hidden;}
.block-container{max-width:1080px;padding-top:2.2rem;padding-bottom:4rem;}
h1,h2,h3{font-family:'Bricolage Grotesque',sans-serif!important;color:var(--text)!important;}
label,.stMarkdown p,[data-testid="stWidgetLabel"] p{color:var(--muted)!important;font-size:.92rem;}
.hero{padding:1rem 0 .4rem;}
.live{display:inline-flex;align-items:center;gap:.55rem;color:var(--muted);font-size:.9rem;margin-bottom:1.1rem;}
.dot{width:9px;height:9px;border-radius:50%;background:var(--create);box-shadow:0 0 0 0 rgba(61,220,151,.6);animation:pulse 2s infinite;}
@keyframes pulse{70%{box-shadow:0 0 0 10px rgba(61,220,151,0);}100%{box-shadow:0 0 0 0 rgba(61,220,151,0);}}
.hero h1{font-size:clamp(2.6rem,7vw,4.6rem);line-height:1.15;font-weight:800;margin:0;letter-spacing:-.03em;}
.window{display:inline-block;height:1.15em;overflow:hidden;vertical-align:bottom;}
.verbs{display:block;animation:roll 9s cubic-bezier(.7,0,.2,1) infinite;}
.v{display:block;height:1.15em;}
.v.c{color:var(--create);}.v.r{color:var(--read);}.v.u{color:var(--update);}.v.d{color:var(--delete);}
@keyframes roll{0%,20%{transform:translateY(0);}25%,45%{transform:translateY(-1.15em);}
50%,70%{transform:translateY(-2.3em);}75%,95%{transform:translateY(-3.45em);}100%{transform:translateY(-4.6em);}}
.sub{color:var(--muted);font-size:1.05rem;max-width:34rem;margin:1rem 0 0;line-height:1.55;}
.by{margin-top:1.2rem;display:inline-block;padding:.35rem .9rem;border:1px solid var(--line);border-radius:999px;color:var(--muted);font-size:.9rem;}
.by b{color:var(--text);font-weight:700;}
.strip{display:flex;gap:2.8rem;flex-wrap:wrap;margin:2rem 0 1.6rem;padding:1.1rem 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);}
.stat b{display:block;font-family:'Bricolage Grotesque',sans-serif;font-size:2rem;font-weight:700;line-height:1;}
.stat span{color:var(--muted);font-size:.85rem;}
.stTabs [data-baseweb="tab-list"]{gap:.4rem;border-bottom:1px solid var(--line);}
.stTabs [data-baseweb="tab"]{color:var(--muted);font-weight:500;padding:.6rem 1rem;background:transparent;}
.stTabs [aria-selected="true"]{color:var(--text)!important;}
.stTabs [data-baseweb="tab-highlight"]{background:var(--read);}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:.9rem;margin-top:.6rem;}
.fcard{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:1rem;transition:transform .18s,border-color .18s;}
.fcard:hover{transform:translateY(-3px);border-color:var(--read);}
.ext{display:inline-block;font-size:.72rem;font-weight:700;letter-spacing:.04em;color:var(--read);background:rgba(91,157,255,.14);border-radius:6px;padding:.15rem .5rem;}
.fname{font-weight:700;margin:.8rem 0 .2rem;word-break:break-all;}
.fmeta{color:var(--muted);font-size:.82rem;}
.empty{border:1px dashed var(--line);border-radius:14px;padding:2rem;color:var(--muted);text-align:center;margin-top:.6rem;}
.act{display:flex;align-items:center;gap:.6rem;padding:.55rem 0;border-bottom:1px solid var(--line);font-size:.9rem;}
.act time{margin-left:auto;color:var(--muted);font-size:.78rem;}
.pip{width:8px;height:8px;border-radius:50%;flex:none;}
.pip.create{background:var(--create);}.pip.read{background:var(--read);}.pip.update{background:var(--update);}.pip.delete{background:var(--delete);}
.stTextInput input,.stTextArea textarea,[data-baseweb="select"]>div{background:var(--panel)!important;border:1px solid var(--line)!important;color:var(--text)!important;border-radius:10px!important;}
.stButton>button,.stFormSubmitButton>button,.stDownloadButton>button{border-radius:10px;font-weight:700;border:1px solid var(--line);background:var(--panel);color:var(--text);transition:transform .12s;}
.stButton>button:hover,.stFormSubmitButton>button:hover{transform:translateY(-1px);border-color:var(--read);color:var(--text);}
.stButton>button[kind="primary"],.stFormSubmitButton>button[kind="primary"]{background:var(--read);border-color:var(--read);color:#0A1222;}
[data-testid="stForm"]{border:1px solid var(--line);border-radius:14px;background:transparent;}
[data-testid="stCode"] pre{background:var(--panel)!important;border:1px solid var(--line);border-radius:12px;}
.foot{color:var(--muted);font-size:.85rem;margin-top:3rem;text-align:center;}
@media (prefers-reduced-motion:reduce){.verbs,.dot{animation:none;}.fcard{transition:none;}}
</style>
"""
    ),
    unsafe_allow_html=True,
)

if "flash" in st.session_state:
    msg, icon = st.session_state.pop("flash")
    st.toast(msg, icon=icon)

# ------------------------------------------------------------------ hero
files = list_files()
total = sum(p.stat().st_size for p in files)
actions = len(st.session_state.get("log", []))

st.markdown(
    block(
        f"""
<div class="hero">
<div class="live"><span class="dot"></span>Workspace is live</div>
<h1><span class="window"><span class="verbs">
<span class="v c">Create</span><span class="v r">Read</span><span class="v u">Update</span><span class="v d">Delete</span><span class="v c">Create</span>
</span></span> files.<br>No terminal needed.</h1>
<p class="sub">A file manager built on Python's pathlib. Every button below runs a real file operation in the workspace folder.</p>
<div class="by">Made by <b>Sudhanshu Tiwari</b></div>
</div>
<div class="strip">
<div class="stat"><b>{len(files)}</b><span>files in workspace</span></div>
<div class="stat"><b>{fmt_size(total)}</b><span>total size</span></div>
<div class="stat"><b>{actions}</b><span>actions this session</span></div>
</div>
"""
    ),
    unsafe_allow_html=True,
)

tab_files, tab_create, tab_read, tab_update, tab_delete = st.tabs(
    ["Files", "Create", "Read", "Update", "Delete"]
)

# ------------------------------------------------------------------ Files
with tab_files:
    left, right = st.columns([3, 1.3], gap="large")
    with left:
        st.subheader("Your files")
        if files:
            cards = "".join(
                f'<div class="fcard"><span class="ext">{html.escape((p.suffix.lstrip(".") or "file")[:5].upper())}</span>'
                f'<div class="fname">{html.escape(p.name)}</div>'
                f'<div class="fmeta">{fmt_size(p.stat().st_size)}, edited {ago(p.stat().st_mtime)}</div></div>'
                for p in files
            )
            st.markdown(f'<div class="grid">{cards}</div>', unsafe_allow_html=True)
        else:
            empty_state("No files yet. Open the Create tab to make your first one.")
    with right:
        st.subheader("Activity")
        entries = st.session_state.get("log", [])[:8]
        if entries:
            rows = "".join(
                f'<div class="act"><span class="pip {a}"></span><span>{html.escape(t)}</span><time>{ts}</time></div>'
                for ts, a, t in entries
            )
            st.markdown(rows, unsafe_allow_html=True)
        else:
            empty_state("Your actions will appear here.")

# ------------------------------------------------------------------ Create
with tab_create:
    st.subheader("Create a file")
    with st.form("create_form", clear_on_submit=True):
        name = st.text_input("File name", placeholder="notes.txt")
        data = st.text_area("Content", height=180, placeholder="Write something...")
        go = st.form_submit_button("Create file", type="primary")
    if go:
        path = safe_path(name)
        if not path:
            st.error("Enter a file name first.")
        elif path.exists():
            st.error(f"{path.name} already exists. Choose another name, or use the Update tab.")
        else:
            try:
                path.write_text(data, encoding="utf-8")
                log("create", f"Created {path.name}")
                flash(f"Created {path.name}")
                st.rerun()
            except OSError as err:
                st.error(f"Could not create the file: {err}")

# ------------------------------------------------------------------ Read
with tab_read:
    st.subheader("Read a file")
    files = list_files()
    if not files:
        empty_state("Nothing to read yet. Create a file first.")
    else:
        pick = st.selectbox("Choose a file", [p.name for p in files], key="read_pick")
        path = WORKSPACE / pick
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
            st.code(content if content else "(this file is empty)", language=None)
            c1, c2 = st.columns([1, 1])
            with c1:
                st.download_button("Download", content, file_name=pick)
            with c2:
                if st.button("Log this read", key="read_log"):
                    log("read", f"Read {pick}")
                    st.rerun()
        except OSError as err:
            st.error(f"Could not read the file: {err}")

# ------------------------------------------------------------------ Update
with tab_update:
    st.subheader("Update a file")
    files = list_files()
    if not files:
        empty_state("Nothing to update yet. Create a file first.")
    else:
        pick = st.selectbox("Choose a file", [p.name for p in files], key="upd_pick")
        path = WORKSPACE / pick
        op = st.radio(
            "What do you want to do?",
            ["Rename", "Clear content", "Append text", "Overwrite content"],
            horizontal=True,
            key="upd_op",
        )
        try:
            if op == "Rename":
                new = st.text_input("New file name", key="upd_new")
                if st.button("Rename file", type="primary", key="btn_rename"):
                    new_path = safe_path(new)
                    if not new_path:
                        st.error("Enter the new file name.")
                    elif new_path.exists():
                        st.error(f"{new_path.name} already exists. Choose a different name.")
                    else:
                        path.rename(new_path)
                        log("update", f"Renamed {pick} to {new_path.name}")
                        flash(f"Renamed to {new_path.name}")
                        st.rerun()

            elif op == "Clear content":
                st.caption("This empties the file but keeps it in the workspace.")
                if st.button("Clear content", type="primary", key="btn_clear"):
                    path.write_text("", encoding="utf-8")
                    log("update", f"Cleared {pick}")
                    flash(f"Cleared {pick}")
                    st.rerun()

            elif op == "Append text":
                extra = st.text_area("Text to add at the end", key=f"app_{pick}", height=140)
                if st.button("Append text", type="primary", key="btn_append"):
                    with open(path, "a", encoding="utf-8") as fs:
                        fs.write("\n" + extra)
                    log("update", f"Appended to {pick}")
                    flash(f"Added text to {pick}")
                    st.rerun()

            else:
                current = path.read_text(encoding="utf-8", errors="replace")
                new_text = st.text_area("New content", value=current, key=f"ow_{pick}", height=200)
                if st.button("Save content", type="primary", key="btn_over"):
                    path.write_text(new_text, encoding="utf-8")
                    log("update", f"Overwrote {pick}")
                    flash(f"Saved {pick}")
                    st.rerun()
        except OSError as err:
            st.error(f"Could not update the file: {err}")

# ------------------------------------------------------------------ Delete
with tab_delete:
    st.subheader("Delete a file")
    files = list_files()
    if not files:
        empty_state("Nothing to delete.")
    else:
        pick = st.selectbox("Choose a file", [p.name for p in files], key="del_pick")
        sure = st.checkbox(f"Delete {pick} permanently. This can't be undone.", key="del_sure")
        if st.button("Delete file", type="primary", disabled=not sure, key="btn_del"):
            try:
                (WORKSPACE / pick).unlink()
                log("delete", f"Deleted {pick}")
                flash(f"Deleted {pick}", "🗑️")
                st.session_state["del_sure"] = False
                st.rerun()
            except OSError as err:
                st.error(f"Could not delete the file: {err}")

st.markdown('<div class="foot">Made by Sudhanshu Tiwari. Built with Python, pathlib and Streamlit</div>', unsafe_allow_html=True)