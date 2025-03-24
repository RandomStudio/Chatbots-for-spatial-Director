import os
from openai import OpenAI
from pathlib import Path
from typing import List, Dict, Optional, Generator, Any

try:
    # Define OpenAI parameters
    OPENAI_KEY_FILE = Path(__file__).parent / "openai_api_key.txt"

    # Set up OpenAI client
    with open(OPENAI_KEY_FILE, "r") as file:
        key = file.read().strip()

except:
    key = os.environ.get("OPENAI_KEY")

client = OpenAI(
    api_key=key
)


def send_chat_completion_stream(history: List[Dict[str, Any]]) -> Generator[str, None, None]:
    """ 
    Sends a chat request to an OpenAI model and retrieves the response in a streaming manner.

    The function returns a generator that yields pieces of the response as they are received from the OpenAI API.

    Parameters
    ----------
    history : List[Dict[str, Any]]
        The list of successive messages in the current conversation, with the appropriate base prompt for the required task as the "system" message.

    Yields
    -------
    Generator[str, None, None]
        A generator that yields each chunk of the response text as it is streamed from the OpenAI service.

    Raises
    ------
    RuntimeError
        If there is an error communicating with the OpenAI service or if the response does not contain valid choices.
    """

    # Send request to OpenAI
    response = client.chat.completions.create(
        model="gpt-4",
        messages=history,
        temperature=1,
        stream=True
    )

    # Extract response
    for chunk in response:
        if chunk.choices != [] and chunk.choices[0].delta.content is not None:
            yield (chunk.choices[0].delta.content)
