from faker import Faker
import random
import csv

fake = Faker()

keywords_pool = [
    "radar", "missile", "cybersecurity", "AI", "drone", "surveillance", "stealth",
    "ballistics", "communication", "electronic warfare", "robotics", "autonomous", 
    "military", "satellite", "defense", "sensor", "GPS", "UAV", "targeting"
]

NUM_BOOKS = 5000

with open("synthetic_books_dataset.csv", "w", newline='', encoding="utf-8") as csvfile:
    fieldnames = ["title", "author", "year", "keywords", "abstract"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for _ in range(NUM_BOOKS):
        title = f"{fake.catch_phrase()} in {random.choice(['Defense', 'Military', 'Warfare', 'Combat'])}"
        author = fake.name()
        year = random.randint(1970, 2024)
        keywords = ", ".join(random.sample(keywords_pool, k=random.randint(3, 6)))
        abstract = fake.text(max_nb_chars=200)

        writer.writerow({
            "title": title,
            "author": author,
            "year": year,
            "keywords": keywords,
            "abstract": abstract
        })

print(f"✅ {NUM_BOOKS} synthetic books generated in 'synthetic_books_dataset.csv'")
