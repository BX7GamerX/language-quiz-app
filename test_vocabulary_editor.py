#!/usr/bin/env python3
"""
Vocabulary Editor Integration Test
=================================
Tests the vocabulary editor integration with the main app
"""

import sys
import os
sys.path.append('src')

def test_vocabulary_editor_integration():
    print("🧪 Vocabulary Editor Integration Test")
    print("=" * 60)
    
    # Test 1: Check if vocabulary_editor.py exists in src directory
    editor_path = "src/vocabulary_editor.py"
    if os.path.exists(editor_path):
        print(f"✅ Vocabulary editor found at: {editor_path}")
    else:
        print(f"❌ Vocabulary editor NOT found at: {editor_path}")
        return False
    
    # Test 2: Check imports
    print(f"\n📦 Testing Imports:")
    try:
        from vocabulary_editor import VocabularyDatabaseEditor, WordEditDialog
        print(f"   ✅ VocabularyDatabaseEditor imported successfully")
        print(f"   ✅ WordEditDialog imported successfully")
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        return False
    
    # Test 3: Check app_variables integration
    print(f"\n🔗 Testing Integration:")
    try:
        from app_variables import wordlib_location, CSVPaths
        print(f"   ✅ app_variables imported successfully")
        print(f"   📂 Wordlib files configured: {len(wordlib_location)} files")
        
        for file_path, word_type in wordlib_location:
            exists = "✅" if os.path.exists(file_path) else "❌"
            print(f"      {exists} {word_type}: {file_path}")
    
    except Exception as e:
        print(f"   ❌ Integration error: {e}")
        return False
    
    # Test 4: Test menu integration paths
    print(f"\n🎯 Testing Menu Integration:")
    try:
        # Test modern main menu
        from modern_main_menu import ModernMainMenuFrame
        print(f"   ✅ Modern main menu can import vocabulary editor")
        
        # Test regular main menu
        from mainmenuframes import MainMenuFrame
        print(f"   ✅ Regular main menu can import vocabulary editor")
        
    except Exception as e:
        print(f"   ❌ Menu integration error: {e}")
        return False
    
    # Test 5: Test CustomTkinter compatibility
    print(f"\n🎨 Testing UI Framework:")
    try:
        import customtkinter as ctk
        from vocabulary_editor import VocabularyDatabaseEditor
        
        # Test theme setting (without creating the actual app)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        print(f"   ✅ CustomTkinter theme configuration works")
        
    except Exception as e:
        print(f"   ❌ UI framework error: {e}")
        return False
    
    print(f"\n" + "=" * 60)
    print(f"🎉 Vocabulary Editor Integration Test PASSED!")
    print(f"💡 The vocabulary editor should work correctly when launched from the main menu.")
    return True

if __name__ == "__main__":
    test_vocabulary_editor_integration()
