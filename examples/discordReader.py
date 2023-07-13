import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
import nest_asyncio

nest_asyncio.apply()
from llama_index import ListIndex, DiscordReader
from IPython.display import Markdown, display
import os
discord_token = os.getenv("DISCORD_TOKEN")
channel_ids = [1057178784895348746]  # Replace with your channel_id
documents = DiscordReader(discord_token=discord_token).load_data(
    channel_ids=channel_ids
)
index = ListIndex.from_documents(documents)
# set Logging to DEBUG for more detailed outputs
query_engine = index.as_query_engine()
response = query_engine.query("<query_text>")
display(Markdown(f"<b>{response}</b>"))