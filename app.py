import os # API-Key holen
import pandas as pd
import streamlit as st # Web App bauen 
from openai import OpenAI # KI benutzen 


# CSV hochladen → Daten analysieren → anzeigen → KI gibt Empfehlungen

# Titel und Beschreibung der Seite bzw. was der User im Browser sieht 
st.set_page_config(page_title="Bravo AI Analytics", page_icon="🍕")
st.title("AI Restaurant Analytics")
st.write("Upload a restaurant orders CSV file to analyze sales and generate AI recommendations.")

uploaded_file = st.file_uploader("Upload orders.csv", type=["csv"]) # erzeugt upload Button im browser 

# Data Teil
def build_analysis(df: pd.DataFrame):
    df["total"] = df["price"] * df["quantity"] # neue Spalte erstellen 
    df["timestamp"] = pd.to_datetime(df["timestamp"]) # in time data format umwandeln
    df["hour"] = df["timestamp"].dt.hour  # Stunden extrahieren 

    total_revenue = df["total"].sum() # Gesamtumsatz berechnen 
    top_items = (
        df.groupby("item_name")["total"]
        .sum()
        .sort_values(ascending=False) # Umsatz pro Gericht 
    )
    popular_items = df["item_name"].value_counts() # wird oft bestellt
    order_types = df["order_type"].value_counts() # delivery vs pickup
    peak_hours = df["hour"].value_counts().sort_index() # Stoßzeiten 

    return {
        # alles wird gesammelt zurückgegeben
        "df": df,
        "total_revenue": total_revenue,
        "top_items": top_items,
        "popular_items": popular_items,
        "order_types": order_types,
        "peak_hours": peak_hours,
    }

# KI Teil
def build_prompt(results):
    top_items = results["top_items"].to_string() # in Text umwandeln 
    popular_items = results["popular_items"].to_string()
    order_types = results["order_types"].to_string()
    peak_hours = results["peak_hours"].to_string()
    total_revenue = results["total_revenue"]

# prompt für KI bauen 
    return f"""
Du bist ein Restaurantberater.

Analysiere die folgenden Kennzahlen eines Restaurants und gib:
1. 3 konkrete Verbesserungsvorschläge
2. 2 Ideen zur Umsatzsteigerung
3. 2 Hinweise zur Personalplanung

Bleibe konkret, kurz und praxisnah.

Daten:
Top Gerichte nach Umsatz:
{top_items}

Beliebteste Gerichte nach Anzahl:
{popular_items}

Delivery vs Pickup:
{order_types}

Bestellungen pro Stunde:
{peak_hours}

Gesamtumsatz:
{total_revenue:.2f} Euro
"""

if uploaded_file is not None: # Nur wenn User Datei hochlädt 
    try:
        df = pd.read_csv(uploaded_file) # CSV einlesen 
        results = build_analysis(df) # Analyse führen und Dictionary in results speichern 

        # Daten anzeigen 
        st.subheader("Kennzahlen")
        col1, col2 = st.columns(2)
        col1.metric("Gesamtumsatz", f'{results["total_revenue"]:.2f} €')
        col2.metric("Anzahl Bestellungen", len(results["df"])) # len(df) = Anzahl Zeilen (Bestellungen)

        st.subheader("Top Gerichte nach Umsatz")
        st.dataframe(results["top_items"].reset_index(name="revenue")) # zeigt Tabellen im Browser bzw. macht normales Format zu Tabelle

        st.subheader("Beliebteste Gerichte nach Anzahl")
        st.dataframe(results["popular_items"].reset_index(name="count"))

        st.subheader("Delivery vs Pickup")
        st.bar_chart(results["order_types"]) # zeigt Diagramme

        st.subheader("Bestellungen pro Stunde")
        st.bar_chart(results["peak_hours"])

        st.subheader("KI-Empfehlungen")
        if st.button("Generate AI Recommendations"): # User klickt KI Button
            api_key = os.getenv("OPENAI_API_KEY") # API Key holen 
            if not api_key:
                st.error("OPENAI_API_KEY ist nicht gesetzt.")
            else:
                client = OpenAI(api_key=api_key) # Verbindung zur KI hertsellen 
                prompt = build_prompt(results)

                with st.spinner("KI analysiert die Daten..."): # zeigt Lade-Kreis + Text während API läuft und User wartet
                    response = client.responses.create(
                        model="gpt-4.1-mini",
                        input=prompt # das was man der KI als Input gibt (Text)
                    ) # Anfrage an KI schicken 

                st.success("Analyse fertig")
                st.write(response.output_text) # zeigt Antwort im Browser

        with st.expander("Prompt anzeigen"): # man kann sehen, was an KI geschickt wird, expander = einklappbar
            st.code(build_prompt(results)) # zeigt den KI-Prompt schön formatiert 

    except Exception as e:
        st.error(f"Fehler beim Verarbeiten der Datei: {e}")
else:
    st.info("Bitte lade eine CSV-Datei hoch.")


    