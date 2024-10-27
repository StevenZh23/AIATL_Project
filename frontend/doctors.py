from pymongo import MongoClient
import os
from dotenv import find_dotenv, load_dotenv
from users import users_collection

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

PASSWORD = os.getenv("PASSWORD")
CONNECTION_STRING = f"mongodb+srv://stevenzdragons:{PASSWORD}@aiatl.zehxy.mongodb.net/?retryWrites=true&w=majority&appName=AIAtl"

client = MongoClient(CONNECTION_STRING)  # Connect to MongoDB Atlas through Steven's key
db = client.myDatabase  # Create or get the user database

doctors_collection = db["doctors"]


def register_doctor(user, full_name, email, field, patient):
    doctor_info = {
        "user":user,
        "full_name":full_name,
        "email":email,
        "field":field,
        "patient":patient
    }
    if users_collection.find({"full_name":full_name, "identity":"doctor"}):
        doctors_collection.insert_one(doctor_info)
    else:
        return "No such doctor exists"

def remove_doctor(user, field):
    result = doctors_collection.delete_one({"user":user, "field":field})
        
        # Check if a document was deleted
    if result.deleted_count > 0:
        return "Document deleted successfully."
    else:
        return "No document found matching the criteria."

def find_doctor(user, field):
    doc = doctors_collection.find({"user": user, "field":field})
    for doc1 in doc:
        if not doc1:
            return f"You don't have a {field} doctor currently registered."
        else:
            return [doc1["full_name"], doc1["email"]]
        


#print(find_doctor("a","General"))
#register_doctor("a","Buzz", "szhou390@gatech.edu", "Cardiologist", "stevenzhou")
