import os
from langfuse.callback import CallbackHandler
from dotenv import load_dotenv

load_dotenv(override=True)  # Load env variables

langfuse_handler = CallbackHandler()
