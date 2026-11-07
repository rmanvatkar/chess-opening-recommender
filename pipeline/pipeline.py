from src.vector_store import VectorStoreBuilder
from src.recommender import OpeningRecommender
from config.config import GROQ_APIKEY, MODEL_NAME
from utils.logger import get_logger
from utils.custom_exception import CustomException


logger = get_logger(__name__)

class OpeningRecommendationPipeline:
    def __init__(self, persist_dir="chess_openings_db"):
        try:
            logger.info("Initializing chess opening recommendation pipeline")

            vector_builder = VectorStoreBuilder(csv_path="", persist_directory=persist_dir)

            retriever = vector_builder.load_vector_store().as_retriever()

            self.recommender = OpeningRecommender(retriever, GROQ_APIKEY, MODEL_NAME)

            logger.info("Chess opening recommendation pipeline initialized")

        except Exception as e:
            logger.error(f"Failed to initialize chess opening recommendation pipeline: {e}")
            raise CustomException("Failed to initialize chess opening recommendation pipeline", e)

    def recommend(self, query: str) -> str:
        try:
            logger.info(f"Generating chess opening recommendations for query: {query}")
            recommendations = self.recommender.get_recommendations(query)
            logger.info("Recommendations generated successfully")
            return recommendations
        except Exception as e:
            logger.error(f"Failed to generate chess opening recommendations: {e}")
            raise CustomException("Failed to generate chess opening recommendations", e)