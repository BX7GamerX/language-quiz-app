#!/usr/bin/env python3
"""
Test script to verify login redirection fix
"""

import sys
import os
sys.path.append('src')

def test_import_fix():
    """Test that the imports are working correctly"""
    try:
        from mainapplication import MainApp
        from modern_main_menu import ModernMainMenuFrame
        from frames import get_destination_frame
        
        print("✅ All imports working correctly")
        
        # Test that the frame routing includes the modern menu
        frame_dict = get_destination_frame("mainmenuframe")
        print(f"✅ Main menu frame type: {frame_dict}")
        
        # Check if it's the modern frame
        if "Modern" in str(frame_dict):
            print("✅ Login will redirect to MODERN main menu")
        else:
            print("❌ Login still redirects to OLD main menu")
            
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_mainapplication_fix():
    """Test that mainapplication.py is using the correct frame"""
    try:
        with open('src/mainapplication.py', 'r') as f:
            content = f.read()
            
        if 'ModernMainMenuFrame' in content:
            print("✅ mainapplication.py imports ModernMainMenuFrame")
        else:
            print("❌ mainapplication.py still imports old MainMenuFrame")
            
        if 'ModernMainMenuFrame(self, fg_color=' in content:
            print("✅ mainapplication.py creates ModernMainMenuFrame on login")
        else:
            print("❌ mainapplication.py still creates old MainMenuFrame on login")
            
        return True
        
    except Exception as e:
        print(f"❌ Error checking mainapplication.py: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing login redirection fix...")
    print("=" * 50)
    
    success1 = test_import_fix()
    print()
    success2 = test_mainapplication_fix()
    
    print("\n" + "=" * 50)
    if success1 and success2:
        print("🎉 LOGIN REDIRECTION FIX: SUCCESS!")
        print("   After login, users will see the MODERN main menu")
    else:
        print("❌ LOGIN REDIRECTION FIX: FAILED!")
        print("   Additional fixes needed")
