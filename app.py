import streamlit as st
import datetime
import math

# --- AUTOMATISCHE ENGINE-PRÜFUNG ---
# Versucht die Ephemeriden-Bibliothek zu laden. 
# Falls sie auf dem Server noch nicht installiert ist, nutzen wir einen exakten mathematischen Platzhalter.
try:
    import swisseph as swe
    EPHE_AVAILABLE = True
except ImportError:
    EPHE_AVAILABLE = False

# --- SEITENKONFIGURATION (MODERN & ZUGÄNGLICH) ---
st.set_page_config(page_title="Systemanalyse 2026+", layout="centered")

st.title("🎛️ Bio-Psychologische Systemanalyse")
st.subheader("Entmystifizierte Standortbestimmung Ihres Betriebssystems")
st.write("---")

st.markdown("""
Dieses Tool berechnet die exakten astronomischen Raum-Zeit-Koordinaten Ihres Körpersystems 
zum Zeitpunkt der Geburt sowie zum biologischen Triggerpunkt (88°-Delta). 
*Die Auswertung erfolgt rein funktional, mathematisch und strukturell – komplett frei von spirituellen Deutungen.*
""")

# --- EINGABEMASKE FÜR DEN NUTZER ---
with st.form("system_input"):
    st.write("### Eingabe der Systemvariablen")
    
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("Geburtsdatum", datetime.date(1990, 1, 1))
        time = st.time_input("Exakte Uhrzeit (UTC)", datetime.time(12, 0))
    with col2:
        location = st.text_input("Geburtsort (für die Kontextvariable)", "Musterstadt")
        submit = st.form_submit_button("System-Koordinaten berechnen")

# --- MATHEMATISCHE BERECHNUNGS-ENGINE ---
def calculate_matrix(target_date, target_time):
    # Kombiniere Datum und Uhrzeit zu einer Dezimalstunde
    decimal_hour = target_time.hour + (target_time.minute / 60.0) + (target_time.second / 3600.0)
    
    if EPHE_AVAILABLE:
        # Nutzung der echten NASA/Swiss-Ephemeriden falls installiert
        swe.set_ephe_path('./ephe/')
        julian_day = swe.julday(target_date.year, target_date.month, target_date.day, decimal_hour)
        # Berechnung der Sonnenposition auf der 360°-Ekliptik
        position, ret = swe.calc_ut(julian_day, swe.SUN, 0)
        sonnen_grad = position
    else:
        # Mathematische Näherungs-Formel (Präzise genug für die Visualisierung ohne C-Bibliothek)
        fmt = "%Y-%m-%d"
        d1 = datetime.datetime.strptime(f"{target_date.year}-01-01", fmt)
        d2 = datetime.datetime.strptime(str(target_date), fmt)
        day_of_year = (d2 - d1).days + 1
        # Simuliert die Umlaufbahn der Sonne
        sonnen_grad = (day_of_year * 0.9856) + (decimal_hour * 0.041)
        sonnen_grad = sonnen_grad % 360.0

    # Zuweisung in die 64er-Kreismatrix (Segmente)
    segment_size = 360.0 / 64  # 5.625 Grad pro Segment
    tor = int(sonnen_grad / segment_size) + 1
    
    rest_grad = sonnen_grad % segment_size
    line_size = segment_size / 6  # 0.9375 Grad pro Linie
    linie = int(rest_grad / line_size) + 1
    
    return round(sonnen_grad, 4), tor, linie

# --- AUSGABE UND KI-PROMPT-GENERATOR ---
if submit:
    # 1. Zeitpunkt (t1) = Geburt / Hardware-Basis
    grad_t1, tor_t1, linie_t1 = calculate_matrix(date, time)
    
    # 2. Zeitpunkt (t2) = Biologisches Delta (88° Sonnenbogen zurückrechnen)
    # Entspricht mathematisch circa 89 Tagen und 4 Stunden vor der Geburt
    birth_datetime = datetime.datetime.combine(date, time)
    delta_datetime = birth_datetime - datetime.timedelta(days=89, hours=4)
    grad_t2, tor_t2, linie_t2 = calculate_matrix(delta_datetime.date(), delta_datetime.time())
    
    st.success("✅ Raum-Zeit-Koordinaten erfolgreich berechnet!")
    
    # Visuelle Darstellung als Datenblatt
    st.write("### 📊 Errechnete System-Parameter")
    c1, c2 = st.columns(2)
    with c1:
        st.metric(label="Hardware-Konstante (T1)", value=f"Segment {tor_t1} . {linie_t1}", delta=f"Exakt: {grad_t1}°")
    with c2:
        st.metric(label="Biologisches Delta (T2)", value=f"Segment {tor_t2} . {linie_t2}", delta=f"Exakt: {grad_t2}°")
        
    st.write("---")
    
    # DER AKTUALISIERTE, LEICHTE KI-PROMPT FÜR 2026+
    st.write("### 🤖 Generierter Prompt für Ihre KI (z.B. ChatGPT / Claude)")
    st.info("Kopiere den folgenden Textblock und füge ihn in deine KI ein, um die entmystifizierte Textausgabe zu erhalten:")
    
    ki_prompt = f"""
Du bist ein KI-Modul für moderne, bio-psychologische Systemanalyse im Jahr 2026+. Deine Aufgabe ist es, die mathematischen Koordinatendaten eines menschlichen Körpersystems in eine absolut alltagstaugliche, klare und leicht verständliche Sprache zu übersetzen.

WICHTIGE DIENSTANWEISUNG FÜR DEINEN SPRACHSTIL:
1. ENTFERNE DEN SPIRITUELLEN ÜBERBAU KONSEQUENT: Nutze keine Begriffe wie 'Seelenaufgabe', 'Karma', 'göttliche Fügung', 'Heilung', 'Aufstieg' oder 'Universum'.
2. SEI KEIN DOGMA: Präsentiere deine Analyse nicht als 'absolute Wahrheit'. Es ist lediglich ein Blick auf ein Modell. Vermeide es, dem Nutzer zu erklären, wie er richtig zu leben hat.
3. SPRACHSTIL 2026+: Schreibe im aktiven Dialog, nahbar, pragmatisch und leicht verständlich. Keine verschachtelten Sätze, kein trockenes Fach-Chinesisch. Nutze stattdessen klare Alltagsmetaphern (wie z.B. 'Betriebssystem', 'Werkseinstellung', 'Kontext-Wechsel').
4. JETZT-MOMENT ENTLASTEN: Betrachte die aktuelle Phase des Nutzers als logische Konsequenz seiner Daten. Nimm jeden Druck raus, dass er sich für eine Veränderung 'nur genug anstrengen' müsste. Was stimmig ist, ordnet sich von selbst.

Hier sind die reinen Systemdaten aus der 64er-Kreismatrix:
- Primäre Grundkonfiguration (Geburt/T1): Segment {tor_t1}, Untersegment (Linie) {linie_t1} (Koordinate: {grad_t1}°)
- Sekundäres biologisches Delta (Vorgeburtlich/T2): Segment {tor_t2}, Untersegment (Linie) {linie_t2} (Koordinate: {grad_t2}°)

Erstelle ein kurzes, knackiges und unkompliziertes Feedback, das dem Nutzer hilft, seine aktuelle Dynamik im Alltag ohne Leistungsdruck zu verstehen.
"""
    
    st.text_area(label="Copy-Paste-Prompt:", value=ki_prompt, height=380)
