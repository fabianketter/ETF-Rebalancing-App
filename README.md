# Rebalancing-Rechner mit Sparratenanpassung
Dieses Tool berechnet, wie Portfolios entweder durch **hartes Rebalancing** (kaufen und verkaufen) oder durch **softes Rebalancing** (Sparratenanpassung) wieder in ihre Zielallokation gebracht werden können.

## Features
- Hartes Rebalancing (Käufe und Verkäufe)
- Softes Rebalancing (Sparratenanpassung)
- Einfache grafische Benutzeroberfläche (Tkinter)
- Web App basierend auf Streamlit für einfache Nutzung im Browser
- .exe-Datei für Nutzung ohne Python-Installation (erstellt mit PyInstaller)
- Grafische Darstellung der aktuellen- und Zielallokation

## Installation
1. Python (Version 3.7 oder höher) installieren
2. Abhängigkeiten installieren
```bash
pip install -r requirements.txt
```
3. Desktop-App starten (Tkinter GUI):
```bash
python src/main.pyw
```
4. Web-App starten (Streamlit)
```bash
streamlit run src/web_app.py
```
## Nutzung
- Desktop-App: Einfach main.pyw starten, Werte eingeben, Rebalancing durchführen
- Web-App: Browser öffnet sich automatisch beim Start mit Streamlit, interaktive Nutzung
- Optional kannst das tool mit der dist/Rebalancing.exe Datei ohne Python verwendet werden

## Hinweise
- Das Tool ist für Privatanleger gedacht, die ihre Portfolios rebalancen möchten
- Die Berechnung basiert auf aktuellen Depotwerten und definierten Zielallokationen

## Lizenz
- Dieses Projekt steht unter der MIT-Lizenz. Siehe LICENSE für Details.

## Kontakt
- Bei Fragen oder Feedback kannst du mich gerne kontaktieren:
- Fabian Ketter 
- fabianketter99@gmail.com
- github.com/fabianketter

