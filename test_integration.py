#!/usr/bin/env python3
"""
Integration test script for the LingoLeap language learning app.
Tests all major components and their interactions.
"""
import sys
import os
sys.path.append('src')

def test_imports():
    """Test that all major components can be imported"""
    print("Testing imports...")
    
    try:
        from word_library import build_library
        print("✅ word_library imported successfully")
    except Exception as e:
        print(f"❌ word_library import failed: {e}")
    
    try:
        from user_progress import progress_manager
        print("✅ user_progress imported successfully")
    except Exception as e:
        print(f"❌ user_progress import failed: {e}")
    
    try:
        from audio_manager import AudioManager
        print("✅ audio_manager imported successfully")
    except Exception as e:
        print(f"❌ audio_manager import failed: {e}")
    
    try:
        from interactive_modes import InteractiveModeFrame
        print("✅ interactive_modes imported successfully")
    except Exception as e:
        print(f"❌ interactive_modes import failed: {e}")
    
    try:
        from proficiency_levels import A2DeutschFrame, B1DeutschFrame, B2DeutschFrame
        print("✅ proficiency_levels imported successfully")
    except Exception as e:
        print(f"❌ proficiency_levels import failed: {e}")
    
    print()

def test_library_building():
    """Test library building functionality"""
    print("Testing library building...")
    
    try:
        from word_library import build_library
        from app_variables import vocab_files_path
        
        # Check if vocabulary files exist
        vocab_files = ['nouns', 'verbs', 'adjectives', 'adverbs']
        missing_files = []
        
        for vocab_file in vocab_files:
            file_path = os.path.join(vocab_files_path, vocab_file)
            if not os.path.exists(file_path):
                missing_files.append(vocab_file)
        
        if missing_files:
            print(f"⚠️  Missing vocabulary files: {missing_files}")
        else:
            print("✅ All vocabulary files found")
        
        # Test library building
        build_library()
        print("✅ Library building completed successfully")
        
    except Exception as e:
        print(f"❌ Library building failed: {e}")
    
    print()

def test_user_progress():
    """Test user progress functionality"""
    print("Testing user progress system...")
    
    try:
        from user_progress import progress_manager
        
        # Test basic functionality
        summary = progress_manager.get_progress_summary()
        print(f"✅ Progress summary retrieved: {len(summary)} metrics")
        
        # Test session recording
        progress_manager.record_session({
            "score": 100,
            "questions_attempted": 10,
            "correct_answers": 8,
            "duration_minutes": 5
        })
        print("✅ Session recorded successfully")
        
        # Test recommendations
        recommendations = progress_manager.get_recommendations()
        print(f"✅ Got {len(recommendations)} recommendations")
        
    except Exception as e:
        print(f"❌ User progress test failed: {e}")
    
    print()

def test_audio_system():
    """Test audio system (may fail if dependencies not installed)"""
    print("Testing audio system...")
    
    try:
        from audio_manager import AudioManager
        audio_manager = AudioManager()
        
        # Test initialization
        print(f"✅ AudioManager initialized, available engines: {audio_manager.available_engines}")
        
        # Test basic synthesis (might not produce sound in headless environment)
        if audio_manager.available_engines:
            audio_manager.speak("Test", speed=0.8)
            print("✅ Text-to-speech test completed")
        else:
            print("⚠️  No TTS engines available")
        
    except Exception as e:
        print(f"⚠️  Audio system test failed (expected if dependencies missing): {e}")
    
    print()

def test_frame_routing():
    """Test frame routing system"""
    print("Testing frame routing...")
    
    try:
        from frames import get_destination_frame, frame_window
        
        # Test that all frames are registered
        expected_frames = [
            'mainmenuframe', 'translation_game_frame', 'a1_deutsch_frame',
            'a2_deutsch_frame', 'b1_deutsch_frame', 'b2_deutsch_frame',
            'interactive_mode', 'pronunciation_practice', 'progress_dashboard'
        ]
        
        missing_frames = []
        for frame_name in expected_frames:
            if frame_name not in frame_window:
                missing_frames.append(frame_name)
        
        if missing_frames:
            print(f"⚠️  Missing frames in routing: {missing_frames}")
        else:
            print("✅ All expected frames registered in routing")
        
        # Test frame retrieval
        main_frame = get_destination_frame('mainmenuframe')
        print(f"✅ Frame retrieval working: {main_frame.__name__}")
        
    except Exception as e:
        print(f"❌ Frame routing test failed: {e}")
    
    print()

def test_vocabulary_data():
    """Test vocabulary data integrity"""
    print("Testing vocabulary data...")
    
    try:
        from app_variables import vocab_files_path
        import csv
        
        vocab_files = ['nouns', 'verbs', 'adjectives', 'adverbs']
        total_words = 0
        
        for vocab_file in vocab_files:
            file_path = os.path.join(vocab_files_path, vocab_file)
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        reader = csv.reader(f)
                        rows = list(reader)
                        word_count = len(rows)
                        total_words += word_count
                        print(f"✅ {vocab_file}: {word_count} entries")
                except Exception as e:
                    print(f"❌ Error reading {vocab_file}: {e}")
            else:
                print(f"⚠️  {vocab_file} file not found")
        
        print(f"✅ Total vocabulary entries: {total_words}")
        
    except Exception as e:
        print(f"❌ Vocabulary data test failed: {e}")
    
    print()

def test_progress_export():
    """Test progress export functionality"""
    print("Testing progress export...")
    
    try:
        from user_progress import progress_manager
        import tempfile
        
        # Create a temporary file for export
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_file = f.name
        
        # Test export
        progress_manager.export_progress_report(temp_file)
        
        # Check if file was created and has content
        if os.path.exists(temp_file):
            file_size = os.path.getsize(temp_file)
            print(f"✅ Progress report exported successfully ({file_size} bytes)")
            
            # Clean up
            os.unlink(temp_file)
        else:
            print("❌ Progress report file was not created")
    
    except Exception as e:
        print(f"❌ Progress export test failed: {e}")
    
    print()

def main():
    """Run all integration tests"""
    print("=" * 60)
    print("LingoLeap Integration Test Suite")
    print("=" * 60)
    print()
    
    test_imports()
    test_library_building()
    test_user_progress()
    test_audio_system()
    test_frame_routing()
    test_vocabulary_data()
    test_progress_export()
    
    print("=" * 60)
    print("Integration tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()
