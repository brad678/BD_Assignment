import os
from langfuse.callback import CallbackHandler
from dotenv import load_dotenv

load_dotenv(override=True)  # Load env variables
# Make sure you're explicitly pointing to the root-level `.env`
# load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

langfuse_handler = CallbackHandler()
