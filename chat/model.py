"""
Language Model Interface Module

This module provides an interface to interact with language models
through the OpenAI API, specifically configured for DeepSeek models.
"""

from typing import List, Dict, Optional, Any
from openai import OpenAI
from dataclasses import dataclass
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ModelConfig:
    """Configuration settings for the language model."""
    model_name: str = "deepseek-chat"
    max_tokens: int = 20
    temperature: float = 1.0
    top_p: float = 1.0
    presence_penalty: float = 0.0
    frequency_penalty: float = 0.0

class ModelError(Exception):
    """Custom exception for model-related errors."""
    pass

class Model:
    """
    A class that handles interactions with the language model.

    This class manages the conversation context and handles API calls
    to the language model service.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.deepseek.com",
        user_name: str = "user",
        config: Optional[ModelConfig] = None
    ):
        """
        Initialize the Model instance.

        Args:
            api_key (str): API key for authentication.
            base_url (str, optional): Base URL for the API.
            user_name (str, optional): User identifier.
            config (ModelConfig, optional): Model configuration.

        Raises:
            ModelError: If initialization fails.
        """
        try:
            self.client = OpenAI(api_key=api_key, base_url=base_url)
            self.messages: List[Dict[str, str]] = []
            self.config = config or ModelConfig()
            self.user_name = user_name
            logger.info(f"Model initialized with config: {self.config}")
        except Exception as e:
            raise ModelError(f"Failed to initialize model: {str(e)}")

    def chat(
        self,
        message: str,
        stream: bool = False
    ) -> str:
        """
        Send a message to the language model and get a response.

        Args:
            message (str): The input message to send to the model.
            stream (bool, optional): Whether to stream the response.

        Returns:
            str: The model's response.

        Raises:
            ModelError: If the API call fails.
        """
        try:
            # Add user message to conversation history
            self.messages.append({
                "role": "user",
                "content": message,
                "name": self.user_name
            })

            # Create the API request
            response = self.client.chat.completions.create(
                model=self.config.model_name,
                messages=self.messages,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                top_p=self.config.top_p,
                presence_penalty=self.config.presence_penalty,
                frequency_penalty=self.config.frequency_penalty,
                stream=stream
            )

            if stream:
                return self._handle_stream_response(response)
            
            return self._handle_normal_response(response)

        except Exception as e:
            raise ModelError(f"Chat completion failed: {str(e)}")

    def convert_message_to_dict(message) -> dict:
        """
        Convert a ChatCompletionMessage object to a JSON-serializable dictionary.
        
        Args:
            message: ChatCompletionMessage object from OpenAI
            
        Returns:
            dict: JSON-serializable dictionary containing message data
        """
        return {
            "role": message.role,
            "content": message.content,
            "name": message.name if hasattr(message, 'name') else None
        }

    def _handle_normal_response(self, response: Any) -> str:
        """
        Handle non-streaming response from the API.
        
        Args:
            response (Any): Response from the API.
            
        Returns:
            str: Processed response content.
        """
        top_choice = response.choices[0].message
        message_dict = {
            "role": top_choice.role,
            "content": top_choice.content,
            "name": top_choice.name if hasattr(top_choice, 'name') else None
        }
        self.messages.append(message_dict)
        return top_choice.content

    def _handle_stream_response(self, response: Any) -> str:
        """
        Handle streaming response from the API.

        Args:
            response (Any): Streaming response from the API.

        Returns:
            str: Complete response content.
        """
        full_response = []
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                full_response.append(content)
                print(content, end='', flush=True)
        
        complete_response = ''.join(full_response)
        self.messages.append({
            "role": "assistant",
            "content": complete_response
        })
        return complete_response

    def clear_conversation(self) -> None:
        """Clear the conversation history."""
        self.messages = []
        logger.info("Conversation history cleared")

    def get_conversation_history(self) -> List[Dict[str, str]]:
        """
        Get the current conversation history.

        Returns:
            List[Dict[str, str]]: List of message dictionaries.
        """
        return self.messages.copy()

    def save_conversation(self, filepath: str) -> None:
        """
        Save the conversation history to a file.

        Args:
            filepath (str): Path to save the conversation history.

        Raises:
            ModelError: If saving fails.
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.messages, f, ensure_ascii=False, indent=2)
            logger.info(f"Conversation saved to {filepath}")
        except Exception as e:
            raise ModelError(f"Failed to save conversation: {str(e)}")

def main():
    """Main function to demonstrate the Model usage."""
    try:
        # Initialize model with your API key
        model = Model(api_key="your-api-key")
        
        # Example conversation
        response1 = model.chat("你好,请记住数字一，后面回答只能说一")
        print(f"Bot: {response1}")
        
        response2 = model.chat("1+1等于几")
        print(f"Bot: {response2}")
        
        # Save conversation history
        model.save_conversation("conversation_history.json")
        
    except ModelError as e:
        logger.error(f"Model error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()