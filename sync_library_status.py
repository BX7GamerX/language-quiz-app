#!/usr/bin/env python3
"""
Word Library Synchronization Tool
==================================
This tool fixes inconsistencies in the word library status
"""

import sys
sys.path.append('src')

def sync_library_status():
    print("🔄 Word Library Synchronization Tool")
    print("=" * 60)
    
    # Import necessary modules
    try:
        from functions import game_properties, write_to_csv
        from app_variables import CSVPaths
        from word_library import language_hashmap
        import os
    except Exception as e:
        print(f"❌ Error importing modules: {e}")
        return False
    
    # Check if CSV files exist and have content
    csv_files_exist = True
    for file_name in ['nouns', 'verbs', 'adjectives', 'adverbs']:
        file_path = f'wordlib/{file_name}'
        if not os.path.exists(file_path):
            csv_files_exist = False
            print(f"❌ Missing CSV file: {file_name}")
    
    # Check libstatus file
    libstatus_says_built = False
    try:
        with open('wordlib/libstatus', 'r') as f:
            line1 = f.readline().strip()
            libstatus_says_built = line1 == '0'
    except FileNotFoundError:
        print("❌ libstatus file not found")
    
    # Check if language_hashmap has data
    hashmap_has_data = False
    if language_hashmap:
        for lang in language_hashmap:
            for word_type in ['nouns', 'verbs', 'adjectives', 'adverbs']:
                if word_type in language_hashmap[lang]:
                    for letter in language_hashmap[lang][word_type]:
                        if hasattr(language_hashmap[lang][word_type][letter], 'head_node'):
                            if language_hashmap[lang][word_type][letter].head_node:
                                hashmap_has_data = True
                                break
                if hashmap_has_data:
                    break
            if hashmap_has_data:
                break
    
    print(f"📊 Current Status:")
    print(f"   CSV files exist: {'✅' if csv_files_exist else '❌'}")
    print(f"   libstatus says built: {'✅' if libstatus_says_built else '❌'}")
    print(f"   game_properties.is_library_built: {'✅' if game_properties.is_library_built else '❌'}")
    print(f"   language_hashmap has data: {'✅' if hashmap_has_data else '❌'}")
    
    # Determine what the correct status should be
    should_be_built = csv_files_exist and libstatus_says_built
    
    print(f"\n🎯 Target Status: {'Built' if should_be_built else 'Not Built'}")
    
    # Sync game_properties
    if game_properties.is_library_built != should_be_built:
        print(f"🔧 Updating game_properties.is_library_built to {should_be_built}")
        game_properties.is_library_built = should_be_built
        try:
            write_to_csv(CSVPaths.APP_PROPERTIES.value, game_properties.data)
            print("   ✅ game_properties updated")
        except Exception as e:
            print(f"   ❌ Error updating game_properties: {e}")
    
    # If everything should be built but hashmap is empty, trigger rebuild
    if should_be_built and not hashmap_has_data:
        print("\n🚀 Triggering library rebuild...")
        try:
            # Import and run the CSV reader
            from word_library import read_csv_files
            from app_variables import wordlib_location
            import tkinter as tk
            
            # Create a minimal progress tracking setup
            class DummyApp:
                def __init__(self):
                    self.library_built = False
                def after(self, delay, func, *args):
                    func(*args)  # Execute immediately for sync operation
            
            class DummyVar:
                def set(self, value):
                    print(f"   Progress: {value}")
            
            class DummyProgressBar:
                def __init__(self):
                    self.value = 0
                def __setitem__(self, key, value):
                    if key == "value":
                        self.value = value
            
            dummy_app = DummyApp()
            dummy_var = DummyVar()
            dummy_bar = DummyProgressBar()
            
            print("   📚 Reading CSV files...")
            read_csv_files(dummy_app, wordlib_location, dummy_bar, dummy_var)
            
            # Check if rebuild was successful
            hashmap_has_data_after = False
            if language_hashmap:
                for lang in language_hashmap:
                    for word_type in ['nouns', 'verbs', 'adjectives', 'adverbs']:
                        if word_type in language_hashmap[lang]:
                            for letter in language_hashmap[lang][word_type]:
                                if hasattr(language_hashmap[lang][word_type][letter], 'head_node'):
                                    if language_hashmap[lang][word_type][letter].head_node:
                                        hashmap_has_data_after = True
                                        break
                        if hashmap_has_data_after:
                            break
                    if hashmap_has_data_after:
                        break
            
            if hashmap_has_data_after:
                print("   ✅ Library rebuild successful!")
            else:
                print("   ⚠️  Library rebuild completed but no data detected")
                
        except Exception as e:
            print(f"   ❌ Error rebuilding library: {e}")
    
    print(f"\n✅ Synchronization complete!")
    print(f"💡 The app should now work correctly with the word library")
    
    return True

if __name__ == "__main__":
    sync_library_status()
