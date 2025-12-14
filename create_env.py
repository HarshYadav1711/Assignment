"""
Helper script to create .env file from template.
Run: python create_env.py
"""
import shutil
import os

def create_env_file():
    """Create .env file from env_template.txt if it doesn't exist"""
    template_file = 'env_template.txt'
    env_file = '.env'
    
    if not os.path.exists(template_file):
        print(f"ERROR: {template_file} not found!")
        print("Please ensure env_template.txt exists in the current directory.")
        return False
    
    if os.path.exists(env_file):
        print(f"{env_file} already exists.")
        response = input("Do you want to overwrite it? (y/N): ")
        if response.lower() != 'y':
            print("Skipping .env creation.")
            return False
    
    try:
        shutil.copy(template_file, env_file)
        print(f"✓ Created {env_file} from {template_file}")
        print(f"\n⚠️  IMPORTANT: Edit {env_file} and add your OpenAI API key!")
        print("   OPENAI_API_KEY=sk-your-key-here")
        return True
    except Exception as e:
        print(f"ERROR: Failed to create {env_file}: {e}")
        return False

if __name__ == '__main__':
    print("Creating .env file from template...")
    create_env_file()

