"""
Speech Recognition Adaptor Module

This module provides a wrapper for the speech recognition functionality,
supporting both file-based and microphone-based audio input.
"""

import speech_recognition as sr
from typing import Optional, Union, List
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RecognitionError(Exception):
    """Custom exception for speech recognition errors."""
    pass

class RecognizerAdaptor:
    """
    A wrapper class for speech recognition functionality.

    This class provides methods to recognize speech from both audio files
    and microphone input using Google's Speech Recognition service.
    """

    def __init__(
        self,
        energy_threshold: int = 4000,
        pause_threshold: float = 0.8,
        dynamic_energy_threshold: bool = True
    ):
        """
        Initialize the RecognizerAdaptor with customizable parameters.

        Args:
            energy_threshold (int): Energy level threshold for recognizing speech.
            pause_threshold (float): Seconds of non-speaking audio before a phrase is complete.
            dynamic_energy_threshold (bool): Whether to automatically adjust energy threshold.
        """
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = energy_threshold
        self.recognizer.pause_threshold = pause_threshold
        self.recognizer.dynamic_energy_threshold = dynamic_energy_threshold

    def recognize(
        self,
        audio_file: Union[str, Path],
        language: Optional[str] = None,
    ) -> str:
        """
        Recognize speech from an audio file.

        Args:
            audio_file (Union[str, Path]): Path to the audio file.
            language (str, optional): Language code for recognition.

        Returns:
            str: Transcribed text from the audio.

        Raises:
            RecognitionError: If recognition fails or service is unavailable.
            FileNotFoundError: If the audio file doesn't exist.
        """
        try:
            with sr.AudioFile(str(audio_file)) as source:
                audio = self.recognizer.record(source)
            
            result = self.recognizer.recognize_google(
                audio,
                language=language
            )
            logger.info(f"Successfully recognized audio from file: {audio_file}")
            return result

        except sr.UnknownValueError:
            raise RecognitionError("Speech could not be understood")
        except sr.RequestError as e:
            raise RecognitionError(f"Speech recognition service error: {str(e)}")
        except FileNotFoundError:
            raise FileNotFoundError(f"Audio file not found: {audio_file}")
        except Exception as e:
            raise RecognitionError(f"Recognition failed: {str(e)}")

    def recognize_from_mic(
        self,
        language: Optional[str] = None,
        phrase_time_limit: Optional[float] = None
    ) -> str:
        """
        Recognize speech from microphone input.

        Args:
            language (str, optional): Language code for recognition.
            phrase_time_limit (float, optional): Maximum time in seconds for a phrase.

        Returns:
            str: Transcribed text from the speech.

        Raises:
            RecognitionError: If recognition fails or service is unavailable.
        """
        try:
            with sr.Microphone() as source:
                logger.info("Listening... Say something!")
                
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                # Listen for audio input
                audio = self.recognizer.listen(
                    source,
                    phrase_time_limit=phrase_time_limit
                )

            result = self.recognizer.recognize_google(
                audio,
                language=language
            )
            logger.info("Successfully recognized speech from microphone")
            return result

        except sr.UnknownValueError:
            raise RecognitionError("Speech could not be understood")
        except sr.RequestError as e:
            raise RecognitionError(f"Speech recognition service error: {str(e)}")
        except Exception as e:
            raise RecognitionError(f"Recognition failed: {str(e)}")

    @property
    def available_microphones(self) -> List[str]:
        """
        Get a list of available microphone devices.

        Returns:
            List[str]: List of available microphone names.
        """
        return sr.Microphone.list_microphone_names()

    def adjust_for_noise(self, duration: float = 1.0) -> None:
        """
        Adjust the recognizer for ambient noise.

        Args:
            duration (float): Number of seconds to sample ambient noise.
        """
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=duration)

def main():
    """Main function to demonstrate the RecognizerAdaptor usage."""
    try:
        adaptor = RecognizerAdaptor()
        
        # List available microphones
        print("Available microphones:")
        for i, mic in enumerate(adaptor.available_microphones):
            print(f"{i}: {mic}")

        # Test microphone recognition
        print("\nTesting microphone recognition:")
        result = adaptor.recognize_from_mic(language="en-US")
        print(f"Recognized: {result}")

    except RecognitionError as e:
        logger.error(f"Recognition error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()