"""Generate ability/power traits for all characters."""

def get_ability_traits():
    """Return ability traits for each character."""
    return {
        # Harry Potter Universe
        "Harry Potter": {"magic": 1, "flying": 1},
        "Hermione Granger": {"magic": 1, "intelligent": 1},
        "Ron Weasley": {"magic": 1},
        "Albus Dumbledore": {"magic": 1, "powerful_magic": 1},
        
        # Star Wars
        "Darth Vader": {"force_user": 1, "lightsaber": 1, "super_strength": 1},
        "Luke Skywalker": {"force_user": 1, "lightsaber": 1},
        "Princess Leia": {"force_user": 1, "leadership": 1},
        "Han Solo": {"gun_user": 1, "piloting": 1},
        
        # Lord of the Rings
        "Frodo Baggins": {"stealth": 1, "ring_bearer": 1},
        "Gandalf": {"magic": 1, "powerful_magic": 1, "sword_user": 1},
        "Aragorn": {"sword_user": 1, "leadership": 1, "healing": 1},
        "Legolas": {"bow_user": 1, "super_agility": 1, "keen_senses": 1},
        "Bilbo Baggins": {"stealth": 1, "ring_bearer": 1},
        
        # Hunger Games
        "Katniss Everdeen": {"bow_user": 1, "survival_skills": 1},
        "Peeta Mellark": {"super_strength": 1, "camouflage": 1},
        "President Snow": {"manipulation": 1},
        
        # Detective/Spy
        "Sherlock Holmes": {"super_intelligence": 1, "deduction": 1},
        "John Watson": {"medical_skills": 1, "gun_user": 1},
        "James Bond": {"gun_user": 1, "martial_arts": 1, "gadgets": 1},
        "Indiana Jones": {"whip_user": 1, "archaeology": 1, "gun_user": 1},
        
        # DC Comics
        "Batman": {"martial_arts": 1, "gadgets": 1, "super_intelligence": 1, "stealth": 1},
        "Superman": {"super_strength": 1, "super_speed": 1, "flying": 1, "laser_vision": 1, "invulnerability": 1},
        "Wonder Woman": {"super_strength": 1, "sword_user": 1, "flying": 1, "lasso": 1},
        "The Joker": {"manipulation": 1, "chaos_creation": 1, "unpredictable": 1},
        "Harley Quinn": {"martial_arts": 1, "acrobatics": 1, "weapon_user": 1},
        
        # Marvel
        "Spider-Man": {"super_strength": 1, "wall_crawling": 1, "web_shooting": 1, "spider_sense": 1, "super_agility": 1},
        "Iron Man": {"tech_genius": 1, "flying": 1, "energy_blasts": 1, "super_intelligence": 1},
        "Captain America": {"super_strength": 1, "shield_user": 1, "super_agility": 1, "leadership": 1},
        "Hulk": {"super_strength": 1, "invulnerability": 1, "regeneration": 1, "rage_power": 1},
        "Thor": {"super_strength": 1, "weather_control": 1, "flying": 1, "hammer_user": 1, "lightning": 1},
        "Black Widow": {"martial_arts": 1, "gun_user": 1, "stealth": 1, "espionage": 1},
        "Loki": {"magic": 1, "shapeshifting": 1, "illusions": 1, "manipulation": 1},
        "Thanos": {"super_strength": 1, "invulnerability": 1, "energy_manipulation": 1, "cosmic_power": 1},
        
        # Naruto
        "Naruto Uzumaki": {"ninjutsu": 1, "shadow_clones": 1, "super_speed": 1, "martial_arts": 1, "rasengan": 1},
        "Sasuke Uchiha": {"ninjutsu": 1, "fire_control": 1, "lightning_control": 1, "sharingan": 1},
        "Sakura Haruno": {"super_strength": 1, "medical_skills": 1, "martial_arts": 1},
        "Kakashi Hatake": {"ninjutsu": 1, "lightning_control": 1, "sharingan": 1, "copying_abilities": 1},
        
        # One Piece
        "Monkey D. Luffy": {"super_strength": 1, "elasticity": 1, "martial_arts": 1, "devil_fruit": 1},
        "Roronoa Zoro": {"sword_user": 1, "three_sword_style": 1, "super_strength": 1},
        "Nami": {"weather_control": 1, "staff_user": 1, "navigation": 1},
        "Sanji": {"martial_arts": 1, "fire_control": 1, "cooking": 1},
        
        # Death Note
        "Light Yagami": {"death_note": 1, "super_intelligence": 1, "manipulation": 1},
        "L Lawliet": {"super_intelligence": 1, "deduction": 1},
        
        # Dragon Ball
        "Goku": {"super_strength": 1, "super_speed": 1, "energy_blasts": 1, "flying": 1, "transformation": 1, "ki_control": 1},
        "Vegeta": {"super_strength": 1, "super_speed": 1, "energy_blasts": 1, "flying": 1, "transformation": 1, "ki_control": 1},
        "Piccolo": {"super_strength": 1, "energy_blasts": 1, "flying": 1, "regeneration": 1, "stretching": 1},
        
        # Pokemon
        "Ash Ketchum": {"pokemon_trainer": 1, "leadership": 1},
        "Pikachu": {"electricity": 1, "super_speed": 1, "lightning_attacks": 1},
        
        # Nintendo
        "Mario": {"super_jump": 1, "power_ups": 1, "fire_control": 1},
        "Luigi": {"super_jump": 1, "power_ups": 1},
        "Princess Peach": {"floating": 1, "magic": 1},
        "Bowser": {"fire_breathing": 1, "super_strength": 1, "shell_defense": 1},
        "Link": {"sword_user": 1, "bomb_user": 1, "bow_user": 1, "magic_items": 1},
        "Zelda": {"magic": 1, "light_power": 1, "wisdom": 1},
        "Ganondorf": {"dark_magic": 1, "sword_user": 1, "super_strength": 1, "transformation": 1},
        
        # Video Games
        "Kratos": {"super_strength": 1, "weapon_master": 1, "god_powers": 1, "rage_mode": 1},
        "Atreus": {"bow_user": 1, "magic": 1, "animal_communication": 1},
        "Master Chief": {"super_strength": 1, "gun_user": 1, "super_agility": 1, "enhanced_reflexes": 1},
        "Cortana": {"hacking": 1, "super_intelligence": 1, "data_manipulation": 1},
        "Geralt of Rivia": {"sword_user": 1, "magic_signs": 1, "alchemy": 1, "enhanced_senses": 1, "monster_hunting": 1},
        "Yennefer": {"magic": 1, "powerful_magic": 1, "teleportation": 1},
        "Ciri": {"sword_user": 1, "teleportation": 1, "time_space_manipulation": 1, "super_speed": 1},
        
        # Attack on Titan
        "Eren Yeager": {"titan_shifting": 1, "regeneration": 1, "super_strength": 1, "hardening": 1},
        "Mikasa Ackerman": {"sword_user": 1, "super_agility": 1, "combat_genius": 1},
        "Armin Arlert": {"super_intelligence": 1, "strategy": 1, "titan_shifting": 1},
        "Levi Ackerman": {"sword_user": 1, "super_agility": 1, "super_speed": 1, "combat_master": 1},
        
        # Walking Dead
        "Rick Grimes": {"gun_user": 1, "leadership": 1, "survival_skills": 1},
        "Michonne": {"sword_user": 1, "martial_arts": 1, "survival_skills": 1},
        
        # Simpsons
        "Homer Simpson": {"durability": 1, "luck": 1},
        "Bart Simpson": {"skateboarding": 1, "pranks": 1},
        "Lisa Simpson": {"super_intelligence": 1, "music": 1},
        
        # SpongeBob
        "SpongeBob SquarePants": {"underwater_breathing": 1, "regeneration": 1, "cooking": 1, "karate": 1},
        "Patrick Star": {"super_strength": 1, "durability": 1, "underwater_breathing": 1},
        "Squidward Tentacles": {"music": 1, "art": 1, "underwater_breathing": 1},
        
        # Shrek
        "Shrek": {"super_strength": 1, "ogre_powers": 1, "roar": 1},
        "Donkey": {"talking": 1, "flying": 1},
        "Fiona": {"martial_arts": 1, "ogre_powers": 1, "transformation": 1},
        
        # Frozen
        "Elsa": {"ice_magic": 1, "snow_creation": 1, "powerful_magic": 1, "winter_control": 1},
        "Anna": {"bravery": 1, "determination": 1},
        "Olaf": {"living_snowman": 1, "detachable_parts": 1},
        
        # Avatar
        "Aang": {"airbending": 1, "waterbending": 1, "earthbending": 1, "firebending": 1, "avatar_state": 1, "flying": 1},
        "Zuko": {"firebending": 1, "sword_user": 1, "lightning_redirection": 1},
        "Katara": {"waterbending": 1, "healing": 1, "bloodbending": 1},
        "Sokka": {"weapon_user": 1, "strategy": 1, "engineering": 1},
        
        # Breaking Bad
        "Walter White": {"chemistry": 1, "super_intelligence": 1, "manipulation": 1},
        "Jesse Pinkman": {"chemistry": 1, "street_smarts": 1},
        "Saul Goodman": {"manipulation": 1, "legal_expertise": 1, "persuasion": 1},
        
        # Stranger Things
        "Eleven": {"telekinesis": 1, "telepathy": 1, "psychic_powers": 1, "dimensional_travel": 1},
        "Mike Wheeler": {"leadership": 1, "strategy": 1},
        "Vecna": {"psychic_powers": 1, "mind_control": 1, "reality_manipulation": 1, "super_strength": 1},
        
        # Game of Thrones
        "Jon Snow": {"sword_user": 1, "leadership": 1, "resurrection": 1, "warging": 1},
        "Daenerys Targaryen": {"dragon_control": 1, "leadership": 1, "fire_immunity": 1},
        "Tyrion Lannister": {"super_intelligence": 1, "strategy": 1, "diplomacy": 1},
        "Arya Stark": {"sword_user": 1, "stealth": 1, "assassination": 1, "face_changing": 1},
        
        # Sonic
        "Sonic the Hedgehog": {"super_speed": 1, "spin_attack": 1, "running": 1},
        "Dr. Eggman": {"super_intelligence": 1, "robotics": 1, "inventions": 1},
        
        # Adventure Games
        "Lara Croft": {"gun_user": 1, "bow_user": 1, "acrobatics": 1, "archaeology": 1, "survival_skills": 1},
        "Nathan Drake": {"gun_user": 1, "climbing": 1, "treasure_hunting": 1, "combat": 1},
        "Joel Miller": {"gun_user": 1, "survival_skills": 1, "stealth": 1, "crafting": 1},
        "Ellie Williams": {"gun_user": 1, "stealth": 1, "immunity": 1, "knife_user": 1},
    }

