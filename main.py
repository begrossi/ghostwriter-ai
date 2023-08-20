import os
import json
import logging
import slugify
import generate
from config import BASE_DIR, BOOK_LANGUAGE, BOOK_TITLE, BOOK_INSTRUCTIONS
from bookprinter import print_book



# A function that read title and toc from a book.json file or generate a new one.
def get_book(book_base_dir, title, instructions, language):
    book_json_path = f'{book_base_dir}/book.json'

    book = {}
    if os.path.exists(book_json_path):
        logging.info(f"Reading book {book_json_path}...")
        with open(book_json_path, 'r') as f:
            book = json.load(f)

    for b in generate.write_book(book, title, instructions, language):
        with open(book_json_path, 'w') as f:
            json.dump(b, f, indent=4)
            logging.info(">> Book saved to book.json")

    for chapter in book['toc']['chapters']:
        nstr = "{:02}".format(chapter['number'])
        chapter_slug = slugify.slugify(chapter['title'])
        chapter["file"] = f"{nstr}-{chapter_slug}.md"

    return book

def main():
    logging.info(f">> Book Writer AI")


    language = BOOK_LANGUAGE or input("In which language do you want to write the book? (you can use BOOK_LANGUAGE env variable): ")
    original_title = BOOK_TITLE or input("What is the title of the book? (you can use BOOK_TITLE env variable): ")
    instructions = BOOK_INSTRUCTIONS or input("What are the instructions for the book? (you can use BOOK_INSTRUCTIONS env variable): ")

    book_base_dir = f"{BASE_DIR}/books/{slugify.slugify(original_title)}"
    # create directory if not exists
    os.makedirs(book_base_dir, exist_ok=True)

    book = get_book(book_base_dir, original_title, instructions, language)

    print_book(book_base_dir, book)

if __name__ == "__main__":
    main()