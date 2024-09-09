import chainlit as cl
from langchain.cache import SQLiteCache
from langchain.globals import set_llm_cache
from langchain_core.runnables import RunnableBranch
from utils.utils import format_chat_history, get_session_history
from utils.retrievers import RETRIEVER
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai.chat_models import ChatOpenAI
from utils.prompts import CONTEXT_PROMPT, SYSTEM_PROMPT

set_llm_cache(SQLiteCache())

llm = ChatOpenAI(
    openai_api_base = "https://api.groq.com/openai/v1",
    model="llama3-70b-8192",
    temperature=0.7,
    api_key="YOUR_KEY",
    streaming=True
)

context_chain = RunnableBranch(
  (
    lambda x: not x.get("chat_history", False),
    lambda x: x["input"],
  ),
  format_chat_history | CONTEXT_PROMPT | llm | StrOutputParser(),
)

retrieval_chain = {"context": RETRIEVER , "input": RunnablePassthrough()}

chain = context_chain | retrieval_chain | SYSTEM_PROMPT | llm | StrOutputParser()

conversational_rag_chain = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

@cl.on_chat_start
async def on_chat_start():
  cl.user_session.set("chain", conversational_rag_chain)

@cl.on_message
async def on_message(message: cl.Message):
  chain = cl.user_session.get("chain")
  msg = cl.Message(content="", author="PolyBot")
  for chunk in chain.stream(
    {"input": message.content},
    config={
        "configurable": {"session_id": 'massamba'}
    },
    ):
    await msg.stream_token(token=chunk)
    await msg.send()

