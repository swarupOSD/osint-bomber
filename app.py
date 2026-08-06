import streamlit as st
import pandas as pd
from scanner import OSINTSanner
from hibp_checker import HIBPChecker
from pdf_generator import PDFReport
from geoip_checker import GeoIPChecker
import time
import os
import pyperclip
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sqlite3
import json
import zipfile
import io

# ========== PAGE CONFIGURATION ==========
st.set_page_config(
    page_title="OSINT Bomber - 1000+ Site Scanner",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== LANGUAGE DICTIONARY ==========
LANGUAGES = {
    "English": {
        "title": "OSINT BOMBER",
        "subtitle": "Professional OSINT Intelligence Tool",
        "tagline": "⚡ 1000+ Platforms • Real-time Analytics • GeoIP",
        "warning": "⚠️ WARNING: This tool is for checking YOUR OWN accounts only!\nScanning others without permission is ILLEGAL!",
        "enter_details": "🔎 Enter Details",
        "username": "👤 Username",
        "username_placeholder": "e.g., elonmusk, john_doe",
        "username_help": "Enter any username to search across 1000+ platforms",
        "email": "📧 Email (optional)",
        "email_placeholder": "your_email@example.com",
        "email_help": "Check if your email was in any data breaches",
        "start_scan": "🚀 Start Scan",
        "clear": "🔄 Clear",
        "logs": "📋 Real-time Logs",
        "analytics": "📊 Analytics Dashboard",
        "platform_dist": "📈 Platform Distribution",
        "geoip": "🌍 GeoIP Map",
        "download_export": "📥 Download & Export",
        "pdf": "📄 PDF",
        "pdf_caption": "Professional PDF Report",
        "txt": "📝 TXT",
        "txt_caption": "Simple Text Report",
        "csv": "📊 CSV",
        "csv_caption": "Excel Compatible",
        "copy": "📋 Copy",
        "copy_caption": "Copy all links",
        "copy_links": "📋 Copy All Links",
        "copied": "✅ All links copied to clipboard!",
        "copy_failed": "⚠️ Auto-copy failed. Copy manually below.",
        "view_links": "🔗 View All Links (Copy Manually)",
        "all_profiles": "All Profiles Found",
        "scan_time": "⏱️ Scan Time",
        "sites_scanned": "📊 Sites Scanned",
        "profiles_found": "✅ Profiles Found",
        "reports": "📁 Reports",
        "scan_complete": "🎉 Scan complete! Download your reports above.",
        "no_profiles": "😕 No profiles found for this username!",
        "no_results": "✅ Scan Complete - No results",
        "enter_username": "❌ Please enter a username to scan!",
        "found_profiles": "✅ Found {} profiles for '{}'!",
        "file_upload": "📂 Upload File (TXT/CSV)",
        "file_upload_help": "Upload a file with multiple usernames (one per line)",
        "or": "OR",
        "scanning": "Scanning 1000+ sites...",
        "initializing": "Initializing...",
        "processing": "Processing results...",
        "checking_email": "Checking email...",
        "fetching_geoip": "Fetching GeoIP data...",
        "generating_reports": "Generating reports...",
        "generating_analytics": "Generating analytics..."
    },
    "বাংলা": {
        "title": "ওএসআইএনটি বোম্বার",
        "subtitle": "পেশাদার ওএসআইএনটি ইন্টেলিজেন্স টুল",
        "tagline": "⚡ ১০০০+ প্ল্যাটফর্ম • রিয়েল-টাইম অ্যানালিটিক্স • জিওআইপি",
        "warning": "⚠️ সতর্কতা: এই টুল শুধু আপনার নিজের অ্যাকাউন্ট চেক করার জন্য!\nঅন্যের অনুমতি ছাড়া স্ক্যান করা বেআইনি!",
        "enter_details": "🔎 বিস্তারিত দিন",
        "username": "👤 ইউজারনেম",
        "username_placeholder": "যেমন: elonmusk, john_doe",
        "username_help": "১০০০+ প্ল্যাটফর্মে সার্চ করতে ইউজারনেম দিন",
        "email": "📧 ইমেইল (ঐচ্ছিক)",
        "email_placeholder": "আপনার_ইমেইল@example.com",
        "email_help": "আপনার ইমেইল ডেটা লিকে আছে কিনা চেক করুন",
        "start_scan": "🚀 স্ক্যান শুরু",
        "clear": "🔄 মুছুন",
        "logs": "📋 রিয়েল-টাইম লগ",
        "analytics": "📊 অ্যানালিটিক্স ড্যাশবোর্ড",
        "platform_dist": "📈 প্ল্যাটফর্ম বিতরণ",
        "geoip": "🌍 জিওআইপি ম্যাপ",
        "download_export": "📥 ডাউনলোড ও এক্সপোর্ট",
        "pdf": "📄 পিডিএফ",
        "pdf_caption": "পেশাদার পিডিএফ রিপোর্ট",
        "txt": "📝 টিএক্সটি",
        "txt_caption": "সাধারণ টেক্সট রিপোর্ট",
        "csv": "📊 সিএসভি",
        "csv_caption": "এক্সেল কম্প্যাটিবল",
        "copy": "📋 কপি",
        "copy_caption": "সব লিংক কপি করুন",
        "copy_links": "📋 সব লিংক কপি",
        "copied": "✅ সব লিংক ক্লিপবোর্ডে কপি হয়েছে!",
        "copy_failed": "⚠️ অটো-কপি কাজ করেনি। নিচে ম্যানুয়ালি কপি করুন।",
        "view_links": "🔗 সব লিংক দেখুন (ম্যানুয়ালি কপি)",
        "all_profiles": "সব প্রোফাইল পাওয়া গেছে",
        "scan_time": "⏱️ স্ক্যান সময়",
        "sites_scanned": "📊 স্ক্যান করা সাইট",
        "profiles_found": "✅ প্রোফাইল পাওয়া গেছে",
        "reports": "📁 রিপোর্ট",
        "scan_complete": "🎉 স্ক্যান শেষ! উপরের রিপোর্ট ডাউনলোড করুন।",
        "no_profiles": "😕 এই ইউজারনেমের জন্য কোনো প্রোফাইল পাওয়া যায়নি!",
        "no_results": "✅ স্ক্যান শেষ - কোনো ফলাফল নেই",
        "enter_username": "❌ অনুগ্রহ করে একটি ইউজারনেম দিন!",
        "found_profiles": "✅ '{}' এর জন্য {} টি প্রোফাইল পাওয়া গেছে!",
        "file_upload": "📂 ফাইল আপলোড করুন (TXT/CSV)",
        "file_upload_help": "একাধিক ইউজারনেম সম্বলিত ফাইল আপলোড করুন (প্রতি লাইনে একটি)",
        "or": "অথবা",
        "scanning": "১০০০+ সাইট স্ক্যান হচ্ছে...",
        "initializing": "চালু হচ্ছে...",
        "processing": "ফলাফল প্রক্রিয়াকরণ...",
        "checking_email": "ইমেইল চেক করা হচ্ছে...",
        "fetching_geoip": "জিওআইপি ডেটা সংগ্রহ...",
        "generating_reports": "রিপোর্ট তৈরি...",
        "generating_analytics": "অ্যানালিটিক্স তৈরি..."
    },
    "हिंदी": {
        "title": "ओएसआईएनटी बॉम्बर",
        "subtitle": "प्रोफेशनल ओएसआईएनटी इंटेलिजेंस टूल",
        "tagline": "⚡ 1000+ प्लेटफॉर्म • रियल-टाइम एनालिटिक्स • जियोआईपी",
        "warning": "⚠️ चेतावनी: यह टूल केवल आपके अपने खातों की जाँच के लिए है!\nदूसरों की अनुमति के बिना स्कैन करना अवैध है!",
        "enter_details": "🔎 विवरण दर्ज करें",
        "username": "👤 यूजरनेम",
        "username_placeholder": "जैसे: elonmusk, john_doe",
        "username_help": "1000+ प्लेटफॉर्म पर खोजने के लिए यूजरनेम दर्ज करें",
        "email": "📧 ईमेल (वैकल्पिक)",
        "email_placeholder": "आपका_ईमेल@example.com",
        "email_help": "जाँच करें कि आपका ईमेल किसी डेटा लीक में तो नहीं है",
        "start_scan": "🚀 स्कैन शुरू करें",
        "clear": "🔄 साफ़ करें",
        "logs": "📋 रियल-टाइम लॉग",
        "analytics": "📊 एनालिटिक्स डैशबोर्ड",
        "platform_dist": "📈 प्लेटफॉर्म वितरण",
        "geoip": "🌍 जियोआईपी मैप",
        "download_export": "📥 डाउनलोड और एक्सपोर्ट",
        "pdf": "📄 पीडीएफ",
        "pdf_caption": "प्रोफेशनल पीडीएफ रिपोर्ट",
        "txt": "📝 टेक्स्ट",
        "txt_caption": "सरल टेक्स्ट रिपोर्ट",
        "csv": "📊 सीएसवी",
        "csv_caption": "एक्सेल संगत",
        "copy": "📋 कॉपी",
        "copy_caption": "सभी लिंक कॉपी करें",
        "copy_links": "📋 सभी लिंक कॉपी करें",
        "copied": "✅ सभी लिंक क्लिपबोर्ड पर कॉपी हो गए!",
        "copy_failed": "⚠️ ऑटो-कॉपी विफल। नीचे मैन्युअल रूप से कॉपी करें।",
        "view_links": "🔗 सभी लिंक देखें (मैन्युअल कॉपी)",
        "all_profiles": "सभी प्रोफाइल मिले",
        "scan_time": "⏱️ स्कैन समय",
        "sites_scanned": "📊 स्कैन की गई साइटें",
        "profiles_found": "✅ प्रोफाइल मिले",
        "reports": "📁 रिपोर्ट",
        "scan_complete": "🎉 स्कैन पूरा! ऊपर रिपोर्ट डाउनलोड करें।",
        "no_profiles": "😕 इस यूजरनेम के लिए कोई प्रोफाइल नहीं मिला!",
        "no_results": "✅ स्कैन पूरा - कोई परिणाम नहीं",
        "enter_username": "❌ कृपया एक यूजरनेम दर्ज करें!",
        "found_profiles": "✅ '{}' के लिए {} प्रोफाइल मिले!",
        "file_upload": "📂 फ़ाइल अपलोड करें (TXT/CSV)",
        "file_upload_help": "कई यूजरनेम वाली फ़ाइल अपलोड करें (प्रति पंक्ति एक)",
        "or": "या",
        "scanning": "1000+ साइट स्कैन हो रहा है...",
        "initializing": "प्रारंभ हो रहा है...",
        "processing": "परिणाम संसाधित...",
        "checking_email": "ईमेल जाँच...",
        "fetching_geoip": "जियोआईपी डेटा प्राप्त...",
        "generating_reports": "रिपोर्ट तैयार...",
        "generating_analytics": "एनालिटिक्स तैयार..."
    }
}

# ========== LANGUAGE SELECTOR ==========
with st.sidebar:
    st.markdown("### 🌐 Language")
    lang = st.selectbox(
        "",
        ["English", "বাংলা", "हिंदी"],
        key="language_selector",
        label_visibility="collapsed"
    )
    st.markdown("---")
    T = LANGUAGES[lang]

# ========== DATABASE SETUP ==========
def init_db():
    conn = sqlite3.connect('scans.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS scans
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  timestamp TEXT,
                  results TEXT,
                  email TEXT,
                  total_found INTEGER)''')
    conn.commit()
    conn.close()

def save_scan(username, results, email="", total_found=0):
    conn = sqlite3.connect('scans.db')
    c = conn.cursor()
    c.execute("""INSERT INTO scans 
                 (username, timestamp, results, email, total_found) 
                 VALUES (?, ?, ?, ?, ?)""",
              (username, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
               json.dumps(results), email, total_found))
    conn.commit()
    conn.close()

def get_recent_scans(limit=5):
    conn = sqlite3.connect('scans.db')
    c = conn.cursor()
    c.execute("SELECT username, timestamp, total_found FROM scans ORDER BY id DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return rows

init_db()

# ========== ADVANCED PROFESSIONAL CSS ==========
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;600;700;800&display=swap');
    * { margin: 0; padding: 0; box-sizing: border-box; }
    .stApp { background: #0a0a0f; font-family: 'Inter', sans-serif; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .main-header {
        font-size: 4.2rem;
        font-weight: 900;
        font-family: 'Orbitron', sans-serif;
        background: linear-gradient(135deg, #00d4ff 0%, #7b2ffc 40%, #ff006e 80%, #ffd93d 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1.5rem 0 0.5rem 0;
        text-shadow: 0 0 60px rgba(0, 212, 255, 0.2);
        letter-spacing: 6px;
        animation: glowPulse 4s ease-in-out infinite;
        position: relative;
    }
    .main-header::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 60%;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00d4ff, #7b2ffc, #ff006e, transparent);
    }
    @keyframes glowPulse {
        0% { text-shadow: 0 0 30px rgba(0, 212, 255, 0.15); }
        50% { text-shadow: 0 0 70px rgba(123, 47, 252, 0.35), 0 0 100px rgba(255, 0, 110, 0.15); }
        100% { text-shadow: 0 0 30px rgba(0, 212, 255, 0.15); }
    }
    .sub-header {
        text-align: center;
        color: #8888aa;
        font-size: 1.2rem;
        letter-spacing: 14px;
        text-transform: uppercase;
        font-weight: 300;
        margin-top: -0.5rem;
        margin-bottom: 1.5rem;
        font-family: 'Orbitron', sans-serif;
        opacity: 0.8;
    }
    .tagline {
        text-align: center;
        color: #556;
        font-size: 0.95rem;
        letter-spacing: 4px;
        margin-bottom: 1.5rem;
        font-weight: 400;
        background: rgba(255,255,255,0.03);
        padding: 0.5rem;
        border-radius: 50px;
        border: 1px solid rgba(255,255,255,0.03);
        display: inline-block;
        margin-left: auto;
        margin-right: auto;
        width: auto;
        padding: 0.6rem 2rem;
    }
    .warning-box {
        background: rgba(255, 0, 0, 0.08);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 0, 0, 0.15);
        padding: 1.2rem;
        border-radius: 16px;
        color: #ff6b6b;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 600;
        letter-spacing: 1px;
        box-shadow: 0 8px 40px rgba(255, 0, 0, 0.08);
        transition: all 0.3s ease;
    }
    .warning-box:hover {
        border-color: rgba(255, 0, 0, 0.3);
        box-shadow: 0 8px 50px rgba(255, 0, 0, 0.15);
        transform: scale(1.01);
    }
    .result-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 1.2rem 1.5rem;
        border-radius: 16px;
        margin: 0.7rem 0;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border-left: 4px solid transparent;
        background: linear-gradient(135deg, rgba(255,255,255,0.015), rgba(255,255,255,0.035));
        position: relative;
        overflow: hidden;
    }
    .result-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.02), rgba(123, 47, 252, 0.02));
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    .result-card:hover::before { opacity: 1; }
    .result-card:hover {
        transform: translateX(12px) scale(1.008);
        border-left-color: #00d4ff;
        background: rgba(0, 212, 255, 0.04);
        box-shadow: 0 10px 50px rgba(0, 212, 255, 0.06);
    }
    .result-card a { color: #00d4ff !important; text-decoration: none; font-weight: 400; transition: 0.3s; position: relative; z-index: 1; }
    .result-card a:hover { color: #7b2ffc !important; text-shadow: 0 0 25px rgba(123, 47, 252, 0.25); }
    .result-card strong { color: #fff; font-weight: 600; font-size: 1.05rem; display: block; margin-bottom: 0.25rem; position: relative; z-index: 1; }
    
    .stButton button {
        width: 100%;
        background: linear-gradient(135deg, #00d4ff, #7b2ffc);
        color: white !important;
        font-weight: 700;
        font-size: 1.1rem;
        border: none;
        padding: 0.85rem;
        border-radius: 14px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 25px rgba(0, 212, 255, 0.2);
        letter-spacing: 1.5px;
        text-transform: uppercase;
        font-family: 'Inter', sans-serif;
        position: relative;
        overflow: hidden;
    }
    .stButton button::after {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 60%);
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    .stButton button:hover::after { opacity: 1; }
    .stButton button:hover { transform: translateY(-3px) scale(1.02); box-shadow: 0 8px 45px rgba(0, 212, 255, 0.35); }
    .stButton button:active { transform: translateY(0px) scale(0.97); }
    
    .stDownloadButton button {
        background: linear-gradient(135deg, #00b894, #00a381) !important;
        box-shadow: 0 4px 25px rgba(0, 184, 148, 0.2) !important;
        font-weight: 600 !important;
    }
    .stDownloadButton button:hover { box-shadow: 0 8px 45px rgba(0, 184, 148, 0.35) !important; transform: translateY(-3px); }
    
    .css-1d391kg { background: rgba(10, 10, 15, 0.95); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border-right: 1px solid rgba(255, 255, 255, 0.03); }
    
    .log-container {
        background: rgba(0, 0, 0, 0.6);
        padding: 1.2rem;
        border-radius: 16px;
        max-height: 350px;
        overflow-y: auto;
        font-family: 'Courier New', monospace;
        font-size: 0.85rem;
        border: 1px solid rgba(0, 212, 255, 0.08);
        box-shadow: inset 0 0 60px rgba(0, 0, 0, 0.6);
        scrollbar-width: thin;
        scrollbar-color: #00d4ff transparent;
    }
    .log-container::-webkit-scrollbar { width: 5px; }
    .log-container::-webkit-scrollbar-track { background: rgba(255, 255, 255, 0.02); border-radius: 10px; }
    .log-container::-webkit-scrollbar-thumb { background: linear-gradient(135deg, #00d4ff, #7b2ffc); border-radius: 10px; }
    .log-success { color: #00d4ff; text-shadow: 0 0 15px rgba(0, 212, 255, 0.15); }
    .log-error { color: #ff006e; text-shadow: 0 0 15px rgba(255, 0, 110, 0.15); }
    .log-info { color: #8888ff; }
    .log-warning { color: #ffd93d; text-shadow: 0 0 15px rgba(255, 217, 61, 0.15); }
    
    .watermark {
        position: fixed;
        bottom: 20px;
        right: 25px;
        opacity: 0.06;
        font-size: 16px;
        color: #00d4ff;
        pointer-events: none;
        z-index: 999;
        font-family: 'Orbitron', sans-serif;
        letter-spacing: 4px;
        font-weight: 700;
    }
    
    .stProgress .st-ba {
        background: linear-gradient(90deg, #00d4ff, #7b2ffc, #ff006e) !important;
        border-radius: 12px;
        height: 8px !important;
        box-shadow: 0 0 30px rgba(0, 212, 255, 0.2);
    }
    .stProgress .st-bg { background: rgba(255, 255, 255, 0.03) !important; border-radius: 12px; }
    
    .footer {
        text-align: center;
        color: #444;
        padding: 2.5rem 1rem;
        border-top: 1px solid rgba(255, 255, 255, 0.02);
        margin-top: 2.5rem;
        background: rgba(0,0,0,0.2);
        border-radius: 20px 20px 0 0;
    }
    .footer .brand {
        font-size: 1.4rem;
        background: linear-gradient(135deg, #00d4ff, #7b2ffc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-family: 'Orbitron', sans-serif;
        letter-spacing: 2px;
    }
    .footer a { color: #00d4ff !important; text-decoration: none; transition: 0.3s; }
    .footer a:hover { color: #7b2ffc !important; text-shadow: 0 0 25px rgba(123, 47, 252, 0.2); }
    
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 14px !important;
        color: white !important;
        padding: 0.9rem 1.2rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        font-family: 'Inter', sans-serif;
    }
    .stTextInput > div > div > input:focus {
        border-color: #00d4ff !important;
        box-shadow: 0 0 40px rgba(0, 212, 255, 0.06), inset 0 0 40px rgba(0, 212, 255, 0.02) !important;
    }
    .stTextInput > div > div > input::placeholder { color: #444 !important; font-weight: 300; }
    
    .stMetric {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.04);
        border-radius: 16px;
        padding: 1.2rem;
        transition: all 0.3s ease;
    }
    .stMetric:hover {
        border-color: rgba(0, 212, 255, 0.15);
        box-shadow: 0 4px 35px rgba(0, 212, 255, 0.04);
    }
    .stMetric label { color: #888 !important; font-weight: 400; }
    .stMetric .stMetricValue { color: #fff !important; font-weight: 700; }
    
    .history-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.03);
        padding: 0.8rem 1rem;
        border-radius: 14px;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
        border-left: 3px solid transparent;
    }
    .history-card:hover {
        border-left-color: #00d4ff;
        background: rgba(0, 212, 255, 0.03);
        transform: translateX(4px);
    }
    .history-card strong { color: #fff; font-weight: 600; }
    .history-card span { color: #444; font-size: 0.7rem; }
    .history-card .count { color: #00d4ff; font-size: 0.85rem; font-weight: 600; }
    
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.02) !important;
        border-radius: 14px !important;
        color: #aaa !important;
        border: 1px solid rgba(255, 255, 255, 0.04) !important;
        font-weight: 500 !important;
        transition: 0.3s ease !important;
    }
    .streamlit-expanderHeader:hover {
        border-color: rgba(0, 212, 255, 0.15) !important;
        background: rgba(0, 212, 255, 0.02) !important;
    }
    
    .sidebar-title {
        color: #666;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 3px;
        font-weight: 700;
        margin: 1rem 0 0.8rem 0;
        opacity: 0.7;
    }
    .upload-box {
        border: 2px dashed rgba(0, 212, 255, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        background: rgba(255, 255, 255, 0.01);
        transition: 0.3s ease;
    }
    .upload-box:hover {
        border-color: rgba(0, 212, 255, 0.2);
        background: rgba(0, 212, 255, 0.02);
    }
</style>
""", unsafe_allow_html=True)

# ========== WATERMARK ==========
st.markdown("""
<div class="watermark">
    ◆ OSINT BOMBER ◆
</div>
""", unsafe_allow_html=True)

# ========== HEADER WITH LOGO ==========
col_logo, col_header = st.columns([1, 4])

with col_logo:
    st.image(
        "https://www.vaadata.com/wp-content/uploads/2026/03/cyber-osint.png",
        width=120
    )

with col_header:
    st.markdown(f"""
    <div style="display: flex; flex-direction: column; justify-content: center; height: 100%; padding: 0.5rem 0;">
        <div class="main-header">
            {T['title']}
        </div>
        <div class="sub-header">
            {T['subtitle']}
        </div>
        <div style="text-align: center;">
            <div class="tagline">
                {T['tagline']}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ========== WARNING ==========
st.markdown(f"""
<div class="warning-box">
    {T['warning'].replace('\n', '<br>')}
</div>
""", unsafe_allow_html=True)

# ========== SIDEBAR ==========
with st.sidebar:
    st.image(
        "https://www.vaadata.com/wp-content/uploads/2026/03/cyber-osint.png",
        width=60
    )
    st.markdown(f"""
    <div style="text-align: center; padding: 0.5rem 0; margin-bottom: 0.5rem;">
        <div style="font-weight: 700; font-size: 1.2rem; 
                     background: linear-gradient(135deg, #00d4ff, #7b2ffc);
                     -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                     font-family: 'Orbitron', sans-serif; letter-spacing: 1px;">
            {T['title']}
        </div>
        <div style="color: #444; font-size: 0.7rem; letter-spacing: 3px;">v3.0 • Professional</div>
        <div style="color: #333; font-size: 0.6rem; margin-top: 0.2rem; letter-spacing: 1px;">⚡ 1000+ Platforms</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ===== SCAN HISTORY =====
    st.markdown(f'<div class="sidebar-title">📜 Scan History</div>', unsafe_allow_html=True)
    recent_scans = get_recent_scans(5)
    if recent_scans:
        for username, timestamp, count in recent_scans:
            st.markdown(f"""
            <div class="history-card">
                <strong>{username}</strong><br>
                <span>{timestamp}</span><br>
                <span class="count">Found: {count} profiles</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No scans yet. Start your first scan!")
    
    st.markdown("---")
    
    # ===== FEATURES =====
    st.markdown(f'<div class="sidebar-title">🚀 Features</div>', unsafe_allow_html=True)
    features = [
        ("🔍", "1000+ Platforms"),
        ("📊", "Real-time Analytics"),
        ("🌍", "GeoIP Location"),
        ("📄", "PDF/TXT/CSV Export"),
        ("📋", "Copy to Clipboard"),
        ("💾", "Scan History"),
        ("🌐", "Multi-Language"),
        ("📂", "File Upload")
    ]
    for icon, text in features:
        st.markdown(f"<div style='color: #888; font-size: 0.85rem; padding: 0.2rem 0;'>{icon} {text}</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ===== STATS =====
    st.markdown(f'<div class="sidebar-title">📊 Live Stats</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🖥️ Sites", "1,000+", delta=None)
    with col2:
        st.metric("🌍 Regions", "50+", delta=None)
    
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: #333; font-size: 0.7rem; letter-spacing: 1px; padding: 0.5rem 0;">
        Made with ❤️<br>
        <span style="color: #222; font-weight: 600;">Python + Streamlit</span>
    </div>
    """, unsafe_allow_html=True)

# ========== MAIN FORM ==========
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(f"""
    <div style="text-align: center; font-size: 1.4rem; font-weight: 700; 
                 background: linear-gradient(135deg, #00d4ff, #7b2ffc);
                 -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                 margin-bottom: 1.2rem; letter-spacing: 2px;">
        {T['enter_details']}
    </div>
    """, unsafe_allow_html=True)
    
    # ===== FILE UPLOAD =====
    with st.expander("📂 " + T['file_upload']):
        st.markdown('<div class="upload-box">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            T['file_upload_help'],
            type=['txt', 'csv'],
            accept_multiple_files=False,
            label_visibility="visible"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        if uploaded_file:
            try:
                content = uploaded_file.read().decode('utf-8')
                usernames = [line.strip() for line in content.splitlines() if line.strip()]
                st.success(f"✅ Found {len(usernames)} usernames in file!")
                st.write("**Usernames:**", ", ".join(usernames[:10]) + ("..." if len(usernames) > 10 else ""))
                st.session_state.uploaded_usernames = usernames
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")
    
    st.markdown(f"<div style='text-align: center; color: #444; margin: 0.5rem 0; font-weight: 300;'>—— {T['or']} ——</div>", unsafe_allow_html=True)
    
    with st.form("scan_form"):
        username = st.text_input(
            T['username'],
            placeholder=T['username_placeholder'],
            help=T['username_help']
        )
        
        email = st.text_input(
            T['email'],
            placeholder=T['email_placeholder'],
            help=T['email_help']
        )
        
        col_a, col_b = st.columns(2)
        with col_a:
            submit = st.form_submit_button(T['start_scan'], use_container_width=True)
        with col_b:
            clear = st.form_submit_button(T['clear'], use_container_width=True)
    
    if clear:
        st.rerun()

# ========== SCAN LOGIC ==========
def run_scan(username, email="", lang="English"):
    T = LANGUAGES[lang]
    
    os.makedirs("output", exist_ok=True)
    
    start_time = time.time()
    
    timer_placeholder = st.empty()
    timer_placeholder.metric("⏱️ " + T['scan_time'], "0.0s")
    
    st.markdown(f"### {T['logs']}")
    log_container = st.container()
    
    progress_bar = st.progress(0)
    progress_text = st.empty()
    progress_text.text(T['initializing'])
    
    results = {}
    logs = []
    total_found = 0
    total_sites = 1000
    
    with log_container:
        st.markdown(f"""
        <div class="log-container">
            <div class="log-info">[INFO] Initializing OSINT Bomber...</div>
        </div>
        """, unsafe_allow_html=True)
    
    def add_log(message, log_type="info"):
        color_map = {
            "success": "log-success",
            "error": "log-error",
            "info": "log-info",
            "warning": "log-warning"
        }
        log_html = f'<div class="{color_map.get(log_type, "log-info")}">[{log_type.upper()}] {message}</div>'
        logs.append(log_html)
        
        with log_container:
            st.markdown(f"""
            <div class="log-container">
                {"".join(logs[-20:])}
            </div>
            """, unsafe_allow_html=True)
        
        elapsed = time.time() - start_time
        timer_placeholder.metric("⏱️ " + T['scan_time'], f"{elapsed:.1f}s")
    
    add_log(f"Starting scan for username: {username}", "info")
    progress_bar.progress(10)
    progress_text.text(T['scanning'])
    
    scanner = OSINTSanner(username)
    
    for step in range(20, 51, 10):
        time.sleep(0.15)
        progress_bar.progress(step)
        add_log(f"Scanning sites... {step}% complete", "info")
    
    results = scanner.scan_all()
    total_found = len(results)
    
    add_log(f"Scan complete! Found {total_found} profiles", "success")
    progress_bar.progress(50)
    progress_text.text(T['processing'])
    
    if results:
        st.success(T['found_profiles'].format(len(results), username))
        add_log(f"Displaying {len(results)} profiles", "info")
        
        col1, col2 = st.columns(2)
        site_list = list(results.items())
        mid = len(site_list) // 2
        
        with col1:
            for site, url in site_list[:mid]:
                st.markdown(f"""
                <div class="result-card">
                    <strong>{site}</strong>
                    <a href="{url}" target="_blank">{url}</a>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            for site, url in site_list[mid:]:
                st.markdown(f"""
                <div class="result-card">
                    <strong>{site}</strong>
                    <a href="{url}" target="_blank">{url}</a>
                </div>
                """, unsafe_allow_html=True)
        
        # Email Check
        email_check_result = None
        if email:
            add_log("Checking email for breaches...", "info")
            progress_text.text(T['checking_email'])
            progress_bar.progress(60)
            
            checker = HIBPChecker(email)
            email_check_result = checker.check()
            progress_bar.progress(65)
            
            if "DANGER" in email_check_result:
                st.error(email_check_result)
                add_log("Email found in data breaches!", "error")
            elif "Good news" in email_check_result:
                st.success(email_check_result)
                add_log("Email is safe!", "success")
            else:
                st.info(email_check_result)
                add_log("Email check completed", "info")
        
        # GeoIP
        add_log("Fetching GeoIP locations...", "info")
        progress_text.text(T['fetching_geoip'])
        progress_bar.progress(70)
        
        geo_checker = GeoIPChecker()
        locations = geo_checker.get_all_locations(results)
        
        if locations:
            add_log(f"GeoIP data fetched for {len(locations)} domains", "success")
        
        # Reports
        add_log("Generating reports...", "info")
        progress_text.text(T['generating_reports'])
        progress_bar.progress(75)
        
        txt_report = scanner.generate_report(email_check_result)
        df = pd.DataFrame(list(results.items()), columns=['Platform', 'URL'])
        csv = df.to_csv(index=False).encode('utf-8')
        
        try:
            pdf_report = PDFReport(username, results, email_check_result)
            pdf_path = pdf_report.generate()
            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()
            add_log("PDF report generated", "success")
        except Exception as e:
            st.warning(f"⚠️ PDF generation error: {str(e)}")
            pdf_bytes = None
            add_log("PDF generation failed", "error")
        
        # Analytics
        add_log("Generating analytics...", "info")
        progress_text.text(T['generating_analytics'])
        progress_bar.progress(85)
        
        categories = {
            'Social Media': ['Twitter', 'Instagram', 'Facebook', 'LinkedIn', 'TikTok', 'Snapchat', 'Reddit', 'Pinterest', 'Tumblr', 'YouTube', 'Telegram', 'Discord', 'Twitch', 'VK', 'OK', 'Weibo'],
            'Developer': ['GitHub', 'GitLab', 'Bitbucket', 'StackOverflow', 'HackerNews', 'LeetCode', 'HackerRank', 'CodeChef', 'TopCoder', 'Kaggle', 'PyPI', 'NPM', 'RubyGems', 'DockerHub'],
            'Creative': ['DeviantArt', 'Behance', 'Dribbble', 'Flickr', 'SoundCloud', 'Spotify', 'Vimeo', 'Imgur'],
            'Professional': ['LinkedIn', 'AngelList', 'ProductHunt', 'Meetup', 'Keybase'],
            'Other': ['Quora', 'Medium', 'Substack', 'Gravatar', 'BuzzFeed', 'Replit', 'CodePen', 'JSFiddle', 'Figma', 'Notion', 'Slack', 'Xing']
        }
        
        category_counts = {}
        for site in results.keys():
            found = False
            for cat, sites in categories.items():
                if site in sites:
                    category_counts[cat] = category_counts.get(cat, 0) + 1
                    found = True
                    break
            if not found:
                category_counts['Other'] = category_counts.get('Other', 0) + 1
        
        # Charts
        st.markdown(f"### {T['analytics']}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"#### {T['platform_dist']}")
            if category_counts:
                fig_pie = px.pie(
                    values=list(category_counts.values()),
                    names=list(category_counts.keys()),
                    title="Profile Distribution by Category",
                    color_discrete_sequence=px.colors.sequential.Plasma
                )
                fig_pie.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    font_family='Inter, sans-serif'
                )
                st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.markdown(f"#### {T['geoip']}")
            if locations:
                map_data = []
                for site, loc in locations.items():
                    if loc:
                        map_data.append({
                            'Site': site,
                            'Lat': loc.get('lat', 0),
                            'Lon': loc.get('lon', 0),
                            'Country': loc.get('country', 'Unknown'),
                            'City': loc.get('city', 'Unknown')
                        })
                
                if map_data:
                    df_map = pd.DataFrame(map_data)
                    fig_map = px.scatter_geo(
                        df_map,
                        lat='Lat',
                        lon='Lon',
                        hover_name='Site',
                        hover_data={'Country': True, 'City': True},
                        title="Server Locations",
                        color='Country',
                        size_max=20
                    )
                    fig_map.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font_color='white',
                        font_family='Inter, sans-serif',
                        geo=dict(
                            showland=True,
                            landcolor='#1a1a2e',
                            coastlinecolor='#333',
                            showocean=True,
                            oceancolor='#0a0a15'
                        )
                    )
                    st.plotly_chart(fig_map, use_container_width=True)
                else:
                    st.info("🌍 No GeoIP data available")
        
        # Download Options
        st.markdown(f"### {T['download_export']}")
        st.markdown("---")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"#### {T['pdf']}")
            st.caption(T['pdf_caption'])
            if pdf_bytes:
                st.download_button(
                    label="📥 Download PDF",
                    data=pdf_bytes,
                    file_name=f"report_{username}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            else:
                st.button("⚠️ Unavailable", disabled=True, use_container_width=True)
            st.caption("Includes all URLs + metadata")
        
        with col2:
            st.markdown(f"#### {T['txt']}")
            st.caption(T['txt_caption'])
            st.download_button(
                label="📥 Download TXT",
                data=txt_report,
                file_name=f"report_{username}.txt",
                mime="text/plain",
                use_container_width=True
            )
            st.caption("Plain text format")
        
        with col3:
            st.markdown(f"#### {T['csv']}")
            st.caption(T['csv_caption'])
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"report_{username}.csv",
                mime="text/csv",
                use_container_width=True
            )
            st.caption("Open in Excel/Sheets")
        
        with col4:
            st.markdown(f"#### {T['copy']}")
            st.caption(T['copy_caption'])
            
            all_links = ""
            for site, url in results.items():
                all_links += f"{site}: {url}\n"
            
            if st.button(T['copy_links'], use_container_width=True):
                try:
                    pyperclip.copy(all_links)
                    st.success(T['copied'])
                    add_log("Links copied to clipboard", "success")
                except:
                    st.warning(T['copy_failed'])
        
        # Quick Copy
        with st.expander(T['view_links']):
            st.markdown(f"### {T['all_profiles']}")
            copy_text = f"OSINT Bomber Report - {username}\n\n"
            for site, url in results.items():
                copy_text += f"{site}: {url}\n"
            st.text_area("Copy all links from here:", copy_text, height=200)
            st.caption("Select all, right-click, and copy")
        
        # Save to Database
        save_scan(username, results, email, total_found)
        add_log(f"Scan saved to database", "success")
        
        # Scan Time
        end_time = time.time()
        scan_duration = end_time - start_time
        
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(f"⏱️ {T['scan_time']}", f"{scan_duration:.2f}s")
        with col2:
            st.metric(f"📊 {T['sites_scanned']}", total_sites)
        with col3:
            st.metric(f"✅ {T['profiles_found']}", total_found)
        with col4:
            st.metric(f"📁 {T['reports']}", "4 Types")
        
        add_log(f"Scan completed in {scan_duration:.2f} seconds", "success")
        
        progress_bar.progress(100)
        progress_text.text("✅ " + T['scan_complete'])
        st.balloons()
        st.success(T['scan_complete'])
        
    else:
        st.warning(T['no_profiles'])
        add_log("No profiles found", "warning")
        save_scan(username, {}, email, 0)
        progress_bar.progress(100)
        progress_text.text("✅ " + T['no_results'])

# ========== MAIN SCAN EXECUTION ==========
if submit and username:
    run_scan(username, email, lang)
elif submit and not username:
    st.error(T['enter_username'])

# ========== BATCH SCAN FROM FILE ==========
if 'uploaded_usernames' in st.session_state and st.session_state.uploaded_usernames:
    if st.button("🚀 " + T['start_scan'] + " (All Usernames)", use_container_width=True):
        for uname in st.session_state.uploaded_usernames:
            st.markdown(f"---")
            st.markdown(f"### 🔍 Scanning: {uname}")
            run_scan(uname, "", lang)

# ========== FOOTER ==========
st.markdown(f"""
<div class="footer">
    <div class="brand">◆ {T['title']} v3.0 ◆</div>
    <div style="color: #444; margin-top: 0.5rem; font-size: 0.9rem;">
        Made with ❤️ using Python & Streamlit | 
        <a href="#">GitHub</a> | 
        <a href="#">Documentation</a>
    </div>
    <div style="color: #333; margin-top: 0.5rem; font-size: 0.8rem;">
        ⚠️ For Educational Purposes Only | Ethical Hacking Tool
    </div>
    <div style="color: #222; margin-top: 0.3rem; font-size: 0.7rem; letter-spacing: 2px;">
        © 2026 OSINT Bomber. All rights reserved.
    </div>
</div>
""", unsafe_allow_html=True)