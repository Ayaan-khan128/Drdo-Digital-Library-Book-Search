from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from fuzzywuzzy import fuzz
from sqlalchemy import or_
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

# Define Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100),nullable=False)
    year = db.Column(db.Integer,nullable=False)
    keywords = db.Column(db.String(300),nullable=False)  # comma-separated
    abstract = db.Column(db.Text)

# Create database (first time only)
with app.app_context():
    db.create_all()
    if Book.query.count() == 0:
     book1 = Book(
        title="Introduction to ayaan",
        author="Merrill I. Skolnik",
        year=2001,
        keywords="radar, signal processing, antennas, electronics",
        abstract="This book explains the principles of radar and its applications in defense."
    )
    book2 = Book(
        title="Advanced Missile Guidance",
        author="K. Deb",
        year=2015,
        keywords="missile, guidance, targeting, radar",
        abstract="Covers algorithms and techniques for missile guidance systems."
    )
    
    db.session.add_all([])
    db.session.commit()
    

    


# Sample search function
# def search_books(query):
#     books = Book.query.all()
#     results = []
#     for book in books:
#         score = 0
#         for kw in book.keywords.split(','):
#             score += fuzz.partial_ratio(query.lower(), kw.strip().lower())
#         results.append((book, score))
#     results.sort(key=lambda x: x[1], reverse=True)
#     return [r[0] for r in results if r[1] > 50]

# def search_books_by_keyword(query):
   # all_books = Book.query.all()
   # filtered_books = []

   # for book in all_books:
      #  match_score = 0
      #  for kw in book.keywords.split(','):
       #     kw = kw.strip().lower()
       #     match_score += fuzz.partial_ratio(query.lower(), kw)

       # if match_score > 50:  # Only include books with good match score
        #    filtered_books.append((book, match_score))

    # Sort by score descending
   # filtered_books.sort(key=lambda x: x[1], reverse=True)
    
    # Return only book objects (not score)
   # return [b[0] for b in filtered_books]

# @app.route("/", methods=["GET", "POST"])
# def index():
#     results = []
#     if request.method == "POST":
#         query = request.form["query"]
#         results = search_books_by_keyword(query)
#     return render_template("index.html", results=results)
# Search function
def search_books_by_keyword(query):
    if not query:
        return []

    # Search by title, author, or year
    return Book.query.filter(
        or_(
            Book.title.ilike(f"%{query}%"),
            Book.author.ilike(f"%{query}%"),
            Book.year.like(f"%{query}%")
        )
    ).all()

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    query = ""

    if request.method == "POST":
        query = request.form.get("query", "").strip()
        if query:
            results = search_books_by_keyword(query)  # Only matched books
        else:
            results = []  # Don't return anything if no query

    return render_template("index.html", results=results, query=query)
@app.route("/add", methods=["GET", "POST"])
def add_book():
    message = ""

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        year = request.form.get("year", "").strip()

        if title and author and year.isdigit():
            new_book = Book(title=title, author=author, year=int(year))
            db.session.add(new_book)
            db.session.commit()
            message = "Book added successfully!"
        else:
            message = "Please enter valid book details."

    return render_template("add_book.html", message=message)
@app.route("/delete", methods=["GET", "POST"])
def delete_book():
    message = ""

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()

        if not title and not author:
            message = "Please enter at least a title or author to delete."
        else:
            # Build query filter
            filters = []
            if title:
                filters.append(Book.title.ilike(f"%{title}%"))
            if author:
                filters.append(Book.author.ilike(f"%{author}%"))

            books_to_delete = Book.query.filter(*filters).all()

            if books_to_delete:
                for book in books_to_delete:
                    db.session.delete(book)
                db.session.commit()
                message = f"{len(books_to_delete)} book(s) deleted successfully."
            else:
                message = "No matching books found to delete."

    return render_template("delete_book.html", message=message)
@app.route("/edit", methods=["GET", "POST"])
def edit_book():
    message = ""
    
    if request.method == "POST":
        # Fields to identify the book
        search_title = request.form.get("search_title", "").strip()
        search_author = request.form.get("search_author", "").strip()

        # New data to update
        new_title = request.form.get("new_title", "").strip()
        new_author = request.form.get("new_author", "").strip()
        new_year = request.form.get("new_year", "").strip()

        if not (search_title or search_author):
            message = "Enter at least a title or author to search the book."
        else:
            # Search for book(s)
            filters = []
            if search_title:
                filters.append(Book.title.ilike(f"%{search_title}%"))
            if search_author:
                filters.append(Book.author.ilike(f"%{search_author}%"))

            books = Book.query.filter(*filters).all()

            if not books:
                message = "No matching book found."
            else:
                count = 0
                for book in books:
                    if new_title:
                        book.title = new_title
                    if new_author:
                        book.author = new_author
                    if new_year.isdigit():
                        book.year = int(new_year)
                    count += 1
                db.session.commit()
                message = f"{count} book(s) updated successfully."

    return render_template("edit_book.html", message=message)

if __name__ == "__main__":
    app.run(debug=True)
    

