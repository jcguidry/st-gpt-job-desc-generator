from langchain.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.vectorstores import FAISS
from langchain.text_splitter import *

text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size = 200,
    chunk_overlap  = 0,
    length_function = len,
    add_start_index = True,
)

pdf_path = "../rag-data/raw/Mission Statement.pdf"
loader = PyPDFLoader(pdf_path)

pages = loader.load_and_split(text_splitter=text_splitter)

index_creator = VectorstoreIndexCreator(vectorstore_cls=FAISS)

index = index_creator.from_documents(pages)

index.vectorstore.save_local("../rag-data/indexed/pdf_index")