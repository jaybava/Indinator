"""Generate identity and basic info traits for all characters."""

def get_identity_traits():
    """Return identity traits for each character."""
    return {
        # Harry Potter Universe
        "Harry Potter": {
            "gender_m": 1, "age_young": 1, "species_human": 1, 
            "alignment_good": 1, "origin_earth": 1
        },
        "Hermione Granger": {
            "gender_f": 1, "age_young": 1, "species_human": 1, 
            "alignment_good": 1, "origin_earth": 1
        },
        "Ron Weasley": {
            "gender_m": 1, "age_young": 1, "species_human": 1, 
            "alignment_good": 1, "origin_earth": 1
        },
        "Albus Dumbledore": {
            "gender_m": 1, "age_old": 1, "species_human": 1, 
            "alignment_good": 1, "origin_earth": 1
        },
        
        # Star Wars
        "Darth Vader": {
            "gender_m": 1, "age_adult": 1, "species_human": 1, 
            "alignment_evil": 1, "origin_space": 1
        },
        "Luke Skywalker": {
            "gender_m": 1, "age_young": 1, "species_human": 1, 
            "alignment_good": 1, "origin_space": 1
        },
        "Princess Leia": {
            "gender_f": 1, "age_young": 1, "species_human": 1, 
            "alignment_good": 1, "origin_space": 1
        },
        "Han Solo": {
            "gender_m": 1, "age_adult": 1, "species_human": 1, 
            "alignment_good": 1, "origin_space": 1
        },
        
        # Lord of the Rings
        "Frodo Baggins": {
            "gender_m": 1, "age_young": 1, "species_hobbit": 1, 
            "alignment_good": 1, "origin_fantasy": 1
        },
        "Gandalf": {
            "gender_m": 1, "age_old": 1, "species_wizard": 1, 
            "alignment_good": 1, "origin_fantasy": 1
        },
        "Aragorn": {
            "gender_m": 1, "age_adult": 1, "species_human": 1, 
            "alignment_good": 1, "origin_fantasy": 1
        },
        "Legolas": {
            "gender_m": 1, "age_adult": 1, "species_elf": 1, 
            "alignment_good": 1, "origin_fantasy": 1
        },
        "Bilbo Baggins": {
            "gender_m": 1, "age_old": 1, "species_hobbit": 1, 
            "alignment_good": 1, "origin_fantasy": 1
        },
        
        # Hunger Games
        "Katniss Everdeen": {
            "gender_f": 1, "age_young": 1, "species_human": 1, 
            "alignment_good": 1, "origin_earth": 1
        },
        "Peeta Mellark": {
            "gender_m": 1, "age_young": 1, "species_human": 1, 
            "alignment_good": 1, "origin_earth": 1
        },
        "President Snow": {
            "gender_m": 1, "age_old": 1, "species_human": 1, 
            "alignment_evil": 1, "origin_earth": 1
        },
        
        # Detective/Spy
        "Sherlock Holmes": {
            "gender_m": 1, "age_adult": 1, "species_human": 1, 
            "alignment_good": 1, "origin_earth": 1
        },
        "John Watson": {
            "gender_m": 1, "age_adult": 1, "species_human": 1, 
            "alignment_good": 1, "origin_earth": 1
        },
        "James Bond": {
            "gender_m": 1, "age_adult": 1, "species_human": 1, 
            "alignment_good": 1, "origin_earth": 1
        },
        "Indiana Jones": {
            "gender_m": 1, "age_adult": 1, "species_human": 1, 
            "alignment_good": 1, "origin_earth": 1
        },
        
        # DC Comics
        "Batman": {
            "gender_m": 1, "age_adult": 1, "species_human": 1, 
            "alignment_good": 1, "origin_earth": 1
        },
        "Superman": {
            "gender_m": 1, "age_adult": 1, "species_kryptonian": 1, 
            "alignment_good": 1, "origin_space": 1
        },
        "Wonder Woman": {
            "gender_f": 1, "age_adult": 1, "species_demigod": 1, 
            "alignment_good": 1, "origin_fantasy": 1
        },
        "The Joker": {
            "gender_m": 1, "age_adult": 1, "species_human": 1, 
            "alignment_evil": 1, "origin_earth": 1
        },
        "Harley Quinn": {
            "gender_f": 1, "age_adult": 1, "species_human": 1, 
            "alignment_evil": 1, "origin_earth": 1
        },
        
        # Marvel
        "Spider-Man": {
            "gender_m": 1, "age_young": 1, "species_human": 1, 
            "alignment_good": 1, "origin_earth": 1
        },
        "Iron Man": {
            "gender_m": 1, "age_adult": 1, "species_human": 1, 
            "alignment_good": 1, "origin_earth": 1
        },
        "Captain America": {
            "gender_m": 1, "age_adult": 1, "species_human": 1, 
            "alignment_good": 1, "origin_earth": 1
        },
        "Hulk": {
            "gender_m": 1, "age_adult": 1, "species_human": 1, 
            "alignment_good": 1, "origin_earth": 1
        },
        "Thor": {
            "gender_m": 1, "age_adult": 1, "species_god": 1, 
            "alignment_good": 1, "origin_space": 1
        },
        "Black Widow": {
            "gender_f": 1, "age_adult": 1, "species_human": 1, 
            "alignment_good": 1, "origin_earth": 1
        },
        "Loki": {
            "gender_m": 1, "age_adult": 1, "species_god": 1, 
            "alignment_evil": 1, "origin_space": 1
        },
        "Thanos": {
            "gender_m": 1, "age_adult": 1, "species_titan": 1, 
            "alignment_evil": 1, "origin_space": 1
        },
        
        # Naruto
        "Naruto Uzumaki": {
            "gender_m": 1, "age_young": 1, "species_human": 1, 
            "alignment_good": 1, "origin_earth": 1
        },
        "Sasuke Uchiha": {
            "gender_m": 1, "age_young": 1, "species_human": 1, 
            "alignment_neutral": 1, "origin_earth": 1
        },
        "Sakura Haruno": {
            "gender_f": 1, "age_young": 1, "species_human": 1, 
            "alignment_good": 1, "origin_earth": 1
        },
        "Kakashi Hatake": {
            "gender_m": 1, "age_adult": 1, "species_human": 1, 
            "alignment_good": 1, "origin_earth": 1
        },
        
        # One Piece
        "Monkey D. Luffy": {
            "gender_m": 1, "age_young": 1, "species_human": 1, 
            "alignment_good": 1, "origin_earth": 1
        },
        "Roronoa Zoro": {
            "gender_m": 1, "age_young": 1, "species_human": 1, 
            "alignment_good": 1, "origin_earth": 1
        },
        "Nami": {
            "gender_f": 1, "age_young": 1, "species_human": 1, 
            "alignment_good": 1, "origin_earth": 1
        },
        "Sanji": {
            "gender_m": 1, "age_young": 1, "species_human": 1, 
            "alignment_good": 1, "origin_earth": 1
        },
        
        # Death Note
        "Light Yagami": {
            "gender_m": 1, "age_young": 1, "species_human": 1, 
            "alignment_evil": 1, "origin_earth": 1
        },
        "L Lawliet": {
            "gender_m": 1, "age_young": 1, "species_human": 1, 
            "alignment_good": 1, "origin_earth": 1
        },
        
        # Dragon Ball
        "Goku": {
            "gender_m": 1, "age_adult": 1, "species_saiyan": 1, 
            "alignment_good": 1, "origin_space": 1
        },
        "Vegeta": {
            "gender_m": 1, "age_adult": 1, "species_saiyan": 1, 
            "alignment_neutral": 1, "origin_space": 1
        },
        "Piccolo": {
            "gender_m": 1, "age_adult": 1, "species_namekian": 1, 
            "alignment_good": 1, "origin_space": 1
        },
        
        # Pokemon
        "Ash Ketchum": {
            "gender_m": 1, "age_young": 1, "species_human": 1, 
            "alignment_good": 1, "origin_earth": 1
        },
        "Pikachu": {
            "gender_neutral": 1, "age_young": 1, "species_pokemon": 1, 
            "alignment_good": 1, "origin_earth": 1
        },
        
        # Nintendo
        "Mario": {
            "gender_m": 1, "age_adult": 1, "species_human": 1, 
            "alignment_good": 1, "origin_fantasy": 1
        },
        "Luigi": {
            "gender_m": 1, "age_adult": 1, "species_human": 1, 
            "alignment_good": 1, "origin_fantasy": 1
        },
        "Princess Peach": {
            "gender_f": 1, "age_adult": 1, "species_human": 1, 
            "alignment_good": 1, "origin_fantasy": 1
        },
        "Bowser": {
            "gender_m": 1, "age_adult": 1, "species_koopa": 1, 
            "alignment_evil": 1, "origin_fantasy": 1
        },
        "Link": {
            "gender_m": 1, "age_young": 1, "species_hylian": 1, 
            "alignment_good": 1, "origin_fantasy": 1
        },
        "Zelda": {
            "gender_f": 1, "age_young": 1, "species_hylian": 1, 
            "alignment_good": 1, "origin_fantasy": 1
        },
        "Ganondorf": {
            "gender_m": 1, "age_adult": 1, "species_gerudo": 1, 
            "alignment_evil": 1, "origin_fantasy": 1
        },
        
        # Video Games
        "Kratos": {
            "gender_m": 1, "age_adult": 1, "species_god": 1, 
            "alignment_neutral": 1, "origin_fantasy": 1
        },
        "Atreus": {
            "gender_m": 1, "age_young": 1, "species_demigod": 1, 
            "alignment_good": 1, "origin_fantasy": 1
        },
        "Master Chief": {
            "gender_m": 1, "age_adult": 1, "species_human": 1, 
            "alignment_good": 1, "origin_space": 1
        },
        "Cortana": {
            "gender_f": 1, "age_adult": 1, "species_ai": 1, 
            "alignment_good": 1, "origin_space": 1
        },
        "Geralt of Rivia": {
            "gender_m": 1, "age_adult": 1, "species_witcher": 1, 
            "alignment_good": 1, "origin_fantasy": 1
        },
        "Yennefer": {
            "gender_f": 1, "age_adult": 1, "species_human": 1, 
            "alignment_good": 1, "origin_fantasy": 1
        },
        "Ciri": {
            "gender_f": 1, "age_young": 1, "species_human": 1, 
            "alignment_good": 1, "origin_fantasy": 1
        },
        
        # Attack on Titan
        "Eren Yeager": {
            "gender_m": 1, "age_young": 1, "species_human": 1, 
            "alignment_neutral": 1, "origin_earth": 1
        },
        "Mikasa Ackerman": {
            "gender_f": 1, "age_young": 1, "species_human": 1, 
            "alignment_good": 1, "origin_earth": 1
        },
        "Armin Arlert": {
            "gender_m": 1, "age_young": 1, "species_human": 1, 
            "alignment_good": 1, "origin_earth": 1
        },
        "Levi Ackerman": {
            "gender_m": 1, "age_adult": 1, "species_human": 1, 
            "alignment_good": 1, "origin_earth": 1
        },
        
        # Walking Dead
        "Rick Grimes": {
            "gender_m": 1, "age_adult": 1, "species_human": 1, 
            "alignment_good": 1, "origin_earth": 1
        },
        "Michonne": {
            "gender_f": 1, "age_adult": 1, "species_human": 1, 
            "alignment_good": 1, "origin_earth": 1
        },
        
        # Simpsons
        "Homer Simpson": {
            "gender_m": 1, "age_adult": 1, "species_human": 1, 
            "alignment_neutral": 1, "origin_earth": 1
        },
        "Bart Simpson": {
            "gender_m": 1, "age_young": 1, "species_human": 1, 
            "alignment_neutral": 1, "origin_earth": 1
        },
        "Lisa Simpson": {
            "gender_f": 1, "age_young": 1, "species_human": 1, 
            "alignment_good": 1, "origin_earth": 1
        },
        
        # SpongeBob
        "SpongeBob SquarePants": {
            "gender_m": 1, "age_adult": 1, "species_sponge": 1, 
            "alignment_good": 1, "origin_fantasy": 1
        },
        "Patrick Star": {
            "gender_m": 1, "age_adult": 1, "species_starfish": 1, 
            "alignment_good": 1, "origin_fantasy": 1
        },
        "Squidward Tentacles": {
            "gender_m": 1, "age_adult": 1, "species_octopus": 1, 
            "alignment_neutral": 1, "origin_fantasy": 1
        },
        
        # Shrek
        "Shrek": {
            "gender_m": 1, "age_adult": 1, "species_ogre": 1, 
            "alignment_good": 1, "origin_fantasy": 1
        },
        "Donkey": {
            "gender_m": 1, "age_adult": 1, "species_donkey": 1, 
            "alignment_good": 1, "origin_fantasy": 1
        },
        "Fiona": {
            "gender_f": 1, "age_adult": 1, "species_ogre": 1, 
            "alignment_good": 1, "origin_fantasy": 1
        },
        
        # Frozen
        "Elsa": {
            "gender_f": 1, "age_adult": 1, "species_human": 1, 
            "alignment_good": 1, "origin_fantasy": 1
        },
        "Anna": {
            "gender_f": 1, "age_young": 1, "species_human": 1, 
            "alignment_good": 1, "origin_fantasy": 1
        },
        "Olaf": {
            "gender_m": 1, "age_young": 1, "species_snowman": 1, 
            "alignment_good": 1, "origin_fantasy": 1
        },
        
        # Avatar
        "Aang": {
            "gender_m": 1, "age_young": 1, "species_human": 1, 
            "alignment_good": 1, "origin_fantasy": 1
        },
        "Zuko": {
            "gender_m": 1, "age_young": 1, "species_human": 1, 
            "alignment_good": 1, "origin_fantasy": 1
        },
        "Katara": {
            "gender_f": 1, "age_young": 1, "species_human": 1, 
            "alignment_good": 1, "origin_fantasy": 1
        },
        "Sokka": {
            "gender_m": 1, "age_young": 1, "species_human": 1, 
            "alignment_good": 1, "origin_fantasy": 1
        },
        
        # Breaking Bad
        "Walter White": {
            "gender_m": 1, "age_adult": 1, "species_human": 1, 
            "alignment_evil": 1, "origin_earth": 1
        },
        "Jesse Pinkman": {
            "gender_m": 1, "age_young": 1, "species_human": 1, 
            "alignment_neutral": 1, "origin_earth": 1
        },
        "Saul Goodman": {
            "gender_m": 1, "age_adult": 1, "species_human": 1, 
            "alignment_neutral": 1, "origin_earth": 1
        },
        
        # Stranger Things
        "Eleven": {
            "gender_f": 1, "age_young": 1, "species_human": 1, 
            "alignment_good": 1, "origin_earth": 1
        },
        "Mike Wheeler": {
            "gender_m": 1, "age_young": 1, "species_human": 1, 
            "alignment_good": 1, "origin_earth": 1
        },
        "Vecna": {
            "gender_m": 1, "age_adult": 1, "species_monster": 1, 
            "alignment_evil": 1, "origin_fantasy": 1
        },
        
        # Game of Thrones
        "Jon Snow": {
            "gender_m": 1, "age_adult": 1, "species_human": 1, 
            "alignment_good": 1, "origin_fantasy": 1
        },
        "Daenerys Targaryen": {
            "gender_f": 1, "age_adult": 1, "species_human": 1, 
            "alignment_neutral": 1, "origin_fantasy": 1
        },
        "Tyrion Lannister": {
            "gender_m": 1, "age_adult": 1, "species_human": 1, 
            "alignment_good": 1, "origin_fantasy": 1
        },
        "Arya Stark": {
            "gender_f": 1, "age_young": 1, "species_human": 1, 
            "alignment_good": 1, "origin_fantasy": 1
        },
        
        # Sonic
        "Sonic the Hedgehog": {
            "gender_m": 1, "age_young": 1, "species_hedgehog": 1, 
            "alignment_good": 1, "origin_fantasy": 1
        },
        "Dr. Eggman": {
            "gender_m": 1, "age_adult": 1, "species_human": 1, 
            "alignment_evil": 1, "origin_fantasy": 1
        },
        
        # Adventure Games
        "Lara Croft": {
            "gender_f": 1, "age_adult": 1, "species_human": 1, 
            "alignment_good": 1, "origin_earth": 1
        },
        "Nathan Drake": {
            "gender_m": 1, "age_adult": 1, "species_human": 1, 
            "alignment_good": 1, "origin_earth": 1
        },
        "Joel Miller": {
            "gender_m": 1, "age_adult": 1, "species_human": 1, 
            "alignment_good": 1, "origin_earth": 1
        },
        "Ellie Williams": {
            "gender_f": 1, "age_young": 1, "species_human": 1, 
            "alignment_good": 1, "origin_earth": 1
        },
    }

