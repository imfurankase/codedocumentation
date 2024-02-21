# Code Documentation Generator 🛠️

This tool generates code documentation, comments code files, and provides code analysis reports using OpenAI's GPT-3.5-turbo-instruct

## Prerequisites 📋

- Python 3.0 or higher installed on your system 🐍
- An OpenAI API key 🔑

## Installation ⬇️

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/imfurankase/code-documentation-generator.git
    ```

2. Navigate to the project directory:

    ```bash
    cd code-documentation-generator
    ```

3. Create and activate a virtual environment (because we like to keep our coding environments as tidy as a freshly made bed):

    ```bash
    python -m venv venv
    source venv/bin/activate  # For Linux/macOS
    .\venv\Scripts\activate   # For Windows
    ```

4. Install the required Python packages using pip (don't worry, it's just a few dependencies, not your whole life story):

    ```bash
    pip install -r requirements.txt
    ```

5. Set up your OpenAI API key (but keep it safe, we don't want rogue AIs taking over the world):

    - Sign up for an account on the [OpenAI website](https://openai.com).
    - Retrieve your API key from the dashboard.
    - Create a `.env` file in the project directory.
    - Add your API key to the `.env` file:

        ```plaintext
        OPENAI_API_KEY=your-api-key-here
        ```

## Usage 🚀

1. Run the `commentor.py` script:

    ```bash
    python commentor.py
    ```

2. Select the complexity level of comments and the desired action from the GUI options.

3. Upload the code file you want to analyze or document using the "Upload File" button.

4. Enter your question about the code in the provided field.

5. Click on the "Generate" button to generate the desired output.

6. Follow the on-screen instructions to view or save the generated documentation, commented code, or code analysis report.

## Contributing 🤝

Contributions are welcome! If you find any bugs or have suggestions for improvements, please open an issue or create a pull request.

## License 📝

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
