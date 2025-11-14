"""
Main entry point for Indinator game.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from indinator import AkinatorAI, AkinatorGame


def main():
    """Initialize and run the game."""
    # Define file paths
    data_dir = project_root / "data"
    traits_file = data_dir / "traits_flat.json"
    questions_file = data_dir / "questions.json"
    characters_file = data_dir / "characters.json"
    
    # Check if required files exist
    missing_files = []
    if not traits_file.exists():
        missing_files.append(str(traits_file))
    if not questions_file.exists():
        missing_files.append(str(questions_file))
    if not characters_file.exists():
        missing_files.append(str(characters_file))
    
    if missing_files:
        print("❌ Error: Missing required data files:")
        for f in missing_files:
            print(f"   - {f}")
        print("\nPlease run 'python scripts/combine_traits.py' first to generate traits files.")
        return 1
    
    try:
        # Initialize AI engine
        print("🔧 Initializing AI engine...")
        ai = AkinatorAI(
            traits_file=str(traits_file),
            questions_file=str(questions_file),
            characters_file=str(characters_file)
        )
        
        # Create and run game
        print("✓ AI engine ready!\n")
        game = AkinatorGame(ai)
        game.run()
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error initializing game: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

