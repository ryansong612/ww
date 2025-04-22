"""
Chat API Module

This module provides the main interface for the robot's chat functionality,
integrating speech recognition and language model response generation.
"""

from typing import List, Tuple, Optional, Dict
import jieba.analyse
from model import Model, ModelConfig
from recog import RecognizerAdaptor, RecognitionError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatError(Exception):
    """Custom exception for chat-related errors."""
    pass

class ChatAPI:
    """
    Main interface for the robot's chat functionality.

    This class integrates speech recognition and language model capabilities
    to enable real-time conversation with the robot.
    """

    def __init__(
        self,
        api_key: str,
        model_config: Optional[ModelConfig] = None,
        language: str = "zh-CN",
        user_name: str = "user"
    ):
        """
        Initialize the ChatAPI with required components.

        Args:
            api_key (str): API key for the language model service.
            model_config (ModelConfig, optional): Configuration for the language model.
            language (str, optional): Default language for speech recognition.
            user_name (str, optional): Identifier for the user.
        """
        try:
            self.model = Model(api_key=api_key, config=model_config, user_name=user_name)
            self.recognizer = RecognizerAdaptor()
            self.default_language = language
        except Exception as e:
            raise ChatError(f"Failed to initialize ChatAPI: {str(e)}")

    def extract_keywords(self, text: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """
        Extract keywords from the input text using jieba analysis.

        Args:
            text (str): The input text to extract keywords from.
            top_k (int, optional): Number of top keywords to extract.

        Returns:
            List[Tuple[str, float]]: List of tuples containing keywords and their weights.
        """
        try:
            return jieba.analyse.extract_tags(text, topK=top_k, withWeight=True)
        except Exception as e:
            logger.error(f"Keyword extraction failed: {str(e)}")
            return []

    def stream_chat(
        self,
        language: Optional[str] = None,
        stream_response: bool = False
    ) -> Tuple[str, str]:
        """
        Process a single chat interaction using speech recognition and model response.

        Args:
            language (str, optional): Language code for speech recognition.
            stream_response (bool, optional): Whether to stream the model's response.

        Returns:
            Tuple[str, str]: A tuple containing (user_input, bot_response).

        Raises:
            ChatError: If chat processing fails.
        """
        try:
            # Use default language if none specified
            lang = language or self.default_language
            
            # Get user input through speech recognition
            user_input = self.recognizer.recognize_from_mic(language=lang)
            logger.info(f"User: {user_input}")

            # Get model response
            response = self.model.chat(user_input, stream=stream_response)
            logger.info(f"Bot: {response}")

            return user_input, response

        except RecognitionError as e:
            raise ChatError(f"Speech recognition failed: {str(e)}")
        except Exception as e:
            raise ChatError(f"Chat processing failed: {str(e)}")

    def get_conversation_history(self) -> List[Dict[str, str]]:
        """
        Get the current conversation history.

        Returns:
            List[Dict[str, str]]: List of conversation messages.
        """
        return self.model.get_conversation_history()

    def save_conversation(self, filepath: str) -> None:
        """
        Save the current conversation to a file.

        Args:
            filepath (str): Path to save the conversation.
        """
        self.model.save_conversation(filepath)

    def clear_conversation(self) -> None:
        """Clear the current conversation history."""
        self.model.clear_conversation()

def main():
    """Main function to demonstrate the ChatAPI usage."""
    try:
        # Initialize ChatAPI with your API key
        chat = ChatAPI(api_key="REPLACE_API")
        
        # Start a conversation
        user_input, bot_response = chat.stream_chat()
        
        # Extract keywords from the conversation
        keywords = chat.extract_keywords(user_input)
        print(f"Keywords: {keywords}")
        
        # Save the conversation
        chat.save_conversation("chat_history.json")

    except ChatError as e:
        logger.error(f"Chat error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()