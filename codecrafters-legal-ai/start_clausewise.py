"""
ClauseWise Startup Script
Handles graceful initialization of the Granite AI model with proper error handling
"""

import sys
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_dependencies():
    """Check if all required dependencies are available"""
    required_packages = [
        ('fastapi', 'FastAPI'),
        ('uvicorn', 'Uvicorn'),
        ('streamlit', 'Streamlit'),
        ('transformers', 'Transformers'),
        ('torch', 'PyTorch'),
        ('pydantic', 'Pydantic')
    ]
    
    missing = []
    for package, name in required_packages:
        try:
            __import__(package)
            logger.info(f"✅ {name} is available")
        except ImportError:
            logger.error(f"❌ {name} is missing")
            missing.append(name)
    
    return missing

def load_environment():
    """Load environment variables"""
    try:
        # Check for .env file
        env_path = os.path.join(os.getcwd(), '.env')
        if os.path.exists(env_path):
            logger.info("✅ .env file found")
            
            # Check for required tokens
            hf_token = os.getenv('HUGGINGFACE_TOKEN')
            if hf_token and hf_token != 'your_huggingface_token_here':
                logger.info("✅ Hugging Face token configured")
            else:
                logger.warning("⚠️ Hugging Face token not configured")
                
        else:
            logger.warning("⚠️ .env file not found")
            
    except Exception as e:
        logger.error(f"❌ Error loading environment: {e}")

def test_backend_import():
    """Test if backend can be imported"""
    try:
        from backend.main import app
        logger.info("✅ Backend imported successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Backend import failed: {e}")
        return False

def start_backend():
    """Start the FastAPI backend"""
    try:
        import uvicorn
        logger.info("🚀 Starting ClauseWise Backend...")
        uvicorn.run(
            "backend.main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="info"
        )
    except Exception as e:
        logger.error(f"❌ Failed to start backend: {e}")
        return False

def start_frontend():
    """Start the Streamlit frontend"""
    try:
        import subprocess
        logger.info("🚀 Starting ClauseWise Frontend...")
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "frontend/streamlit_app.py", 
            "--server.port", "8501"
        ])
    except Exception as e:
        logger.error(f"❌ Failed to start frontend: {e}")
        return False

if __name__ == "__main__":
    print("🎯 ClauseWise: Legal Document Analyzer")
    print("=" * 50)
    
    # Check dependencies
    print("\n1. Checking dependencies...")
    missing = check_dependencies()
    
    if missing:
        print(f"\n❌ Missing dependencies: {', '.join(missing)}")
        print("Please install missing packages with: pip install -r requirements.txt")
        sys.exit(1)
    
    # Load environment
    print("\n2. Loading environment...")
    load_environment()
    
    # Test backend import
    print("\n3. Testing backend...")
    if not test_backend_import():
        print("❌ Backend import failed. Check the error logs above.")
        sys.exit(1)
    
    print("\n✅ All checks passed!")
    print("\nChoose an option:")
    print("1. Start Backend only (port 8000)")
    print("2. Start Frontend only (port 8501)")
    print("3. Start both (recommended)")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        start_backend()
    elif choice == "2":
        start_frontend()
    elif choice == "3":
        print("\n🚀 Starting both Backend and Frontend...")
        print("Backend will be available at: http://localhost:8000")
        print("Frontend will be available at: http://localhost:8501")
        print("API Documentation: http://localhost:8000/docs")
        print("\nStarting backend first...")
        start_backend()
    else:
        print("Invalid choice. Exiting.")
        sys.exit(1)
