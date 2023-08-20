import config

def title(title_string):
    return (f'''
I want you to write a book with title "{title_string}".
Translate the title to YourLanguage if necessary, normalize it so that it looks like a real book title,
and output it as plain text. It should not contain a trailing period '.'.
Do not wrap the output in single or double quotes.
Capitalize the first letter of some words, to add meaning.

Example output 1:
A Small Book on Time Series in R

Example output 2:
A Comprehensive Guide to Music Therapy

Example output 3:
A Guide to the Project Management Body of Knowledge

The plain text normalized title on specified language is:
''')


def table_of_contents(instructions):
    return (f'''
Generate Table of Contents with chapters and sections for the book.
{instructions}.

It should be in YourLanguage.
It should contain at least 11 top level chapters, each with 5 to 10 sections.
It should contain only top level chapters with sections, no subsections should be included.
Do not include any extra text or notes before or after the desired output.

Do not include Glossary.
Do not include Key Terms and Definitions.
Do not incude References.
Do not include Acknowledgments.
Do not include About the Author.
Do not include Appendices.
Do not add any notes after the table of contents.

Output in JSON format, with the following format:
(replace the placeholders in double curely braces with the actual values):

{{
    "chapters": [
        {{  "number":{{chapter number}},
            "title":"{{chapter title}}",
            "sections": [
                {{"number":{{section number}},"title":"{{section title}}"}},
                {{"number":{{section number}},"title":"{{section title}}"}}
            ]
        }}
        {{rest of chapters with sections in the same format}}
    ]
}}
'''.strip())



def summary(book, instructions):
    return f'''
You need to write a summary to the book with instructions:
{instructions}.

Generate two plain text paragraphs in YourLanguage summarizing the book {book["title"]}.
The summary should be two single paragraphs, without any links, images or headers.
Here is the summary of the book:
'''.strip();

def chapter_topics(book, chapter, toc_text):
    return (f'''
The book has the following table of contents:
{toc_text}

You are writing an introduction to chapter number {chapter["number"]} with title "{chapter["title"]}".
List 3 important topics that should be covered in this chapter.
Do not include topics that are already covered in previous chapters or will be covered in future chapters.
Dot not explain the topics, just list them, separed by semicolon. Do not list as a numbered list.
'''.strip())


def chapter(book, chapter, toc_text):
    return (f'''
The book has the following table of contents:
{toc_text}

You are writing an introduction to chapter number {chapter["number"]} with title "{chapter["title"]}".
Here are the topics that should be covered in this chapter: {chapter["topics"]}.
Generate a short introduction to this chapter with at least 2 paragraphs.
The generated text content should be in a sequence of paragraphs, without any links, images or headers.
Use markdown format.
Do not include chapter title or number in the output.
'''.strip())

def section_topics(book, chapter, section, toc_text):
    return (f'''
The book has the following table of contents:
{toc_text}
You are writing a section number {chapter["number"]}.{section["number"]} with title "{section["title"]}"
in the chapter called "{chapter["title"]}".
Here are the topics that should be covered in this chapter: {chapter["topics"]}

List 3 to 6 important topics, separated by semicolons, that should be covered in this section.
Do not include topics that are already covered in previous sections or will be covered in future sections.
Dot not explain the topics, just list them, separed by semicolon. Do not list as a numbered list.
'''.strip())


def section(book, chapter, section):
    return (f'''
You are writing a section number {chapter["number"]}.{section["number"]} with title "{section["title"]}" on a chapter called "{chapter["title"]}".
Generate the content text of this section with at least {len(section["topics"].split(";"))} paragraphs covering all this topics: {section["topics"]}.
The generated text content should be in a sequence of paragraphs, without any links, images or headers.
Use markdown format.
Do not include chapter or section title or number in the output.
'''.strip())
