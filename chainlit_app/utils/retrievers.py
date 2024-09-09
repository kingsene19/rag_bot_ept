from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

embeddings_function = HuggingFaceEmbeddings(model_name="sentence-transformers/gtr-t5-large")
db2 = Chroma(persist_directory="./chroma_db", embedding_function=embeddings_function)
RETRIEVER = db2.as_retriever()