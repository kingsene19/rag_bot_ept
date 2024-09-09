from typing import Dict
from langchain.chains.combine_documents.base import DEFAULT_DOCUMENT_PROMPT
from langchain_core.prompts import format_document
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

store = {}

def format_docs(inputs: dict) -> str:
  inputs["context"] = "\n\n".join(
      f"Document {i}:\n {format_document(doc, DEFAULT_DOCUMENT_PROMPT)}" for i, doc in enumerate(inputs["context"])
  )
  return inputs

def format_chat_history(data):
  formatize_chat_history = ""
  if "chat_history" in data.keys():
    for message in data["chat_history"]:
      message_type = str(type(message)).split("'")[1].split(".")[-1]
      message_content = message.content.replace("\n", "")
      formatize_chat_history += f"\t{message_type}: {message_content}\n"
    data["chat_history"] = formatize_chat_history
  return data

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]