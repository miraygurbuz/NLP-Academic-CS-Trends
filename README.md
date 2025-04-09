# 📖 NLP Academic CS Trends

This project collects academic papers from [arXiv.org](https://arxiv.org/) over the past 5 years and applies text preprocessing to analyze trends in computer science research.

## Setup

- Clone the project:

```
git clone https://github.com/miraygurbuz/NLP-Academic-CS-Trends.git
```
   
- Install the dependencies:

```
pip install -r requirements.txt
```

## Usage

### 1. Configuration

#### Scraper Configuration

```python
# arXiv advanced search configuration
BASE_URL = 'https://arxiv.org/search/advanced'
DEFAULT_TERM = 'ACM OR IEEE'            # First search term (journal reference)
SECOND_TERM = 'Springer OR Elsevier'    # Second search term (journal reference)
CLASSIFICATION_COMPUTER_SCIENCE = 'y'   # Include Computer Science papers
INCLUDE_CROSS_LIST = 'exclude'          # Exclude cross-listed papers
SIZE = 200                              # Number of results per page
ORDER = ''                              # Default ordering
ABSTRACTS = 'show'                      # Show abstracts in results
```

#### Preprocessing Configuration
```python
ACADEMIC_STOPWORDS = {...}              # Common academic words to exclude from analysis

NORMALIZATION_PATTERNS = {
    'html_tags': r'<.*?>',              # Removes HTML tags  
    'urls': r'http\S+',                 # Removes URLs  
    'numbers': r'\d+',                  # Removes digits  
    'multiple_spaces': r'\s+',          # Replaces multiple spaces with one  
    'punctuation': string.punctuation   # Removes punctuation  
}

CONFIG = {
    'data_path': '../data/raw/merged.csv',                 # Input dataset  
    'cleaned_output': '../data/processed/cleaned.csv',     # Output of cleaned data  
    'processed_output': '../data/processed/processed.csv', # Final processed output  
    'url_replacement': '[URL]',                            # Placeholder for removed URLs  
    'min_token_length': 2,                                 # Minimum length of tokens to keep  
    'normalization_lowercase': True,                       # Convert text to lowercase  
    'normalization_patterns': NORMALIZATION_PATTERNS       # Apply regex patterns  
}

```

### 2. Data Scraping

#### Run the scraper:

```bash
python scraper/scraper.py
```

  - Collects papers based on journal references, subject classification and date range
  - Temporary CSVs are created every 400 papers to avoid data loss
    
or

```bash
python scraper/yearly_scraper.py
```
  - Collects papers year by year based on subject classification

  #### Notes
  
  - Both scripts rely on shared config in config.py
  - All activity is logged to scraper.log
  - Columns in the output CSV:
    
      - `title`: The title of the academic paper
      - `abstract`: The abstract of the academic paper
      - `year`: The year the paper was published
      - `timestamp`: The time when the data was collected

### 3. Data Preprocessing

Run the preprocessing script to clean and process your collected papers:

```bash
python preprocessing/main.py
```

The preprocessing module performs the following operations:

1. **Basic Text Cleaning**
   - Removes HTML tags
   - Normalizes multiple spaces
   - Replaces URLs with placeholder text
   - Preserves case, punctuation, and numbers

2. **Advanced Text Processing**
   - Converts text to lowercase
   - Removes HTML tags, punctuation, and numbers
   - Normalizes whitespace
   - Tokenizes text into individual words
   - Filters tokens by minimum length
   - Removes stopwords

3. **NLP Operations**
   - **Tokenization**: Splits text into individual words
   - **Lemmatization**: Reduces words to their base or dictionary form
   - **Stemming**: Reduces words to their word stem

  - #### Input Data Format

    The input CSV should have at least the following columns:
    - `title`: The title of the academic paper
    - `abstract`: The abstract of the academic paper

  - #### Output

    - **cleaned.csv**: Contains basic cleaned text with minimal alterations
      - `cleaned_title`: Basic cleaned title
      - `cleaned_abstract`: Basic cleaned abstract
      - `combined_text`: Combined title and abstract with [SEP] separator
   
    - **processed.csv**: Contains fully processed text for NLP analysis
      - `cleaned_title`/`cleaned_abstract`: Thoroughly cleaned text
      - `title_tokens`/`abstract_tokens`: Tokenized words
      - `title_lemmatized`/`abstract_lemmatized`: Lemmatized tokens
      - `title_stemmed`/`abstract_stemmed`: Stemmed tokens
      - `combined_lemmatized`: Combined lemmatized text from title and abstract
      - `combined_stemmed`: Combined stemmed text from title and abstract

  - #### Code Structure

    - `main.py`: Entry point script
    - `preprocessing.py`: Core text processing functions
    - `config.py`: Configuration parameters and stopwords
   
## Data Source

This project uses data from [arXiv.org](https://arxiv.org/), an open-access repository of electronic preprints for scientific papers.