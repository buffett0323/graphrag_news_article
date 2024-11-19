import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import pandas as pd
from PyPDF2 import PdfReader

from search import global_search


st.title("本地 LLM 應用")
st.write("請在下面的輸入框中輸入您的問題")

# 加載模型和分詞器（請確保模型已經下載到本地）
model_name = "gpt2"  # 替換成您的本地模型名稱
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# 設定 GPU 支持
device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)

user_input = st.text_input("Your question:")

uploaded_file = st.file_uploader("Or upload a file:", type=["txt", "csv", "pdf"])

# Function to read file content based on file type
def read_file_content(uploaded_file):
    if uploaded_file is None:
        return ""
    file_type = uploaded_file.name.split(".")[-1].lower()
    if file_type == "txt":
        return uploaded_file.read().decode("utf-8")
    elif file_type == "csv":
        df = pd.read_csv(uploaded_file)
        return df.to_string(index=False)
    elif file_type == "pdf":
        pdf_reader = PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    else:
        st.write("Unsupported file format.")
        return ""

# Button for submission
if st.button("Generate Response"):
    # Check if there's user input or an uploaded file
    combined_input = user_input if user_input else ""
    
    # Add file content if a file was uploaded
    if uploaded_file is not None:
        file_content = read_file_content(uploaded_file)
        combined_input += " " + file_content

    # Only proceed if there's any input to process
    if combined_input.strip():
        print(f"combined_input:{combined_input}")
        response = global_search(combined_input)
        # Display the response
        st.write("Model Response:")
        st.write(response)
    else:
        st.write("Please enter text or upload a file before generating a response.")

