from tkinter import *
from tkinter import messagebox
import random
from PIL import ImageTk, Image
import os
from difflib import get_close_matches
import requests
from urllib.request import urlopen
from io import BytesIO


root = Tk()
root.title("Book Recommendation System")
root.geometry("1250x750")
root.config(bg="#F5F5DA")
root.resizable(True, True)
root.grid_rowconfigure(2, weight=1)  # Make middle row expandable
root.grid_columnconfigure(1, weight=1)  # Make right column expandable

##########################################################################

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "Images")

image_cache = {}


# Books database
books = [
    {
        "titre": "Bride",
        "auteur": "Ali Hazelwood",
        "date": "2024",
        "rating": 4.6,
        "genre": "Romance, Paranormal Romance",
        "category": "romance",
        "poster": os.path.join(IMAGE_DIR, "bride.jpeg")
    },
    {
        "titre": "Mate",
        "auteur": "Ali Hazelwood",
        "date": "2025",
        "rating": 4.1,
        "genre": "Romance, Paranormal Romance, Fantasy",
        "category": "romance",
        "poster": os.path.join(IMAGE_DIR, "mate.jpg")
    },
    {
        "titre": "From Blood and Ash",
        "auteur": "Jennifer L. Armentrout",
        "date": "2020",
        "rating": 4.2,
        "genre": "Fantasy, Romance",
        "category": "fantasy",
        "poster": os.path.join(IMAGE_DIR, "Blood&Ash.jpg")
    },
    {
        "titre": "God of Malice",
        "auteur": "Rina Kent",
        "date": "2022",
        "rating": 4.3,
        "genre": "Dark Romance",
        "category": "romance",
        "poster": os.path.join(IMAGE_DIR, "GodMalice.jpg")
    },
    {
        "titre": "God of Ruin",
        "auteur": "Rina Kent",
        "date": "2023",
        "rating": 4.1,
        "genre": "Dark Romance",
        "category": "romance",
        "poster": os.path.join(IMAGE_DIR, "Ruin.jpg")
    },
    {
        "titre": "God of Wrath",
        "auteur": "Rina Kent",
        "date": "2023",
        "rating": 4.2,
        "genre": "Dark Romance",
        "category": "romance",
        "poster": os.path.join(IMAGE_DIR, "Wrath.jpg")
    },
    {
        "titre": "The Fine Print",
        "auteur": "Lauren Asher",
        "date": "2021",
        "rating": 3.8,
        "genre": "Contemporary Romance",
        "category": "romance",
        "poster": os.path.join(IMAGE_DIR, "TheFinePrint.jpg")
    },
    {
        "titre": "King of Wrath",
        "auteur": "Ana Huang",
        "date": "2022",
        "rating": 4.5,
        "genre": "Contemporary Romance",
        "category": "romance",
        "poster": os.path.join(IMAGE_DIR, "KingWrath.jpg")
    },
    {
        "titre": "Twisted Love",
        "auteur": "Ana Huang",
        "date": "2021",
        "rating": 4.0,
        "genre": "Contemporary Romance",
        "category": "romance",
        "poster": os.path.join(IMAGE_DIR, "Twisted.png")
    },
    {
        "titre": "The 48 Laws of Power",
        "auteur": "Robert Greene",
        "date": "1998",
        "rating": 4.8,
        "genre": "Self-Help, Philosophy, Psychology",
        "category": "non-fiction",
        "poster": os.path.join(IMAGE_DIR, "48.jpg")
    },
    {
        "titre": "The Prince",
        "auteur": "Niccolò Machiavelli",
        "date": "1532",
        "rating": 3.9,
        "genre": "Philosophy, Political Science",
        "category": "non-fiction",
        "poster": os.path.join(IMAGE_DIR, "ThePrince.jpg")
    },
    {
        "titre": "The Laws of Human Nature",
        "auteur": "Robert Greene",
        "date": "2018",
        "rating": 4.4,
        "genre": "Psychology, Self-Help, Philosophy",
        "category": "non-fiction",
        "poster": os.path.join(IMAGE_DIR, "HumanNature.jpg")
    },
    {
        "titre": "The Art of War",
        "auteur": "Sun Tzu",
        "date": "Unknown",
        "rating": 3.9,
        "genre": "Philosophy, Military Strategy",
        "category": "non-fiction",
        "poster": os.path.join(IMAGE_DIR, "ArtofWar.jpg")
    },
    {
        "titre": "Crime and Punishment",
        "auteur": "Fyodor Dostoevsky",
        "date": "1880",
        "rating": 4.3,
        "genre": "Classics, Psychological Fiction, Philosophy",
        "category": "classics",
        "poster": os.path.join(IMAGE_DIR, "CrimePunishment.jpg")
    },
    {
        "titre": "The Stranger",
        "auteur": "Albert Camus",
        "date": "1942",
        "rating": 4.0,
        "genre": "Classics, Philosophy, Absurdist Fiction",
        "category": "classics",
        "poster": os.path.join(IMAGE_DIR, "Stranger.png")
    },
    {
        "titre": "No Longer Human",
        "auteur": "Osamu Dazai",
        "date": "1948",
        "rating": 4.1,
        "genre": "Classics, Psychological Fiction",
        "category": "classics",
        "poster": os.path.join(IMAGE_DIR, "NoLonger.jpg")
    },
    {
        "titre": "The Metamorphosis",
        "auteur": "Franz Kafka",
        "date": "1915",
        "rating": 4.0,
        "genre": "Classics, Absurdist Fiction, Psychological Fiction",
        "category": "classics",
        "poster": os.path.join(IMAGE_DIR, "Metamorphosis.jpg")
    },
]

