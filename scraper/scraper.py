from config import *
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import time
import pandas as pd

logger = setup_logger('scraper_logger', 'scraper.log')

def fetch_arxiv_pages(from_year, to_year, max_pages, term=DEFAULT_TERM, output=OUTPUT1_CSV):
    columns = ['title', 'abstract', 'year', 'timestamp']
    data = []

    for start in range(0, max_pages * SIZE, SIZE):
        url = (
            f'{BASE_URL}?advanced=&terms-0-operator=AND'
            f'&terms-0-term={term}&terms-0-field=journal_ref'
            f'&terms-1-operator=AND&terms-1-term=&terms-1-field=journal_ref'
            f'&classification-computer_science={CLASSIFICATION_COMPUTER_SCIENCE}'
            f'&classification-include_cross_list={INCLUDE_CROSS_LIST}'
            f'&date-filter_by=date_range&date-from_date={from_year}&date-to_date={to_year}'
            f'&date-date_type=submitted_date&abstracts={ABSTRACTS}&size={SIZE}'
            f'&order={ORDER}&start={start}'
        )

        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')
        papers = soup.find_all('li', class_='arxiv-result')

        if not papers:
            logger.warning(f'{start} itibariyle makale bulunamadı.')
            break

        for i, paper in enumerate(papers):
            title = paper.find('p', class_='title is-5 mathjax').get_text(strip=True)
            abstract_full = paper.find('span', class_='abstract-full')
            if abstract_full:
                abstract = abstract_full.get_text(strip=True)
                abstract = abstract.replace('△ Less', '').strip()
            else:
                abstract = 'Ozet mevcut değil.'
            submitted = paper.find('p', class_='is-size-7').get_text(strip=True)
            year_part = submitted.split(' ')[2]
            year = year_part.split(';')[0]
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data.append([title, abstract, year, timestamp])

            if len(data) % 400 == 0 and len(data) > 0:
                temp_file_name = os.path.join(TEMP_DIR, f'papers_temp.csv')
                temp_df = pd.DataFrame(data, columns=columns)
                temp_df.to_csv(temp_file_name, mode='a', index=False)
                logger.info(f'Ara kayit: {len(data)} makale kaydedildi.')

            logger.info(f'[{timestamp}] Makale {i+1} cekildi: {title[:50]}... ({year})')
        time.sleep(10)

    df = pd.DataFrame(data, columns=columns)
    df.to_csv(output, index=False)
    logger.info(f'CSV dosyasina kaydedildi: {output}')

if __name__ == '__main__':
    fetch_arxiv_pages(2020, 2025, 50)
    fetch_arxiv_pages(2020, 2025, 50, SECOND_TERM, OUTPUT2_CSV)
    try:
        df1 = pd.read_csv(OUTPUT1_CSV)
        df2 = pd.read_csv(OUTPUT2_CSV)
        merged_df = pd.concat([df1, df2]).drop_duplicates(subset=['title', 'abstract'])
        merged_df = merged_df.sort_values(by='year', ascending=True)
        merged_df.to_csv(MERGED_OUTPUT_CSV, index=False)
        logger.info(f'CSV dosyaları birlestirildi ve kaydedildi: {MERGED_OUTPUT_CSV}')
    except Exception as e:
        logger.error(f'CSV birlestirme sirasinda hata oluştu: {e}')

