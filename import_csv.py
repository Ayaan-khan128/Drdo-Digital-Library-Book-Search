import csv
from app import db, Book, app  # make sure these match your actual file structure

with app.app_context():
    with open('synthetic_books_dataset.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        books = []

        for row in reader:
            try:
                book = Book(
                    title=row['title'],
                    author=row['author'],
                    year=int(row['year']),
                    keywords=row['keywords'],
                    abstract=row['abstract']
                )
                books.append(book)
            except Exception as e:
                print(f"❌ Error in row: {row}\n{e}")

        db.session.bulk_save_objects(books)
        db.session.commit()
        print(f"✅ Imported {len(books)} books into the database.")