## API 
def search_openlibrary(title):
    try:
        url = f"https://openlibrary.org/search.json?title={title}&limit=5"

        response = requests.get(url)
        data = response.json()
        api_books = []

        for doc in data["docs"]:
            cover_id = doc.get("cover_i")
            if cover_id:
                cover = f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
            else:
                cover = ""
            book = {
                "titre": doc.get("title","Unknown"),
                "auteur": ", ".join(doc.get("author_name",["Unknown"])),
                "date": str(doc.get("first_publish_year","Unknown")),
                "rating": 4,
                "genre": "Fiction",
                "category": "other",
                "poster": cover
            }

            api_books.append(book)

        return api_books

    except:
        return []


# Search history
search_history = []
MAX_HISTORY = 10

def get_main_category(book):
    genre_lower = book["genre"].lower()
    
    if "romance" in genre_lower:
        return "romance"
    elif "fantasy" in genre_lower:
        return "fantasy"
    elif "dystopian" in genre_lower or "science fiction" in genre_lower:
        return "sci-fi"
    elif "self-help" in genre_lower or "philosophy" in genre_lower or "psychology" in genre_lower:
        return "non-fiction"
    elif "classics" in genre_lower:
        return "classics"
    else:
        return "other"

def find_similar_books(search_title):

    # Find the book in the local database
    target_book = None
    for book in books:
        if book["titre"].lower() == search_title.lower().strip():
            target_book = book
            break

    # If not found locally, try fuzzy match
    if not target_book:
        titles = [book["titre"] for book in books]
        matches = get_close_matches(search_title, titles, n=3, cutoff=0.6)

        if matches:
            choice = messagebox.askyesno(
                "Book Not Found",
                f"Did you mean '{matches[0]}'?\n\nClick Yes to search for this book."
            )

            if choice:
                for book in books:
                    if book["titre"] == matches[0]:
                        target_book = book
                        break
            else:
                return [], None

    # If STILL not found, go search online
    if not target_book:
        api_results = search_openlibrary(search_title)

        if api_results:
            target_book = api_results[0]
            recommendations = []
            for book in api_results[1:5]:
                recommendations.append((50, book, ["Online result"]))
            return recommendations, target_book
        else:
            messagebox.showinfo(
                "Book Not Found",
                f"No results found for '{search_title}'."
            )
            return [], None

    # LOCAL RECOMMENDATION PART
    target_category = get_main_category(target_book)
    target_author = target_book["auteur"]
    target_genres = set(g.strip().lower() for g in target_book["genre"].split(","))

    recommendations = []

    for book in books:
        if book["titre"] == target_book["titre"]:
            continue
        score = 0
        reasons = []

        book_genres = set(g.strip().lower() for g in book["genre"].split(","))
        common_genres = target_genres.intersection(book_genres)

        if not common_genres and book["auteur"] != target_author:
            continue

        if book["auteur"] == target_author:
            score += 50
            reasons.append("Same author")

        for genre in common_genres:
            if genre in ["romance", "fantasy", "dark romance"]:
                score += 30
            elif genre in ["classics", "philosophy", "psychology"]:
                score += 25
            elif genre in ["self-help", "non-fiction"]:
                score += 25
            else:
                score += 20

        if len(common_genres) >= 2:
            score += 15
            reasons.append("Multiple shared genres")
        elif len(common_genres) == 1:
            reasons.append("Shared genre")

        book_category = get_main_category(book)
        if book_category == target_category:
            score += 10

        rating_diff = abs(book["rating"] - target_book["rating"])
        if rating_diff <= 0.3:
            score += 10
        elif rating_diff <= 0.5:
            score += 5

        if score >= 40:
            recommendations.append((score, book, reasons))

    recommendations.sort(key=lambda x: x[0], reverse=True)
    return recommendations[:4], target_book

