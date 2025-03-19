
import os
import google.generativeai as genai
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import tkinter as tk
from tkinter import filedialog, scrolledtext
from PIL import Image, ImageTk
import time

# Configure your Gemini API key 
GOOGLE_API_KEY = "UR API key"  # Replace with your actual API key
genai.configure(api_key=GOOGLE_API_KEY)

# Use a valid model name
model = genai.GenerativeModel('gemini-1.5-pro-latest')  # or 'gemini-1.5-flash-latest'

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""  # Handle potential None returns
    except FileNotFoundError:
        print(f"Error: PDF file not found at {pdf_path}")
    return text

def load_and_preprocess_pdfs(folder_path):
    """Loads and preprocesses PDFs from a folder."""
    all_texts = []
    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]

    if not pdf_files:
        print("Warning: No PDF files found in the specified folder.")
        return []

    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        text = extract_text_from_pdf(pdf_path)
        if text:  # Avoid adding empty strings
            all_texts.append(text)
    return all_texts

def find_relevant_context(question, documents):
    """Finds the most relevant context from the documents."""
    if not documents:
        return ""

    vectorizer = TfidfVectorizer()
    document_vectors = vectorizer.fit_transform(documents)
    question_vector = vectorizer.transform([question])
    similarities = cosine_similarity(question_vector, document_vectors).flatten()
    most_relevant_index = similarities.argmax()

    return documents[most_relevant_index]

def generate_response(question, context):
    """Generates a response using the Gemini API with rate limiting."""
    prompt = f"""
    Answer the following question based on the provided context.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
    try:
        response = model.generate_content(prompt)
        countdown_label.config(text="Waiting...")
        for i in range(10, 0, -1):  # 10-second delay (adjust as needed)
            countdown_label.config(text=f"Waiting... {i} seconds")
            root.update()  # Update the UI to show the countdown
            time.sleep(1)
        countdown_label.config(text="")  # Clear the countdown
        return response.text
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Sorry, I could not generate a response."

def browse_folder():
    """Opens a file dialog to select a folder."""
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_path_entry.delete(0, tk.END)
        folder_path_entry.insert(0, folder_path)
        global documents
        documents = load_and_preprocess_pdfs(folder_path)

def ask_question():
    """Handles the question-asking process."""
    question = question_entry.get()
    if not question:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Please enter a question.")
        return

    try:
        context = find_relevant_context(question, documents)
        if not context:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, "No relevant information found in the documents.")
            return

        answer = generate_response(question, context)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, answer)
    except NameError:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Please select a folder first.")

# UI setup
root = tk.Tk()
root.title("RAG Model")
root.geometry("900x600")

# Load background image
bg_image = Image.open("background.jpg")  # Replace with your image
bg_image = bg_image.resize((900, 600), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root, width=900, height=600)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

canvas.create_text(450, 40, text="RAG Model", font=("Arial", 24, "bold"), fill="white")

canvas.create_text(150, 90, text="PDF Folder:", font=("Arial", 12, "bold"), fill="white")
folder_path_entry = tk.Entry(root, width=50, font=("Arial", 10))
folder_path_entry.place(x=230, y=80)

browse_button = tk.Button(root, text="Browse", font=("Arial", 10, "bold"), fg="black",
                            bg=root.cget("bg"), relief="flat", borderwidth=0, command=browse_folder)
browse_button.place(x=600, y=75)

canvas.create_text(150, 140, text="Question:", font=("Arial", 12, "bold"), fill="white")
question_entry = tk.Entry(root, width=50, font=("Arial", 10))
question_entry.place(x=230, y=130)

ask_button = tk.Button(root, text="Ask", font=("Arial", 10, "bold"), fg="black",
                        bg=root.cget("bg"), relief="flat", borderwidth=0, command=ask_question)
ask_button.place(x=600, y=125)

result_text = scrolledtext.ScrolledText(root, width=100, height=25, font=("Arial", 10))
result_text.place(x=50, y=180)

countdown_label = tk.Label(root, text="", font=("Arial", 12), fg="white", bg="black")
countdown_label.place(x=700, y=125)

root.mainloop()
