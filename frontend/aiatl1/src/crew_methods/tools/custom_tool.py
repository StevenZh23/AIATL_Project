from crewai_tools import BaseTool
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface.embeddings import HuggingFaceEmbeddings

#Instantiate Context and Vector Store
CardiologistTEXT_FILE_PATH = "/Users/lindsayhwang/aiatl/frontend/aiatl1/Cardiologist_Report.txt"
with open(CardiologistTEXT_FILE_PATH, "r", encoding="utf-8") as file:
    cardiotext = file.read()

# Split text into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,  # Adjust based on your needs
    chunk_overlap=50,  # Overlap between chunks
    separators=["\n\n", "\n", " ", ""]
)
Cardiochunks = text_splitter.split_text(cardiotext)

#Embeddings
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
vector_store = FAISS.from_texts(Cardiochunks, embedding_model)

# Initialize the retriever
retriever = vector_store.as_retriever()

class CardioMedicalReportRAG(BaseTool):
    name: str = "CardioMedicalReportRAG"
    description: str = (
        "This tool is used to search patient medical reports in regards to the agent's specific medical knowledge to aid in diagnosis of new symptoms. Find pertinent medical history to combine with symptoms to aid in diagnosis."
    )

    def _run(self, query: str) -> str:
        # Implementation goes here
        return retriever.get_relevant_documents(query)
    

#Instantiate Context and Vector Store
PulmonologistTEXT_FILE_PATH = "/Users/lindsayhwang/aiatl/frontend/aiatl1/Pulmonologist_Report.txt"
with open(PulmonologistTEXT_FILE_PATH, "r", encoding="utf-8") as file:
    pulmotext = file.read()

# Split text into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,  # Adjust based on your needs
    chunk_overlap=50,  # Overlap between chunks
    separators=["\n\n", "\n", " ", ""]
)
Pulmochunks = text_splitter.split_text(pulmotext)

#Embeddings
#embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
Pvector_store = FAISS.from_texts(Pulmochunks, embedding_model)

# Initialize the retriever
Pretriever = Pvector_store.as_retriever()

class PulmoMedicalReportRAG(BaseTool):
    name: str = "PulmoMedicalReportRAG"
    description: str = (
        "This tool is used to search patient medical reports in regards to the agent's specific medical knowledge to aid in diagnosis of new symptoms. Find pertinent medical history to combine with symptoms to aid in diagnosis."
    )

    def _run(self, query: str) -> str:
        # Implementation goes here
        return Pretriever.get_relevant_documents(query)


#Instantiate Context and Vector Store
NeurologistTEXT_FILE_PATH = "/Users/lindsayhwang/aiatl/frontend/aiatl1/Neurologist_Report.txt"
with open(NeurologistTEXT_FILE_PATH, "r", encoding="utf-8") as file:
    neurotext = file.read()

# Split text into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,  # Adjust based on your needs
    chunk_overlap=50,  # Overlap between chunks
    separators=["\n\n", "\n", " ", ""]
)
Neurochunks = text_splitter.split_text(pulmotext)

#Embeddings
#embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
Nvector_store = FAISS.from_texts(Neurochunks, embedding_model)

# Initialize the retriever
Pretriever = Nvector_store.as_retriever()

class NeuroMedicalReportRAG(BaseTool):
    name: str = "NeuroMedicalReportRAG"
    description: str = (
        "This tool is used to search patient medical reports in regards to the agent's specific medical knowledge to aid in diagnosis of new symptoms. Find pertinent medical history to combine with symptoms to aid in diagnosis."
    )

    def _run(self, query: str) -> str:
        # Implementation goes here
        return Pretriever.get_relevant_documents(query)
