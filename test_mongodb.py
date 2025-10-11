#!/usr/bin/env python3
"""
Test MongoDB Atlas connection
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient

def test_connection():
    load_dotenv()
    MONGODB_URI = os.getenv('MONGODB_URI')
    
    if not MONGODB_URI:
        print("❌ MONGODB_URI not found in .env file")
        return False
    
    print(f"🔍 Testing connection string: {MONGODB_URI[:50]}...")
    
    try:
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        # Test the connection
        client.admin.command('ping')
        print("✅ Successfully connected to MongoDB Atlas!")
        
        # Test database access
        db = client.myDatabase
        print(f"📊 Database: {db.name}")
        
        # List collections
        collections = db.list_collection_names()
        print(f"📁 Collections: {collections}")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\n🔧 Troubleshooting tips:")
        print("1. Check your username and password")
        print("2. URL encode special characters in password")
        print("3. Verify network access is set up in Atlas")
        print("4. Make sure your IP is whitelisted")
        return False

if __name__ == "__main__":
    test_connection()
