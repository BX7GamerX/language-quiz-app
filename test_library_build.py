#!/usr/bin/env python3
"""
Test script to verify library building process
"""

import sys
import os
sys.path.append('src')

def test_library_status():
    """Test library status detection"""
    print("🧪 Testing Library Status Detection")
    print("=" * 50)
    
    # Test libstatus file reading (like main.py does)
    try:
        with open('wordlib/libstatus', 'r') as file:
            line1 = file.readline().strip()
            line2 = file.readline().strip()
        
        lib_built_from_file = True if line1 == '0' else False
        print(f"📄 libstatus file - Line 1: '{line1}', Line 2: '{line2}'")
        print(f"📄 Library built according to libstatus: {lib_built_from_file}")
    except Exception as e:
        print(f"❌ Error reading libstatus: {e}")
    
    # Test game_properties status
    try:
        from functions import game_properties
        print(f"🎮 game_properties.is_library_built: {game_properties.is_library_built}")
        print(f"🎮 Game properties data: {game_properties.data}")
    except Exception as e:
        print(f"❌ Error reading game_properties: {e}")

def test_library_building():
    """Test actual library building"""
    print("\n🔨 Testing Library Building Process")
    print("=" * 50)
    
    try:
        from word_library import build_library
        from functions import game_properties, write_to_csv
        from app_variables import CSVPaths
        
        print("🚀 Starting library build test...")
        
        # Test basic library building
        result = build_library()
        if result:
            print("✅ Library building function executed successfully")
            
            # Update status
            game_properties.is_library_built = True
            write_to_csv(CSVPaths.APP_PROPERTIES.value, game_properties.data)
            print("✅ Status updated in appproperties")
            
            # Check if libstatus was also updated
            try:
                with open('wordlib/libstatus', 'r') as f:
                    content = f.read()
                    print(f"📄 Updated libstatus content: {repr(content)}")
            except Exception as e:
                print(f"⚠️ Could not read updated libstatus: {e}")
        else:
            print("❌ Library building failed")
            
    except Exception as e:
        print(f"❌ Error during library building test: {e}")

def test_vocabulary_files():
    """Test if vocabulary files exist"""
    print("\n📚 Testing Vocabulary Files")
    print("=" * 50)
    
    vocab_files = [
        'wordlib/nouns',
        'wordlib/verbs', 
        'wordlib/adjectives',
        'wordlib/adverbs'
    ]
    
    for file_path in vocab_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                print(f"✅ {file_path}: {len(lines)} lines")
            except Exception as e:
                print(f"⚠️ {file_path}: exists but error reading: {e}")
        else:
            print(f"❌ {file_path}: not found")

if __name__ == "__main__":
    print("🎓 LingoLeap Library Build Test")
    print("=" * 60)
    
    test_library_status()
    test_vocabulary_files() 
    test_library_building()
    
    print("\n" + "=" * 60)
    print("🏁 Test completed!")
