from langchain.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.vectorstores import FAISS


pdf_path = "../rag-data/raw/Mission Statement.pdf"
loader = PyPDFLoader(pdf_path)
pages = loader.load_and_split()

index_creator = VectorstoreIndexCreator(vectorstore_cls=FAISS)

index = index_creator.from_documents(pages)

index.vectorstore.save_local("../rag-data/indexed/pdf_index")