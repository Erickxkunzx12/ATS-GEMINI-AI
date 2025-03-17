import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json
import re

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt):
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(input_prompt)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Prompt Template
input_prompt = """
Actúa como un ATS (Sistema de Seguimiento de Solicitantes) experto con profundo conocimiento en tecnología, ingeniería de software, ciencia de datos, análisis de datos e ingeniería de big data. Evalúa el currículum según la descripción del puesto. El mercado laboral es competitivo, proporciona la mejor asistencia para mejorar los currículums. Asigna el porcentaje de coincidencia y las palabras clave faltantes con precisión.
Currículum: {text}
Descripción del puesto: {jd}

Responde en formato JSON con las siguientes claves:
{{"Porcentaje de Coincidencia": (porcentaje numérico), "Palabras Clave Faltantes": (lista de cadenas), "Resumen del Perfil": (cadena de texto)}}
"""

# Streamlit app
with st.sidebar:
    st.image("LOCHER.jpg", width=300)
    st.title("Smart ATS para Currículums")
    st.subheader("Acerca de")
    st.write("Este proyecto de ATS sofisticado, desarrollado con Gemini Pro y Streamlit, incorpora a la perfección funciones avanzadas que incluyen porcentaje de coincidencia de currículum, análisis de palabras clave para identificar criterios faltantes y la generación de resúmenes de perfiles completos, lo que mejora la eficiencia y la precisión del proceso de evaluación de candidatos para profesionales exigentes de adquisición de talento.")
    st.markdown("""
        - [Streamlit](https://streamlit.io/)
        - [Gemini Pro](https://deepmind.google/technologies/gemini/#introduction)
        - [API Key makersuite](https://makersuite.google.com/)
    """)
    add_vertical_space(4)
    st.write("LOCHER_ATS")

st.title("Sistema AI para análisis de Currículums")
st.text("Mejore su currículum ATS")

jd = st.text_area("Descripción del Puesto")
uploaded_file = st.file_uploader("Sube tu Currículum (PDF)", type="pdf", help="Sube tu currículum en formato PDF")

submit = st.button("Analizar Currículum")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        formatted_prompt = input_prompt.format(text=text, jd=jd)
        response = get_gemini_response(formatted_prompt)
        try:
            json_string = re.search(r'{[\s\S]*}', response).group(0)
            response_json = json.loads(json_string)
            st.subheader("Análisis ATS:")
            st.write(f"Porcentaje de Coincidencia: {response_json.get('Porcentaje de Coincidencia', 'N/A')}%")
            st.write(f"Palabras Clave Faltantes: {response_json.get('Palabras Clave Faltantes', 'N/A')}")
            st.write(f"Resumen del Perfil: {response_json.get('Resumen del Perfil', 'N/A')}")
        except (json.JSONDecodeError, AttributeError):
            st.error("Error: La respuesta de Gemini no es un JSON válido.")
            st.write(response)
    else:
        st.error("Sube un currículum en formato PDF.")