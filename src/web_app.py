import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def insert_colored_text(text, content, color, weight="normal"):
    """
    Fügt farbigen HTML-Text zu einem bestehenden Textstring hinzu.

    Args:
        text (str): Der vorhandene Text, zu dem der farbige Text hinzugefügt wird.
        content (str): Der farbige Textinhalt.
        color (str): Die Farbe des Textes (z.B. "red", "#ff0000").
        weight (str, optional): Schriftgewicht, "bold" für fett, sonst normal. Standard ist "normal".

    Returns:
        str: Der kombinierte Text mit farbigem HTML-Text.
    """
    weight_style = "font-weight:bold;" if weight=="bold" else ""
    colored_content = f'<div style="color:{color}; {weight_style} text-align:center;">{content}</div>'
    return text + colored_content + "\n"

def calculate_rebalancing(names, worths, allocations, saving_rate):
    """
    Berechnet das Rebalancing eines ETF-Portfolios.

    Args:
        names (list of str): Namen der ETFs.
        worths (list of float): Aktueller Wert der ETFs.
        allocations (list of float): Zielallokation in Prozent.
        saving_rate (float): Monatliche Sparrate in Euro.

    Returns:
        tuple:
            trade_text (str): Text mit Kauf-/Verkaufsempfehlungen für Rebalancing.
            adjust_text (str): Text mit Sparratenanpassungsempfehlungen.
            dicts (list of dict): Liste mit ETF-Daten inklusive Sollwerten.
            total_worth (float): Gesamtwert des Portfolios.
    """
    total_worth = sum(worths)
    dicts = []
    for i, name in enumerate(names):
        d = {
            'name': name,
            'alloc': allocations[i],
            'worth': worths[i],
            'worth_soll': total_worth * (allocations[i] / 100)
        }
        dicts.append(d)
    
    hyphen_number = 80

    # Trade-Rebalancing (Buy/Sell)
    trade_text = "-" * hyphen_number + "\n"
    trade_text += "Rebalancing through Buy/Sell:\n"
    trade_text += "-" * hyphen_number + "\n"

    perc_diff_list = []
    for d in dicts:
        if d['worth_soll'] == 0:
            perc_diff_list.append(0)
        else:
            perc_diff_list.append(d['worth'] / d['worth_soll'])

        if d['worth_soll'] == d['worth']:
            trade_text += f"Do not trade {d['name']}\n"
        elif d['worth_soll'] > d['worth']:
            trade_text += f"Buy {round(d['worth_soll'] - d['worth'])}€ of {d['name']}\n"
        elif d['worth_soll'] < d['worth']:
            trade_text += f"Sell {round(d['worth'] - d['worth_soll'])}€ of {d['name']}\n"

    trade_text += "-" * hyphen_number + "\n"
    trade_text += "-" * hyphen_number + "\n"
    trade_text += f"⮞⮞⮞ Portfolio Value: {round(total_worth)}€ ⮜⮜⮜\n"
    trade_text += "-" * hyphen_number + "\n"
    trade_text += "-" * hyphen_number + "\n"

    # Saving rate adaptation
    adjust_text = "-" * hyphen_number + "\n"
    adjust_text += "Rebalancing through saving rate adaptation:\n"
    adjust_text += "-" * hyphen_number + "\n"
    adjust_text += f"Adjusting rates on {dicts[perc_diff_list.index(max(perc_diff_list))]['name']}....\n"
    adjust_text += "-" * hyphen_number + "\n"

    total_difference = 0
    for d in dicts:
        if d['worth_soll'] == 0:
            continue
        elif d == dicts[perc_diff_list.index(max(perc_diff_list))]:
            continue
        else:
            d['worth_soll_new'] = d['worth_soll'] * max(perc_diff_list)
            total_difference += d['worth_soll_new'] - d['worth']

    for d in dicts:
        if d['worth_soll'] == 0:
            adjust_text += f"Allocation of {d['name']} is 0, excluded\n"
        elif d == dicts[perc_diff_list.index(max(perc_diff_list))]:
            adjust_text += f"Adjust rate of {d['name']} to 0€\n"
        else:
            new_rate = round((saving_rate * (d['worth_soll_new'] - d['worth'])) / total_difference) if total_difference != 0 else 0
            adjust_text += f"Adjust rate of {d['name']} to {new_rate}€\n"

    adjust_text += "-" * hyphen_number + "\n"
    months = round(total_difference / saving_rate) if saving_rate != 0 else 0
    adjust_text += f"Time to Adjust: {months} Months....\n"
    adjust_text += "-" * hyphen_number + "\n"

    return trade_text, adjust_text, dicts, total_worth

def show_plots(dicts, total_worth):
    """
    Zeigt zwei Donut-Diagramme der aktuellen und Ziel-Portfoliobewertungen.

    Args:
        dicts (list of dict): Liste mit ETF-Daten.
        total_worth (float): Gesamtwert des Portfolios.
    """
    labels = [d['name'] for d in dicts]
    current_values = [d['worth'] for d in dicts]
    target_values = [d['worth_soll'] for d in dicts]

    fig, axs = plt.subplots(1, 2, figsize=(12, 6))

    # Donut chart - aktueller Stand
    wedges1, texts1, autotexts1 = axs[0].pie(current_values, labels=labels, autopct='%1.1f%%', startangle=0,
                                            pctdistance=1.2, labeldistance=1.05, wedgeprops=dict(width=0.5))
    axs[0].set_title("Current Allocation")

    # Donut chart - Ziel-Allokation
    wedges2, texts2, autotexts2 = axs[1].pie(target_values, labels=labels, autopct='%1.1f%%', startangle=0,
                                            pctdistance=1.2, labeldistance=1.05, wedgeprops=dict(width=0.5))
    axs[1].set_title("Target Allocation")

    st.pyplot(fig)

def main():
    """
    Hauptfunktion der Streamlit Web-App für ETF Rebalancing.
    Fragt Benutzereingaben ab, berechnet Rebalancing und zeigt Ergebnisse an.
    """
    st.title("ETF Rebalancing Calculator")

    number_of_etfs = st.number_input("Number of ETFs", min_value=2, max_value=20, value=2, step=1)

    names = []
    worths = []
    allocations = []
    
    saving_rate = st.number_input("Saving rate (€ per month)", min_value=0.0, step=1.0, value=100.0)

    for i in range(number_of_etfs):
        st.markdown(f"### ETF {i+1}")
        name = st.text_input(f"ETF Name", value=f"ETF {i+1}", key=f"name_{i}")
        worth = st.number_input(f"Current ETF worth (€)", min_value=0.0, step=0.01, value=1000.0, key=f"worth_{i}")
        alloc = st.number_input(f"Target Allocation (%)", min_value=0.0, max_value=100.0, step=0.1, value=round(100/number_of_etfs, 2), key=f"alloc_{i}")

        names.append(name)
        worths.append(worth)
        allocations.append(alloc)


    if st.button("Calculate Rebalancing"):
        # Validations
        if sum(worths) == 0:
            st.error("You have nothing in your portfolio?! Why are you using this application?")
            return
        if round(sum(allocations), 2) != 100:
            st.error("Allocations must add up to 100%.")
            return

        trade_text, adjust_text, dicts, total_worth = calculate_rebalancing(names, worths, allocations, saving_rate)

        st.subheader("Rebalancing through Buy/Sell")
        st.text(trade_text)

        st.subheader("Rebalancing through saving rate adaptation")
        st.text(adjust_text)

        st.subheader("Portfolio Allocation Donut Charts")
        show_plots(dicts, total_worth)

if __name__ == "__main__":
    main()
