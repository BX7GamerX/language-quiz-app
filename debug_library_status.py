#!/usr/bin/env python3
"""
Word Library Status Debug Tool
===============================
This tool helps diagnose word library loading issues
"""

import sys
import os
sys.path.append('src')

def check_library_status():
    print("🔍 Word Library Debug Tool")
    print("=" * 60)
    
    # Check file-based status
    print("\n📁 File-based Status Checks:")
    try:
        with open('wordlib/libstatus', 'r') as f:
            line1 = f.readline().strip()
            line2 = f.readline().strip()
            file_built = line1 == '0'
            print(f"   libstatus file: {'✅ Built' if file_built else '❌ Not built'} ({line1})")
            print(f"   Version: {line2}")
    except FileNotFoundError:
        print("   ❌ libstatus file not found")
        file_built = False
    
    # Check wordlib files
    print(f"\n📚 Wordlib Files:")
    wordlib_files = ['nouns', 'verbs', 'adjectives', 'adverbs', 'appproperties']
    for file_name in wordlib_files:
        file_path = f'wordlib/{file_name}'
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = len(f.readlines())
                print(f"   ✅ {file_name}: {lines} lines")
            except Exception as e:
                print(f"   ⚠️  {file_name}: Error reading ({e})")
        else:
            print(f"   ❌ {file_name}: Missing")
    
    # Check app properties status
    print(f"\n⚙️  App Properties Status:")
    try:
        from functions import game_properties
        print(f"   is_library_built: {'✅ True' if game_properties.is_library_built else '❌ False'}")
        print(f"   user_language: {game_properties.user_language}")
        print(f"   word_type: {game_properties.word_type}")
    except Exception as e:
        print(f"   ❌ Error loading game_properties: {e}")
    
    # Test word library functions
    print(f"\n🎯 Word Library Function Tests:")
    try:
        from word_library import random_word_gen, is_library_ready, translate_two
        
        # Test library ready check
        ready = is_library_ready()
        print(f"   is_library_ready(): {'✅ True' if ready else '❌ False'}")
        
        # Test word generation
        test_word = random_word_gen('deutsch', 'nouns')
        print(f"   random_word_gen('deutsch', 'nouns'): '{test_word}'")
        
        # Test translation
        if test_word and test_word != 'word library not found':
            translation = translate_two(test_word, 'deutsch', 'english', 'nouns')
            print(f"   translate_two('{test_word}'): '{translation}'")
        
    except Exception as e:
        print(f"   ❌ Error testing functions: {e}")
    
    # Test language hashmap
    print(f"\n🗺️  Language Hashmap Status:")
    try:
        from word_library import language_hashmap
        if language_hashmap:
            for lang in language_hashmap:
                print(f"   {lang}: {list(language_hashmap[lang].keys())}")
                # Test if any words exist
                word_count = 0
                for word_type in ['nouns', 'verbs', 'adjectives', 'adverbs']:
                    if word_type in language_hashmap[lang]:
                        for letter in language_hashmap[lang][word_type]:
                            if hasattr(language_hashmap[lang][word_type][letter], 'head_node'):
                                if language_hashmap[lang][word_type][letter].head_node:
                                    word_count += 1
                print(f"      📊 Words available: ~{word_count} letter groups")
        else:
            print("   ❌ language_hashmap is empty")
            
    except Exception as e:
        print(f"   ❌ Error checking hashmap: {e}")
    
    print(f"\n💡 Recommendations:")
    if not file_built:
        print("   🔧 Run the app and log in to build the word library")
    
    if ready:
        print("   ✅ Word library appears to be working correctly")
    else:
        print("   🔧 Word library needs to be built - fallback words will be used")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    check_library_status()
