"""Combine all trait categories into a single traits.json file."""

import json
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from generate_identity_traits import get_identity_traits
from generate_franchise_traits import get_franchise_traits
from generate_appearance_traits import get_appearance_traits
from generate_ability_traits import get_ability_traits
from generate_role_traits import get_role_traits
from generate_archetype_traits import get_archetype_traits
from generate_personality_traits import get_personality_traits


def combine_all_traits():
    """Combine all trait categories into a single dictionary."""
    identity_traits = get_identity_traits()
    franchise_traits = get_franchise_traits()
    appearance_traits = get_appearance_traits()
    ability_traits = get_ability_traits()
    role_traits = get_role_traits()
    archetype_traits = get_archetype_traits()
    personality_traits = get_personality_traits()
    
    # Get all character names
    all_characters = set()
    for traits_dict in [identity_traits, franchise_traits, appearance_traits, 
                        ability_traits, role_traits, archetype_traits, personality_traits]:
        all_characters.update(traits_dict.keys())
    
    # Combine traits for each character
    combined_traits = {}
    for character in sorted(all_characters):
        combined_traits[character] = {
            "identity": identity_traits.get(character, {}),
            "franchise": franchise_traits.get(character, {}),
            "appearance": appearance_traits.get(character, {}),
            "abilities": ability_traits.get(character, {}),
            "role": role_traits.get(character, {}),
            "archetype": archetype_traits.get(character, {}),
            "personality": personality_traits.get(character, {})
        }
    
    return combined_traits


def flatten_traits(nested_traits):
    """Flatten nested traits dict for easier ML processing."""
    flat_traits = {}
    for character, categories in nested_traits.items():
        flat_traits[character] = {}
        for category, traits in categories.items():
            for trait_key, trait_value in traits.items():
                # Prefix trait with category for clarity
                flat_key = f"{category}_{trait_key}"
                flat_traits[character][flat_key] = trait_value
    return flat_traits


if __name__ == "__main__":
    # Combine all traits
    print("Combining all trait categories...")
    combined = combine_all_traits()
    
    # Save nested version
    output_path = Path(__file__).parent.parent / "data" / "traits.json"
    output_path.parent.mkdir(exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Saved nested traits to {output_path}")
    
    # Save flattened version for ML
    flat_output_path = Path(__file__).parent.parent / "data" / "traits_flat.json"
    flat_traits = flatten_traits(combined)
    
    with open(flat_output_path, 'w', encoding='utf-8') as f:
        json.dump(flat_traits, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Saved flattened traits to {flat_output_path}")
    
    # Print statistics
    num_characters = len(combined)
    sample_char = list(combined.keys())[0]
    sample_traits = flat_traits[sample_char]
    num_total_traits = len(sample_traits)
    
    print(f"\n📊 Statistics:")
    print(f"  - Characters: {num_characters}")
    print(f"  - Sample character: {sample_char}")
    print(f"  - Trait dimensions: {num_total_traits}")
    print(f"\nSample traits for {sample_char}:")
    for key, val in list(sample_traits.items())[:10]:
        print(f"  - {key}: {val}")

