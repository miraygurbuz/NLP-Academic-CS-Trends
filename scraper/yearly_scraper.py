from config import *
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import time
import pandas as pd
import os

logger = setup_logger('scraper_logger', 'scraper.log')

def fetch_arxiv_pages(year, max_pages, output=None):
    columns = ['title', 'abstract', 'year', 'timestamp']
    data = []
    if output is None:
        output = get_output_file(year)

    for page in range(0, max_pages):
        start = page * SIZE
        url = (
            f'{BASE_URL}?advanced=&terms-0-operator=AND&terms-0-term=&terms-0-field=title'
            f'&classification-include_cross_list={INCLUDE_CROSS_LIST}'
            f'&classification-computer_science={CLASSIFICATION_COMPUTER_SCIENCE}'
            f'&date-filter_by=specific_year&date-year={year}'
            f'&date-from_date={year}&date-to_date='
            f'&date-date_type=submitted_date&abstracts={ABSTRACTS}'
            f'&size={SIZE}&order={ORDER}&start={start}'
        )
        try:
            response = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(response.text, 'html.parser')
            papers = soup.find_all('li', class_='arxiv-result')
            if not papers:
                logger.warning(f'{year} yili, {page+1} sayfasinda makale bulunamadi')
                break
            for paper in papers:
                try:
                    title_elem = paper.find('p', class_='title is-5 mathjax')
                    if not title_elem:
                        continue
                    title = title_elem.get_text(strip=True)
                    abstract_full = paper.find('span', class_='abstract-full')
                    abstract = abstract_full.get_text(strip=True).replace('△ Less', '').strip() if abstract_full else 'Özet mevcut değil.'
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    data.append([title, abstract, year, timestamp])
                except Exception as e:
                    logger.error(f"Hata: {e}")
            logger.info(f'{year} yili icin {len(data)} makale cekildi')
            time.sleep(10)
        except Exception as e:
            logger.error(f"Hata: {e}")
            break

    df = pd.DataFrame(data, columns=columns)
    df.to_csv(output, index=False)
    logger.info(f'{year} yili verisi CSV dosyasina kaydedildi: {output}')

def merge_yearly_data(start_year, end_year, output=Y_MERGED_OUTPUT_CSV):
    all_data = []
    for year in range(start_year, end_year + 1):
        file_path = get_output_file(year)
        try:
            if os.path.exists(file_path):
                year_data = pd.read_csv(file_path)
                all_data.append(year_data)
                logger.info(f'{file_path} - {len(year_data)} kayit eklendi')
            else:
                logger.warning(f'Bulunamadi {file_path}')
        except Exception as e:
            logger.error(f'Hata {file_path}: {e}')
            continue
    if all_data:
        merged_df = pd.concat(all_data).drop_duplicates(subset=['title', 'abstract']).sort_values(by='year', ascending=True)
        merged_df.to_csv(output, index=False)
        logger.info(f'Tum yillar birlestirildi ve kaydedildi: {output}')
    else:
        logger.warning('Veri yok')

if __name__ == '__main__':
    try:
        for year in range(2020, 2026):
            fetch_arxiv_pages(year, 50)
        merge_yearly_data(2020, 2025)
    except Exception as e:
        logger.error(f'Hata olustu: {e}')