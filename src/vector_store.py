from dotenv import load_dotenv
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import CharacterTextSplitter


load_dotenv()


class VectorStoreBuilder:
    def __init__(self, csv_path: str, persist_directory: str = "chess_openings_db"):
        self.csv_path = csv_path
        self.persist_directory = persist_directory
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    def build_and_save_vector_Store(self):
        loader = CSVLoader(
            file_path=self.csv_path,
            encoding="utf-8",
            metadata_columns=[],
        )
        data = loader.load()
        splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = splitter.split_documents(data)
        Chroma.from_documents(
            texts,
            self.embeddings,
            persist_directory=self.persist_directory,
        )

    def load_vector_store(self):
        return Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings,
        )
