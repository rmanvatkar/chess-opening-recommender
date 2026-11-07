from src.data_loader import OpeningDataLoader
from src.vector_store import VectorStoreBuilder
from utils.custom_exception import CustomException
from utils.logger import get_logger


logger = get_logger(__name__)


def main():
    try:
        logger.info("Starting chess opening data processing")

        loader = OpeningDataLoader(
            "data/chess_openings.csv",
            "data/openings_processed.csv",
        )
        processed_csv = loader.load_and_process()

        logger.info("Chess opening data processed successfully")

        vector_store_builder = VectorStoreBuilder(
            processed_csv,
            persist_directory="chess_openings_db",
        )
        vector_store_builder.build_and_save_vector_Store()

        logger.info("Chess opening vector store built and saved successfully")
    except Exception as e:
        logger.error(f"Failed to build chess opening recommendation data: {e}")
        raise CustomException("Failed to build chess opening recommendation data", e)


if __name__ == "__main__":
    main()
