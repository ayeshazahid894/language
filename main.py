import streamlit as st
from deep_translator import GoogleTranslator
from langdetect import detect, DetectorFactory
import pandas as pd
import csv
import os
from datetime import datetime

DetectorFactory.seed = 0

# Languages
LANGS = {
    'auto': 'Auto Detect',
    "af": "Afrikaans",
    "sq": "Albanian",
    "am": "Amharic",
    "ar": "Arabic",
    "hy": "Armenian",
    "az": "Azerbaijani",
    "eu": "Basque",
    "be": "Belarusian",
    "bn": "Bengali",
    "bs": "Bosnian",
    "bg": "Bulgarian",
    "ca": "Catalan",
    "ceb": "Cebuano",
    "ny": "Chichewa",
    "zh-cn": "Chinese (Simplified)",
    "zh-tw": "Chinese (Traditional)",
    "co": "Corsican",
    "hr": "Croatian",
    "cs": "Czech",
    "da": "Danish",
    "nl": "Dutch",
    "en": "English",
    "eo": "Esperanto",
    "et": "Estonian",
    "tl": "Filipino",
    "fi": "Finnish",
    "fr": "French",
    "fy": "Frisian",
    "gl": "Galician",
    "ka": "Georgian",
    "de": "German",
    "el": "Greek",
    "gu": "Gujarati",
    "ht": "Haitian Creole",
    "ha": "Hausa",
    "haw": "Hawaiian",
    "he": "Hebrew",
    "hi": "Hindi",
    "hmn": "Hmong",
    "hu": "Hungarian",
    "is": "Icelandic",
    "ig": "Igbo",
    "id": "Indonesian",
    "ga": "Irish",
    "it": "Italian",
    "ja": "Japanese",
    "jw": "Javanese",
    "kn": "Kannada",
    "kk": "Kazakh",
    "km": "Khmer",
    "rw": "Kinyarwanda",
    "ko": "Korean",
    "ku": "Kurdish (Kurmanji)",
    "ky": "Kyrgyz",
    "lo": "Lao",
    "la": "Latin",
    "lv": "Latvian",
    "lt": "Lithuanian",
    "lb": "Luxembourgish",
    "mk": "Macedonian",
    "mg": "Malagasy",
    "ms": "Malay",
    "ml": "Malayalam",
    "mt": "Maltese",
    "mi": "Maori",
    "mr": "Marathi",
    "mn": "Mongolian",
    "my": "Myanmar (Burmese)",
    "ne": "Nepali",
    "no": "Norwegian",
    "or": "Odia",
    "ps": "Pashto",
    "fa": "Persian",
    "pl": "Polish",
    "pt": "Portuguese",
    "pa": "Punjabi",
    "ro": "Romanian",
    "ru": "Russian",
    "sm": "Samoan",
    "gd": "Scots Gaelic",
    "sr": "Serbian",
    "st": "Sesotho",
    "sn": "Shona",
    "sd": "Sindhi",
    "si": "Sinhala",
    "sk": "Slovak",
    "sl": "Slovenian",
    "so": "Somali",
    "es": "Spanish",
    "su": "Sundanese",
    "sw": "Swahili",
    "sv": "Swedish",
    "tg": "Tajik",
    "ta": "Tamil",
    "tt": "Tatar",
    "te": "Telugu",
    "th": "Thai",
    "tr": "Turkish",
    "tk": "Turkmen",
    "uk": "Ukrainian",
    "ur": "Urdu",
    "ug": "Uyghur",
    "uz": "Uzbek",
    "vi": "Vietnamese",
    "cy": "Welsh",
    "xh": "Xhosa",
    "yi": "Yiddish",
    "yo": "Yoruba",
    "zu": "Zulu"
}

NAME_TO_CODE = {v: k for k, v in LANGS.items()}
HISTORY_FILE = 'translation_history.csv'

# Functions 
def detect_language(text):
    try:
        return detect(text)
    except:
        return None

def translate_text(text, source_code, target_code):
    if not text.strip():
        return ''
    try:
        return GoogleTranslator(source=source_code, target=target_code).translate(text)
    except Exception as e:
        return f"[ERROR] {e}"

def save_history(src, tgt, src_text, translated):
    exists = os.path.exists(HISTORY_FILE)
    with open(HISTORY_FILE, 'a', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        if not exists:
            w.writerow(['timestamp','source','target','source_text','translated_text'])
        w.writerow([datetime.utcnow().isoformat(), src, tgt, src_text, translated])

st.set_page_config(page_title="Language Translator", layout="wide")
st.title("🌐 Language Translator")

col1, col2 = st.columns([3,1])

with col1:
    src_text = st.text_area("Enter Text", height=200)

    col_ctrl1, col_ctrl2, col_ctrl3 = st.columns([1,1,1])
    with col_ctrl1:
        from_lang = st.selectbox("From", list(LANGS.values()), index=list(LANGS.values()).index("Auto Detect"))
    with col_ctrl2:
        to_lang = st.selectbox("To", [v for k,v in LANGS.items() if k!="auto"], index=list(LANGS.values()).index("English")-1)
    with col_ctrl3:
        if st.button("Detect Language"):
            code = detect_language(src_text)
            lang_name = LANGS.get(code, "Unknown")
            st.info(f"Detected language: {lang_name} ({code})")

    if st.button("Translate →"):
        src_code = NAME_TO_CODE.get(from_lang, 'auto')
        tgt_code = NAME_TO_CODE.get(to_lang, 'en')
        translated = translate_text(src_text, src_code, tgt_code)
        st.text_area("Translated Text", value=translated, height=200)
        save_history(from_lang, to_lang, src_text, translated)

with col2:
    st.subheader("Tools")
    if os.path.exists(HISTORY_FILE):
        if st.button("Show History"):
            df = pd.read_csv(HISTORY_FILE)
            st.dataframe(df)
    if st.button("Download History CSV"):
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "rb") as f:
                st.download_button("Download CSV", data=f, file_name="translation_history.csv")