#Cover
def load_image_safe(image_path, size=(150,150)):
    cache_key = f"{image_path}_{size}"
    if cache_key in image_cache:
        return image_cache[cache_key]

    try:
        # If image is from internet
        if str(image_path).startswith("http"):
            with urlopen(image_path) as u:
                raw_data = u.read()
            pil_image = Image.open(BytesIO(raw_data))

        else:
            if not os.path.exists(image_path):
                return None
            pil_image = Image.open(image_path)

        pil_image = pil_image.resize(size, Image.LANCZOS)

        photo = ImageTk.PhotoImage(pil_image)

        image_cache[cache_key] = photo
        return photo

    except:
        return None


#Ajouter a l'historique
def add_to_history(book_title):
    if book_title and book_title not in search_history:
        search_history.insert(0, book_title)
        if len(search_history) > MAX_HISTORY:
            search_history.pop()
        update_history_menu()

def update_history_menu():
    history_menu.menu.delete(0, "end")
    
    if search_history:
        for title in search_history:
            history_menu.menu.add_command(label=title, 
                                        command=lambda t=title: search_from_history(t))
    else:
        history_menu.menu.add_command(label="No history", state="disabled")

#############################################################################################
def search_from_history(title):
    Search.set(title)
    recomm_update()

def create_book_frame(parent, book, row, col, score=None, reasons=None):
    frame = Frame(parent, bg="#f0c597", relief="raised", bd=1)
    frame.grid(row=row, column=col, padx=10, pady=8, sticky="n")
    
    # Load and display image
    img = load_image_safe(book["poster"], (140, 140))
    if img:
        img_label = Label(frame, image=img, bg="#f0c597")
        img_label.image = img
        img_label.pack(pady=(5, 2))
    else:
        placeholder = Label(frame, text="📚", font=("Arial", 40),
                          bg="#d9b382", fg="#2B0D2C", width=8, height=3)
        placeholder.pack(pady=(5, 2))
    
    # Title
    title_text = book["titre"][:18] + "..." if len(book["titre"]) > 18 else book["titre"]
    Label(frame, text=title_text, font=("Arial", 9, "bold"),
          bg="#f0c597", fg="#2B0D2C").pack()
    
    # Author
    author_text = book["auteur"][:15] + "..." if len(book["auteur"]) > 15 else book["auteur"]
    Label(frame, text=author_text, font=("Arial", 7),
          bg="#f0c597", fg="#a5633a").pack()
    
    # Rating stars
    stars = "⭐" * int(book["rating"])
    Label(frame, text=stars, font=("Arial", 7),
          bg="#f0c597", fg="#FFB800").pack()
    
    # Year
    Label(frame, text=book["date"], font=("Arial", 7),
          bg="#f0c597", fg="#a5633a").pack()
    
    # Match quality badge
    if score:
        if score >= 80:
            badge = "🔥 Perfect Match"
            badge_color = "#FF4500"
        elif score >= 60:
            badge = "👍 Excellent"
            badge_color = "#32CD32"
        else:
            badge = "📚 Good Match"
            badge_color = "#1E90FF"
        
        Label(frame, text=badge, font=("Arial", 6, "bold"),
              bg=badge_color, fg="white").pack(pady=(2, 0))
    
    return frame

#clear searcj
def clear_search():
    Search.set("")
    for widget in searched_frame.winfo_children():
        widget.destroy()
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    result_label.config(text="")

#random book recomm
def show_random_book():
    random_book = random.choice(books)
    Search.set(random_book["titre"])
    recomm_update()

