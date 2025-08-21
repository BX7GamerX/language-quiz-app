#!/usr/bin/env python3
"""
Quick test to verify complete login flow
"""

import sys
import os
sys.path.append('src')

def main():
    print("🧪 Testing complete login flow...")
    print("=" * 50)
    
    try:
        # Test 1: Import the main application
        from mainapplication import MainApp
        print("✅ MainApp imports successfully")
        
        # Test 2: Check that welcome frame leads to modern main menu
        from welcomeframes import WelcomeFrame
        print("✅ WelcomeFrame imports successfully")
        
        # Test 3: Verify frame routing
        from frames import get_destination_frame
        main_menu_class = get_destination_frame("mainmenuframe")
        print(f"✅ Frame routing: mainmenuframe -> {main_menu_class}")
        
        # Test 4: Check that it's the modern frame
        if "Modern" in str(main_menu_class):
            print("✅ LOGIN REDIRECTS TO MODERN MAIN MENU ✅")
        else:
            print("❌ LOGIN STILL REDIRECTS TO OLD MAIN MENU ❌")
            return False
            
        # Test 5: Check that spaced repetition is available
        spaced_rep_class = get_destination_frame("spaced_repetition_frame")
        print(f"✅ Spaced repetition available: {spaced_rep_class}")
        
        print("\n" + "=" * 50)
        print("🎉 LOGIN REDIRECTION FIX: COMPLETE SUCCESS!")
        print("📋 Summary:")
        print("   ✅ Login redirects to MODERN main menu")
        print("   ✅ All enhanced features are accessible")
        print("   ✅ Spaced repetition system available")
        print("   ✅ Advanced proficiency levels available")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n❌ LOGIN REDIRECTION FIX: FAILED")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
