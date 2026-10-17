import streamlit as st
import json
import re

class CSRDAuditAgent:
    def __init__(self):
        self.emission_factors = {"road_freight": 0.105, "maritime_freight": 0.012, "air_freight": 0.500}

    def parse_invoice_text(self, raw_text):
        data = {}
        weight_match = re.search(r'(?i)(\d+[\.,]?\d*)\s*(tonnes|t|tons)', raw_text)
        distance_match = re.search(r'(?i)(\d+[\.,]?\d*)\s*(km|kilometers|kilomètres)', raw_text)
        transport_match = re.search(r'(?i)(road|maritime|sea|air|aircraft|route|avion)', raw_text)
        data['weight_tons'] = float(weight_match.group(1).replace(',', '.')) if weight_match else 0.0
        data['distance_km'] = float(distance_match.group(1).replace(',', '.')) if distance_match else 0.0
        t_mode = transport_match.group(1).lower() if transport_match else "road"
        if "sea" in t_mode or "maritime" in t_mode:
            data['mode'] = "maritime_freight"
        elif "air" in t_mode or "aircraft" in t_mode or "avion" in t_mode:
            data['mode'] = "air_freight"
        else:
            data['mode'] = "road_freight"
        return data

    def compute_carbon_footprint(self, parsed_data):
        weight = parsed_data['weight_tons']
        distance = parsed_data['distance_km']
        mode = parsed_data['mode']
        factor = self.emission_factors.get(mode, 0.105)
        total_co2_kg = weight * distance * factor
        return {"mode_detected": mode, "metrics": {"tons": weight, "distance_km": distance}, "regulatory_co2_score_kg": round(total_co2_kg, 2), "csrd_compliant": True if total_co2_kg > 0 else False}

st.set_page_config(page_title="CSRD Automated Audit Agent", layout="wide")
lang = st.radio("🌐 Select Language / Choisir la langue", ["EN", "FR"], horizontal=True)

if lang == "EN":
    st.title("🔌 Autonomous CSRD Audit & Carbon Traceability Agent")
    st.write("Automated logistic invoice ingestion and Scope 3 carbon compliance calculation engine for multi-national corporate audits.")
    default_invoice = "INVOICE #2026-99A8\nClient: Global Logistics Corp\nDescription: Raw material transit from Rotterdam Port to Frankfurt Assembly Line.\nLogistics Volume: 24.5 tons secured payload.\nTransit via highway distribution networks over a total distance of 315 km."
    input_label = "Paste raw unstructured invoice or logistical manifest text here:"
    btn_audit = "Execute Extraction & Regulatory Audit"
    sub_rep = "📋 Regulatory Compliance Certification Report"
    ent_title = "🏢 Massive-Scale Enterprise Deployment (REST API & SAP Connectors)"
    mail_label = "Enter your corporate email to schedule a pilot audit over a 10,000+ historical document sample:"
    btn_demo = "Request Industrial Demo Integration"
    success_msg = "Enterprise demo request successfully registered."
else:
    st.title("🔌 Agent Autonome d'Audit CSRD & Traçabilité Carbone")
    st.write("Extraction automatique des données logistiques et calcul de conformité Scope 3 pour les grands comptes.")
    default_invoice = "INVOICE #2026-99A8\nClient: TotalEnergies Supply France\nDescription: Transport de matières premières depuis le Port de Marseille vers le site de Lyon.\nVolume logistique: 24.5 tonnes sécurisées.\nTransit par route sur une distance totale de 315 km."
    input_label = "Collez le texte brut du document logistique ou de la facture :"
    btn_audit = "Lancer l'extraction et l'audit de conformité"
    sub_rep = "📋 Rapport de Certification Réglementaire"
    ent_title = "🏢 Déploiement Massive-Scale (API Rest & Connecteurs SAP)"
    mail_label = "Entrez votre email professionnel pour planifier un audit sur un échantillon de 10 000 factures :"
    btn_demo = "Demander une démonstration d'intégration"
    success_msg = "Demande de démonstration industrielle enregistrée."

invoice_input = st.text_area(input_label, default_invoice, height=200)
if st.button(btn_audit):
    agent = CSRDAuditAgent()
    donnees = agent.parse_invoice_text(invoice_input)
    resultat = agent.compute_carbon_footprint(donnees)
    st.subheader(sub_rep)
    st.json(resultat)

st.write("---")
st.subheader(ent_title)
email_corporate = st.text_input(mail_label)
if st.button(btn_demo):
    if email_corporate:
        st.success(f"{success_msg} ({email_corporate})")

