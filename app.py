import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# Configuration de la page
st.set_page_config(
    page_title="ClearTerms", 
    page_icon="⚖️", 
    layout="centered"
)

# 🔑 CONFIGURATION DE TES INFOS :
MA_CLE_API = st.secrets["AIzaSyCmZWtF8k2n61a690y7kBbaj9-eXZ0MlHk"]
st.write(f"Clé détectée (début) : {MA_CLE_API[:7]}")
MON_EMAIL_BUSINESS = "contact@clearterms.com"

# Configuration automatique de l'API avec ta clé
genai.configure(api_key=MA_CLE_API)

# --- BARRE LATÉRALE ---
st.sidebar.header("🏢 À propos de ClearTerms")
st.sidebar.write("Une idée de partenariat ? Un bug à signaler ? Contactez notre équipe business :")
st.sidebar.info(f"📧 **{MON_EMAIL_BUSINESS}**")

# --- CORPS DE LA PAGE ---
st.title("⚖️ ClearTerms")
st.subheader("Traduisez le jargon juridique en clair et évitez les pièges.")
st.write("Analyse instantanée de vos documents juridiques (Texte, PDF ou Image).")

# Liste des catégories pour cibler les offres partenaires
categories = [
    "🔍 Détection automatique",
    "🌐 Web, Tech & Apps (CGU, CGV, Confidentialité)",
    "🛒 Vie quotidienne & Consommation (Abonnements, Assurances)",
    "🏠 Logement & Immobilier (Bail, Colocation, Vente)",
    "💼 Travail & Professionnel (Contrat de travail, NDA, Freelance)",
    "❤️ Vie privée & Famille (Mariage, PACS, Donation)"
]

type_document = st.selectbox("Quel type de document voulez-vous analyser ?", categories)

# Organisation de l'interface avec des onglets (Tabs)
onglet_texte, onglet_pdf, onglet_image = st.tabs([
    "📝 Copier-coller du texte", 
    "📄 Fichier PDF", 
    "📸 Image / Photo"
])

contenu_gemini = None

# --- ONGLET 1 : TEXTE ---
with onglet_texte:
    texte_contrat = st.text_area(
        "Collez le texte du document ici :", 
        height=300, 
        placeholder="Copiez-collez le texte complet ici..."
    )
    if texte_contrat.strip():
        contenu_gemini = texte_contrat

# --- ONGLET 2 : PDF ---
with onglet_pdf:
    fichier_pdf = st.file_uploader("Glissez-déposez votre fichier PDF ici :", type=["pdf"])
    if fichier_pdf is not None:
        st.success(f"📄 Fichier chargé : {fichier_pdf.name}")
        pdf_data = fichier_pdf.getvalue()
        contenu_gemini = {
            "mime_type": "application/pdf",
            "data": pdf_data
        }

# --- ONGLET 3 : IMAGE ---
with onglet_image:
    fichier_image = st.file_uploader("Glissez-déposez ou photographiez le contrat :", type=["png", "jpg", "jpeg"])
    if fichier_image is not None:
        image = Image.open(fichier_image)
        st.image(image, caption="Aperçu du document", use_container_width=True)
        contenu_gemini = image