def recomm_update():
    title = Search.get().strip()
    
    if not title:
        messagebox.showwarning("Input Needed", "Please enter a book title!")
        return
    
    # Show loading indicator
    loading_label = Label(scrollable_frame, text="Finding recommendations...", 
                         font=("Arial", 12), fg="#a5633a", bg="#F5F5DA")
    loading_label.grid(row=0, column=0, padx=10, pady=10)
    root.update()
    
    # Get recommendations (max 4)
    recommendations, target_book = find_similar_books(title)
    
    # Remove loading indicator
    loading_label.destroy()
    
    if not recommendations:
        if target_book:
            messagebox.showinfo("No Recommendations", 
                               f"We found '{target_book['titre']}' but don't have any strongly similar books.\n\nTry searching for another book by the same author.")
        return
    
    # Add to history
    add_to_history(target_book["titre"])
    
    # Display searched book
    display_searched_book(target_book)
    
    # Update result count
    result_label.config(text=f"Found {len(recommendations)} similar books")
    
    # Clear previous recommendations
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    
    # Display recommendations (max 4 in a row)
    for i, (score, book, reasons) in enumerate(recommendations):
        create_book_frame(scrollable_frame, book, 0, i, score, reasons)
    
    # Update scroll region
    scrollable_frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

#searched book display in the left corner
def display_searched_book(book):
    for widget in searched_frame.winfo_children():
        widget.destroy()
    
    Label(searched_frame, text="You searched:", font=("Arial", 9, "bold"),
          bg="#e8b882", fg="#2B0D2C").pack(anchor="w", padx=5, pady=2)
    
    # Book image
    img = load_image_safe(book["poster"], (150, 200))
    if img:
        img_label = Label(searched_frame, image=img, bg="#e8b882")
        img_label.image = img
        img_label.pack(pady=5)
    else:
        Label(searched_frame, text="📚", font=("Arial", 60),
              bg="#e8b882", fg="#2B0D2C").pack(pady=20)
    
    # Book details
    details_frame = Frame(searched_frame, bg="#e8b882")
    details_frame.pack(fill="x", padx=5, pady=5)
    
    title_text = book["titre"][:20] + "..." if len(book["titre"]) > 20 else book["titre"]
    Label(details_frame, text=title_text, font=("Arial", 10, "bold"),
          bg="#e8b882", fg="#2B0D2C", wraplength=140).pack()
    
    Label(details_frame, text=book["auteur"], font=("Arial", 8),
          bg="#e8b882", fg="#a5633a").pack()
    
    stars = "⭐" * int(book["rating"])
    Label(details_frame, text=stars, font=("Arial", 8),
          bg="#e8b882", fg="#FFB800").pack()
    
    Label(details_frame, text=f"Published: {book['date']}", font=("Arial", 7),
          bg="#e8b882", fg="#a5633a").pack()
    
    # Category badge
    category = get_main_category(book)
    category_colors = {
        "romance": "#FF69B4",
        "fantasy": "#9370DB",
        "sci-fi": "#4169E1",
        "non-fiction": "#CD853F",
        "classics": "#708090",
        "other": "#808080"
    }
    color = category_colors.get(category, "#808080")
    Label(details_frame, text=category.upper(), font=("Arial", 7, "bold"),
          bg=color, fg="white").pack(pady=2)

#Reset the scroll region when the frame size changes
def on_frame_configure(event): 
    canvas.configure(scrollregion=canvas.bbox("all"))

def on_canvas_configure(event):
    #Resize the inner frame when canvas is resized
    canvas.itemconfig(canvas_frame_id, width=event.width)

def on_mousewheel(event):
    #For mousewheel scrolling
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

####################################################################################

# Create header frame
header_frame = Frame(root, bg="#FEFD98", height=267)
header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
header_frame.grid_propagate(False)

# load header image
try:
    header_img = load_image_safe(os.path.join(IMAGE_DIR, "background.png"), (1250, 267))
    if header_img:
        header_label = Label(header_frame, image=header_img, bg="#FEFD98")
        header_label.place(x=0, y=0, relwidth=1, relheight=1)
except:
    pass

#load logo
try:
    logo_img = load_image_safe(os.path.join(IMAGE_DIR, "logo.png"), (132, 132))
    if logo_img:
        logo_label = Label(header_frame, image=logo_img, bg="#FEFD98")
        logo_label.place(x=200, y=30)
