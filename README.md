# GhostWriter AI: Experimental Book Writer using OpenAI GPT LLM

This project is an experimental attempt to write books using the OpenAI GPT LLM model. It's inspired by various other projects in the AI and literature domains. While the current implementation has shown promising results, there's always room for improvement and optimization.

## Running the Code

To run the code, you'll need to set up several environment variables. These variables help configure the OpenAI API and other related parameters for generating the book content.

### Environment Variables

1. `OPENAI_API_KEY`: Your personal API key for accessing OpenAI services.
2. `OPENAI_ENGINE`: The engine you're using for the OpenAI model.
3. `OPENAI_MODEL` (optional): The specific model you're using (e.g., `gpt4`).
4. `BOOK_LANGUAGE`: The language in which you want the book to be written. (**will be asked if not set**)
5. `BOOK_TITLE`: The title of the book you're generating. (**will be asked if not set**)
6. `BOOK_INSTRUCTIONS`: Specific instructions or prompts you want to give to the model for generating the book content. (**will be asked if not set**)
7. `OPENAI_API_BASE` (optional): The base URL for the OpenAI API.
8. `OPENAI_API_TYPE` (optional): The type of API you're accessing (e.g., `v1`).
9. `OPENAI_API_VERSION` (optional): The version of the API you're using.
10. `TEMPERATURE` (optional): A parameter that controls the randomness of the model's output. Higher values make the output more random, while lower values make it more deterministic. (default: 0.2)
11. `TOKEN_LIMIT` (optional): The maximum number of tokens (words/characters) can hangle in a single request. (default: `4096`)
12. `MAX_TOKEN` (optional): The absolute maximum number of tokens the model can handle. (default: `TOKEN_LIMIT/4`)
13. `MAX_TOKENS_SHORT` (optional): The absolute maximum number of tokens the model can handle for short awnsers. (default: `MAX_TOKENS/4`)

### Steps to Run

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Create a virtual environment and install the dependencies: `pip install -r requirements.txt`
4. Set up the environment variables. You can do this by exporting them in your shell or by using a `.env` file.
5. Once the environment variables are set, run the main script (e.g., `python main.py`).
6. The script will use the provided environment variables to generate the book content based on your specifications.

Note: Ensure you have all the necessary dependencies installed and that you handle the OpenAI API rate limits and costs associated with generating large amounts of text.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). This license allows for reuse of parts or all of the code, as long as the original source is acknowledged.

Feel free to contribute, suggest changes, or fork the repository. Your feedback and contributions are always welcome!
