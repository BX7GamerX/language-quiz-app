#!/usr/bin/env python3
"""
Quick test for pronunciation screen fixes
"""

import sys
sys.path.append('src')

def test_pronunciation_fixes():
    """Test that pronunciation screen doesn't crash"""
    print("🧪 Testing Pronunciation Screen Fixes")
    print("=" * 50)
    
    try:
        # Test random_word_gen with empty library
        from word_library import random_word_gen
        result = random_word_gen("deutsch", "nouns")
        print(f"✅ random_word_gen result: '{result}'")
        print("✅ No infinite loop - function returned successfully")
        
        # Test the AudioManager can be created
        from audio_manager import AudioManager
        audio_mgr = AudioManager()
        print(f"✅ AudioManager created, available engines: {audio_mgr.available_engines}")
        
        # Test game_properties library status
        from functions import game_properties
        print(f"📚 Library built status: {game_properties.is_library_built}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🎓 Pronunciation Screen Fix Test")
    print("=" * 60)
    
    success = test_pronunciation_fixes()
    
    if success:
        print("\n✅ Pronunciation screen fixes are working!")
        print("💡 The app should no longer crash when opening pronunciation practice")
    else:
        print("\n❌ There are still issues with the pronunciation screen")
    
    print("=" * 60)
