from postmarker.core import PostmarkClient
import os
import google.generativeai as genai
from dotenv import find_dotenv, load_dotenv
from pymongo import MongoClient
from models.doctor import find_doctor



dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

PASSWORD = os.getenv("PASSWORD")
CONNECTION_STRING = f"mongodb+srv://stevenzdragons:{PASSWORD}@aiatl.zehxy.mongodb.net/?retryWrites=true&w=majority&appName=AIAtl"

client = MongoClient(CONNECTION_STRING)  # Connect to MongoDB Atlas through Steven's key
db = client.myDatabase  # Create or get the user database

doctors_collection = db["doctors"]

POSTMARK_API = os.getenv("POSTMARK_API")
GEMENI_API = os.getenv("GEMINI_API")



genai.configure(api_key=os.environ["GEMINI_API"])

# Create the model
generation_config = {
  "temperature": 0.7,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

chat_session = model.start_chat(
  history=[
  ]
)
def get_email(field, symptoms, user):
    tmp = find_doctor(user, field)
    print(tmp)
    if not tmp:
        return f"You don't have a {field} doctor currently registered."
    else:
        doc = tmp[0]
        docemail = tmp[1]
    response = chat_session.send_message(f"Write a polite and professional email to Dr. {doc} inquiring about several medical symptoms. The symptoms are {symptoms}. The email should include a respectful greeting, a brief description of the symptoms, and any relevant context, such as duration or severity. Request advice on whether the symptoms warrant a visit to the clinic or if there are recommended home treatments. Use a calm and respectful tone, and thank the doctor for their time. Do not leave any information up to the user to input.")

    return [response.text,docemail]

#print(get_email("General","a","a"))
postmark = PostmarkClient(server_token=POSTMARK_API)

def send_email_postmark(sender_email, recipient_email, subject, body):
    try:

        email = postmark.emails.send(
            From=sender_email,  # Your verified sender email
            To=recipient_email,  # Recipient's email address
            Subject=subject,  # Email subject
            TextBody=body  # Email body
        )
        
        # Send the email
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Example usage
sender_email = "szhou390@gatech.edu"  # Replace with your verified sender email

subject = "Questions on Illness Symptoms"
tmp = get_email("General","a",'a')
body = tmp[0]
recipient_email = tmp[1]  # Replace with recipient email
send_email_postmark(sender_email, recipient_email, subject, body)
