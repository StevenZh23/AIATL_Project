from pymongo import MongoClient
from bson.binary import Binary
import os
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

PASSWORD = os.getenv("PASSWORD")
CONNECTION_STRING = f"mongodb+srv://stevenzdragons:{PASSWORD}@aiatl.zehxy.mongodb.net/?retryWrites=true&w=majority&appName=AIAtl"

client = MongoClient(CONNECTION_STRING)  # Connect to MongoDB Atlas through Steven's key
db = client.myDatabase  # Create or get the user database

documents_collection = db["documents"]

def store_pdf(pdf_path, pdf_name, user, classification, description=""):
    """
    Stores a PDF file as binary data in MongoDB.
    
    Args:
        pdf_path (str): The file path to the PDF file.
        pdf_name (str): A name to identify the PDF in the database.
        description (str, optional): A description of the PDF file.
    """
    try:
        with open(pdf_path, "rb") as f:
            pdf_data = f.read()
        pdf_document = {
            "name": pdf_name,
            "description": description,
            "user": user,
            "classification": classification,
            "pdf_file": Binary(pdf_data)
        }
        documents_collection.insert_one(pdf_document)
        print(f"PDF '{pdf_name}' stored successfully.")
    except FileNotFoundError:
        print(f"The file at path '{pdf_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def retrieve_pdfs(user, save_directory, type):
    """
    Retrieves a PDF stored as binary data in MongoDB and saves it to a specified path.
    
    Args:
        pdf_name (str): The name of the PDF to retrieve from the database.
        save_path (str): The file path to save the retrieved PDF.
    """
    #if not os.path.exists(save_directory):
    #    os.makedirs(save_directory)

    pdf_docs = documents_collection.find({"user": user})


    for pdf_doc in pdf_docs:    

        pdf_data = pdf_doc["pdf_file"]
        pdf_class = pdf_doc["classification"]
        save_path = save_directory +  "/" + f"{type}.pdf"
        #print(save_path)
        directory = os.path.dirname(save_path)

        if not os.path.exists(directory):
            os.makedirs(directory)
        #print(directory)
        #print("Is this a file?", os.path.isfile(save_path))

        if os.path.isdir(save_path):
            raise ValueError(f"A directory exists with the name '{save_path}', cannot create a file.")
 
        with open(save_path, "wb") as f:
            f.write(pdf_data)
        print(f"PDF '{user}' retrieved and saved to '{save_path}'.")
        
    


def delete_files_by_name(collection, file_name):

    # Delete all documents with the specified file name
    result = collection.delete_many({"name": file_name})  # Adjust the filter as needed
    print(f"Deleted {result.deleted_count} documents containing files named '{file_name}'.")

delete_files_by_name(documents_collection, f"Sample PDF")
store_pdf("Sample_Report.pdf", "Sample PDF", "StevenZ2", "Neurologist")
retrieve_pdfs("StevenZ2", "/workspaces/AIATL_Project/aiatl1/", "Neurologist")