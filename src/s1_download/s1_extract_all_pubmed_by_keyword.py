from paperscraper.pubmed import get_and_dump_pubmed_papers
from src.configs import disease, method

if __name__ == '__main__':
    query = [disease, method]
    get_and_dump_pubmed_papers(query, output_filepath='../../data/Gaucher.jsonl')
