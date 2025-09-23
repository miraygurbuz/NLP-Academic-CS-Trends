# Computer Science Research Trends (2020–2025)

Academic papers in computer science from [arXiv.org](https://arxiv.org/) were collected, preprocessed, and analyzed through topic modeling with BERTopic, Top2Vec, FASTopic, CombinedTM, and ZeroShotTM to identify research trends.

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

## Results

| Metric | BERTopic | Top2Vec | FASTopic | CombinedTM | ZeroShotTM |
|--------|----------|---------|----------|------------|------------|
| C_v Coherence | 0.7625 | 0.6937 | 0.5601 | 0.6116 | 0.6223 |
| U_Mass Coherence | -2.2975 | -3.5214 | -3.6915 | -2.3955 | -2.2460 |
| NPMI Coherence | 0.1865 | 0.1625 | 0.0190 | 0.0735 | 0.0910 |
| UCI Coherence | 1.7352 | 0.5529 | -0.9888 | 0.3238 | 0.7254 |

### BERTopic Results

* **Embedding Model:** paraphrase-mpnet-base-v2

#### Growing Topics from 2020 to 2025

<img width="1250" height="450" alt="growing" src="https://github.com/user-attachments/assets/9508d803-9c17-4cba-ba41-a1efaf06aa7b" />


| Topic ID | Description | Keywords |
|----------|-|-|
| 5        | Diffusion-Based Image & Video Generation | diffusion, diffusion model, image, edit, generation, style, texttoimage, model, video, image generation |
| 21       | Reasoning & Prompting in LLMs|reason, llm, language model, prompt, language, large language, cot, reason task, answer, model llm| 
| 19       | Multimodal Question Answering (VQA) |visual, mllms, vlms, visionlanguage, vqa, multimodal, reason, token, answer, question|
| 54       | 3D Rendering via Gaussian Splatting|gaussian, splatting, gaussian splatting, dg, render, scene, gaussians, reconstruction, view, splatting dg|
| 18       | Code Generation & Software Debugging |code, bug, program, software, code generation, test, llm, developer, language, generation|
| 35       | Retrieval-Augmented Generation (RAG) |retrieval, rag, query, document, search, retrievalaugmented, llm, retrieve, retriever, answer|
| 36       | Video Understanding & Captioning |video, temporal, caption, moment, video understand, video caption, long video, understand, retrieval, videotext|
| 91       | Human Motion Synthesis & Animation  |motion, human motion, motion generation, human, generation, motion synthesis, animation, diffusion, motion sequence, video|
| 64       | Vision Transformers (ViTs) |vision transformer, transformer, vits, vit, vision, token, attention, transformer vits, image, patch|
| 113      | Parameter-Efficient Fine-Tuning (LoRA, PEFT) |finetuning, lora, peft, lowrank, parameter, parameterefficient, lowrank adaptation, adapter, parameterefficient finetuning, adaptation|
## Data Source

This project uses data from [arXiv.org](https://arxiv.org/), an open-access repository of electronic preprints for scientific papers.