except:
    pass

# Title
title_label = Label(header_frame, text="BOOK RECOMMENDATION", font=("Wednesday", 40, "bold"),
                   fg="#2B0D2C", bg="#FEFD98")
title_label.place(relx=0.5, y=95, anchor="center")

# Exit button
exit_btn = Button(header_frame, text="✕ Exit", font=("Arial", 10),
                 bg="#FEFD98", fg="#a5633a", cursor="hand2",
                 command=root.destroy, relief="flat")
exit_btn.place(relx=0.95, y=15, anchor="ne")

# Search section in header
search_frame = Frame(header_frame, bg="#FEFD98")
search_frame.place(relx=0.5, y=190, anchor="center")

Search = StringVar()
search_entry = Entry(search_frame, textvariable=Search, width=25, 
                    font=("Arial", 25), fg="#000000", bg="#ffffff")
search_entry.pack(side=LEFT, padx=(110, 5))
search_entry.bind("<Return>", lambda event: recomm_update())

# Search button
search_btn = Button(search_frame, text="🔍 Search", font=("Arial", 12),
                   bg="#FEFD98", fg="#2B0D2C", cursor="hand2",
                   command=recomm_update, relief="raised", bd=1)
search_btn.pack(side=LEFT)

# Clear button
clear_btn = Button(search_frame, text="✕ Clear", font=("Arial", 10),
                  bg="#FEFD98", fg="#a5633a", cursor="hand2",
                  command=clear_search, relief="flat")
clear_btn.pack(side=LEFT, padx=5)

# Random book button
random_btn = Button(search_frame, text="🎲 Random", font=("Arial", 10),
                   bg="#FEFD98", fg="#2B0D2C", cursor="hand2",
                   command=show_random_book, relief="flat")
random_btn.pack(side=LEFT)

# History dropdown
history_menu = Menubutton(search_frame, text="📜 History", font=("Arial", 10),
                         bg="#FEFD98", fg="#2B0D2C", relief="raised")
history_menu.pack(side=LEFT, padx=5)
history_menu.menu = Menu(history_menu, tearoff=0)
history_menu["menu"] = history_menu.menu
update_history_menu()

# Result label (now in main grid)
result_label = Label(root, text="", font=("Arial", 10), 
                    fg="#a5633a", bg="#F5F5DA")
result_label.grid(row=1, column=0, columnspan=2, sticky="w", padx=(250, 0), pady=(0, 5))

# Main content area with grid
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=0)  # Left panel doesn't expand
root.grid_columnconfigure(1, weight=1)  # Right panel expands

# Left panel for searched book
searched_frame = Frame(root, width=220, height=400, bg="#e8b882", 
                      relief="sunken", bd=2)
searched_frame.grid(row=2, column=0, sticky="nw", padx=(200, 130), pady=(50, 100))
#searched_frame.grid_propagate(False)

# Canvas with scrollbar for recommendations
canvas_container = Frame(root, bg="#F5F5DA")
canvas_container.grid(row=2, column=1, sticky="nsew", padx=(0, 20), pady=(0, 20))
canvas_container.grid_rowconfigure(0, weight=1)
canvas_container.grid_columnconfigure(0, weight=1)

canvas = Canvas(canvas_container, bg="#F5F5DA", highlightthickness=0)
scrollbar = Scrollbar(canvas_container, orient="vertical", command=canvas.yview)

scrollbar.grid(row=0, column=1, sticky="ns")
canvas.grid(row=0, column=0, sticky="nsew")

canvas.configure(yscrollcommand=scrollbar.set)

# Frame inside canvas for recommendations
scrollable_frame = Frame(canvas, bg="#F5F5DA")

# Create canvas window and store its ID
canvas_frame_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# Bind events
scrollable_frame.bind("<Configure>", on_frame_configure)
canvas.bind("<Configure>", on_canvas_configure)
canvas.bind_all("<MouseWheel>", on_mousewheel)

# Show a random book on startup
root.after(500, show_random_book)

# Watermark
watermark = Label(root, text="made by nourmiyy03", font=("Arial", 18, "italic"),
                 fg="#a5633a", bg="#F5F5DA")
watermark.place(relx=0.59, rely=0.22, anchor="se")
##################################################################################################

root.mainloop()