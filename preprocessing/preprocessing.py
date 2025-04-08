import re
import pandas as pd
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from tqdm import tqdm

tqdm.pandas()

def download_nltk_resources():
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('taggers/averaged_perceptron_tagger')
        nltk.data.find('corpora/stopwords')
        nltk.data.find('corpora/wordnet')
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        print('Downloading necessary NLTK resources...')
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('averaged_perceptron_tagger_eng')
        nltk.download('stopwords')
        nltk.download('wordnet')
        nltk.download('punkt_tab')

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

def get_wordnet_pos(word):
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {
        'J': wordnet.ADJ,
        'N': wordnet.NOUN,
        'V': wordnet.VERB,
        'R': wordnet.ADV
    }
    return tag_dict.get(tag, wordnet.NOUN)

def clean_text_basic(text, config):
    if not isinstance(text, str):
        return ''
    text = re.sub(config['normalization_patterns']['html_tags'], '', text)
    text = re.sub(config['normalization_patterns']['multiple_spaces'], ' ', text)
    text = re.sub(config['normalization_patterns']['urls'], config['url_replacement'], text)
    return text.strip()

def clean_text(text, config):
    if not isinstance(text, str):
        return ''
    if config['normalization_lowercase']:
        text = text.lower()
    text = re.sub(config['normalization_patterns']['html_tags'], '', text)
    text = text.translate(str.maketrans('', '', config['normalization_patterns']['punctuation']))
    text = re.sub(config['normalization_patterns']['numbers'], '', text)
    text = re.sub(config['normalization_patterns']['multiple_spaces'], ' ', text)
    return text.strip()

def preprocess_text(text, config, stop_words):
    text = clean_text(text, config)
    tokens = word_tokenize(text)
    filtered_tokens = []
    
    for token in tokens:
        if len(token) > config['min_token_length']: 
            stemmed_token = stemmer.stem(token)
            if token not in stop_words and stemmed_token not in stop_words:
                filtered_tokens.append(token)
    
    lemmatized = [lemmatizer.lemmatize(token, get_wordnet_pos(token)) for token in filtered_tokens]
    stemmed = [stemmer.stem(token) for token in filtered_tokens]
    return {
        'tokens': filtered_tokens,
        'lemmatized': lemmatized,
        'stemmed': stemmed
    }

def load_data(filepath):
    print(f"'{filepath}' dosyasından veri yükleniyor...")
    df = pd.read_csv(filepath)
    print(f'Veri başarıyla yüklendi. Boyut: {df.shape}')
    return df

def process_dataframe(df, config, stop_words):
    cleaned = df.copy()
    processed = df.copy()
    
    print('\nBasit metin temizleme işlemi başlatılıyor...')
    cleaned['cleaned_title'] = cleaned['title'].apply(lambda x: clean_text_basic(x, config))
    cleaned['cleaned_abstract'] = cleaned['abstract'].apply(lambda x: clean_text_basic(x, config))
    cleaned['combined_text'] = cleaned['cleaned_title'] + ' [SEP] ' + cleaned['cleaned_abstract']
    
    print('\n"title" sütununda temizlik başlatılıyor...')
    processed['cleaned_title'] = processed['title'].progress_apply(lambda x: clean_text(x, config))
    
    print('\n"abstract" sütununda temizlik başlatılıyor...')
    processed['cleaned_abstract'] = processed['abstract'].progress_apply(lambda x: clean_text(x, config))
    
    print('\n"cleaned_title" için tokenize/stem/lemmatize işlemleri uygulanıyor...')
    title_processed = processed['cleaned_title'].progress_apply(lambda x: preprocess_text(x, config, stop_words))
    
    print('\n"cleaned_abstract" için tokenize/stem/lemmatize işlemleri uygulanıyor...')
    abstract_processed = processed['cleaned_abstract'].progress_apply(lambda x: preprocess_text(x, config, stop_words))
    
    print('\n"title" processed sonuçları ayrıştırılıyor...')
    processed['title_tokens'] = title_processed.progress_apply(lambda x: x['tokens'])
    processed['title_lemmatized'] = title_processed.progress_apply(lambda x: x['lemmatized'])
    processed['title_stemmed'] = title_processed.progress_apply(lambda x: x['stemmed'])
    
    print('\n"abstract" processed sonuçları ayrıştırılıyor...')
    processed['abstract_tokens'] = abstract_processed.progress_apply(lambda x: x['tokens'])
    processed['abstract_lemmatized'] = abstract_processed.progress_apply(lambda x: x['lemmatized'])
    processed['abstract_stemmed'] = abstract_processed.progress_apply(lambda x: x['stemmed'])
    
    print('\nLemmatized ve stemmed vektörler birleştiriliyor...')
    processed['combined_lemmatized'] = processed.progress_apply(
        lambda row: ' '.join(row['title_lemmatized'] + row['abstract_lemmatized']), axis=1)
    processed['combined_stemmed'] = processed.progress_apply(
        lambda row: ' '.join(row['title_stemmed'] + row['abstract_stemmed']), axis=1)
    return cleaned, processed

def save_processed_data(cleaned_df, processed_df, cleaned_path, processed_path):
    print(f"Temizlenmiş veri '{cleaned_path}' konumuna kaydediliyor...")
    cleaned_df.to_csv(cleaned_path, index=False)
    print(f"İşlenmiş veri '{processed_path}' konumuna kaydediliyor...")
    processed_df.to_csv(processed_path, index=False)
    print('✅ Veriler başarıyla kaydedildi.')

def display_sample(df, cleaned_df, processed_df, sample_idx=0):
    print('\n📝 Örnek Makale Karşılaştırması:')
    print(f'Orijinal özet: {df.iloc[sample_idx]['abstract']}')
    print(f'Basit temizlenmiş: {cleaned_df.iloc[sample_idx]['cleaned_abstract']}')
    print(f'Kapsamlı temizlenmiş: {processed_df.iloc[sample_idx]['cleaned_abstract']}')
    print(f'Lemmatized özet: {', '.join(processed_df.iloc[sample_idx]['abstract_lemmatized'])}')
    print(f'Stemmed özet: {', '.join(processed_df.iloc[sample_idx]['abstract_stemmed'])}')
    print('\n📊 Özet Bilgiler:')
    print(f'Orijinal veri boyutu: {df.shape}')
    print(f'Basit ön işleme yapılmış veri (cleaned.csv): {cleaned_df.shape}')
    print(f'Kapsamlı ön işleme yapılmış veri (processed.csv): {processed_df.shape}')