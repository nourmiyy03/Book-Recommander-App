# Book Recommendation System

A desktop app built with Python that recommends books based on what you search. Built with Tkinter for the UI and Pillow for cover images. If a book isn't in the local database it falls back to the Open Library API automatically.




## What it does

You type in a book title, and the app finds up to 4 similar books based on shared genres, same author, and close ratings. Each result gets a match score so you know why it was recommended.

A few extra things:
- Fuzzy matching — if you misspell a title it suggests the closest one
- Search history — dropdown keeps your last 10 searches
- Random button — picks a random book if you're not sure what to search
- Covers load locally or get fetched from the internet if they're missing


---

## Setup

**Requirements:** Python 3.8+

```bash
pip install Pillow requests
```

Clone the repo and put your cover images in an `Images/` folder:

```
project/
├── book_recommendation.py
├── Images/
│   ├── bride.jpeg
│   ├── mate.jpg
│   └── ...
```

Then just run it:

```bash
python book_recommendation.py
```

---

## Adding books

The database is just a list of dicts at the top of the file. Add as many as you want:

```python
{
    "titre": "Title",
    "auteur": "Author",
    "date": "2023",
    "rating": 4.2,
    "genre": "Fantasy, Romance",
    "category": "fantasy",
    "poster": os.path.join(IMAGE_DIR, "cover.jpg")
}
```

Categories: `romance`, `fantasy`, `sci-fi`, `non-fiction`, `classics`, `other`

---

## Dependencies

- `tkinter` — GUI (standard library)
- `Pillow` — image loading and resizing
- `requests` — API calls
- `difflib` — fuzzy title matching
- [Open Library API](https://openlibrary.org/developers/api) — online book search fallback
