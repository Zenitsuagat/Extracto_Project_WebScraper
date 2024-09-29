import tkinter as tk
from tkinter import scrolledtext, filedialog
import requests
from bs4 import BeautifulSoup


# Function to fetch webpage content
def fetch_webpage_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            result_text.insert(tk.END, f"Failed to retrieve the webpage. Status Code: {response.status_code}\n")
            return None
    except Exception as e:
        result_text.insert(tk.END, f"Error fetching the webpage: {e}\n")
        return None


# Function to extract specific content
def extract_specific_content(html_content, tag):
    soup = BeautifulSoup(html_content, 'html.parser')
    elements = soup.find_all(tag)

    if not elements:
        result_text.insert(tk.END, f"No elements found for the tag '{tag}'\n")
    else:
        for idx, element in enumerate(elements, start=1):
            result_text.insert(tk.END, f"--- {tag.upper()} #{idx} ---\n")
            if tag == 'img':
                img_src = element.get('src')
                result_text.insert(tk.END, f"Image Source: {img_src}\n\n")
            else:
                result_text.insert(tk.END, element.get_text() + "\n\n")


# Function to scrape contents when the button is clicked
def scrape_content():
    result_text.delete(1.0, tk.END)  # Clear previous results
    url = url_entry.get()
    tag = tag_entry.get()

    if url and tag:
        html_content = fetch_webpage_content(url)
        if html_content:
            extract_specific_content(html_content, tag)
    else:
        result_text.insert(tk.END, "Please enter both URL and tag.\n")


# Function to save the contents to a text file
def save_to_file():
    content = result_text.get(1.0, tk.END)
    if content.strip():
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            result_text.insert(tk.END, f"\nContent saved to {file_path}\n")
    else:
        result_text.insert(tk.END, "No content to save.\n")


# Function to close the application
def close_app():
    root.destroy()


# Tkinter GUI
root = tk.Tk()
root.title("Extracto")
root.geometry("600x550")
root.config(bg="#f0f8ff")

# URL Label and Entry
url_label = tk.Label(root, text="Enter the URL:", bg="#f0f8ff", font=("Arial", 12))
url_label.pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Tag Label and Entry
tag_label = tk.Label(root, text="Enter the HTML tag (e.g., p, h2, img):", bg="#f0f8ff", font=("Arial", 12))
tag_label.pack(pady=5)
tag_entry = tk.Entry(root, width=50)
tag_entry.pack(pady=5)

# Button Styles
button_style = {"bg": "#4CAF50", "fg": "white", "font": ("Arial", 10, "bold")}

# Scrape Button
scrape_button = tk.Button(root, text="Scrape", command=scrape_content, **button_style)
scrape_button.pack(pady=10)

# Scrollable Text Box for Results
result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=15, bg="#e6f2ff")
result_text.pack(pady=10)

# Save Button
save_button = tk.Button(root, text="Save to File", command=save_to_file, **button_style)
save_button.pack(pady=10)

# Close Button
close_button = tk.Button(root, text="Close", command=close_app, **button_style)
close_button.pack(pady=10)

# Run the GUI
root.mainloop()
