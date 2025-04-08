from nltk.corpus import stopwords
import argparse
from preprocessing import (
    download_nltk_resources, load_data, process_dataframe,
    save_processed_data, display_sample
)
from config import CONFIG, ACADEMIC_STOPWORDS

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', type=str, default=CONFIG['data_path'],)
    parser.add_argument('--cleaned_output', type=str, default=CONFIG['cleaned_output'],)
    parser.add_argument('--processed_output', type=str, default=CONFIG['processed_output'],)
    parser.add_argument('--sample_idx', type=int, default=0,)
    args = parser.parse_args()
    CONFIG['data_path'] = args.data_path
    CONFIG['cleaned_output'] = args.cleaned_output
    CONFIG['processed_output'] = args.processed_output
    return args

def main():
    args = parse_arguments()
    download_nltk_resources()
    stop_words = set(stopwords.words('english'))
    stop_words.update(ACADEMIC_STOPWORDS)
    df = load_data(CONFIG['data_path'])
    print("\nVeri Seti Örneği:")
    print(df.head(5))
    print("\nVeri Seti Bilgileri:")
    print(f"Satır sayısı: {df.shape[0]}")
    print(f"Sütun sayısı: {df.shape[1]}")
    print(f"Sütunlar: {', '.join(df.columns)}")
    cleaned_df, processed_df = process_dataframe(df, CONFIG, stop_words)
    save_processed_data(
        cleaned_df, 
        processed_df, 
        CONFIG['cleaned_output'], 
        CONFIG['processed_output']
    )
    display_sample(df, cleaned_df, processed_df, args.sample_idx)
    return df, cleaned_df, processed_df

if __name__ == "__main__":
    main()