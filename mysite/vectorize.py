import os

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import TokenTextSplitter
from langchain.document_loaders import DirectoryLoader

os.environ["OPENAI_API_KEY"] = "sk-li3V"


def get_documents(url_function=None):
    if url_function == "url_function":
        loader = DirectoryLoader("mysite/demo_link_file/", glob="**/*.txt")
        data = loader.load()

    else:
        loader = DirectoryLoader("mysite/demo_files/", glob="**/*.txt")
        data = loader.load()
        print(len(data))

    return data


def create_db(url_function=None):
    persist_directory = "demo_db"

    if url_function == "url_function":
        db_data = get_documents(url_function)

    else:
        db_data = get_documents()

    text_splitter = TokenTextSplitter(chunk_size=1800, chunk_overlap=0)
    db_doc = text_splitter.split_documents(db_data)

    embeddings = OpenAIEmbeddings()

    vectordb = Chroma.from_documents(
        db_doc, embeddings, persist_directory=persist_directory
    )
    vectordb.persist()
