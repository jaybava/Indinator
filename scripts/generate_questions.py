import json
import re

INPUT_FILE = "../data/traits_flat.json"
OUTPUT_FILE = "../data/questions.json"


# ------------------------------------------------
# Helper: Generate natural-language question string
# ------------------------------------------------
def trait_to_question(trait):
    """
    Convert a raw trait key into a natural-language question.
    Trait format: group_traitname e.g. appearance_has_sword
    """

    group, raw = trait.split("_", 1)
    raw_pretty = raw.replace("_", " ")

    # ---- APPEARANCE ----
    if group == "appearance":
        if raw.startswith("has_"):
            return f"Does your character have {raw_pretty[4:]}?"
        if raw.startswith("hair_"):
            return f"Does your character have {raw_pretty[5:]} hair?"
        if raw.startswith("color_"):
            return f"Is your character associated with the color {raw_pretty[6:]}?"
        if raw.startswith("height_"):
            return f"Is your character {raw_pretty[7:]} in height?"
        return f"Is your character {raw_pretty}?"

    # ---- IDENTITY ----
    if group == "identity":
        if raw.startswith("gender_"):
            gender = raw.split("_")[1]
            if gender == "m":
                return "Is your character male?"
            if gender == "f":
                return "Is your character female?"
            return f"Does your character identify as {gender}?"
        if raw.startswith("species_"):
            return f"Is your character a {raw_pretty[8:]}?"
        if raw.startswith("age_"):
            return f"Is your character {raw_pretty[4:]}?"
        if raw.startswith("origin_"):
            return f"Does your character originate from {raw_pretty[7:]}?"
        if raw.startswith("alignment_"):
            return f"Is your character generally {raw_pretty[10:]}?"
        return f"Is your character {raw_pretty}?"

    # ---- FRANCHISE ----
    if group == "franchise":
        cleaned = raw_pretty.replace("franchise ", "")
        return f"Is your character from {cleaned}?"

    # ---- ABILITIES ----
    if group == "abilities":
        return f"Does your character have the ability '{raw_pretty}'?"

    # ---- ROLE ----
    if group == "role":
        return f"Does your character play the role of a {raw_pretty}?"

    # ---- ARCHETYPE ----
    if group == "archetype":
        return f"Is your character an example of a {raw_pretty} archetype?"

    # ---- PERSONALITY ----
    if group == "personality":
        return f"Is your character {raw_pretty}?"

    # ---- FALLBACK ----
    return f"Does your character have the trait '{raw_pretty}'?"


# ------------------------------------------------
# MAIN SCRIPT
# ------------------------------------------------
def main():
    print("Loading traits...")
    with open(INPUT_FILE, "r") as f:
        traits_data = json.load(f)

    # Collect all trait keys from all characters
    print("Extracting trait keys...")
    all_traits = set()
    for character, traits in traits_data.items():
        for trait in traits.keys():
            all_traits.add(trait)

    print(f"Found {len(all_traits)} unique traits.")

    questions = []

    # Convert each trait into a question entry
    print("Generating questions...")
    for trait in sorted(all_traits):
        group = trait.split("_")[0]  # identity / appearance / etc.
        question = trait_to_question(trait)

        questions.append({
            "trait": trait,
            "group": group,
            "question": question
        })

    # Save output JSON
    print(f"Writing to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, "w") as f:
        json.dump(questions, f, indent=4)

    print("Done! questions.json has been created.")


if __name__ == "__main__":
    main()
