"""
Test script for ClauseWise Granite LLM integration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_granite_import():
    """Test if we can import the Granite service"""
    try:
        from backend.services.granite_llm import get_granite_service
        print("✅ Granite LLM service imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_dependencies():
    """Test if all dependencies are available"""
    dependencies = [
        ('torch', 'PyTorch'),
        ('transformers', 'Transformers'),
        ('huggingface_hub', 'Hugging Face Hub')
    ]
    
    all_good = True
    for module, name in dependencies:
        try:
            __import__(module)
            print(f"✅ {name} is available")
        except ImportError:
            print(f"❌ {name} is NOT available")
            all_good = False
    
    return all_good

def test_granite_initialization():
    """Test if Granite service can be initialized"""
    try:
        print("🚀 Attempting to initialize Granite service...")
        from backend.services.granite_llm import get_granite_service
        
        # This will attempt to load the model
        granite = get_granite_service()
        print("✅ Granite service initialized successfully")
        
        # Test a simple response
        response = granite.generate_response("Hello, this is a test.", max_length=50)
        print(f"✅ Test response: {response[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Granite initialization failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing ClauseWise Granite Integration")
    print("=" * 50)
    
    # Test 1: Dependencies
    print("\n1. Testing dependencies...")
    deps_ok = test_dependencies()
    
    # Test 2: Import
    print("\n2. Testing imports...")
    import_ok = test_granite_import()
    
    # Test 3: Initialization (only if previous tests pass)
    if deps_ok and import_ok:
        print("\n3. Testing Granite initialization...")
        init_ok = test_granite_initialization()
    else:
        print("\n3. Skipping initialization test due to dependency issues")
        init_ok = False
    
    print("\n" + "=" * 50)
    if deps_ok and import_ok and init_ok:
        print("🎉 All tests passed! ClauseWise is ready with Granite AI")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
