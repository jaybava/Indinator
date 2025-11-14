"""Generate franchise/universe traits for all characters."""

def get_franchise_traits():
    """Return franchise traits for each character."""
    return {
        # Harry Potter Universe
        "Harry Potter": {"franchise_harry_potter": 1},
        "Hermione Granger": {"franchise_harry_potter": 1},
        "Ron Weasley": {"franchise_harry_potter": 1},
        "Albus Dumbledore": {"franchise_harry_potter": 1},
        
        # Star Wars
        "Darth Vader": {"franchise_star_wars": 1},
        "Luke Skywalker": {"franchise_star_wars": 1},
        "Princess Leia": {"franchise_star_wars": 1},
        "Han Solo": {"franchise_star_wars": 1},
        
        # Lord of the Rings
        "Frodo Baggins": {"franchise_lotr": 1},
        "Gandalf": {"franchise_lotr": 1},
        "Aragorn": {"franchise_lotr": 1},
        "Legolas": {"franchise_lotr": 1},
        "Bilbo Baggins": {"franchise_lotr": 1},
        
        # Hunger Games
        "Katniss Everdeen": {"franchise_hunger_games": 1},
        "Peeta Mellark": {"franchise_hunger_games": 1},
        "President Snow": {"franchise_hunger_games": 1},
        
        # Detective/Spy
        "Sherlock Holmes": {"franchise_sherlock": 1},
        "John Watson": {"franchise_sherlock": 1},
        "James Bond": {"franchise_james_bond": 1},
        "Indiana Jones": {"franchise_indiana_jones": 1},
        
        # DC Comics
        "Batman": {"franchise_dc": 1},
        "Superman": {"franchise_dc": 1},
        "Wonder Woman": {"franchise_dc": 1},
        "The Joker": {"franchise_dc": 1},
        "Harley Quinn": {"franchise_dc": 1},
        
        # Marvel
        "Spider-Man": {"franchise_marvel": 1},
        "Iron Man": {"franchise_marvel": 1},
        "Captain America": {"franchise_marvel": 1},
        "Hulk": {"franchise_marvel": 1},
        "Thor": {"franchise_marvel": 1},
        "Black Widow": {"franchise_marvel": 1},
        "Loki": {"franchise_marvel": 1},
        "Thanos": {"franchise_marvel": 1},
        
        # Naruto
        "Naruto Uzumaki": {"franchise_naruto": 1, "anime": 1},
        "Sasuke Uchiha": {"franchise_naruto": 1, "anime": 1},
        "Sakura Haruno": {"franchise_naruto": 1, "anime": 1},
        "Kakashi Hatake": {"franchise_naruto": 1, "anime": 1},
        
        # One Piece
        "Monkey D. Luffy": {"franchise_one_piece": 1, "anime": 1},
        "Roronoa Zoro": {"franchise_one_piece": 1, "anime": 1},
        "Nami": {"franchise_one_piece": 1, "anime": 1},
        "Sanji": {"franchise_one_piece": 1, "anime": 1},
        
        # Death Note
        "Light Yagami": {"franchise_death_note": 1, "anime": 1},
        "L Lawliet": {"franchise_death_note": 1, "anime": 1},
        
        # Dragon Ball
        "Goku": {"franchise_dragon_ball": 1, "anime": 1},
        "Vegeta": {"franchise_dragon_ball": 1, "anime": 1},
        "Piccolo": {"franchise_dragon_ball": 1, "anime": 1},
        
        # Pokemon
        "Ash Ketchum": {"franchise_pokemon": 1, "anime": 1},
        "Pikachu": {"franchise_pokemon": 1, "anime": 1},
        
        # Nintendo
        "Mario": {"franchise_mario": 1, "nintendo": 1, "video_game": 1},
        "Luigi": {"franchise_mario": 1, "nintendo": 1, "video_game": 1},
        "Princess Peach": {"franchise_mario": 1, "nintendo": 1, "video_game": 1},
        "Bowser": {"franchise_mario": 1, "nintendo": 1, "video_game": 1},
        "Link": {"franchise_zelda": 1, "nintendo": 1, "video_game": 1},
        "Zelda": {"franchise_zelda": 1, "nintendo": 1, "video_game": 1},
        "Ganondorf": {"franchise_zelda": 1, "nintendo": 1, "video_game": 1},
        
        # Video Games
        "Kratos": {"franchise_god_of_war": 1, "video_game": 1},
        "Atreus": {"franchise_god_of_war": 1, "video_game": 1},
        "Master Chief": {"franchise_halo": 1, "video_game": 1},
        "Cortana": {"franchise_halo": 1, "video_game": 1},
        "Geralt of Rivia": {"franchise_witcher": 1, "video_game": 1},
        "Yennefer": {"franchise_witcher": 1, "video_game": 1},
        "Ciri": {"franchise_witcher": 1, "video_game": 1},
        
        # Attack on Titan
        "Eren Yeager": {"franchise_aot": 1, "anime": 1},
        "Mikasa Ackerman": {"franchise_aot": 1, "anime": 1},
        "Armin Arlert": {"franchise_aot": 1, "anime": 1},
        "Levi Ackerman": {"franchise_aot": 1, "anime": 1},
        
        # Walking Dead
        "Rick Grimes": {"franchise_walking_dead": 1, "tv_show": 1},
        "Michonne": {"franchise_walking_dead": 1, "tv_show": 1},
        
        # Simpsons
        "Homer Simpson": {"franchise_simpsons": 1, "tv_show": 1},
        "Bart Simpson": {"franchise_simpsons": 1, "tv_show": 1},
        "Lisa Simpson": {"franchise_simpsons": 1, "tv_show": 1},
        
        # SpongeBob
        "SpongeBob SquarePants": {"franchise_spongebob": 1, "tv_show": 1},
        "Patrick Star": {"franchise_spongebob": 1, "tv_show": 1},
        "Squidward Tentacles": {"franchise_spongebob": 1, "tv_show": 1},
        
        # Shrek
        "Shrek": {"franchise_shrek": 1, "movie": 1},
        "Donkey": {"franchise_shrek": 1, "movie": 1},
        "Fiona": {"franchise_shrek": 1, "movie": 1},
        
        # Frozen
        "Elsa": {"franchise_frozen": 1, "disney": 1, "movie": 1},
        "Anna": {"franchise_frozen": 1, "disney": 1, "movie": 1},
        "Olaf": {"franchise_frozen": 1, "disney": 1, "movie": 1},
        
        # Avatar
        "Aang": {"franchise_avatar": 1, "tv_show": 1},
        "Zuko": {"franchise_avatar": 1, "tv_show": 1},
        "Katara": {"franchise_avatar": 1, "tv_show": 1},
        "Sokka": {"franchise_avatar": 1, "tv_show": 1},
        
        # Breaking Bad
        "Walter White": {"franchise_breaking_bad": 1, "tv_show": 1},
        "Jesse Pinkman": {"franchise_breaking_bad": 1, "tv_show": 1},
        "Saul Goodman": {"franchise_breaking_bad": 1, "tv_show": 1},
        
        # Stranger Things
        "Eleven": {"franchise_stranger_things": 1, "tv_show": 1},
        "Mike Wheeler": {"franchise_stranger_things": 1, "tv_show": 1},
        "Vecna": {"franchise_stranger_things": 1, "tv_show": 1},
        
        # Game of Thrones
        "Jon Snow": {"franchise_got": 1, "tv_show": 1},
        "Daenerys Targaryen": {"franchise_got": 1, "tv_show": 1},
        "Tyrion Lannister": {"franchise_got": 1, "tv_show": 1},
        "Arya Stark": {"franchise_got": 1, "tv_show": 1},
        
        # Sonic
        "Sonic the Hedgehog": {"franchise_sonic": 1, "video_game": 1},
        "Dr. Eggman": {"franchise_sonic": 1, "video_game": 1},
        
        # Adventure Games
        "Lara Croft": {"franchise_tomb_raider": 1, "video_game": 1},
        "Nathan Drake": {"franchise_uncharted": 1, "video_game": 1},
        "Joel Miller": {"franchise_tlou": 1, "video_game": 1},
        "Ellie Williams": {"franchise_tlou": 1, "video_game": 1},
    }

