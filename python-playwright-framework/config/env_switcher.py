"""
Environment Switcher Utility
Helps switch between different environment configurations
"""

import os
import shutil
from pathlib import Path


class EnvironmentSwitcher:
    """Switch between different environment configurations"""
    
    # Available environments
    ENVIRONMENTS = ["dev", "qa", "staging", "prod"]
    
    # Root directory (framework root)
    ROOT_DIR = Path(__file__).parent.parent
    
    @classmethod
    def switch_env(cls, environment: str) -> bool:
        """
        Switch to specified environment
        
        Args:
            environment: Environment name (dev, qa, staging, prod)
            
        Returns:
            bool: True if successful, False otherwise
        """
        if environment not in cls.ENVIRONMENTS:
            print(f"❌ Invalid environment: {environment}")
            print(f"✅ Available environments: {', '.join(cls.ENVIRONMENTS)}")
            return False
        
        source_file = cls.ROOT_DIR / f".env.{environment}"
        target_file = cls.ROOT_DIR / ".env"
        
        if not source_file.exists():
            print(f"❌ Configuration file not found: {source_file}")
            return False
        
        try:
            # Copy environment file to .env
            shutil.copy(source_file, target_file)
            print(f"✅ Switched to {environment.upper()} environment")
            print(f"📄 Active config: .env.{environment} → .env")
            
            # Display current settings
            cls.display_current_env()
            return True
            
        except Exception as e:
            print(f"❌ Error switching environment: {e}")
            return False
    
    @classmethod
    def display_current_env(cls) -> None:
        """Display current environment settings"""
        env_file = cls.ROOT_DIR / ".env"
        
        if not env_file.exists():
            print("⚠️ No .env file found. Run switch_env() first.")
            return
        
        print("\n📋 Current Environment Settings:")
        print("=" * 50)
        
        # Read and display key settings
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                # Show only important settings
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    if key in ['BASE_URL', 'ENV', 'HEADLESS', 'WORKERS']:
                        print(f"  {key}: {value}")
        
        print("=" * 50)
    
    @classmethod
    def list_environments(cls) -> None:
        """List all available environments"""
        print("\n🌍 Available Environments:")
        print("=" * 50)
        
        for env in cls.ENVIRONMENTS:
            env_file = cls.ROOT_DIR / f".env.{env}"
            status = "✅" if env_file.exists() else "❌"
            print(f"  {status} {env.upper():<10} (.env.{env})")
        
        print("=" * 50)
    
    @classmethod
    def get_current_env(cls) -> str:
        """Get current active environment"""
        env_file = cls.ROOT_DIR / ".env"
        
        if not env_file.exists():
            return "None (no .env file)"
        
        # Read ENV variable from .env
        with open(env_file, 'r') as f:
            for line in f:
                if line.strip().startswith('ENV='):
                    return line.split('=')[1].strip()
        
        return "Unknown"


# CLI Interface
if __name__ == "__main__":
    import sys
    
    switcher = EnvironmentSwitcher()
    
    if len(sys.argv) < 2:
        print("\n🎯 Environment Switcher CLI")
        print("=" * 50)
        print("\nUsage:")
        print("  python env_switcher.py <environment>")
        print("  python env_switcher.py list")
        print("  python env_switcher.py current")
        print("\nExamples:")
        print("  python env_switcher.py dev")
        print("  python env_switcher.py qa")
        print("  python env_switcher.py staging")
        print("  python env_switcher.py prod")
        print("  python env_switcher.py list")
        switcher.list_environments()
    
    elif sys.argv[1] == "list":
        switcher.list_environments()
    
    elif sys.argv[1] == "current":
        current = switcher.get_current_env()
        print(f"\n📍 Current Environment: {current.upper()}")
        switcher.display_current_env()
    
    else:
        environment = sys.argv[1].lower()
        switcher.switch_env(environment)
