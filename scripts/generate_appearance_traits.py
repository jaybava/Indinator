"""Generate appearance/visual traits for all characters."""

def get_appearance_traits():
    """Return appearance traits for each character."""
    return {
        # Harry Potter Universe
        "Harry Potter": {
            "hair_black": 1, "has_glasses": 1, "height_average": 1,
            "distinctive_scar": 1, "wears_robe": 1
        },
        "Hermione Granger": {
            "hair_brown": 1, "height_average": 1, "wears_robe": 1
        },
        "Ron Weasley": {
            "hair_red": 1, "height_tall": 1, "wears_robe": 1
        },
        "Albus Dumbledore": {
            "hair_white": 1, "has_beard": 1, "height_tall": 1, 
            "wears_robe": 1, "has_glasses": 1
        },
        
        # Star Wars
        "Darth Vader": {
            "wears_armor": 1, "has_helmet": 1, "color_black": 1,
            "height_tall": 1, "has_cape": 1, "iconic_mask": 1
        },
        "Luke Skywalker": {
            "hair_blonde": 1, "height_average": 1, "wears_robe": 1,
            "has_lightsaber": 1
        },
        "Princess Leia": {
            "hair_brown": 1, "height_average": 1, "distinctive_hairstyle": 1,
            "wears_dress": 1
        },
        "Han Solo": {
            "hair_brown": 1, "height_tall": 1, "has_vest": 1,
            "has_gun": 1
        },
        
        # Lord of the Rings
        "Frodo Baggins": {
            "hair_brown": 1, "height_short": 1, "has_ring": 1,
            "pointed_ears": 1
        },
        "Gandalf": {
            "hair_white": 1, "has_beard": 1, "height_tall": 1,
            "wears_robe": 1, "has_staff": 1, "has_hat": 1
        },
        "Aragorn": {
            "hair_black": 1, "has_beard": 1, "height_tall": 1,
            "has_sword": 1, "wears_armor": 1
        },
        "Legolas": {
            "hair_blonde": 1, "height_tall": 1, "pointed_ears": 1,
            "has_bow": 1
        },
        "Bilbo Baggins": {
            "hair_brown": 1, "height_short": 1, "has_ring": 1,
            "pointed_ears": 1
        },
        
        # Hunger Games
        "Katniss Everdeen": {
            "hair_black": 1, "height_average": 1, "has_bow": 1,
            "distinctive_braid": 1
        },
        "Peeta Mellark": {
            "hair_blonde": 1, "height_tall": 1
        },
        "President Snow": {
            "hair_white": 1, "has_beard": 1, "height_average": 1,
            "wears_suit": 1
        },
        
        # Detective/Spy
        "Sherlock Holmes": {
            "hair_brown": 1, "height_tall": 1, "wears_coat": 1,
            "has_hat": 1
        },
        "John Watson": {
            "hair_brown": 1, "height_average": 1, "wears_suit": 1
        },
        "James Bond": {
            "hair_brown": 1, "height_tall": 1, "wears_suit": 1,
            "has_gun": 1
        },
        "Indiana Jones": {
            "hair_brown": 1, "height_tall": 1, "has_whip": 1,
            "has_hat": 1, "wears_jacket": 1
        },
        
        # DC Comics
        "Batman": {
            "wears_armor": 1, "has_mask": 1, "color_black": 1,
            "has_cape": 1, "height_tall": 1
        },
        "Superman": {
            "hair_black": 1, "height_tall": 1, "has_cape": 1,
            "color_blue": 1, "color_red": 1, "has_symbol": 1
        },
        "Wonder Woman": {
            "hair_black": 1, "height_tall": 1, "wears_armor": 1,
            "has_sword": 1, "has_shield": 1, "color_red": 1
        },
        "The Joker": {
            "hair_green": 1, "height_tall": 1, "distinctive_face": 1,
            "color_purple": 1, "wears_suit": 1
        },
        "Harley Quinn": {
            "hair_blonde": 1, "hair_colorful": 1, "height_average": 1,
            "color_red": 1, "color_blue": 1
        },
        
        # Marvel
        "Spider-Man": {
            "wears_mask": 1, "color_red": 1, "color_blue": 1,
            "height_average": 1, "has_symbol": 1
        },
        "Iron Man": {
            "wears_armor": 1, "color_red": 1, "color_gold": 1,
            "has_helmet": 1, "height_tall": 1
        },
        "Captain America": {
            "wears_armor": 1, "has_shield": 1, "color_blue": 1,
            "color_red": 1, "has_helmet": 1, "height_tall": 1
        },
        "Hulk": {
            "color_green": 1, "height_tall": 1, "muscular": 1,
            "no_shirt": 1
        },
        "Thor": {
            "hair_blonde": 1, "height_tall": 1, "has_hammer": 1,
            "has_cape": 1, "wears_armor": 1
        },
        "Black Widow": {
            "hair_red": 1, "height_average": 1, "wears_suit": 1,
            "color_black": 1, "has_gun": 1
        },
        "Loki": {
            "hair_black": 1, "height_tall": 1, "has_horned_helmet": 1,
            "wears_armor": 1, "color_green": 1
        },
        "Thanos": {
            "color_purple": 1, "height_tall": 1, "muscular": 1,
            "wears_armor": 1, "has_gauntlet": 1
        },
        
        # Naruto
        "Naruto Uzumaki": {
            "hair_blonde": 1, "height_average": 1, "color_orange": 1,
            "has_headband": 1
        },
        "Sasuke Uchiha": {
            "hair_black": 1, "height_average": 1, "color_blue": 1,
            "has_headband": 1
        },
        "Sakura Haruno": {
            "hair_pink": 1, "height_average": 1, "color_red": 1,
            "has_headband": 1
        },
        "Kakashi Hatake": {
            "hair_white": 1, "height_tall": 1, "has_mask": 1,
            "has_headband": 1
        },
        
        # One Piece
        "Monkey D. Luffy": {
            "hair_black": 1, "height_average": 1, "has_hat": 1,
            "distinctive_scar": 1, "color_red": 1
        },
        "Roronoa Zoro": {
            "hair_green": 1, "height_tall": 1, "has_sword": 1,
            "has_scar": 1, "muscular": 1
        },
        "Nami": {
            "hair_orange": 1, "height_average": 1
        },
        "Sanji": {
            "hair_blonde": 1, "height_tall": 1, "wears_suit": 1
        },
        
        # Death Note
        "Light Yagami": {
            "hair_brown": 1, "height_tall": 1, "wears_suit": 1
        },
        "L Lawliet": {
            "hair_black": 1, "height_tall": 1, "distinctive_eyes": 1,
            "casual_clothes": 1
        },
        
        # Dragon Ball
        "Goku": {
            "hair_black": 1, "height_tall": 1, "muscular": 1,
            "color_orange": 1, "spiky_hair": 1
        },
        "Vegeta": {
            "hair_black": 1, "height_average": 1, "muscular": 1,
            "spiky_hair": 1, "has_armor": 1
        },
        "Piccolo": {
            "color_green": 1, "height_tall": 1, "muscular": 1,
            "pointed_ears": 1, "has_cape": 1
        },
        
        # Pokemon
        "Ash Ketchum": {
            "hair_black": 1, "height_average": 1, "has_hat": 1,
            "color_blue": 1
        },
        "Pikachu": {
            "color_yellow": 1, "height_short": 1, "distinctive_ears": 1,
            "has_tail": 1, "furry": 1
        },
        
        # Nintendo
        "Mario": {
            "hair_brown": 1, "has_mustache": 1, "height_short": 1,
            "color_red": 1, "has_hat": 1
        },
        "Luigi": {
            "hair_brown": 1, "has_mustache": 1, "height_tall": 1,
            "color_green": 1, "has_hat": 1
        },
        "Princess Peach": {
            "hair_blonde": 1, "height_average": 1, "wears_dress": 1,
            "color_pink": 1, "has_crown": 1
        },
        "Bowser": {
            "color_green": 1, "height_tall": 1, "has_shell": 1,
            "has_horns": 1, "has_tail": 1, "muscular": 1
        },
        "Link": {
            "hair_blonde": 1, "height_average": 1, "color_green": 1,
            "has_sword": 1, "has_shield": 1, "has_hat": 1, "pointed_ears": 1
        },
        "Zelda": {
            "hair_blonde": 1, "height_average": 1, "wears_dress": 1,
            "pointed_ears": 1, "has_crown": 1
        },
        "Ganondorf": {
            "hair_red": 1, "height_tall": 1, "muscular": 1,
            "has_armor": 1, "has_sword": 1
        },
        
        # Video Games
        "Kratos": {
            "color_pale": 1, "height_tall": 1, "muscular": 1,
            "has_beard": 1, "distinctive_tattoo": 1, "bald": 1
        },
        "Atreus": {
            "hair_blonde": 1, "height_short": 1, "has_bow": 1
        },
        "Master Chief": {
            "wears_armor": 1, "has_helmet": 1, "color_green": 1,
            "height_tall": 1, "has_gun": 1
        },
        "Cortana": {
            "color_blue": 1, "height_average": 1, "glowing": 1,
            "holographic": 1
        },
        "Geralt of Rivia": {
            "hair_white": 1, "height_tall": 1, "muscular": 1,
            "has_sword": 1, "distinctive_eyes": 1, "has_scar": 1
        },
        "Yennefer": {
            "hair_black": 1, "height_average": 1, "wears_dress": 1
        },
        "Ciri": {
            "hair_white": 1, "height_average": 1, "has_sword": 1,
            "distinctive_scar": 1
        },
        
        # Attack on Titan
        "Eren Yeager": {
            "hair_brown": 1, "height_average": 1, "distinctive_eyes": 1
        },
        "Mikasa Ackerman": {
            "hair_black": 1, "height_average": 1, "has_scarf": 1,
            "has_sword": 1
        },
        "Armin Arlert": {
            "hair_blonde": 1, "height_average": 1
        },
        "Levi Ackerman": {
            "hair_black": 1, "height_short": 1, "has_sword": 1
        },
        
        # Walking Dead
        "Rick Grimes": {
            "hair_brown": 1, "has_beard": 1, "height_tall": 1,
            "has_gun": 1, "wears_uniform": 1
        },
        "Michonne": {
            "hair_black": 1, "height_average": 1, "has_sword": 1
        },
        
        # Simpsons
        "Homer Simpson": {
            "bald": 1, "height_average": 1, "color_yellow": 1,
            "overweight": 1
        },
        "Bart Simpson": {
            "hair_yellow": 1, "height_short": 1, "color_yellow": 1,
            "spiky_hair": 1
        },
        "Lisa Simpson": {
            "hair_yellow": 1, "height_short": 1, "color_yellow": 1,
            "spiky_hair": 1
        },
        
        # SpongeBob
        "SpongeBob SquarePants": {
            "color_yellow": 1, "height_short": 1, "square_shaped": 1,
            "distinctive_eyes": 1
        },
        "Patrick Star": {
            "color_pink": 1, "height_short": 1
        },
        "Squidward Tentacles": {
            "color_teal": 1, "height_average": 1, "distinctive_nose": 1
        },
        
        # Shrek
        "Shrek": {
            "color_green": 1, "height_tall": 1, "muscular": 1,
            "distinctive_ears": 1
        },
        "Donkey": {
            "color_gray": 1, "height_short": 1, "has_tail": 1,
            "four_legs": 1
        },
        "Fiona": {
            "hair_red": 1, "height_average": 1, "color_green": 1
        },
        
        # Frozen
        "Elsa": {
            "hair_blonde": 1, "height_average": 1, "wears_dress": 1,
            "color_blue": 1
        },
        "Anna": {
            "hair_red": 1, "height_average": 1, "wears_dress": 1
        },
        "Olaf": {
            "color_white": 1, "height_short": 1, "distinctive_nose": 1,
            "made_of_snow": 1
        },
        
        # Avatar
        "Aang": {
            "bald": 1, "height_short": 1, "distinctive_tattoo": 1,
            "has_staff": 1, "color_orange": 1
        },
        "Zuko": {
            "hair_black": 1, "height_tall": 1, "has_scar": 1
        },
        "Katara": {
            "hair_brown": 1, "height_average": 1, "color_blue": 1
        },
        "Sokka": {
            "hair_brown": 1, "height_tall": 1, "has_weapon": 1,
            "color_blue": 1
        },
        
        # Breaking Bad
        "Walter White": {
            "bald": 1, "has_goatee": 1, "height_average": 1,
            "has_glasses": 1
        },
        "Jesse Pinkman": {
            "hair_blonde": 1, "height_average": 1, "has_beard": 1
        },
        "Saul Goodman": {
            "hair_brown": 1, "height_average": 1, "wears_suit": 1,
            "colorful_suit": 1
        },
        
        # Stranger Things
        "Eleven": {
            "hair_brown": 1, "height_short": 1, "distinctive_look": 1
        },
        "Mike Wheeler": {
            "hair_black": 1, "height_average": 1
        },
        "Vecna": {
            "color_pale": 1, "height_tall": 1, "distinctive_face": 1,
            "monstrous": 1
        },
        
        # Game of Thrones
        "Jon Snow": {
            "hair_black": 1, "has_beard": 1, "height_tall": 1,
            "has_sword": 1, "wears_fur": 1
        },
        "Daenerys Targaryen": {
            "hair_white": 1, "height_average": 1, "wears_dress": 1
        },
        "Tyrion Lannister": {
            "hair_blonde": 1, "has_beard": 1, "height_short": 1
        },
        "Arya Stark": {
            "hair_brown": 1, "height_short": 1, "has_sword": 1
        },
        
        # Sonic
        "Sonic the Hedgehog": {
            "color_blue": 1, "height_short": 1, "spiky_hair": 1,
            "has_tail": 1, "distinctive_shoes": 1
        },
        "Dr. Eggman": {
            "has_mustache": 1, "bald": 1, "height_average": 1,
            "has_glasses": 1, "color_red": 1, "overweight": 1
        },
        
        # Adventure Games
        "Lara Croft": {
            "hair_brown": 1, "height_average": 1, "has_gun": 1,
            "athletic": 1
        },
        "Nathan Drake": {
            "hair_brown": 1, "height_tall": 1, "has_gun": 1,
            "casual_clothes": 1
        },
        "Joel Miller": {
            "hair_brown": 1, "has_beard": 1, "height_tall": 1,
            "has_gun": 1
        },
        "Ellie Williams": {
            "hair_brown": 1, "height_average": 1, "has_weapon": 1
        },
    }

