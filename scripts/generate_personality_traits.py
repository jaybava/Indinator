"""Generate personality traits for all characters."""

def get_personality_traits():
    """Return personality traits for each character."""
    return {
        # Harry Potter Universe
        "Harry Potter": {"brave": 1, "loyal": 1, "determined": 1, "selfless": 1},
        "Hermione Granger": {"intelligent": 1, "logical": 1, "perfectionist": 1, "loyal": 1},
        "Ron Weasley": {"loyal": 1, "funny": 1, "insecure": 1, "brave": 1},
        "Albus Dumbledore": {"wise": 1, "calm": 1, "mysterious": 1, "caring": 1},
        
        # Star Wars
        "Darth Vader": {"intimidating": 1, "powerful": 1, "tragic": 1, "conflicted": 1},
        "Luke Skywalker": {"brave": 1, "optimistic": 1, "determined": 1, "compassionate": 1},
        "Princess Leia": {"brave": 1, "strong_willed": 1, "intelligent": 1, "sarcastic": 1},
        "Han Solo": {"cocky": 1, "charismatic": 1, "brave": 1, "sarcastic": 1},
        
        # Lord of the Rings
        "Frodo Baggins": {"brave": 1, "humble": 1, "determined": 1, "burdened": 1},
        "Gandalf": {"wise": 1, "powerful": 1, "caring": 1, "mysterious": 1},
        "Aragorn": {"noble": 1, "brave": 1, "humble": 1, "wise": 1},
        "Legolas": {"calm": 1, "skilled": 1, "elegant": 1, "loyal": 1},
        "Bilbo Baggins": {"adventurous": 1, "clever": 1, "kind": 1},
        
        # Hunger Games
        "Katniss Everdeen": {"brave": 1, "independent": 1, "protective": 1, "stubborn": 1},
        "Peeta Mellark": {"kind": 1, "loyal": 1, "artistic": 1, "selfless": 1},
        "President Snow": {"evil": 1, "manipulative": 1, "cruel": 1, "calculating": 1},
        
        # Detective/Spy
        "Sherlock Holmes": {"intelligent": 1, "arrogant": 1, "observant": 1, "antisocial": 1},
        "John Watson": {"loyal": 1, "brave": 1, "practical": 1, "caring": 1},
        "James Bond": {"charming": 1, "confident": 1, "suave": 1, "ruthless": 1},
        "Indiana Jones": {"brave": 1, "adventurous": 1, "charming": 1, "sarcastic": 1},
        
        # DC Comics
        "Batman": {"serious": 1, "determined": 1, "brooding": 1, "intelligent": 1, "traumatized": 1},
        "Superman": {"heroic": 1, "compassionate": 1, "optimistic": 1, "selfless": 1},
        "Wonder Woman": {"brave": 1, "compassionate": 1, "strong_willed": 1, "noble": 1},
        "The Joker": {"chaotic": 1, "insane": 1, "unpredictable": 1, "sadistic": 1},
        "Harley Quinn": {"chaotic": 1, "fun_loving": 1, "unpredictable": 1, "loyal": 1},
        
        # Marvel
        "Spider-Man": {"funny": 1, "responsible": 1, "caring": 1, "anxious": 1},
        "Iron Man": {"arrogant": 1, "intelligent": 1, "sarcastic": 1, "heroic": 1},
        "Captain America": {"honorable": 1, "brave": 1, "moral": 1, "determined": 1},
        "Hulk": {"angry": 1, "powerful": 1, "misunderstood": 1, "gentle": 1},
        "Thor": {"brave": 1, "noble": 1, "arrogant": 1, "loyal": 1},
        "Black Widow": {"skilled": 1, "secretive": 1, "loyal": 1, "traumatized": 1},
        "Loki": {"cunning": 1, "mischievous": 1, "complex": 1, "jealous": 1},
        "Thanos": {"determined": 1, "ruthless": 1, "philosophical": 1, "powerful": 1},
        
        # Naruto
        "Naruto Uzumaki": {"determined": 1, "optimistic": 1, "loyal": 1, "impulsive": 1},
        "Sasuke Uchiha": {"cold": 1, "determined": 1, "vengeful": 1, "talented": 1},
        "Sakura Haruno": {"caring": 1, "emotional": 1, "determined": 1, "strong_willed": 1},
        "Kakashi Hatake": {"calm": 1, "mysterious": 1, "caring": 1, "lazy": 1},
        
        # One Piece
        "Monkey D. Luffy": {"carefree": 1, "determined": 1, "loyal": 1, "simple_minded": 1},
        "Roronoa Zoro": {"serious": 1, "loyal": 1, "determined": 1, "directionally_challenged": 1},
        "Nami": {"greedy": 1, "intelligent": 1, "caring": 1, "emotional": 1},
        "Sanji": {"chivalrous": 1, "passionate": 1, "romantic": 1, "skilled": 1},
        
        # Death Note
        "Light Yagami": {"intelligent": 1, "manipulative": 1, "arrogant": 1, "ruthless": 1},
        "L Lawliet": {"intelligent": 1, "eccentric": 1, "obsessive": 1, "mysterious": 1},
        
        # Dragon Ball
        "Goku": {"naive": 1, "kind": 1, "determined": 1, "battle_loving": 1},
        "Vegeta": {"proud": 1, "determined": 1, "arrogant": 1, "competitive": 1},
        "Piccolo": {"serious": 1, "wise": 1, "calm": 1, "protective": 1},
        
        # Pokemon
        "Ash Ketchum": {"determined": 1, "optimistic": 1, "brave": 1, "naive": 1},
        "Pikachu": {"loyal": 1, "brave": 1, "energetic": 1, "cute": 1},
        
        # Nintendo
        "Mario": {"brave": 1, "cheerful": 1, "heroic": 1, "determined": 1},
        "Luigi": {"brave": 1, "timid": 1, "loyal": 1, "kind": 1},
        "Princess Peach": {"kind": 1, "gentle": 1, "elegant": 1},
        "Bowser": {"evil": 1, "powerful": 1, "persistent": 1, "comedic": 1},
        "Link": {"brave": 1, "silent": 1, "heroic": 1, "determined": 1},
        "Zelda": {"wise": 1, "kind": 1, "brave": 1, "intelligent": 1},
        "Ganondorf": {"evil": 1, "powerful": 1, "ambitious": 1, "cruel": 1},
        
        # Video Games
        "Kratos": {"angry": 1, "powerful": 1, "determined": 1, "protective": 1},
        "Atreus": {"curious": 1, "brave": 1, "impulsive": 1, "caring": 1},
        "Master Chief": {"stoic": 1, "brave": 1, "determined": 1, "loyal": 1},
        "Cortana": {"intelligent": 1, "caring": 1, "witty": 1, "loyal": 1},
        "Geralt of Rivia": {"stoic": 1, "sarcastic": 1, "skilled": 1, "moral": 1},
        "Yennefer": {"strong_willed": 1, "proud": 1, "caring": 1, "ambitious": 1},
        "Ciri": {"brave": 1, "determined": 1, "caring": 1, "powerful": 1},
        
        # Attack on Titan
        "Eren Yeager": {"determined": 1, "angry": 1, "traumatized": 1, "ruthless": 1},
        "Mikasa Ackerman": {"calm": 1, "protective": 1, "loyal": 1, "skilled": 1},
        "Armin Arlert": {"intelligent": 1, "timid": 1, "strategic": 1, "loyal": 1},
        "Levi Ackerman": {"stoic": 1, "skilled": 1, "clean_freak": 1, "caring": 1},
        
        # Walking Dead
        "Rick Grimes": {"determined": 1, "protective": 1, "traumatized": 1, "ruthless": 1},
        "Michonne": {"strong": 1, "independent": 1, "protective": 1, "traumatized": 1},
        
        # Simpsons
        "Homer Simpson": {"lazy": 1, "funny": 1, "foolish": 1, "loving": 1},
        "Bart Simpson": {"mischievous": 1, "rebellious": 1, "funny": 1, "troublemaker": 1},
        "Lisa Simpson": {"intelligent": 1, "caring": 1, "moral": 1, "mature": 1},
        
        # SpongeBob
        "SpongeBob SquarePants": {"optimistic": 1, "cheerful": 1, "naive": 1, "hardworking": 1},
        "Patrick Star": {"dumb": 1, "funny": 1, "loyal": 1, "lazy": 1},
        "Squidward Tentacles": {"grumpy": 1, "sarcastic": 1, "artistic": 1, "miserable": 1},
        
        # Shrek
        "Shrek": {"grumpy": 1, "kind_hearted": 1, "misunderstood": 1, "loyal": 1},
        "Donkey": {"talkative": 1, "funny": 1, "loyal": 1, "optimistic": 1},
        "Fiona": {"strong": 1, "kind": 1, "independent": 1, "misunderstood": 1},
        
        # Frozen
        "Elsa": {"fearful": 1, "powerful": 1, "protective": 1, "isolated": 1},
        "Anna": {"optimistic": 1, "brave": 1, "impulsive": 1, "loving": 1},
        "Olaf": {"cheerful": 1, "naive": 1, "funny": 1, "innocent": 1},
        
        # Avatar
        "Aang": {"fun_loving": 1, "peaceful": 1, "brave": 1, "caring": 1},
        "Zuko": {"conflicted": 1, "determined": 1, "honorable": 1, "angry": 1},
        "Katara": {"caring": 1, "strong_willed": 1, "motherly": 1, "determined": 1},
        "Sokka": {"funny": 1, "strategic": 1, "brave": 1, "sarcastic": 1},
        
        # Breaking Bad
        "Walter White": {"intelligent": 1, "prideful": 1, "ruthless": 1, "manipulative": 1},
        "Jesse Pinkman": {"emotional": 1, "loyal": 1, "traumatized": 1, "moral": 1},
        "Saul Goodman": {"funny": 1, "cunning": 1, "cowardly": 1, "clever": 1},
        
        # Stranger Things
        "Eleven": {"powerful": 1, "loyal": 1, "brave": 1, "traumatized": 1},
        "Mike Wheeler": {"loyal": 1, "brave": 1, "caring": 1, "determined": 1},
        "Vecna": {"evil": 1, "powerful": 1, "vengeful": 1, "sadistic": 1},
        
        # Game of Thrones
        "Jon Snow": {"honorable": 1, "brave": 1, "conflicted": 1, "brooding": 1},
        "Daenerys Targaryen": {"powerful": 1, "determined": 1, "ruthless": 1, "compassionate": 1},
        "Tyrion Lannister": {"intelligent": 1, "witty": 1, "cynical": 1, "caring": 1},
        "Arya Stark": {"determined": 1, "vengeful": 1, "skilled": 1, "brave": 1},
        
        # Sonic
        "Sonic the Hedgehog": {"cocky": 1, "brave": 1, "fast": 1, "carefree": 1},
        "Dr. Eggman": {"evil": 1, "intelligent": 1, "arrogant": 1, "persistent": 1},
        
        # Adventure Games
        "Lara Croft": {"brave": 1, "intelligent": 1, "determined": 1, "independent": 1},
        "Nathan Drake": {"charming": 1, "funny": 1, "brave": 1, "adventurous": 1},
        "Joel Miller": {"protective": 1, "traumatized": 1, "ruthless": 1, "caring": 1},
        "Ellie Williams": {"brave": 1, "funny": 1, "determined": 1, "traumatized": 1},
    }

