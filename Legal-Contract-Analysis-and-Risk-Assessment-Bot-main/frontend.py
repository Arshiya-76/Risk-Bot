# frontend.py

import streamlit as st
import re
import plotly.express as px
from langdetect import detect, LangDetectException

from backend import get_ai_analysis, get_text_from_file
from chatbot import get_chat_response
from reformatter import reformat_contract_as_template

def is_email_valid(email: str) -> bool:
    if not isinstance(email, str) or not email: return False
    return email.endswith("@gmail.com") and len(email.split('@')[0]) > 0
def get_password_errors(password: str) -> list:
    errors = []
    if len(password) < 8: errors.append("be at least 8 characters long")
    if not re.search(r"[a-z]", password): errors.append("contain at least one lowercase letter")
    if not re.search(r"[A-Z]", password): errors.append("contain at least one uppercase letter")
    if not re.search(r"\d", password): errors.append("contain at least one number")
    if not re.search(r"[!@#$%^&*()]", password): errors.append("contain a special character (e.g., !@#$%)")
    return errors
def initialize_session_state():
    defaults = {"authenticated": False, "analysis_result": None, "reformatted_text": None, "messages": [], "contract_text": None, "language": "en"}
    for key, value in defaults.items():
        if key not in st.session_state: st.session_state[key] = value
def login_page():
    st.set_page_config(page_title="Login - Contract Bot", layout="centered")
    st.title("GenAI Contract Bot Login")
    with st.form("login_form"):
        email = st.text_input("Email (must be a @gmail.com address)")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            email_ok = is_email_valid(email)
            password_errors = get_password_errors(password)
            if email_ok and not password_errors:
                st.session_state.authenticated = True; st.rerun()
            else:
                if not email_ok: st.error("Invalid email. Please use an address ending with @gmail.com.")
                if password_errors: st.error(f"Password must: {', '.join(password_errors)}.")
def logout():
    initialize_session_state()
    st.session_state.authenticated = False
    st.rerun()
