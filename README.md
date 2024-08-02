# Clinical Trial Data Extraction

This project provides a script for extracting clinical trial data from abstracts using OpenAI's API.

## Setup

1. Clone the repository.
2. Install required libraries:
    ```bash
    pip install openai pandas
    ```
3. Set up your OpenAI API key in the script.

## Usage

1. Place your abstracts in a text file and set the file path in the script.
2. Run the script:
    ```bash
    python your_script.py
    ```
3. The extracted data will be saved in the specified output folder.

## Customization

- Modify `general_instruction`, `query_study_info`, `query_outcomes_info1`, and other query variables to customize the extraction process.
- Detailed prompts can be provided upon request.

## License

[IMO License](LICENSE)
