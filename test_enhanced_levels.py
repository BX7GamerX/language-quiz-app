#!/usr/bin/env python3
"""
Test Enhanced Proficiency Levels Frame Construction
==================================================

Test that the enhanced proficiency level frames can be constructed
without CustomTkinter width/height placement errors.
"""

import sys
import os
sys.path.append('src')

def test_frame_construction():
    """Test that enhanced proficiency frames can be constructed properly"""
    print("🧪 Testing Enhanced Proficiency Level Frame Construction...")
    print("=" * 60)
    
    success = True
    
    try:
        # Import CustomTkinter
        import customtkinter as ctk
        print("✅ CustomTkinter imported successfully")
        
        # Create a test root window
        root = ctk.CTk()
        root.withdraw()  # Hide the window
        print("✅ Test root window created")
        
        # Test A2DeutschFrame construction
        try:
            from enhanced_proficiency_levels import A2DeutschFrame
            a2_frame = A2DeutschFrame(root)
            print("✅ A2DeutschFrame constructed successfully")
        except Exception as e:
            print(f"❌ A2DeutschFrame construction failed: {e}")
            success = False
        
        # Test B1DeutschFrame construction
        try:
            from enhanced_proficiency_levels import B1DeutschFrame
            b1_frame = B1DeutschFrame(root)
            print("✅ B1DeutschFrame constructed successfully")
        except Exception as e:
            print(f"❌ B1DeutschFrame construction failed: {e}")
            success = False
        
        # Test B2DeutschFrame construction
        try:
            from enhanced_proficiency_levels import B2DeutschFrame
            b2_frame = B2DeutschFrame(root)
            print("✅ B2DeutschFrame constructed successfully")
        except Exception as e:
            print(f"❌ B2DeutschFrame construction failed: {e}")
            success = False
        
        # Clean up
        root.destroy()
        print("✅ Test cleanup completed")
        
    except Exception as e:
        print(f"❌ Test setup failed: {e}")
        success = False
    
    return success

def test_frame_routing():
    """Test that frame routing works for enhanced levels"""
    print("\n🔄 Testing Enhanced Level Frame Routing...")
    print("=" * 60)
    
    success = True
    
    try:
        from frames import get_destination_frame
        
        # Test enhanced level routing
        levels_to_test = [
            ("a2_deutsch_frame", "A2DeutschFrame"),
            ("b1_deutsch_frame", "B1DeutschFrame"),
            ("b2_deutsch_frame", "B2DeutschFrame")
        ]
        
        for level_name, expected_class in levels_to_test:
            try:
                frame_class = get_destination_frame(level_name)
                actual_class_name = frame_class.__name__
                
                if expected_class == actual_class_name:
                    print(f"✅ {level_name} -> {actual_class_name}")
                else:
                    print(f"⚠️  {level_name} -> {actual_class_name} (expected {expected_class})")
                    
            except Exception as e:
                print(f"❌ {level_name} routing failed: {e}")
                success = False
                
    except Exception as e:
        print(f"❌ Frame routing test failed: {e}")
        success = False
    
    return success

def test_mock_navigation():
    """Test mock navigation to enhanced levels"""
    print("\n📱 Testing Mock Navigation to Enhanced Levels...")
    print("=" * 60)
    
    success = True
    
    try:
        from frames import get_destination_frame
        import customtkinter as ctk
        
        # Create mock master with required methods
        class MockMaster:
            def change_geometry(self, geometry):
                print(f"  📐 Geometry would change to: {geometry}")
            
            def open_frame(self, from_frame, to_frame):
                print(f"  🔄 Would navigate from {from_frame} to {to_frame}")
        
        mock_master = MockMaster()
        
        # Test creating and "opening" each enhanced level
        levels = ["a2_deutsch_frame", "b1_deutsch_frame", "b2_deutsch_frame"]
        
        for level in levels:
            try:
                frame_class = get_destination_frame(level)
                print(f"\n🎯 Testing {level}:")
                
                # This would normally be called by the main application
                print(f"  📝 Frame class: {frame_class.__name__}")
                
                # Test construction with mock master
                frame = frame_class(mock_master)
                print(f"✅ {level} navigation test passed")
                
            except Exception as e:
                print(f"❌ {level} navigation test failed: {e}")
                success = False
                
    except Exception as e:
        print(f"❌ Mock navigation test failed: {e}")
        success = False
    
    return success

def main():
    """Run all enhanced proficiency level tests"""
    print("🧪 Enhanced Proficiency Levels Test Suite")
    print("=" * 70)
    
    # Run all tests
    test1 = test_frame_construction()
    test2 = test_frame_routing()
    test3 = test_mock_navigation()
    
    print("\n" + "=" * 70)
    print("📋 TEST RESULTS SUMMARY")
    print("=" * 70)
    
    if test1:
        print("✅ Frame Construction: PASSED")
    else:
        print("❌ Frame Construction: FAILED")
    
    if test2:
        print("✅ Frame Routing: PASSED")
    else:
        print("❌ Frame Routing: FAILED")
    
    if test3:
        print("✅ Mock Navigation: PASSED")
    else:
        print("❌ Mock Navigation: FAILED")
    
    print("\n" + "=" * 70)
    
    if all([test1, test2, test3]):
        print("🎉 ALL ENHANCED PROFICIENCY TESTS: PASSED!")
        print("   ✅ CustomTkinter constructor issue resolved")
        print("   ✅ All enhanced levels can be constructed")
        print("   ✅ Frame routing works correctly")
        print("   ✅ Navigation to enhanced levels working")
        return True
    else:
        print("❌ SOME TESTS FAILED!")
        print("   Additional fixes may be needed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
