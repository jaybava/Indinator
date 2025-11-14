"""Generate role traits for all characters."""

def get_role_traits():
    """Return role traits for each character."""
    return {
        # Harry Potter Universe
        "Harry Potter": {"main_character": 1, "hero": 1, "chosen_one": 1},
        "Hermione Granger": {"sidekick": 1, "support": 1, "best_friend": 1},
        "Ron Weasley": {"sidekick": 1, "support": 1, "best_friend": 1, "comedic_relief": 1},
        "Albus Dumbledore": {"mentor": 1, "leader": 1, "wise": 1},
        
        # Star Wars
        "Darth Vader": {"villain": 1, "antagonist": 1, "anti_hero": 1},
        "Luke Skywalker": {"main_character": 1, "hero": 1, "chosen_one": 1},
        "Princess Leia": {"leader": 1, "support": 1, "hero": 1},
        "Han Solo": {"anti_hero": 1, "support": 1, "rogue": 1},
        
        # Lord of the Rings
        "Frodo Baggins": {"main_character": 1, "hero": 1, "chosen_one": 1},
        "Gandalf": {"mentor": 1, "wise": 1, "leader": 1},
        "Aragorn": {"hero": 1, "leader": 1, "chosen_one": 1},
        "Legolas": {"support": 1, "warrior": 1},
        "Bilbo Baggins": {"main_character": 1, "hero": 1},
        
        # Hunger Games
        "Katniss Everdeen": {"main_character": 1, "hero": 1, "rebel": 1},
        "Peeta Mellark": {"support": 1, "love_interest": 1},
        "President Snow": {"villain": 1, "antagonist": 1, "leader": 1},
        
        # Detective/Spy
        "Sherlock Holmes": {"main_character": 1, "detective": 1, "genius": 1},
        "John Watson": {"sidekick": 1, "support": 1, "narrator": 1},
        "James Bond": {"main_character": 1, "hero": 1, "spy": 1},
        "Indiana Jones": {"main_character": 1, "hero": 1, "adventurer": 1},
        
        # DC Comics
        "Batman": {"main_character": 1, "hero": 1, "vigilante": 1, "leader": 1},
        "Superman": {"main_character": 1, "hero": 1, "leader": 1, "icon": 1},
        "Wonder Woman": {"main_character": 1, "hero": 1, "leader": 1, "warrior": 1},
        "The Joker": {"villain": 1, "antagonist": 1, "chaos_agent": 1},
        "Harley Quinn": {"villain": 1, "anti_hero": 1, "sidekick": 1},
        
        # Marvel
        "Spider-Man": {"main_character": 1, "hero": 1, "friendly_neighborhood": 1},
        "Iron Man": {"main_character": 1, "hero": 1, "leader": 1, "genius": 1},
        "Captain America": {"main_character": 1, "hero": 1, "leader": 1, "icon": 1},
        "Hulk": {"hero": 1, "monster": 1, "anti_hero": 1},
        "Thor": {"main_character": 1, "hero": 1, "royalty": 1},
        "Black Widow": {"hero": 1, "spy": 1, "assassin": 1},
        "Loki": {"villain": 1, "anti_hero": 1, "trickster": 1},
        "Thanos": {"villain": 1, "antagonist": 1, "main_villain": 1},
        
        # Naruto
        "Naruto Uzumaki": {"main_character": 1, "hero": 1, "chosen_one": 1, "underdog": 1},
        "Sasuke Uchiha": {"rival": 1, "anti_hero": 1, "deuteragonist": 1},
        "Sakura Haruno": {"support": 1, "love_interest": 1, "medical": 1},
        "Kakashi Hatake": {"mentor": 1, "leader": 1, "teacher": 1},
        
        # One Piece
        "Monkey D. Luffy": {"main_character": 1, "hero": 1, "captain": 1, "leader": 1},
        "Roronoa Zoro": {"support": 1, "warrior": 1, "right_hand": 1},
        "Nami": {"support": 1, "navigator": 1},
        "Sanji": {"support": 1, "cook": 1, "warrior": 1},
        
        # Death Note
        "Light Yagami": {"main_character": 1, "villain": 1, "anti_hero": 1},
        "L Lawliet": {"deuteragonist": 1, "detective": 1, "rival": 1},
        
        # Dragon Ball
        "Goku": {"main_character": 1, "hero": 1, "warrior": 1},
        "Vegeta": {"rival": 1, "anti_hero": 1, "warrior": 1},
        "Piccolo": {"mentor": 1, "warrior": 1, "anti_hero": 1},
        
        # Pokemon
        "Ash Ketchum": {"main_character": 1, "hero": 1, "trainer": 1},
        "Pikachu": {"sidekick": 1, "mascot": 1, "partner": 1},
        
        # Nintendo
        "Mario": {"main_character": 1, "hero": 1, "icon": 1},
        "Luigi": {"sidekick": 1, "support": 1, "hero": 1},
        "Princess Peach": {"damsel": 1, "royalty": 1},
        "Bowser": {"villain": 1, "antagonist": 1, "recurring_villain": 1},
        "Link": {"main_character": 1, "hero": 1, "chosen_one": 1},
        "Zelda": {"support": 1, "royalty": 1, "wise": 1},
        "Ganondorf": {"villain": 1, "antagonist": 1, "main_villain": 1},
        
        # Video Games
        "Kratos": {"main_character": 1, "anti_hero": 1, "warrior": 1},
        "Atreus": {"support": 1, "son": 1, "sidekick": 1},
        "Master Chief": {"main_character": 1, "hero": 1, "soldier": 1},
        "Cortana": {"support": 1, "ai_companion": 1, "guide": 1},
        "Geralt of Rivia": {"main_character": 1, "anti_hero": 1, "monster_hunter": 1},
        "Yennefer": {"support": 1, "love_interest": 1, "powerful_ally": 1},
        "Ciri": {"deuteragonist": 1, "chosen_one": 1, "support": 1},
        
        # Attack on Titan
        "Eren Yeager": {"main_character": 1, "hero": 1, "anti_hero": 1, "antagonist": 1},
        "Mikasa Ackerman": {"support": 1, "warrior": 1, "protector": 1},
        "Armin Arlert": {"support": 1, "strategist": 1, "best_friend": 1},
        "Levi Ackerman": {"support": 1, "mentor": 1, "strongest_soldier": 1},
        
        # Walking Dead
        "Rick Grimes": {"main_character": 1, "leader": 1, "survivor": 1},
        "Michonne": {"support": 1, "warrior": 1, "survivor": 1},
        
        # Simpsons
        "Homer Simpson": {"main_character": 1, "father": 1, "comedic_character": 1},
        "Bart Simpson": {"troublemaker": 1, "comedic_character": 1, "son": 1},
        "Lisa Simpson": {"support": 1, "voice_of_reason": 1, "daughter": 1},
        
        # SpongeBob
        "SpongeBob SquarePants": {"main_character": 1, "comedic_character": 1, "optimist": 1},
        "Patrick Star": {"sidekick": 1, "comedic_relief": 1, "best_friend": 1},
        "Squidward Tentacles": {"neighbor": 1, "comedic_character": 1, "antagonist": 1},
        
        # Shrek
        "Shrek": {"main_character": 1, "hero": 1, "anti_hero": 1},
        "Donkey": {"sidekick": 1, "comedic_relief": 1, "best_friend": 1},
        "Fiona": {"love_interest": 1, "hero": 1, "royalty": 1},
        
        # Frozen
        "Elsa": {"main_character": 1, "royalty": 1, "misunderstood": 1},
        "Anna": {"main_character": 1, "hero": 1, "royalty": 1},
        "Olaf": {"sidekick": 1, "comedic_relief": 1, "mascot": 1},
        
        # Avatar
        "Aang": {"main_character": 1, "hero": 1, "chosen_one": 1, "avatar": 1},
        "Zuko": {"rival": 1, "anti_hero": 1, "deuteragonist": 1},
        "Katara": {"support": 1, "love_interest": 1, "healer": 1},
        "Sokka": {"support": 1, "strategist": 1, "comedic_relief": 1},
        
        # Breaking Bad
        "Walter White": {"main_character": 1, "villain": 1, "anti_hero": 1, "tragic": 1},
        "Jesse Pinkman": {"deuteragonist": 1, "sidekick": 1, "victim": 1},
        "Saul Goodman": {"support": 1, "comic_relief": 1, "lawyer": 1},
        
        # Stranger Things
        "Eleven": {"main_character": 1, "hero": 1, "chosen_one": 1},
        "Mike Wheeler": {"main_character": 1, "leader": 1, "love_interest": 1},
        "Vecna": {"villain": 1, "antagonist": 1, "main_villain": 1},
        
        # Game of Thrones
        "Jon Snow": {"main_character": 1, "hero": 1, "leader": 1, "chosen_one": 1},
        "Daenerys Targaryen": {"main_character": 1, "hero": 1, "villain": 1, "royalty": 1},
        "Tyrion Lannister": {"support": 1, "advisor": 1, "wit": 1},
        "Arya Stark": {"main_character": 1, "assassin": 1, "avenger": 1},
        
        # Sonic
        "Sonic the Hedgehog": {"main_character": 1, "hero": 1, "icon": 1},
        "Dr. Eggman": {"villain": 1, "antagonist": 1, "recurring_villain": 1},
        
        # Adventure Games
        "Lara Croft": {"main_character": 1, "hero": 1, "adventurer": 1, "icon": 1},
        "Nathan Drake": {"main_character": 1, "hero": 1, "treasure_hunter": 1},
        "Joel Miller": {"main_character": 1, "anti_hero": 1, "survivor": 1},
        "Ellie Williams": {"deuteragonist": 1, "survivor": 1, "chosen_one": 1},
    }