# Bouton d'analyse commun
st.markdown("---")
if st.button("🚀 Analyser avec ClearTerms", use_container_width=True):
    if MA_CLE_API == "METS_TA_CLE_API_ICI" or not MA_CLE_API:
        st.error("⚠️ Erreur de configuration : Tu as oublié de remplacer 'METS_TA_CLE_API_ICI' par ta vraie clé API dans le code Python ! (Ligne 12)")
    elif contenu_gemini is None:
        st.warning("⚠️ Aucun document fourni. Veuillez coller du texte ou importer un fichier (PDF/Image).")
    else:
        with st.spinner("🔮 ClearTerms décrypte ton document... Patiente deux secondes..."):
            try:
                # Utilisation du modèle gemini-2.5-flash
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                # Le Prompt ClearTerms avec une forte personnalité (Tone Hack)
                prompt_systeme = f"""
                Tu es le grand frère / la grande sœur de l'utilisateur, un expert tech ultra-génial et cash, qui décrypte les contrats pour son pote. Tu parles de manière directe, moderne et percutante (tu dois tutoyer l'utilisateur). Pas de jargon de prof, pas de phrases de 4 lignes. Sois synthétique et va droit au but avec un ton un peu piquant.
                
                Le type de document est : {type_document}.
                
                Rédige ta réponse en suivant STRICTEMENT ce plan :
                
                ## 📝 1. Le topo en deux mots
                (Résume ce que c'est en 2 phrases max, de manière très directe)
                
                ## 📌 2. Les chiffres qui piquent
                - **La douloureuse :** (Le prix ou coût détecté. Si c'est gratuit en apparence, dis ce qu'on paie en échange, ex: tes données)
                - **Le bail (Durée) :** (Combien de temps on t'enchaîne ?)
                - **Pour se barrer (Résiliation) :** (C'est facile ou c'est un parcours du combattant ?)
                - **Tes données :** (Ils en font quoi en vrai ?)
                
                ## ⚠️ 3. Les 3 grosses carottes à éviter
                (Trouve les 3 pires clauses cachées. Fais juste 1 phrase choc par point)
                1. 🛑 **[Nom du piège]** : [L'explication cash]
                2. 🛑 **[Nom du piège]** : [L'explication cash]
                3. 🛑 **[Nom du piège]** : [L'explication cash]
                
                ## 🔮 4. Le verdict : On signe ou pas ?
                🟢 **Le bon plan :** (1 phrase)
                🔴 **Le retour de bâton :** (1 phrase)
                
                Important : Garde un style dynamique et percutant. Pas de gros blocs de texte ennuyeux.
                """
                
                # Envoi du prompt ET du contenu à Gemini
                reponse = model.generate_content([prompt_systeme, contenu_gemini])
                
                # Affichage du résultat de l'analyse
                st.success("✨ Analyse ClearTerms terminée !")
                st.markdown("---")
                st.markdown(reponse.text)
                
                # 🤝 --- SECTION PARTENAIRES & AFFILIATION ---
                st.markdown("---")
                st.header("🤝 Des offres partenaires plus avantageuses pour toi")
                st.write("D'après notre analyse, voici des alternatives qui vont te faire économiser ou t'offrir de meilleures options :")
                
                if "Web" in type_document:
                    st.info("💡 **Alternative ClearTerms :** Marre des CGU abusives sur vos données ? Découvrez **Proton Mail & VPN**, le partenaire suisse qui garantit un anonymat total et 0 pub pour seulement 4€/mois.")
                elif "Consommation" in type_document or "Assurances" in type_document:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric(label="Ton prix estimé", value="50 € / mois", delta="-15 € avec nos partenaires")
                    with col2:
                        st.subheader("Bénéficie de l'offre Alan ou Lovys")
                        st.write("Profite de -20% la première année, zéro engagement, résiliation en 2 clics et application mobile ultra-rapide.")
                        st.button("🔥 Voir l'offre partenaire (Économiser 15€)")
                elif "Logement" in type_document:
                    st.success("🏠 **Bon plan Déménagement :** Notre partenaire **Papernest** résilie gratuitement tous tes anciens contrats d'énergie et transfère ta box internet en 5 minutes. En plus, tu reçois un bon d'achat de 50€ !")
                    st.button("📦 En savoir plus sur Papernest")
                else:
                    st.write("🤖 *Aucun partenaire n'a été trouvé pour cette catégorie spécifique pour le moment.*")
                
            except Exception as e:
                st.error(f"Une erreur est survenue lors de l'analyse : {e}")

# Pied de page & Sécurité
st.markdown("---")
st.caption(f"🔒 **Respect de la vie privée :** ClearTerms ne sauvegarde pas vos documents. Pour toute question RGPD ou contact pro : {MON_EMAIL_BUSINESS}")
st.caption("⚠️ **Avertissement :** ClearTerms utilise une intelligence artificielle pour vous aider à décrypter vos documents. Cela ne remplace en aucun cas les conseils ou l'expertise d'un avocat professionnel.")