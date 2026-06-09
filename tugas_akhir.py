import streamlit as st
import pandas as pd
import random
from dataclasses import dataclass, field
from typing import Optional, List
import time

# ─── KONFIGURASI HALAMAN ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="RS MedCare — Sistem Pencarian Layanan",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CUSTOM CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;600;700&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* ── Background ── */
.stApp { background: #F0F4F8; }

/* ── Header strip ── */
.hero-bar {
    background: linear-gradient(135deg, #0F3460 0%, #16213E 60%, #1A1A2E 100%);
    border-radius: 16px;
    padding: 32px 40px 28px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.hero-bar::after {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(0,212,180,0.18) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.1rem; font-weight: 700;
    color: #FFFFFF; margin: 0 0 4px;
    letter-spacing: -0.5px;
}
.hero-sub {
    font-size: 0.92rem; color: #A8C5DA;
    margin: 0; font-weight: 400;
}
.hero-badge {
    display: inline-block;
    background: rgba(0,212,180,0.15);
    border: 1px solid rgba(0,212,180,0.4);
    color: #00D4B4; border-radius: 20px;
    padding: 3px 12px; font-size: 0.78rem;
    font-weight: 600; margin-bottom: 12px;
    letter-spacing: 0.5px;
}

/* ── Metric cards ── */
.metric-row { display: flex; gap: 14px; margin-bottom: 22px; flex-wrap: wrap; }
.metric-card {
    background: #FFFFFF;
    border-radius: 12px;
    padding: 18px 22px;
    flex: 1; min-width: 140px;
    border-left: 4px solid;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.metric-card.total  { border-color: #0F3460; }
.metric-card.kritis { border-color: #E53E3E; }
.metric-card.berat  { border-color: #DD6B20; }
.metric-card.sedang { border-color: #D69E2E; }
.metric-card.ringan { border-color: #38A169; }
.metric-num { font-family:'Space Grotesk',sans-serif; font-size:1.8rem; font-weight:700; line-height:1; }
.metric-lbl { font-size:0.78rem; color:#718096; margin-top:4px; font-weight:500; }

/* ── Section heading ── */
.sec-head {
    font-family:'Space Grotesk',sans-serif;
    font-size:1.05rem; font-weight:700;
    color:#1A202C; margin:0 0 14px;
    display:flex; align-items:center; gap:8px;
}

/* ── Search box wrapper ── */
.search-wrap {
    background:#FFFFFF;
    border-radius:14px;
    padding:24px 26px;
    box-shadow:0 2px 10px rgba(0,0,0,0.07);
    margin-bottom:20px;
}

/* ── Result card ── */
.result-card {
    background:#FFFFFF;
    border-radius:14px;
    padding:22px 24px;
    box-shadow:0 2px 10px rgba(0,0,0,0.07);
    margin-bottom:14px;
    border-left:5px solid;
    animation: fadeIn 0.35s ease;
}
@keyframes fadeIn { from{opacity:0;transform:translateY(6px)} to{opacity:1;transform:translateY(0)} }
.result-card.kritis { border-color:#E53E3E; }
.result-card.berat  { border-color:#DD6B20; }
.result-card.sedang { border-color:#D69E2E; }
.result-card.ringan { border-color:#38A169; }

.rc-name { font-family:'Space Grotesk',sans-serif; font-size:1.15rem; font-weight:700; color:#1A202C; }
.rc-id   { font-size:0.78rem; color:#A0AEC0; margin-top:2px; }
.rc-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(180px,1fr)); gap:12px; margin-top:16px; }
.rc-item { background:#F7FAFC; border-radius:8px; padding:10px 14px; }
.rc-item-label { font-size:0.72rem; color:#718096; font-weight:600; text-transform:uppercase; letter-spacing:0.4px; }
.rc-item-val   { font-size:0.9rem;  color:#1A202C; font-weight:600; margin-top:2px; }

/* ── Severity badge ── */
.badge {
    display:inline-block; border-radius:6px;
    padding:3px 10px; font-size:0.78rem; font-weight:700;
    letter-spacing:0.3px;
}
.badge.kritis { background:#FFF5F5; color:#C53030; border:1px solid #FEB2B2; }
.badge.berat  { background:#FFFAF0; color:#C05621; border:1px solid #FBD38D; }
.badge.sedang { background:#FFFFF0; color:#975A16; border:1px solid #FAF089; }
.badge.ringan { background:#F0FFF4; color:#276749; border:1px solid #9AE6B4; }

/* ── BST trace box ── */
.bst-trace {
    background:#1A202C; color:#68D391;
    border-radius:10px; padding:16px 20px;
    font-family:'Courier New',monospace;
    font-size:0.82rem; line-height:1.7;
    max-height:220px; overflow-y:auto;
    margin-top:12px;
}
.bst-trace .step-num { color:#63B3ED; }
.bst-trace .found    { color:#F6E05E; font-weight:700; }
.bst-trace .notfound { color:#FC8181; }

/* ── Table ── */
.stDataFrame { border-radius:12px; overflow:hidden; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] { background:#0F3460 !important; }
section[data-testid="stSidebar"] * { color:#E2E8F0 !important; }
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stRadio label { color:#A8C5DA !important; font-size:0.82rem; }

/* ── Streamlit overrides ── */
div[data-testid="stTextInput"] input {
    border-radius:10px !important;
    border:2px solid #E2E8F0 !important;
    padding:10px 16px !important;
    font-size:0.95rem !important;
}
div[data-testid="stTextInput"] input:focus { border-color:#0F3460 !important; box-shadow:0 0 0 3px rgba(15,52,96,0.12) !important; }
.stButton>button {
    background:#0F3460 !important; color:#FFFFFF !important;
    border:none !important; border-radius:10px !important;
    padding:10px 24px !important; font-weight:600 !important;
    font-size:0.9rem !important; transition:all .2s !important;
}
.stButton>button:hover { background:#16213E !important; transform:translateY(-1px); box-shadow:0 4px 12px rgba(15,52,96,0.3) !important; }

.info-box {
    background:#EBF8FF; border-radius:10px;
    border:1px solid #BEE3F8; padding:14px 18px;
    font-size:0.85rem; color:#2B6CB0; margin-top:8px;
}
</style>
""", unsafe_allow_html=True)

# ─── DATA 200 PASIEN ───────────────────────────────────────────────────────────
PENYAKIT = {
    "KRITIS": [
        ("Kanker Stadium IV",           "ICU-K01", 9),
        ("Gagal Jantung Akut",          "ICU-K02", 9),
        ("Stroke Hemoragik",            "ICU-K03", 9),
        ("Sepsis Berat",                "ICU-K04", 9),
        ("Gagal Nafas Akut (ARDS)",     "ICU-K05", 9),
        ("Luka Bakar > 50%",            "ICU-K06", 8),
        ("Trauma Kepala Berat",         "ICU-K07", 8),
        ("Gagal Ginjal Akut Berat",     "ICU-K08", 8),
        ("Syok Septik",                 "ICU-K09", 8),
        ("Emboli Paru Masif",           "ICU-K10", 8),
    ],
    "BERAT": [
        ("Pneumonia Berat",             "IGD-B01", 7),
        ("Diabetes Ketoasidosis",       "IGD-B02", 7),
        ("Perdarahan Saluran Cerna",    "IGD-B03", 7),
        ("Infark Miokard",              "IGD-B04", 7),
        ("Meningitis Bakterial",        "IGD-B05", 7),
        ("Appendisitis Perforasi",      "BED-B06", 6),
        ("Gagal Liver Akut",            "BED-B07", 6),
        ("Eklampsia",                   "BED-B08", 6),
        ("Aritmia Ventrikel",           "IGD-B09", 6),
        ("Peritonitis",                 "BED-B10", 6),
    ],
    "SEDANG": [
        ("Tifus Abdominalis",           "PNY-S01", 5),
        ("Tuberkulosis Paru",           "PNY-S02", 5),
        ("DBD (Dengue Berat)",          "PNY-S03", 5),
        ("Bronkitis Kronik",            "PNY-S04", 4),
        ("Hipertensi Krisis",           "PNY-S05", 5),
        ("Anemia Berat",                "PNY-S06", 4),
        ("Infeksi Saluran Kemih Berat", "PNY-S07", 4),
        ("Gastroenteritis Berat",       "PNY-S08", 4),
        ("Malaria Falciparum",          "PNY-S09", 5),
        ("Hepatitis B Akut",            "PNY-S10", 4),
    ],
    "RINGAN": [
        ("Flu & Batuk",                 "POL-R01", 2),
        ("Maag (Gastritis Ringan)",     "POL-R02", 2),
        ("Sakit Kepala Tegang",         "POL-R03", 1),
        ("Dermatitis Alergi",           "POL-R04", 2),
        ("Konjungtivitis",              "POL-R05", 1),
        ("Rhinitis Alergi",             "POL-R06", 1),
        ("Myalgia",                     "POL-R07", 2),
        ("ISPA Ringan",                 "POL-R08", 2),
        ("Asam Urat Ringan",            "POL-R09", 2),
        ("Diare Ringan",                "POL-R10", 1),
    ],
}

NAMA_DEPAN = [
    "Budi","Siti","Ahmad","Dewi","Rizki","Rina","Hendra","Nur","Fajar","Lestari",
    "Andi","Maya","Doni","Fitri","Reza","Yuli","Bagas","Indah","Wahyu","Sari",
    "Dian","Agus","Wulan","Eko","Ayu","Joko","Tari","Iqbal","Nadia","Fauzi",
    "Gita","Hadi","Lina","Irwan","Citra","Rudi","Desi","Anton","Suci","Yusuf"
]
NAMA_BELAKANG = [
    "Santoso","Rahayu","Wijaya","Kusuma","Pratama","Handayani","Saputra","Wati",
    "Nugroho","Sari","Setiawan","Lestari","Putra","Dewi","Hidayat","Permata",
    "Kurniawan","Utami","Purnomo","Anggraini","Susilo","Wahyuni","Hartono","Novita",
    "Mulyono","Safitri","Haryanto","Astuti","Gunawan","Maharani"
]

GOLDAR = ["A","B","AB","O"]
DOKTER = [
    "dr. Adi Nugroho, Sp.PD","dr. Sari Kusuma, Sp.JP","dr. Bima Prakasa, Sp.S",
    "dr. Rini Setiawati, Sp.B","dr. Yanto Prasetyo, Sp.A","dr. Lela Andriani, Sp.OG",
    "dr. Hasan Maulana, Sp.An","dr. Tuti Rahayu, Sp.PK","dr. Iwan Santosa, Sp.RM",
    "dr. Dina Fitriani, Sp.KK",
]

random.seed(42)

def buat_data():
    pasien = []
    pid = 1
    for level, daftar in PENYAKIT.items():
        per_penyakit = 200 // (len(PENYAKIT) * len(daftar)) + 1
        for (nama_penyakit, kode_kamar, skor) in daftar:
            for _ in range(5):  # 5 pasien per penyakit → 10 penyakit × 4 level × 5 = 200
                nama = f"{random.choice(NAMA_DEPAN)} {random.choice(NAMA_BELAKANG)}"
                usia = random.randint(5, 80)
                pasien.append({
                    "id_pasien":     f"RS{pid:04d}",
                    "nama":          nama,
                    "usia":          usia,
                    "jenis_kelamin": random.choice(["Laki-laki","Perempuan"]),
                    "goldar":        random.choice(GOLDAR),
                    "penyakit":      nama_penyakit,
                    "tingkat":       level,
                    "skor_parah":    skor,
                    "kode_kamar":    kode_kamar,
                    "dokter":        random.choice(DOKTER),
                    "lama_rawat":    random.randint(1, 30) if level in ("KRITIS","BERAT") else random.randint(1, 7),
                    "biaya":         random.randint(5_000_000, 80_000_000) if level == "KRITIS"
                                     else random.randint(3_000_000, 40_000_000) if level == "BERAT"
                                     else random.randint(1_000_000, 15_000_000) if level == "SEDANG"
                                     else random.randint(100_000, 2_000_000),
                })
                pid += 1
    random.shuffle(pasien)
    return pasien[:200]

DATA_PASIEN = buat_data()
DF = pd.DataFrame(DATA_PASIEN)

# ─── BINARY SEARCH TREE ───────────────────────────────────────────────────────
@dataclass
class BSTNode:
    key: str          # nama pasien (lowercase)
    data: dict
    left:  Optional["BSTNode"] = field(default=None, repr=False)
    right: Optional["BSTNode"] = field(default=None, repr=False)

class BST:
    def __init__(self):
        self.root: Optional[BSTNode] = None
        self._count = 0

    def insert(self, key: str, data: dict):
        self.root = self._insert(self.root, key.lower(), data)
        self._count += 1

    def _insert(self, node, key, data):
        if node is None:
            return BSTNode(key, data)
        if key < node.key:
            node.left  = self._insert(node.left,  key, data)
        elif key > node.key:
            node.right = self._insert(node.right, key, data)
        else:  # duplikat: simpan semua (linked list sederhana dengan list)
            if not isinstance(node.data, list):
                node.data = [node.data]
            node.data.append(data)
        return node

    def search_exact(self, key: str) -> tuple[list, list]:
        """Kembalikan (hasil, jejak_langkah)"""
        trace = []
        results = []
        self._search(self.root, key.lower(), trace, results, step=1)
        return results, trace

    def _search(self, node, key, trace, results, step):
        if node is None:
            trace.append((step, None, "NOT_FOUND"))
            return
        trace.append((step, node.key, "VISIT"))
        if key == node.key:
            trace.append((step, node.key, "FOUND"))
            if isinstance(node.data, list):
                results.extend(node.data)
            else:
                results.append(node.data)
        elif key < node.key:
            trace.append((step+1, node.key, "GO_LEFT"))
            self._search(node.left, key, trace, results, step+1)
        else:
            trace.append((step+1, node.key, "GO_RIGHT"))
            self._search(node.right, key, trace, results, step+1)

    def search_prefix(self, prefix: str) -> list:
        """Cari semua nama yang dimulai dengan prefix"""
        prefix = prefix.lower()
        results = []
        self._prefix_search(self.root, prefix, results)
        return results

    def _prefix_search(self, node, prefix, results):
        if node is None:
            return
        if node.key.startswith(prefix):
            if isinstance(node.data, list):
                results.extend(node.data)
            else:
                results.append(node.data)
        if prefix <= node.key:
            self._prefix_search(node.left, prefix, results)
        self._prefix_search(node.right, prefix, results)

    def inorder(self) -> list:
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node is None: return
        self._inorder(node.left, result)
        if isinstance(node.data, list):
            result.extend(node.data)
        else:
            result.append(node.data)
        self._inorder(node.right, result)

# ─── BUILD BST (cache agar tidak rebuild tiap rerun) ──────────────────────────
@st.cache_resource
def build_bst():
    bst = BST()
    for p in DATA_PASIEN:
        bst.insert(p["nama"], p)
    return bst

BST_TREE = build_bst()

# ─── HELPER FUNCTIONS ─────────────────────────────────────────────────────────
SEVERITY_ORDER = {"KRITIS": 0, "BERAT": 1, "SEDANG": 2, "RINGAN": 3}
SEVERITY_COLOR = {"KRITIS": "kritis", "BERAT": "berat", "SEDANG": "sedang", "RINGAN": "ringan"}
SEVERITY_EMOJI = {"KRITIS": "🔴", "BERAT": "🟠", "SEDANG": "🟡", "RINGAN": "🟢"}

def fmt_rupiah(x): return f"Rp {x:,.0f}".replace(",",".")

def render_badge(level):
    c = SEVERITY_COLOR.get(level, "ringan")
    e = SEVERITY_EMOJI.get(level, "")
    return f'<span class="badge {c}">{e} {level}</span>'

def render_result_card(p):
    level = p["tingkat"]
    c = SEVERITY_COLOR[level]
    html = f"""
    <div class="result-card {c}">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px">
            <div>
                <div class="rc-name">👤 {p['nama']}</div>
                <div class="rc-id">ID: {p['id_pasien']} &nbsp;|&nbsp; {p['jenis_kelamin']}, {p['usia']} tahun &nbsp;|&nbsp; Gol. Darah: {p['goldar']}</div>
            </div>
            {render_badge(level)}
        </div>
        <div class="rc-grid">
            <div class="rc-item">
                <div class="rc-item-label">🦠 Penyakit</div>
                <div class="rc-item-val">{p['penyakit']}</div>
            </div>
            <div class="rc-item">
                <div class="rc-item-label">🛏️ Kode Kamar</div>
                <div class="rc-item-val">{p['kode_kamar']}</div>
            </div>
            <div class="rc-item">
                <div class="rc-item-label">👨‍⚕️ Dokter</div>
                <div class="rc-item-val">{p['dokter']}</div>
            </div>
            <div class="rc-item">
                <div class="rc-item-label">📅 Lama Rawat</div>
                <div class="rc-item-val">{p['lama_rawat']} hari</div>
            </div>
            <div class="rc-item">
                <div class="rc-item-label">💰 Estimasi Biaya</div>
                <div class="rc-item-val">{fmt_rupiah(p['biaya'])}</div>
            </div>
            <div class="rc-item">
                <div class="rc-item-label">⚠️ Skor Keparahan</div>
                <div class="rc-item-val">{'★' * p['skor_parah']}{'☆' * (9 - p['skor_parah'])} ({p['skor_parah']}/9)</div>
            </div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_bst_trace(trace, query):
    lines = []
    for i, (step, node_key, action) in enumerate(trace):
        prefix = f'<span class="step-num">[{step}]</span>'
        if action == "VISIT":
            lines.append(f'{prefix} Periksa node: <b>"{node_key}"</b>')
        elif action == "GO_LEFT":
            lines.append(f'{prefix} "{query}" &lt; "{node_key}" → belok <b>kiri</b>')
        elif action == "GO_RIGHT":
            lines.append(f'{prefix} "{query}" &gt; "{node_key}" → belok <b>kanan</b>')
        elif action == "FOUND":
            lines.append(f'<span class="found">✔ DITEMUKAN: "{node_key}"</span>')
        elif action == "NOT_FOUND":
            lines.append(f'<span class="notfound">✘ Node null — data tidak ditemukan</span>')
        if i >= 18:
            lines.append("... (terpotong untuk singkatnya)")
            break
    content = "<br>".join(lines)
    st.markdown(f'<div class="bst-trace">{content}</div>', unsafe_allow_html=True)

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏥 RS MedCare")
    st.markdown("---")
    st.markdown("### 📋 Menu Navigasi")
    halaman = st.radio("", ["🔍 Pencarian Pasien", "📊 Semua Data", "🌳 Visualisasi BST", "📈 Statistik"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("### 🗂️ Filter Level")
    filter_level = st.multiselect(
        "Tingkat Keparahan",
        ["KRITIS","BERAT","SEDANG","RINGAN"],
        default=["KRITIS","BERAT","SEDANG","RINGAN"]
    )
    st.markdown("---")
    st.markdown("### ℹ️ Info Sistem")
    st.markdown(f"**Total Pasien:** {len(DATA_PASIEN)}")
    st.markdown(f"**Struktur:** Binary Search Tree")
    st.markdown(f"**Kunci BST:** Nama Pasien")
    st.markdown(f"**Pengurutan:** Skor Keparahan")

# ─── HERO HEADER ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-bar">
    <div class="hero-badge">🔬 SISTEM INFORMASI RUMAH SAKIT</div>
    <div class="hero-title">RS MedCare — Pencarian Layanan</div>
    <div class="hero-sub">Binary Search Tree • 200 Data Pasien • Klasifikasi Keparahan Penyakit</div>
</div>
""", unsafe_allow_html=True)

# ─── METRIC CARDS ─────────────────────────────────────────────────────────────
cnt = {lv: len([p for p in DATA_PASIEN if p["tingkat"] == lv]) for lv in ["KRITIS","BERAT","SEDANG","RINGAN"]}
st.markdown(f"""
<div class="metric-row">
    <div class="metric-card total">
        <div class="metric-num" style="color:#0F3460">{len(DATA_PASIEN)}</div>
        <div class="metric-lbl">Total Pasien</div>
    </div>
    <div class="metric-card kritis">
        <div class="metric-num" style="color:#E53E3E">{cnt['KRITIS']}</div>
        <div class="metric-lbl">🔴 Kritis (ICU)</div>
    </div>
    <div class="metric-card berat">
        <div class="metric-num" style="color:#DD6B20">{cnt['BERAT']}</div>
        <div class="metric-lbl">🟠 Berat (IGD/Bed)</div>
    </div>
    <div class="metric-card sedang">
        <div class="metric-num" style="color:#D69E2E">{cnt['SEDANG']}</div>
        <div class="metric-lbl">🟡 Sedang (Penyakit)</div>
    </div>
    <div class="metric-card ringan">
        <div class="metric-num" style="color:#38A169">{cnt['RINGAN']}</div>
        <div class="metric-lbl">🟢 Ringan (Poliklinik)</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# HALAMAN 1: PENCARIAN PASIEN
# ═══════════════════════════════════════════════════════════════════════════════
if halaman == "🔍 Pencarian Pasien":

    st.markdown('<div class="sec-head">🔍 Pencarian Data Pasien via Binary Search Tree</div>', unsafe_allow_html=True)

    st.markdown('<div class="search-wrap">', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        query = st.text_input("Nama Pasien", placeholder="Ketik nama pasien (sebagian atau lengkap)...", label_visibility="collapsed")
    with col2:
        mode = st.selectbox("Mode", ["Prefix (Awalan)", "Nama Persis"], label_visibility="collapsed")

    col3, col4 = st.columns([1, 3])
    with col3:
        cari = st.button("🔍 Cari Sekarang", use_container_width=True)
    with col4:
        sort_by = st.selectbox("Urutkan hasil:", ["Parah → Ringan (skor)","Ringan → Parah","Nama (A-Z)"], label_visibility="collapsed")

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        💡 <b>Cara kerja BST:</b> Nama pasien disimpan sebagai <i>key</i> dalam Binary Search Tree.
        Pencarian prefix menelusuri seluruh subtree yang relevan, sedangkan pencarian persis mengikuti
        jalur BST O(log n). Hasil diurutkan berdasarkan <b>skor keparahan penyakit</b>.
    </div>
    """, unsafe_allow_html=True)

    if cari and query.strip():
        t0 = time.time()
        if mode == "Nama Persis":
            results, trace = BST_TREE.search_exact(query.strip())
            show_trace = True
        else:
            results = BST_TREE.search_prefix(query.strip())
            trace = []
            show_trace = False

        elapsed = (time.time() - t0) * 1000

        # Filter level
        results = [r for r in results if r["tingkat"] in filter_level]

        # Sort
        if sort_by == "Parah → Ringan (skor)":
            results.sort(key=lambda x: -x["skor_parah"])
        elif sort_by == "Ringan → Parah":
            results.sort(key=lambda x: x["skor_parah"])
        else:
            results.sort(key=lambda x: x["nama"])

        st.markdown(f"**{len(results)} hasil** ditemukan untuk `\"{query}\"` &nbsp;|&nbsp; ⚡ Waktu BST: `{elapsed:.2f} ms`", unsafe_allow_html=True)

        if show_trace and trace:
            with st.expander("🌳 Jejak Penelusuran BST (klik untuk lihat)"):
                render_bst_trace(trace, query.strip().lower())

        if results:
            for p in results:
                render_result_card(p)
        else:
            st.warning(f"Tidak ada pasien dengan nama mengandung `{query}` pada level yang dipilih.")

    elif cari:
        st.error("⚠️ Masukkan nama pasien terlebih dahulu.")

    # Tampilkan contoh nama
    st.markdown("---")
    st.markdown("**💡 Contoh nama pasien dalam sistem:**")
    sample = random.sample(DATA_PASIEN, 8)
    cols = st.columns(4)
    for i, p in enumerate(sample):
        with cols[i % 4]:
            lv = p["tingkat"]
            e = SEVERITY_EMOJI[lv]
            st.markdown(f"- {e} `{p['nama']}`")

# ═══════════════════════════════════════════════════════════════════════════════
# HALAMAN 2: SEMUA DATA
# ═══════════════════════════════════════════════════════════════════════════════
elif halaman == "📊 Semua Data":
    st.markdown('<div class="sec-head">📊 Daftar Lengkap 200 Pasien (Urut: Parah → Ringan)</div>', unsafe_allow_html=True)

    filtered_df = DF[DF["tingkat"].isin(filter_level)].copy()
    filtered_df = filtered_df.sort_values(["skor_parah","tingkat"], ascending=[False, True])
    filtered_df["tingkat_label"] = filtered_df["tingkat"].map(
        lambda x: f"{SEVERITY_EMOJI[x]} {x}"
    )
    filtered_df["biaya_fmt"] = filtered_df["biaya"].map(fmt_rupiah)

    tampil = filtered_df[[
        "id_pasien","nama","usia","jenis_kelamin","goldar",
        "penyakit","tingkat_label","skor_parah","kode_kamar","dokter","lama_rawat","biaya_fmt"
    ]].rename(columns={
        "id_pasien":"ID","nama":"Nama","usia":"Usia","jenis_kelamin":"J.Kelamin",
        "goldar":"Gol.Darah","penyakit":"Penyakit","tingkat_label":"Tingkat",
        "skor_parah":"Skor","kode_kamar":"Kamar","dokter":"Dokter",
        "lama_rawat":"Hari Rawat","biaya_fmt":"Est. Biaya"
    })

    st.dataframe(tampil, use_container_width=True, height=500)
    st.markdown(f"*Menampilkan {len(filtered_df)} dari {len(DATA_PASIEN)} pasien*")

    # Legenda kamar
    st.markdown("---")
    st.markdown('<div class="sec-head">🗺️ Peta Kode Kamar</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    kamar_info = [
        ("🔴 ICU-K01 s/d K10", "KRITIS", "Intensive Care Unit — pasien kondisi kritis, pemantauan 24 jam"),
        ("🟠 IGD-B01 s/d B09", "BERAT",  "Instalasi Gawat Darurat & Kamar Rawat Bedah — pasien berat"),
        ("🟡 PNY-S01 s/d S10", "SEDANG", "Bangsal Penyakit Dalam — pasien kondisi sedang"),
        ("🟢 POL-R01 s/d R10", "RINGAN", "Poliklinik Rawat Jalan — pasien kondisi ringan"),
    ]
    for col, (judul, level, desc) in zip(cols, kamar_info):
        c = SEVERITY_COLOR[level]
        with col:
            st.markdown(f"""
            <div class="result-card {c}" style="padding:16px 18px">
                <div style="font-weight:700;font-size:0.9rem;color:#1A202C">{judul}</div>
                <div style="font-size:0.78rem;color:#718096;margin-top:6px">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# HALAMAN 3: VISUALISASI BST
# ═══════════════════════════════════════════════════════════════════════════════
elif halaman == "🌳 Visualisasi BST":
    st.markdown('<div class="sec-head">🌳 Struktur Binary Search Tree</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        <b>Cara kerja BST dalam sistem ini:</b><br>
        • <b>Key (Kunci)</b>: Nama pasien (huruf kecil) digunakan sebagai kunci pengurutan BST.<br>
        • <b>Insert</b>: Setiap pasien dimasukkan satu per satu. Nama yang lebih kecil secara alfabet masuk ke subtree kiri, lebih besar ke kanan.<br>
        • <b>Search Exact</b>: Menelusuri jalur dari root mengikuti perbandingan huruf — O(log n) rata-rata.<br>
        • <b>Search Prefix</b>: Menelusuri semua node yang awalan namanya cocok — berguna untuk pencarian parsial.<br>
        • <b>Inorder Traversal</b>: Menghasilkan daftar pasien terurut secara alfabet.
    </div>
    """, unsafe_allow_html=True)

    # Tampilkan 20 node pertama (inorder)
    inorder_res = BST_TREE.inorder()
    st.markdown("---")
    st.markdown(f"**📋 Inorder Traversal BST** (20 dari {len(inorder_res)} node, urut alfabet):")

    cols = st.columns(2)
    for i, p in enumerate(inorder_res[:20]):
        with cols[i % 2]:
            lv = p["tingkat"]
            e = SEVERITY_EMOJI[lv]
            st.markdown(f"""
            <div style="background:#fff;border-radius:8px;padding:10px 14px;margin-bottom:8px;
                        border-left:3px solid {'#E53E3E' if lv=='KRITIS' else '#DD6B20' if lv=='BERAT' else '#D69E2E' if lv=='SEDANG' else '#38A169'}">
                <span style="font-size:0.75rem;color:#A0AEC0">{i+1}.</span>
                <b style="color:#1A202C">{p['nama']}</b>
                <span style="float:right;font-size:0.75rem">{e} {p['tingkat']}</span><br>
                <span style="font-size:0.78rem;color:#718096">{p['penyakit']} | Kamar {p['kode_kamar']}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    **🧮 Kompleksitas Algoritma BST:**

    | Operasi | Best Case | Average Case | Worst Case |
    |---------|-----------|--------------|------------|
    | Insert  | O(log n)  | O(log n)     | O(n)       |
    | Search Exact | O(1) | O(log n)  | O(n)       |
    | Search Prefix | O(k) | O(k·log n) | O(n)     |
    | Inorder Traversal | O(n) | O(n) | O(n)    |

    *n = jumlah node (pasien), k = jumlah hasil ditemukan*
    """)

# ═══════════════════════════════════════════════════════════════════════════════
# HALAMAN 4: STATISTIK
# ═══════════════════════════════════════════════════════════════════════════════
elif halaman == "📈 Statistik":
    st.markdown('<div class="sec-head">📈 Statistik Rumah Sakit</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Distribusi Pasien per Tingkat Keparahan**")
        dist_df = pd.DataFrame([
            {"Tingkat": f"{SEVERITY_EMOJI[lv]} {lv}", "Jumlah": cnt[lv], "Persen": f"{cnt[lv]/2:.1f}%"}
            for lv in ["KRITIS","BERAT","SEDANG","RINGAN"]
        ])
        st.dataframe(dist_df, use_container_width=True, hide_index=True)

        st.markdown("**Top 10 Penyakit Terbanyak**")
        top_penyakit = DF["penyakit"].value_counts().head(10).reset_index()
        top_penyakit.columns = ["Penyakit","Jumlah"]
        st.dataframe(top_penyakit, use_container_width=True, hide_index=True)

    with col2:
        st.markdown("**Rata-rata Lama Rawat per Tingkat**")
        rawat_df = DF.groupby("tingkat")["lama_rawat"].mean().reset_index()
        rawat_df.columns = ["Tingkat","Rata-rata Hari"]
        rawat_df["Rata-rata Hari"] = rawat_df["Rata-rata Hari"].round(1)
        rawat_df = rawat_df.sort_values("Rata-rata Hari", ascending=False)
        st.dataframe(rawat_df, use_container_width=True, hide_index=True)

        st.markdown("**Rata-rata Estimasi Biaya per Tingkat**")
        biaya_df = DF.groupby("tingkat")["biaya"].mean().reset_index()
        biaya_df.columns = ["Tingkat","Rata-rata Biaya"]
        biaya_df["Rata-rata Biaya"] = biaya_df["Rata-rata Biaya"].map(fmt_rupiah)
        biaya_df = biaya_df.sort_values("Tingkat")
        st.dataframe(biaya_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("**👨‍⚕️ Jumlah Pasien per Dokter**")
    dok_df = DF["dokter"].value_counts().reset_index()
    dok_df.columns = ["Dokter","Jumlah Pasien"]
    st.dataframe(dok_df, use_container_width=True, hide_index=True)