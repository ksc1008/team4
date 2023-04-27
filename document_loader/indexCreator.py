from langchain.chains import RetrievalQA, RetrievalQAWithSourcesChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma

dbFolder = './vectorstore'
chroma: Chroma


def createDB():
    global chroma
    loader = TextLoader('./workspace/난초.txt', encoding='utf8')
    documents = loader.load()
    loader = TextLoader('./workspace/운수좋은날.txt', encoding='utf8')
    documents.extend(loader.load())

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=0,
        separators=['\n\n', '\n', ' ', '']
    )
    docs = text_splitter.split_documents(documents)
    embedding = OpenAIEmbeddings()
    db = Chroma.from_documents(documents=docs, embedding=embedding, persist_directory=dbFolder)
    chroma = db


def loadDB():
    global chroma
    embedding = OpenAIEmbeddings()
    chroma = Chroma(persist_directory=dbFolder, embedding_function=embedding)


def promptLangchain(query):
    global chroma
    if chroma is None:
        print("chroma didn't set")
        return 'err'
    retriever = chroma.as_retriever()
    openai = OpenAI()
    openai.max_tokens = 256
    qa = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(temperature=0),
        chain_type='stuff',
        retriever=retriever
    )

    return qa.run(query)
