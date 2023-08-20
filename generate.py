import json
import logging
import prompts
from ai import callOpenAI

def _limit_text(text, limit=200):
    if len(text) > limit:
        return text[:limit] + "..."
    else:
        return text

def _toc_2_text(toc, highlightChapter=None):
    text = ""
    for chapter in toc["chapters"]:
        text += f"{chapter['number']}. {chapter['title']}\n"
        if highlightChapter is None or highlightChapter == chapter:
            for section in chapter["sections"]:
                text += f"    {chapter['number']}.{section['number']}. {section['title']}\n"
        else:
            text += f"    ({len(chapter['sections'])} sections here...)\n"
    return text

def _write_title(book, original_title, history):
    if not book.get('title'):
        logging.info("# Generating a new title...")
        book["title"] = callOpenAI(prompts.title(original_title), history, waitingShortAnwser=True)
        logging.info(f"# New title: {book['title']}")
        yield book
    else:
        logging.info(f"# Writing book {book['title']}...")
        history.append({"role": "system", "content": f'The title of the book is: "{book["title"]}".'})
        # history.append({"role": "user", "content": prompts.title(original_title)})
        # history.append({"role": "assistant", "content": book['title']})
    
    history[0]["content"] += f' The title of the book is "{book["title"]}"'

    logging.info("")

def _write_toc(book, instructions, history):
    if not book.get('toc'):
        logging.info("# Generating a new table of contents...")
        toc_str = callOpenAI(prompts.table_of_contents(instructions), history)
        book["toc"] = json.loads(toc_str)
        #book["toc"]["chapters"] = sorted(book["toc"]["chapters"], key=lambda x: x["number"])
        logging.info(f"Table of Contents:\n{_toc_2_text(book['toc'])}")
        yield book
    else:
        logging.info("# Table of contents already defined...")
        history.append({"role": "system", "content": f"The book has the following table of contents:\n{_toc_2_text(book['toc'])}"})
        # history.append({"role": "user", "content": prompts.table_of_contents(instructions)})
        # history.append({"role": "assistant", "content": json.dumps(book["toc"], indent=4)})
        logging.info(f"Table of Contents:\n{_toc_2_text(book['toc'])}")
    
    logging.info("")

def _write_summary(book, instructions, history):
    if not book.get('summary'):
        logging.info("# Generating a new summary...")
        book["summary"] = callOpenAI(prompts.summary(book, instructions), history, waitingShortAnwser=True, forceMaximum=True)
        logging.info(f'# New summary:\n{book["summary"]}')
        yield book
    else:
        logging.info(f"# Summary is already defined: {_limit_text(book['summary'])}")
        #history.append({"role": "system", "content": f'The book has the following summary:\n{book["summary"]}'})
        # history.append({"role": "user", "content": prompts.summary(book, instructions)})
        # history.append({"role": "assistant", "content": book["summary"]})
    
    history[0]["content"] += f' The summary of the book is: "{book["summary"]}"'
    logging.info("")

def _write_chapter(book, chapter, history):
    chapter_desc = f'"{chapter["number"]}. {chapter["title"]}"'

    if not chapter.get('content'):
        logging.info(f"# Generating a new content for chapter {chapter_desc}:")
        chapter_highlighted_toc = _toc_2_text(book["toc"], chapter)
        chapter["topics"] = callOpenAI(prompts.chapter_topics(book, chapter, chapter_highlighted_toc), history, waitingShortAnwser=True)
        logging.info(f"Topics: {chapter['topics']}")
        chapter["content"] = callOpenAI(prompts.chapter(book, chapter, chapter_highlighted_toc), history, forceMaximum=True)
        logging.info(chapter["content"])
        yield book
    else:
        logging.info(f"# Content for chapter {chapter_desc} is already defined: {_limit_text(chapter['content'])}.\nChapter Topics: {chapter['topics']}")
        history.append({"role": "system", "content": f'The book content for chapter {chapter_desc} is:\n{chapter["content"]}'})
        # history.append({"role": "user", "content": prompts.chapter(book, chapter)})
        # history.append({"role": "assistant", "content": chapter["content"]})

    logging.info("")

def _write_section(book, chapter, section, history):
    section_desc = f'"{chapter["number"]}.{section["number"]}. {section["title"]}"'

    if not section.get('content'):
        logging.info(f"# Generating a new content for section {section_desc}:")
        chapter_highlighted_toc = _toc_2_text(book["toc"], chapter)
        section["topics"] = callOpenAI(prompts.section_topics(book, chapter, section, chapter_highlighted_toc), history, waitingShortAnwser=True)
        logging.info(f"Topics: {section['topics']}")
        section["content"] = callOpenAI(prompts.section(book, chapter, section), history, forceMaximum=True)
        logging.info(section["content"])
        yield book
    else:
        logging.info(f"# Content for section {section_desc} is already defined: {_limit_text(section['content'])}.\nSection Topics: {section['topics']}")
        history.append({"role": "system", "content": f'The book content for section {section_desc} is:\n{section["content"]}'})
        # history.append({"role": "user", "content": prompts.section(book, chapter, section)})
        # history.append({"role": "assistant", "content": section["content"]})
    
    logging.info("")

def write_book(book, original_title, instructions="", language="Brazilian Portuguese"):
    original_message = {"role": "system", "content": f"You are a book writer, writing a new book in {language} refered in the future as BookLanguage."}
    history = [original_message]

    for b in _write_title(book, original_title, history):
        yield b
    
    for b in _write_toc(book, instructions, history):
        yield b
    
    for b in _write_summary(book, instructions, history):
        yield b

    for chapter in book['toc']['chapters']:
        for b in _write_chapter(book, chapter, history):
            yield b

        for section in chapter['sections']:
            for b in _write_section(book, chapter, section, history):
                yield b

    logging.info("")
    logging.info("# Book is finished!")
    yield book
