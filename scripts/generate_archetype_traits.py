"""Generate archetype/occupation traits for all characters."""

def get_archetype_traits():
    """Return archetype traits for each character."""
    return {
        # Harry Potter Universe
        "Harry Potter": {"wizard": 1, "student": 1},
        "Hermione Granger": {"wizard": 1, "student": 1, "scholar": 1},
        "Ron Weasley": {"wizard": 1, "student": 1},
        "Albus Dumbledore": {"wizard": 1, "teacher": 1, "headmaster": 1},
        
        # Star Wars
        "Darth Vader": {"warrior": 1, "sith_lord": 1, "commander": 1},
        "Luke Skywalker": {"warrior": 1, "jedi": 1, "farmer": 1},
        "Princess Leia": {"royalty": 1, "diplomat": 1, "rebel_leader": 1},
        "Han Solo": {"smuggler": 1, "pilot": 1, "scoundrel": 1},
        
        # Lord of the Rings
        "Frodo Baggins": {"explorer": 1, "ring_bearer": 1},
        "Gandalf": {"wizard": 1, "mentor": 1, "wanderer": 1},
        "Aragorn": {"warrior": 1, "ranger": 1, "king": 1},
        "Legolas": {"archer": 1, "warrior": 1, "prince": 1},
        "Bilbo Baggins": {"explorer": 1, "burglar": 1},
        
        # Hunger Games
        "Katniss Everdeen": {"archer": 1, "hunter": 1, "rebel": 1},
        "Peeta Mellark": {"baker": 1, "artist": 1},
        "President Snow": {"politician": 1, "dictator": 1},
        
        # Detective/Spy
        "Sherlock Holmes": {"detective": 1, "consultant": 1, "genius": 1},
        "John Watson": {"doctor": 1, "soldier": 1, "companion": 1},
        "James Bond": {"spy": 1, "assassin": 1, "agent": 1},
        "Indiana Jones": {"archaeologist": 1, "professor": 1, "adventurer": 1},
        
        # DC Comics
        "Batman": {"vigilante": 1, "detective": 1, "billionaire": 1},
        "Superman": {"superhero": 1, "journalist": 1, "alien": 1},
        "Wonder Woman": {"warrior": 1, "superhero": 1, "ambassador": 1, "princess": 1},
        "The Joker": {"criminal": 1, "terrorist": 1, "clown": 1},
        "Harley Quinn": {"criminal": 1, "psychiatrist": 1, "jester": 1},
        
        # Marvel
        "Spider-Man": {"superhero": 1, "student": 1, "photographer": 1},
        "Iron Man": {"superhero": 1, "billionaire": 1, "inventor": 1, "engineer": 1},
        "Captain America": {"superhero": 1, "soldier": 1, "leader": 1},
        "Hulk": {"scientist": 1, "monster": 1, "superhero": 1},
        "Thor": {"god": 1, "warrior": 1, "prince": 1, "superhero": 1},
        "Black Widow": {"spy": 1, "assassin": 1, "agent": 1, "superhero": 1},
        "Loki": {"god": 1, "trickster": 1, "sorcerer": 1, "prince": 1},
        "Thanos": {"warlord": 1, "conqueror": 1, "titan": 1},
        
        # Naruto
        "Naruto Uzumaki": {"ninja": 1, "student": 1, "hokage": 1},
        "Sasuke Uchiha": {"ninja": 1, "avenger": 1, "rogue": 1},
        "Sakura Haruno": {"ninja": 1, "medic": 1, "student": 1},
        "Kakashi Hatake": {"ninja": 1, "teacher": 1, "commander": 1},
        
        # One Piece
        "Monkey D. Luffy": {"pirate": 1, "captain": 1, "fighter": 1},
        "Roronoa Zoro": {"pirate": 1, "swordsman": 1, "warrior": 1},
        "Nami": {"pirate": 1, "navigator": 1, "thief": 1},
        "Sanji": {"pirate": 1, "cook": 1, "fighter": 1},
        
        # Death Note
        "Light Yagami": {"student": 1, "serial_killer": 1, "god_complex": 1},
        "L Lawliet": {"detective": 1, "genius": 1, "investigator": 1},
        
        # Dragon Ball
        "Goku": {"martial_artist": 1, "warrior": 1, "protector": 1},
        "Vegeta": {"martial_artist": 1, "warrior": 1, "prince": 1},
        "Piccolo": {"martial_artist": 1, "warrior": 1, "mentor": 1},
        
        # Pokemon
        "Ash Ketchum": {"trainer": 1, "adventurer": 1},
        "Pikachu": {"pokemon": 1, "companion": 1},
        
        # Nintendo
        "Mario": {"plumber": 1, "hero": 1, "athlete": 1},
        "Luigi": {"plumber": 1, "hero": 1},
        "Princess Peach": {"royalty": 1, "ruler": 1},
        "Bowser": {"king": 1, "villain": 1, "monster": 1},
        "Link": {"warrior": 1, "hero": 1, "knight": 1},
        "Zelda": {"royalty": 1, "princess": 1, "sage": 1},
        "Ganondorf": {"king": 1, "sorcerer": 1, "warlord": 1},
        
        # Video Games
        "Kratos": {"warrior": 1, "god": 1, "slayer": 1},
        "Atreus": {"warrior": 1, "archer": 1, "god": 1},
        "Master Chief": {"soldier": 1, "super_soldier": 1, "warrior": 1},
        "Cortana": {"ai": 1, "companion": 1, "hacker": 1},
        "Geralt of Rivia": {"witcher": 1, "monster_hunter": 1, "mercenary": 1},
        "Yennefer": {"sorceress": 1, "advisor": 1},
        "Ciri": {"warrior": 1, "princess": 1, "witcher": 1},
        
        # Attack on Titan
        "Eren Yeager": {"soldier": 1, "titan_shifter": 1, "warrior": 1},
        "Mikasa Ackerman": {"soldier": 1, "warrior": 1, "bodyguard": 1},
        "Armin Arlert": {"soldier": 1, "strategist": 1, "titan_shifter": 1},
        "Levi Ackerman": {"soldier": 1, "captain": 1, "warrior": 1},
        
        # Walking Dead
        "Rick Grimes": {"sheriff": 1, "leader": 1, "survivor": 1},
        "Michonne": {"warrior": 1, "survivor": 1, "lawyer": 1},
        
        # Simpsons
        "Homer Simpson": {"nuclear_technician": 1, "father": 1, "everyman": 1},
        "Bart Simpson": {"student": 1, "troublemaker": 1, "prankster": 1},
        "Lisa Simpson": {"student": 1, "musician": 1, "activist": 1},
        
        # SpongeBob
        "SpongeBob SquarePants": {"fry_cook": 1, "optimist": 1, "friend": 1},
        "Patrick Star": {"unemployed": 1, "friend": 1, "starfish": 1},
        "Squidward Tentacles": {"cashier": 1, "artist": 1, "musician": 1},
        
        # Shrek
        "Shrek": {"ogre": 1, "hermit": 1, "hero": 1},
        "Donkey": {"companion": 1, "friend": 1, "comic_relief": 1},
        "Fiona": {"princess": 1, "warrior": 1, "ogre": 1},
        
        # Frozen
        "Elsa": {"queen": 1, "sorceress": 1, "royalty": 1},
        "Anna": {"princess": 1, "adventurer": 1, "royalty": 1},
        "Olaf": {"snowman": 1, "companion": 1, "comic_relief": 1},
        
        # Avatar
        "Aang": {"monk": 1, "avatar": 1, "peacekeeper": 1},
        "Zuko": {"prince": 1, "warrior": 1, "firebender": 1},
        "Katara": {"warrior": 1, "healer": 1, "waterbender": 1},
        "Sokka": {"warrior": 1, "strategist": 1, "engineer": 1},
        
        # Breaking Bad
        "Walter White": {"teacher": 1, "chemist": 1, "drug_lord": 1},
        "Jesse Pinkman": {"drug_dealer": 1, "chemist": 1, "dropout": 1},
        "Saul Goodman": {"lawyer": 1, "con_artist": 1, "fixer": 1},
        
        # Stranger Things
        "Eleven": {"experiment": 1, "psychic": 1, "hero": 1},
        "Mike Wheeler": {"student": 1, "friend": 1, "leader": 1},
        "Vecna": {"monster": 1, "villain": 1, "psychic": 1},
        
        # Game of Thrones
        "Jon Snow": {"warrior": 1, "leader": 1, "bastard": 1, "king": 1},
        "Daenerys Targaryen": {"queen": 1, "conqueror": 1, "dragonrider": 1},
        "Tyrion Lannister": {"nobleman": 1, "politician": 1, "strategist": 1},
        "Arya Stark": {"assassin": 1, "warrior": 1, "survivor": 1},
        
        # Sonic
        "Sonic the Hedgehog": {"hero": 1, "speedster": 1, "adventurer": 1},
        "Dr. Eggman": {"scientist": 1, "inventor": 1, "villain": 1},
        
        # Adventure Games
        "Lara Croft": {"archaeologist": 1, "explorer": 1, "adventurer": 1},
        "Nathan Drake": {"treasure_hunter": 1, "explorer": 1, "thief": 1},
        "Joel Miller": {"smuggler": 1, "survivor": 1, "protector": 1},
        "Ellie Williams": {"survivor": 1, "fighter": 1, "immune": 1},
    }

