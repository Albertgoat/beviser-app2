import streamlit as st
import json

# Indlæs JSON-data
import os
filepath = os.path.join(os.path.dirname(__file__), "beviser.json")
with open(filepath, "r", encoding="utf-8") as f:
    data = json.load(f)

# Init session state
if "skridt_index" not in st.session_state:
    st.session_state.skridt_index = 0
if "last_bevis" not in st.session_state:
    st.session_state.last_bevis = ""

# UI: vælg bevis
bevisnavne = [b["bevis"] for b in data["beviser"]]
valg = st.selectbox("Vælg et bevis", bevisnavne)

# Nulstil hvis valgt bevis ændres
if st.session_state.last_bevis != valg:
    st.session_state.skridt_index = 0
    st.session_state.last_bevis = valg

# Find det valgte bevis
valgt_bevis = next(b for b in data["beviser"] if b["bevis"] == valg)

# Vis sætning (hvis den findes)
if "sætning" in valgt_bevis:
    st.markdown("### Sætning")
    st.markdown(valgt_bevis["sætning"])

# Liste over skridt
udførelse = valgt_bevis["udførelse"]

# Navigationsknapper – ALTID i bunden
col1, col2 = st.columns(2)

with col1:
    if st.button("⬅️ Tilbage",
                 key="back_btn",
                 disabled=st.session_state.skridt_index == 0):
        st.session_state.skridt_index = max(0,
                                            st.session_state.skridt_index - 1)

with col2:
    if st.button("➡️ Næste skridt",
                 key="next_btn",
                 disabled=st.session_state.skridt_index >= len(udførelse)):
        st.session_state.skridt_index = min(len(udførelse),
                                            st.session_state.skridt_index + 1)

index = st.session_state.skridt_index  # 👈 vigtigt: opdater efter knapper

# Vis alle skridt op til index
if index > 0:
    st.markdown("---")
    for i in range(index):
        skridt_data = udførelse[i]
        st.markdown(f"#### Skridt {i + 1}")

        # Vis LaTeX-skridt (hvis det findes)
        if skridt_data.get("skridt"):
                st.latex(skridt_data["skridt"])

        # Vis billede (hvis det findes)
        if skridt_data.get("billede"):
                st.image(skridt_data["billede"], use_container_width=True)

        # Vis argumentation (hvis den findes)
        if skridt_data.get("argumentation"):
            st.markdown(
                    f"Argumentation:<br>{skridt_data['argumentation'].replace(chr(10), '<br>')}",
                    unsafe_allow_html=True
                )

            st.markdown("---")

# Hvis færdig
if index == len(udførelse):
    st.success("🎉 Beviset er færdiggjort!")