def main_app():
    st.set_page_config(page_title="Contract Analysis Bot", layout="wide")
    st.title("GenAI Contract Bot")
    st.write("Analyze risks, reformat drafts, or chat with your documents. Now with Multilingual Support!")
    st.sidebar.title("Actions")
    st.sidebar.button("Logout", on_click=logout)
    uploaded_file = st.file_uploader("Upload your contract to begin (English or Hindi)", type=['pdf', 'docx', 'txt'])
    if uploaded_file is not None:
        if st.session_state.get("uploaded_file_name") != uploaded_file.name:
            st.session_state.uploaded_file_name = uploaded_file.name
            with st.spinner("Reading and extracting text..."):
                st.session_state.contract_text = get_text_from_file(uploaded_file)
                if st.session_state.contract_text:
                    try:
                        detected_code = detect(st.session_state.contract_text)
                        st.session_state.language = 'hi' if detected_code != 'en' else 'en'
                    except LangDetectException:
                        st.session_state.language = 'en'
                st.session_state.analysis_result = None; st.session_state.reformatted_text = None; st.session_state.messages = []
        if st.session_state.contract_text:
            lang_map = {'en': 'English', 'hi': 'Hindi'}
            detected_lang_name = lang_map.get(st.session_state.language, "Unknown")
            st.success(f"File '{uploaded_file.name}' is ready. Detected Language: **{detected_lang_name}**.")
            tab1, tab2, tab3 = st.tabs(["Risk Analysis", "Reformatter", "📄 Chat with Document"])
            with tab1:
                st.header("Contract Risk Analysis")
                if st.button("Analyze Risk", type="primary"):
                    with st.spinner("AI is analyzing your document... This may take a moment."):
                        st.session_state.analysis_result = get_ai_analysis(st.session_state.contract_text, language=st.session_state.language)
                if st.session_state.analysis_result:
                    analysis = st.session_state.analysis_result
                    if "error" in analysis:
                        st.error(f"Analysis Failed: {analysis['error']}")
                    else:
                        st.success("Analysis Complete!")
                        summary = analysis.get("summary_analysis", {})
                        st.divider()
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric(label="Total Risk Score", value=f"{summary.get('overall_risk_score', 0)} / 100")
                            st.info(f"**Detected Contract Type:** {summary.get('contract_type', 'N/A')}")
                            st.info(f"**Involved Parties:** {', '.join(summary.get('involved_parties', ['N/A']))}")
                        all_clauses = analysis.get("clause_analysis", [])
                        high_risk = [c for c in all_clauses if "high" in c.get("risk_level", "").lower()]
                        medium_risk = [c for c in all_clauses if "medium" in c.get("risk_level", "").lower()]
                        low_risk = [c for c in all_clauses if "low" in c.get("risk_level", "").lower()]
                        with col2:
                            risk_counts = {"High": len(high_risk), "Medium": len(medium_risk), "Low": len(low_risk)}
                            risk_data = {k: v for k, v in risk_counts.items() if v > 0}
                            if risk_data:
                                fig = px.pie(values=risk_data.values(), names=risk_data.keys(), title='Risk Distribution', color=risk_data.keys(), color_discrete_map={'High':'#FF4B4B', 'Medium':'#FFC300', 'Low':'#28A745'})
                                st.plotly_chart(fig, use_container_width=True)
                        st.divider()
                        st.subheader("Executive Summary")
                        st.write(summary.get('executive_summary', 'No summary available.'))
                        st.subheader("Important Dates")
                        important_dates = summary.get('important_dates', [])
                        if important_dates:
                            date_md = ""
                            for item in important_dates:
                                if isinstance(item, dict):
                                    date_md += f"- **{item.get('date', 'N/A')}:** {item.get('context', 'N/A')}\n"
                                elif isinstance(item, str):
                                    date_md += f"- {item}\n"
                            st.markdown(date_md)
                        else:
                            st.info("No specific dates were mentioned in the document.")
                        st.subheader("Key Sections and Rules at a Glance")
                        sections = summary.get('sections_summary', [])
                        if sections:
                            table_md = "| Section / Rule | Simple Explanation |\n|---|---|\n"
                            
                            for section in sections:
                                if isinstance(section, dict):
                                    
                                    section_name = section.get('section_name', 'N/A').replace('\n', ' ')
                                    explanation = section.get('simple_explanation', 'No explanation provided.').replace('\n', ' ')
                                elif isinstance(section, str):
                                    
                                    parts = section.split(':', 1) 
                                    if len(parts) == 2:
                                        section_name = parts[0].strip()
                                        explanation = parts[1].strip()
                                    else:
                                        section_name = section.strip()
                                        explanation = "See first column"
                                else:
                                    
                                    section_name = "Malformed data"
                                    explanation = "Skipped"
                                table_md += f"| {section_name} | {explanation} |\n"
                            
                            st.markdown(table_md)
                        else:
                            st.info("No specific sections or rules were automatically identified.")
                        st.subheader("Clause-by-Clause Breakdown")
                        if high_risk:
                            st.error("High Risk Clauses")
                            for clause in high_risk:
                                with st.expander(f"**Issue:** {clause.get('identified_issue', 'N/A')}", expanded=True):
                                    st.markdown(f"**Explanation:** {clause.get('explanation', 'N/A')}")
                                    st.markdown(f"**Mitigation:** {clause.get('mitigation_suggestion', 'N/A')}")
                        if medium_risk:
                            st.warning("Medium Risk Clauses")
                            for clause in medium_risk:
                                with st.expander(f"**Issue:** {clause.get('identified_issue', 'N/A')}"):
                                    st.markdown(f"**Explanation:** {clause.get('explanation', 'N/A')}")
                                    st.markdown(f"**Mitigation:** {clause.get('mitigation_suggestion', 'N/A')}")
                        if low_risk:
                            st.success("Low Risk Clauses")
                            for clause in low_risk:
                                with st.expander(f"**Issue:** {clause.get('identified_issue', 'No significant issues identified')}"):
                                    st.markdown(f"**Explanation:** {clause.get('explanation', 'N/A')}")
                                    st.markdown(f"**Mitigation:** {clause.get('mitigation_suggestion', 'N/A')}")
            with tab2:
                st.header("Reformat as a Professional Template")
                template_type = st.selectbox("Select template type:", ("Non-Disclosure Agreement (NDA)", "Service Agreement", "Employment Agreement"), key="template_select")
                if st.button("📄 Reformat as Template"):
                    with st.spinner("AI is redrafting your document..."):
                        st.session_state.reformatted_text = reformat_contract_as_template(st.session_state.contract_text, template_type, language=st.session_state.language)
                if st.session_state.reformatted_text:
                    st.text_area("Reformatted template:", st.session_state.reformatted_text, height=500)
                    st.download_button("Download Template", st.session_state.reformatted_text, file_name=f"Reformatted_{template_type.replace(' ', '_')}.txt")
            with tab3:
                st.header("Chat with Your Document")
                for message in st.session_state.messages:
                    with st.chat_message(message["role"]): st.markdown(message["content"])
                if prompt := st.chat_input("Ask about your contract..."):
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    with st.chat_message("user"): st.markdown(prompt)
                    with st.chat_message("assistant"):
                        with st.spinner("Thinking..."):
                            response = get_chat_response(query=prompt, chat_history=st.session_state.messages, contract_text=st.session_state.contract_text, language=st.session_state.language)
                            st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
initialize_session_state()
if not st.session_state.authenticated:
    login_page()
else:
    main_app()