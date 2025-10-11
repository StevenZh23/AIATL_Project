# 🗄️ MongoDB Atlas Migration Guide

## 📋 **Complete Migration Checklist**

### **Step 1: Set Up Your MongoDB Atlas Cluster**

1. **Log into MongoDB Atlas** (https://cloud.mongodb.com)
2. **Create a New Project** (if you haven't already)
3. **Build a Cluster**:
   - Choose **M0 (Free tier)** for development
   - Select a **region** close to you
   - Choose **AWS, Google Cloud, or Azure**
4. **Set up Network Access**:
   - Add your current IP address
   - Or use `0.0.0.0/0` for development (less secure)
5. **Create Database User**:
   - Username: `aiatl_user` (or your choice)
   - Password: Generate a strong password
   - Database User Privileges: `Read and write to any database`

### **Step 2: Get Your Connection String**

1. **Click "Connect"** on your cluster
2. **Choose "Connect your application"**
3. **Copy the connection string** - it will look like:
   ```
   mongodb+srv://aiatl_user:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```

### **Step 3: Update Your Environment Variables**

Create a `.env` file in your project root:

```bash
# Copy the example file
cp .env.example .env
```

Then edit `.env` with your new connection string:

```env
# MongoDB Configuration
MONGODB_URI=mongodb+srv://YOUR_USERNAME:YOUR_PASSWORD@YOUR_CLUSTER.mongodb.net/?retryWrites=true&w=majority&appName=AIATL

# AI API Keys
GOOGLE_API_KEY=your_google_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
OPENAI_API_KEY=your_openai_api_key

# Email Configuration (Postmark)
POSTMARK_API_TOKEN=your_postmark_api_token
```

### **Step 4: Database Structure**

Your new database will need these collections:

#### **Collections to Create:**
- `users` - User accounts (patients and doctors)
- `doctors` - Doctor information and specialties
- `symptoms` - Patient symptom submissions
- `documents` - PDF files and medical reports

#### **Sample Data Structure:**

**Users Collection:**
```json
{
  "username": "patient1",
  "full_name": "John Doe",
  "email": "john@example.com",
  "role": "patient",
  "age": 35,
  "ethnicity": "Caucasian",
  "sex": "Male"
}
```

**Doctors Collection:**
```json
{
  "user": "doctor1",
  "full_name": "Dr. Smith",
  "email": "dr.smith@hospital.com",
  "field": "Cardiologist",
  "patient": "patient1"
}
```

**Symptoms Collection:**
```json
{
  "username": "patient1",
  "symptoms_text": "I have chest pain and shortness of breath",
  "submitted_at": "2024-01-15T10:30:00Z"
}
```

### **Step 5: Test Your Connection**

Run this test to verify your connection:

```python
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")

try:
    client = MongoClient(MONGODB_URI)
    db = client.myDatabase
    print("✅ Successfully connected to MongoDB!")
    print(f"Database: {db.name}")
    
    # Test collections
    collections = db.list_collection_names()
    print(f"Collections: {collections}")
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
```

### **Step 6: Data Migration (Optional)**

If you have existing data in your friend's database, you can export/import:

#### **Export from Old Database:**
```bash
mongodump --uri="mongodb+srv://stevenzdragons:PASSWORD@aiatl.zehxy.mongodb.net/" --db=myDatabase --out=./backup
```

#### **Import to New Database:**
```bash
mongorestore --uri="mongodb+srv://YOUR_USERNAME:YOUR_PASSWORD@YOUR_CLUSTER.mongodb.net/" --db=myDatabase ./backup/myDatabase
```

### **Step 7: Update Application**

The code has been updated to use environment variables. Just update your `.env` file and restart the application:

```bash
streamlit run main.py
```

## 🔧 **What Was Changed in the Code**

### **Files Updated:**
- `app/utils/helpers.py` - Main MongoDB connection
- `models/user.py` - User model connection
- `models/doctor.py` - Doctor model connection
- `services/email_service.py` - Email service connection
- `app/utils/database.py` - Database operations

### **Changes Made:**
- ✅ Replaced hardcoded connection strings with `MONGODB_URI` environment variable
- ✅ Added fallback to old connection string for backward compatibility
- ✅ All files now use `os.getenv("MONGODB_URI")` for connection

## 🚨 **Important Notes**

### **Security:**
- **Never commit** your `.env` file to git
- **Use strong passwords** for database users
- **Restrict network access** to your IP addresses in production
- **Use environment variables** for all sensitive data

### **Performance:**
- **M0 (Free tier)** has limitations (512MB storage, limited connections)
- **Upgrade to M2+** for production use
- **Choose the right region** for your users

### **Backup:**
- **Enable automatic backups** in Atlas
- **Export data regularly** for important projects
- **Test restore procedures** before you need them

## 🎯 **Quick Start Commands**

```bash
# 1. Create .env file
echo "MONGODB_URI=mongodb+srv://YOUR_USERNAME:YOUR_PASSWORD@YOUR_CLUSTER.mongodb.net/?retryWrites=true&w=majority&appName=AIATL" > .env

# 2. Test connection
python -c "from app.utils.helpers import get_mongo_client; print('Connected!' if get_mongo_client() else 'Failed!')"

# 3. Run application
streamlit run main.py
```

## 🎉 **You're Done!**

Your AIATL application will now use your own MongoDB Atlas cluster. The old connection strings are kept as fallbacks, so the app will still work if the environment variable isn't set.
