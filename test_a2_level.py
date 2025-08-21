#!/usr/bin/env python3
"""
Test script to verify A2 level screen opens without CustomTkinter constructor errors
"""

import sys
import os
sys.path.append('src')

import customtkinter as ctk
from enhanced_proficiency_levels import A2DeutschFrame

def test_a2_frame():
    """Test that A2DeutschFrame can be created without constructor errors"""
    print("🧪 Testing A2DeutschFrame creation...")
    
    # Create root window
    root = ctk.CTk()
    root.withdraw()  # Hide the window
    
    try:
        # Test frame creation - this should not raise any constructor errors
        frame = A2DeutschFrame(
            root, 
            lambda: print("Navigate called"), 
            lambda: print("Update called")
        )
        print("✅ SUCCESS: A2DeutschFrame created without CustomTkinter constructor errors!")
        return True
        
    except Exception as e:
        print(f"❌ FAILED: Error creating A2DeutschFrame: {e}")
        return False
        
    finally:
        root.quit()
        root.destroy()

if __name__ == "__main__":
    print("=" * 60)
    print("Testing CustomTkinter Constructor Fix for A2 Level")
    print("=" * 60)
    
    success = test_a2_frame()
    
    if success:
        print("\n🎉 All tests passed! The CustomTkinter constructor issue has been fixed.")
    else:
        print("\n⚠️ Tests failed. There may still be constructor issues.")
    
    print("=" * 60)
