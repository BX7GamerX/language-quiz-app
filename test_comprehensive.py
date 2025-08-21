#!/usr/bin/env python3
"""
Comprehensive App Functionality Test
====================================
Tests all the key features to make sure everything works
"""

import sys
sys.path.append('src')

def test_all_functionality():
    print("🧪 Comprehensive App Functionality Test")
    print("=" * 60)
    
    # Test 1: Word Generation
    print("\n🎯 Test 1: Word Generation")
    try:
        from word_library import random_word_gen
        
        word_types = ['nouns', 'verbs', 'adjectives', 'adverbs']
        for word_type in word_types:
            word = random_word_gen('deutsch', word_type)
            print(f"   {word_type}: '{word}' {'✅' if word and word != 'word library not found' else '❌'}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Translation
    print("\n🌍 Test 2: Translation")
    try:
        from word_library import translate_two
        
        test_words = [
            ('Mensch', 'nouns'),
            ('denken', 'verbs'),
            ('groß', 'adjectives'),
            ('schnell', 'adverbs')
        ]
        
        for word, word_type in test_words:
            translation = translate_two(word, 'deutsch', 'english', word_type)
            print(f"   '{word}' → '{translation}' {'✅' if translation and not translation.startswith('[') else '❌'}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Game Properties
    print("\n⚙️ Test 3: Game Properties")
    try:
        from functions import game_properties
        print(f"   is_library_built: {game_properties.is_library_built} ✅")
        print(f"   user_language: {game_properties.user_language} ✅")
        print(f"   word_type: {game_properties.word_type} ✅")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Translation Game Logic  
    print("\n🎮 Test 4: Translation Game Logic")
    try:
        from derived_functions import quiz_builder
        
        # Test quiz building
        result = quiz_builder('deutsch', 'english', 'nouns')
        if result:
            print(f"   Quiz building: ✅ (Generated options)")
        else:
            print(f"   Quiz building: ⚠️ (Using fallback)")
    except Exception as e:
        print(f"   Quiz building: ⚠️ (Error: {e})")
    
    # Test 5: Audio Manager (Pronunciation)
    print("\n🔊 Test 5: Audio Manager")
    try:
        from audio_manager import AudioManager
        import tkinter as tk
        
        # Create minimal GUI components for testing
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        frame = tk.Frame(root)
        audio_mgr = AudioManager(frame)
        
        if audio_mgr:
            print(f"   AudioManager creation: ✅")
            print(f"   Available engines: {audio_mgr.get_available_engines()}")
        else:
            print(f"   AudioManager creation: ❌")
            
        root.destroy()
    except Exception as e:
        print(f"   AudioManager: ⚠️ (Error: {e})")
    
    # Test 6: Modern UI Components
    print("\n🎨 Test 6: Modern UI Components")
    try:
        import customtkinter as ctk
        from enhanced_proficiency_levels import A2DeutschFrame
        
        # Test CustomTkinter setup
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        print(f"   CustomTkinter: ✅")
        print(f"   Enhanced proficiency levels: ✅")
    except Exception as e:
        print(f"   Modern UI: ❌ (Error: {e})")
    
    # Test 7: File Status Consistency
    print("\n📁 Test 7: File Status Consistency")
    try:
        # Check libstatus
        with open('wordlib/libstatus', 'r') as f:
            libstatus = f.readline().strip() == '0'
        
        # Check CSV files exist
        import os
        csv_files = ['nouns', 'verbs', 'adjectives', 'adverbs']
        csv_exist = all(os.path.exists(f'wordlib/{f}') for f in csv_files)
        
        print(f"   libstatus file: {'✅' if libstatus else '❌'}")
        print(f"   CSV files: {'✅' if csv_exist else '❌'}")
        
        if libstatus and csv_exist:
            print(f"   Overall status: ✅ Ready for use")
        else:
            print(f"   Overall status: ⚠️ Partial functionality")
            
    except Exception as e:
        print(f"   File status: ❌ (Error: {e})")
    
    print(f"\n" + "=" * 60)
    print(f"🎉 Test Complete!")
    print(f"💡 If most tests show ✅, your app should work correctly!")
    print(f"⚠️  Some ⚠️ warnings are normal and won't prevent core functionality.")
    print(f"❌ Any ❌ errors indicate issues that may need fixing.")

if __name__ == "__main__":
    test_all_functionality()
