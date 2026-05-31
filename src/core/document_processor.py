from pathlib import Path
from pydantic import BaseModel

raw_data_path = Path(__file__).resolve().parent.parent.parent / "data" / "raw"

class Chunk(BaseModel):
    page_content: str
    metadata: dict

def read_and_process_faq(data_path: Path = None):
    """
    Read all Markdown FAQ files in the data directory and split them into chunks.

    This function scans for '*.md' files in the specified directory, extracts the topic 
    (Category) from the first line of each file, and chunks the document based on each 
    question formatted as "## Question: /question/ Content: /answer/".

    Args:
        data_path (Path, optional): The path to the directory containing the FAQ files. 
                                    If not provided (or None), it defaults to the project's 
                                    raw data path.

    Returns:
        list[Chunk]: A list of Chunk objects packed with metadata (source file and category).
    """
    if data_path is None:
        data_path = raw_data_path
    chunks_list: list[Chunk] = []
    for file_path in data_path.glob('*.md'):
        # print(file_path);
        with open(file_path, "r", encoding="utf-8") as file:
            raw_data = file.read().split("## ")
            current_category = raw_data[0].split('# Category: ')[-1].strip()
            current_metadata = {'source_file': file_path.name, 'category': current_category}
            for i in range(1, len(raw_data)):
                chunk = Chunk(
                    page_content = raw_data[i].strip(),
                    metadata = current_metadata
                )
                chunks_list.append(chunk)
    return chunks_list

if __name__ == "__main__":
    clist = read_and_process_faq()
    print(clist)