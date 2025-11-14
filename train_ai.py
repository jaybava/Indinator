"""
Quick training script for the AI
Run this to train the RL agent before playing.
"""

import sys
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent))

from scripts.train_rl_agent import AutoTrainer

if __name__ == "__main__":
    print("🎓 INDINATOR - AI Training Mode")
    print("="*60)
    print("This will train the AI by playing 100 automated games.")
    print("The AI will learn optimal question selection strategies.")
    print("="*60 + "\n")
    
    # Ask for confirmation
    response = input("Start training? (yes/no): ").strip().lower()
    
    if response in ['yes', 'y']:
        try:
            trainer = AutoTrainer()
            trainer.train(num_games=100, verbose_interval=10)
            
            print("\n" + "="*60)
            print("✅ Training Complete!")
            print("The AI is now smarter and ready to play.")
            print("Run 'python main.py' to start playing!")
            print("="*60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n⚠️ Training interrupted!")
            print("Progress has been saved. You can continue training later.")
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("Training cancelled.")

