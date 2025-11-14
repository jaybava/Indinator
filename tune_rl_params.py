"""
Tune RL hyperparameters for better learning.
Experiments with different learning rates, exploration rates, etc.
"""

import json
from pathlib import Path

def tune_parameters():
    """Adjust RL parameters for better performance."""
    
    print("⚙️ RL Hyperparameter Tuning")
    print("="*60)
    print("\nCurrent parameters in indinator/rl_agent.py:")
    print("   alpha (learning rate): 0.1")
    print("   gamma (discount factor): 0.95")
    print("   epsilon (exploration): 0.2 → 0.05")
    print("   epsilon_decay: 0.995")
    print("="*60)
    
    print("\n💡 Recommended Adjustments:\n")
    
    print("1️⃣  FOR FASTER LEARNING:")
    print("   alpha = 0.2  (was 0.1) - learns twice as fast")
    print("   epsilon_decay = 0.99  (was 0.995) - exploits faster")
    print("   Use when: AI hasn't learned enough patterns yet")
    
    print("\n2️⃣  FOR MORE EXPLORATION:")
    print("   epsilon = 0.3  (was 0.2) - explores more")
    print("   epsilon_min = 0.1  (was 0.05) - never stops exploring")
    print("   Use when: AI makes same mistakes repeatedly")
    
    print("\n3️⃣  FOR FINE-TUNING:")
    print("   alpha = 0.05  (was 0.1) - smaller updates")
    print("   epsilon = 0.1  (was 0.2) - mostly exploit")
    print("   Use when: AI is already good, just needs polish")
    
    print("\n4️⃣  FOR AGGRESSIVE LEARNING:")
    print("   alpha = 0.25")
    print("   gamma = 0.98  (was 0.95) - values long-term rewards more")
    print("   epsilon_decay = 0.98  (was 0.995)")
    print("   Use when: Want maximum learning speed")
    
    print("\n" + "="*60)
    print("📝 To apply changes:")
    print("   1. Edit indinator/rl_agent.py")
    print("   2. Find __init__ method (line ~21)")
    print("   3. Modify alpha, gamma, epsilon values")
    print("   4. Delete data/q_table.json to start fresh")
    print("   5. Run training again")
    print("="*60)
    
    print("\n🎯 QUICK WIN - Try this preset:")
    print("   alpha = 0.15  (faster learning)")
    print("   gamma = 0.97  (better long-term planning)")
    print("   epsilon = 0.25  (more exploration)")
    print("   epsilon_decay = 0.992  (balanced)")
    
    print("\n" + "="*60)
    
    # Check current Q-table stats
    q_table_path = Path("data/q_table.json")
    if q_table_path.exists():
        with open(q_table_path, 'r') as f:
            data = json.load(f)
        
        print("\n📊 Current Q-Table Analysis:")
        q_values = data.get('q_values', {})
        
        # Analyze Q-value distribution
        all_q_values = []
        for state_actions in q_values.values():
            all_q_values.extend(state_actions.values())
        
        if all_q_values:
            print(f"   Total Q-values: {len(all_q_values)}")
            print(f"   Average Q-value: {sum(all_q_values)/len(all_q_values):.2f}")
            print(f"   Max Q-value: {max(all_q_values):.2f}")
            print(f"   Min Q-value: {min(all_q_values):.2f}")
            
            # Distribution
            positive = sum(1 for q in all_q_values if q > 0)
            negative = sum(1 for q in all_q_values if q < 0)
            neutral = len(all_q_values) - positive - negative
            
            print(f"\n   Distribution:")
            print(f"   Positive Q-values: {positive} ({positive/len(all_q_values)*100:.1f}%)")
            print(f"   Negative Q-values: {negative} ({negative/len(all_q_values)*100:.1f}%)")
            print(f"   Neutral Q-values: {neutral} ({neutral/len(all_q_values)*100:.1f}%)")
            
            if positive < len(all_q_values) * 0.3:
                print("\n   ⚠️  Low positive Q-values - AI might be pessimistic")
                print("   💡 Try: Increase reward for success (modify train_rl_agent.py)")
            
            if negative > len(all_q_values) * 0.5:
                print("\n   ⚠️  Many negative Q-values - penalties too harsh")
                print("   💡 Try: Reduce question cost from -1 to -0.5")
        
        print("\n" + "="*60)

if __name__ == "__main__":
    tune_parameters()

