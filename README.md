# AI Restaurant Analytics

Dieses Projekt ist eine Webanwendung zur Analyse von Restaurant-Bestelldaten mit anschließender Generierung von Handlungsempfehlungen mithilfe von KI.

## Funktionen

- Upload einer CSV-Datei mit Bestelldaten
- Analyse von:
  - Gesamtumsatz
  - Beliebtesten Gerichten
  - Umsatz pro Gericht
  - Bestellungen pro Stunde (Stoßzeiten)
  - Verhältnis von Lieferung zu Abholung
- Automatische Generierung von Verbesserungsvorschlägen durch KI

## Technologien

- Python
- Pandas (Datenanalyse)
- Streamlit (Web-App)
- OpenAI API (KI-Integration)

## Beispiel-Insights

- Identifikation von Top-Sellern
- Erkennung von Stoßzeiten
- Analyse von Bestellverhalten (Delivery vs Pickup)

## Anwendung starten

1. Abhängigkeiten installieren:
pip install pandas streamlit openai

2. App starten:
streamlit run app.py

3. CSV-Datei hochladen und analysieren

    Die CSV-Datei sollte folgende Spalten enthalten:
    order_id, timestamp, item_name, category, price, quantity, order_type

## Ziel des Projekts: 
-  aus einfachen Bestelldaten sinnvolle Erkenntnisse ableiten und diese durch KI in konkrete Handlungsempfehlungen übersetzen
