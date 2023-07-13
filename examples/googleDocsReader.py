import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
from llama_index import ListIndex, GoogleDocsReader
from IPython.display import Markdown, display
import os
# make sure credentials.json file exists
document_ids = ["<document_id>"]
documents = GoogleDocsReader().load_data(document_ids=document_ids)
index = ListIndex.from_documents(documents)
# set Logging to DEBUG for more detailed outputs
query_engine = index.as_query_engine()
response = query_engine.query("<query_text>")
display(Markdown(f"<b>{response}</b>"))