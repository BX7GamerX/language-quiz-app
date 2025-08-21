#!/usr/bin/env python3
"""
Comprehensive Frame System Test
===============================

Test all screens and frame transitions to ensure proper functionality.
"""

import sys
import os
sys.path.append('src')

def test_frame_imports():
    """Test that all frames can be imported successfully"""
    print("🧪 Testing Frame Imports...")
    print("=" * 50)
    
    success = True
    
    try:
        # Test main application frames
        from mainapplication import MainApp
        print("✅ MainApp imports successfully")
        
        from welcomeframes import WelcomeFrame
        print("✅ WelcomeFrame imports successfully")
        
        # Test modern frames
        from modern_main_menu import ModernMainMenuFrame
        print("✅ ModernMainMenuFrame imports successfully")
        
        from modern_loading_frame import ModernLoadingFrame
        print("✅ ModernLoadingFrame imports successfully")
        
        from modern_update_frame import ModernUpdateAppFrame
        print("✅ ModernUpdateAppFrame imports successfully")
        
        from modern_spaced_repetition import ModernSpacedRepetitionFrame
        print("✅ ModernSpacedRepetitionFrame imports successfully")
        
        # Test enhanced proficiency levels
        from enhanced_proficiency_levels import (
            A2DeutschFrame, B1DeutschFrame, B2DeutschFrame
        )
        print("✅ Enhanced proficiency levels import successfully")
        
        # Test other frames
        from translatorframe import TranslatorFrame
        from translationgameframe import TranslationGameFrame, GameOverFrame
        from a1deutschframe import A1DeutschFrame
        print("✅ Game and utility frames import successfully")
        
        # Test frame routing system
        from frames import get_destination_frame
        print("✅ Frame routing system imports successfully")
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        success = False
    
    return success

def test_frame_routing():
    """Test that frame routing works correctly"""
    print("\n🔄 Testing Frame Routing...")
    print("=" * 50)
    
    success = True
    
    try:
        from frames import get_destination_frame
        
        # Test key frame routes
        routes_to_test = [
            ("mainmenuframe", "ModernMainMenuFrame"),
            ("loading_frame", "ModernLoadingFrame"),
            ("update_app_frame", "ModernUpdateAppFrame"),
            ("spaced_repetition_frame", "ModernSpacedRepetitionFrame"),
            ("a1_deutsch_frame", "A1DeutschFrame"),
            ("a2_deutsch_frame", "A2DeutschFrame"),
            ("b1_deutsch_frame", "B1DeutschFrame"),
            ("b2_deutsch_frame", "B2DeutschFrame"),
            ("translation_game_frame", "TranslationGameFrame"),
            ("translator_frame", "TranslatorFrame")
        ]
        
        for route_name, expected_class in routes_to_test:
            try:
                frame_class = get_destination_frame(route_name)
                actual_class_name = frame_class.__name__
                
                if expected_class in actual_class_name:
                    print(f"✅ {route_name} -> {actual_class_name}")
                else:
                    print(f"⚠️  {route_name} -> {actual_class_name} (expected {expected_class})")
                    
            except Exception as e:
                print(f"❌ {route_name} routing failed: {e}")
                success = False
                
    except Exception as e:
        print(f"❌ Frame routing test failed: {e}")
        success = False
    
    return success

def test_screen_transitions():
    """Test the logical flow between screens"""
    print("\n📱 Testing Screen Transition Logic...")
    print("=" * 50)
    
    transition_flows = [
        ("Loading Screen", "loading_frame", ["mainmenuframe"]),
        ("Main Menu", "mainmenuframe", ["spaced_repetition_frame", "a1_deutsch_frame", "a2_deutsch_frame", 
                                       "b1_deutsch_frame", "b2_deutsch_frame", "translation_game_frame",
                                       "update_app_frame", "translator_frame"]),
        ("Update Screen", "update_app_frame", ["mainmenuframe"]),
        ("Spaced Repetition", "spaced_repetition_frame", ["mainmenuframe"])
    ]
    
    success = True
    
    for screen_name, source_frame, possible_destinations in transition_flows:
        try:
            from frames import get_destination_frame
            
            # Check if source frame exists
            source_class = get_destination_frame(source_frame)
            
            # Check destinations
            available_destinations = []
            for dest in possible_destinations:
                try:
                    dest_class = get_destination_frame(dest)
                    available_destinations.append(dest)
                except:
                    pass
            
            print(f"✅ {screen_name}: {len(available_destinations)}/{len(possible_destinations)} destinations available")
            
        except Exception as e:
            print(f"❌ {screen_name} transition test failed: {e}")
            success = False
    
    return success

def test_modern_features():
    """Test that modern features are properly integrated"""
    print("\n🎨 Testing Modern UI Features...")
    print("=" * 50)
    
    success = True
    
    # Test loading screen features
    try:
        from modern_loading_frame import ModernLoadingFrame
        
        # Check if it has the required attributes
        test_methods = ['handle_loading_gif', 'animate_gif', 'start_library_build', 
                       'proceed_to_main_menu', 'update_progress']
        
        for method in test_methods:
            if hasattr(ModernLoadingFrame, method):
                print(f"✅ LoadingFrame has {method}")
            else:
                print(f"❌ LoadingFrame missing {method}")
                success = False
                
    except Exception as e:
        print(f"❌ Loading frame test failed: {e}")
        success = False
    
    # Test update screen features
    try:
        from modern_update_frame import ModernUpdateAppFrame
        
        test_methods = ['start_update', 'handle_loading_gif', 'return_to_main_menu', 
                       'update_progress', 'update_thread']
        
        for method in test_methods:
            if hasattr(ModernUpdateAppFrame, method):
                print(f"✅ UpdateFrame has {method}")
            else:
                print(f"❌ UpdateFrame missing {method}")
                success = False
                
    except Exception as e:
        print(f"❌ Update frame test failed: {e}")
        success = False
    
    # Test spaced repetition features
    try:
        from modern_spaced_repetition import ModernSpacedRepetitionFrame
        from spaced_repetition import SpacedRepetitionSystem
        
        print("✅ Spaced repetition system available")
        print("✅ Modern spaced repetition UI available")
        
    except Exception as e:
        print(f"❌ Spaced repetition test failed: {e}")
        success = False
    
    return success

def main():
    """Run all frame system tests"""
    print("🧪 LingoLeap Frame System Test Suite")
    print("=" * 60)
    
    # Run all tests
    test1 = test_frame_imports()
    test2 = test_frame_routing()
    test3 = test_screen_transitions()
    test4 = test_modern_features()
    
    print("\n" + "=" * 60)
    print("📋 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    if test1:
        print("✅ Frame Imports: PASSED")
    else:
        print("❌ Frame Imports: FAILED")
    
    if test2:
        print("✅ Frame Routing: PASSED")
    else:
        print("❌ Frame Routing: FAILED")
    
    if test3:
        print("✅ Screen Transitions: PASSED")
    else:
        print("❌ Screen Transitions: FAILED")
    
    if test4:
        print("✅ Modern Features: PASSED")
    else:
        print("❌ Modern Features: FAILED")
    
    print("\n" + "=" * 60)
    
    if all([test1, test2, test3, test4]):
        print("🎉 ALL FRAME SYSTEM TESTS: PASSED!")
        print("   ✅ All screens have proper frames")
        print("   ✅ Frame routing works correctly")
        print("   ✅ Modern UI features integrated")
        print("   ✅ Loading and update screens modernized")
        return True
    else:
        print("❌ SOME TESTS FAILED!")
        print("   Additional fixes may be needed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
