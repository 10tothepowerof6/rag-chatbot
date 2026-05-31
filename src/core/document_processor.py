from pathlib import Path
from pydantic import BaseModel

raw_data_path = Path(__file__).resolve().parent.parent.parent / "data" / "raw"

class Chunk(BaseModel):
    page_content: str
    metadata: dict

def read_and_process_faq():
    chunks_list: list[Chunk] = []
    for file_path in raw_data_path.glob('*.md'):
        # print(file_path);
        with open(file_path, "r", encoding="utf-8") as file:
            raw_data = file.read().split("## Question: ")
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