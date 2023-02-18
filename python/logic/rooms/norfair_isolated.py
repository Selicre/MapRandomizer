from logic.areas import Area, SubArea
from maze_builder.types import Room
from maze_builder.types import Room, DoorIdentifier, Direction, DoorSubtype

LEFT = Direction.LEFT
RIGHT = Direction.RIGHT
UP = Direction.UP
DOWN = Direction.DOWN
ELEVATOR = DoorSubtype.ELEVATOR

rooms = [
    Room(
        name='Business Center',
        rom_address=0x7A7DE,
        map=[
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
        ],
        door_ids=[
            DoorIdentifier(LEFT, 0, 3, 0x192BE, 0x1932A),  # Ice Beam Gate Room
            DoorIdentifier(LEFT, 0, 4, 0x19306, 0x197C2),  # Norfair Map Room
            DoorIdentifier(LEFT, 0, 5, 0x192D6, 0x1941A),  # Hi Jump Energy Tank Room
            DoorIdentifier(RIGHT, 0, 3, 0x192CA, 0x192A6),  # Cathedral Entrance
            DoorIdentifier(RIGHT, 0, 5, 0x192FA, 0x19816),  # Frog Savestation
            DoorIdentifier(RIGHT, 0, 6, 0x192E2, 0x19402),  # Crocomire Escape
        ],
    ),
    Room(
        name='Norfair Map Room',
        rom_address=0x7B0B4,
        map=[[1]],
        door_ids=[
            DoorIdentifier(RIGHT, 0, 0, 0x197C2, 0x19306),  # Business Center
        ],
    ),
    Room(
        name='Hi Jump Energy Tank Room',
        rom_address=0x7AA41,
        map=[
            [1, 1],
            [1, 0],
        ],
        door_ids=[
            DoorIdentifier(LEFT, 0, 1, 0x19426, 0x193F6),  # Hi Jump Boots Room
            DoorIdentifier(RIGHT, 1, 0, 0x1941A, 0x192D6),  # Business Center
        ],
    ),
    Room(
        name='Hi Jump Boots Room',
        rom_address=0x7A9E5,
        map=[[1]],
        door_ids=[
            DoorIdentifier(RIGHT, 0, 0, 0x193F6, 0x19426),  # Hi Jump Energy Tank Room
        ],
    ),
    Room(
        name='Cathedral Entrance',
        rom_address=0x7A7B3,
        map=[
            [1, 1, 1],
            [1, 1, 1],
        ],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x192A6, 0x192CA),  # Business Center
            DoorIdentifier(RIGHT, 2, 0, 0x192B2, 0x1928E),  # Cathedral
        ],
    ),
    Room(
        name='Cathedral',
        rom_address=0x7A788,
        map=[
            [1, 1, 1],
            [1, 1, 1],
        ],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x1928E, 0x192B2),  # Cathedral Entrance
            DoorIdentifier(RIGHT, 2, 1, 0x1929A, 0x19732),  # Rising Tide
        ],
    ),
    Room(
        name='Rising Tide',
        rom_address=0x7AFA3,
        map=[[1, 1, 1, 1, 1]],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x19732, 0x1929A),  # Cathedral
            DoorIdentifier(RIGHT, 4, 0, 0x1973E, 0x1955E),  # Bubble Mountain
        ],
    ),
    Room(
        name='Frog Speedway',
        rom_address=0x7B106,
        map=[[1, 1, 1, 1, 1, 1, 1, 1]],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x197DA, 0x1980A),  # Frog Savestation
            DoorIdentifier(RIGHT, 7, 0, 0x197E6, 0x1970E),  # Upper Norfair Farming Room
        ],
    ),
    Room(
        name='Upper Norfair Farming Room',
        rom_address=0x7AF72,
        map=[
            [1, 1],
            [1, 1],
        ],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x1970E, 0x197E6),  # Frog Speedway
            DoorIdentifier(LEFT, 0, 1, 0x19726, 0x197F2),  # Red Pirate Shaft
            DoorIdentifier(RIGHT, 1, 0, 0x1971A, 0x1956A),  # Bubble Mountain
        ],
    ),
    Room(
        name='Purple Shaft',
        rom_address=0x7AEDF,
        map=[
            [1],
            [1],
            [1],
        ],
        door_ids=[
            DoorIdentifier(RIGHT, 0, 1, 0x196C6, 0x1979E),  # Purple Farming Room
            # TODO: fix the name of this door in sm-json-data:
            DoorIdentifier(RIGHT, 0, 2, 0x196BA, 0x19696),  # Magdollite Tunnel
            DoorIdentifier(UP, 0, 0, 0x196AE, 0x19576),  # Bubble Mountain
        ],
    ),
    Room(
        name='Purple Farming Room',
        rom_address=0x7B051,
        map=[[1]],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x1979E, 0x196C6),  # Purple Shaft
        ],
    ),
    Room(
        name='Frog Savestation',
        rom_address=0x7B167,
        map=[[1]],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x19816, 0x192FA),  # Business Center
            DoorIdentifier(RIGHT, 0, 0, 0x1980A, 0x197DA),  # Frog Speedway
        ],
    ),
    Room(
        name='Bubble Mountain',
        rom_address=0x7ACB3,
        map=[
            [1, 1],
            [1, 1],
            [1, 1],
            [1, 1],
        ],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x19552, 0x1953A),  # Green Bubbles Missile Room
            DoorIdentifier(LEFT, 0, 1, 0x1959A, 0x197CE),  # Bubble Mountain Save Room
            DoorIdentifier(LEFT, 0, 2, 0x1955E, 0x1973E),  # Rising Tide
            DoorIdentifier(LEFT, 0, 3, 0x1956A, 0x1971A),  # Upper Norfair Farming Room
            DoorIdentifier(RIGHT, 1, 0, 0x1958E, 0x197AA),  # Bat Cave
            DoorIdentifier(RIGHT, 1, 1, 0x19582, 0x195CA),  # Single Chamber
            DoorIdentifier(DOWN, 0, 3, 0x19576, 0x196AE),  # Purple Shaft
        ],
    ),
    Room(
        name='Bubble Mountain Save Room',
        rom_address=0x7B0DD,
        map=[[1]],
        door_ids=[
            DoorIdentifier(RIGHT, 0, 0, 0x197CE, 0x1959A),  # Bubble Mountain
        ],
    ),
    Room(
        name='Green Bubbles Missile Room',
        rom_address=0x7AC83,
        map=[[1, 1]],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x19546, 0x1952E),  # Norfair Reserve Tank Room
            DoorIdentifier(RIGHT, 1, 0, 0x1953A, 0x19552),  # Bubble Mountain
        ],
    ),
    Room(
        name='Norfair Reserve Tank Room',
        rom_address=0x7AC5A,
        map=[[1, 1]],
        door_ids=[
            DoorIdentifier(RIGHT, 1, 0, 0x1952E, 0x19546),  # Green Bubbles Missile Room
        ],
    ),
    Room(
        name='Bat Cave',
        rom_address=0x7B07A,
        map=[
            [1],
            [1],
        ],
        door_ids=[
            DoorIdentifier(LEFT, 0, 1, 0x197AA, 0x1958E),  # Bubble Mountain
            DoorIdentifier(RIGHT, 0, 0, 0x197B6, 0x195A6),  # Speed Booster Hall
        ],
    ),
    Room(
        name='Speed Booster Hall',
        rom_address=0x7ACF0,
        map=[
            [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x195A6, 0x197B6),  # Bat Cave
            DoorIdentifier(RIGHT, 11, 1, 0x195B2, 0x195BE),  # Speed Booster Room
        ],
    ),
    Room(
        name='Speed Booster Room',
        rom_address=0x7AD1B,
        map=[[1]],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x195BE, 0x195B2),  # Speed Booster Hall
        ],
    ),
    Room(
        name='Single Chamber',
        rom_address=0x7AD5E,
        map=[
            [1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
        ],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x195CA, 0x19582),  # Bubble Mountain
            DoorIdentifier(RIGHT, 5, 0, 0x195FA, 0x19A4A),  # Three Musketeers' Room
            DoorIdentifier(RIGHT, 0, 1, 0x195D6, 0x19606),  # Double Chamber (top)
            DoorIdentifier(RIGHT, 0, 2, 0x195E2, 0x19612),  # Double Chamber (bottom)
            DoorIdentifier(RIGHT, 0, 3, 0x195EE, 0x19636),  # Spiky Platforms Tunnel
        ],
        parts=[[0, 2, 3, 4], [1]],
        transient_part_connections=[(1, 0)],  # crumble blocks
        missing_part_connections=[(0, 1)],
    ),
    Room(
        name='Double Chamber',
        rom_address=0x7ADAD,
        map=[
            [1, 1, 1, 1],
            [1, 1, 1, 1],
        ],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x19606, 0x195D6),  # Single Chamber (top)
            DoorIdentifier(LEFT, 0, 1, 0x19612, 0x195E2),  # Single Chamber (bottom)
            DoorIdentifier(RIGHT, 3, 0, 0x1961E, 0x1962A),  # Wave Beam Room
        ],
    ),
    Room(
        name='Wave Beam Room',
        rom_address=0x7ADDE,
        map=[[1]],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x1962A, 0x1961E),  # Double Chamber
        ],
    ),
    Room(
        name='Ice Beam Gate Room',
        rom_address=0x7A815,
        map=[
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 0, 0],
        ],
        door_ids=[
            DoorIdentifier(LEFT, 3, 0, 0x19312, 0x1934E),  # Ice Beam Tutorial Room
            DoorIdentifier(LEFT, 3, 2, 0x1931E, 0x19276),  # Ice Beam Acid Room
            DoorIdentifier(LEFT, 0, 3, 0x19336, 0x1938A),  # Crumble Shaft
            DoorIdentifier(RIGHT, 6, 2, 0x1932A, 0x192BE),  # Business Center
        ],
        parts=[[1, 2, 3], [0]],
        transient_part_connections=[(1, 0)],  # crumble blocks
        missing_part_connections=[(0, 1)],
    ),
    Room(
        name='Ice Beam Acid Room',
        rom_address=0x7A75D,
        map=[[1, 1]],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x19282, 0x19366),  # Ice Beam Snake Room
            DoorIdentifier(RIGHT, 1, 0, 0x19276, 0x1931E),  # Ice Beam Gate Room
        ],
    ),
    Room(
        name='Ice Beam Snake Room',
        rom_address=0x7A8B9,
        map=[
            [1, 0],
            [1, 1],
            [1, 0],
        ],
        door_ids=[
            DoorIdentifier(RIGHT, 0, 0, 0x19372, 0x19342),  # Ice Beam Tutorial Room
            DoorIdentifier(RIGHT, 1, 1, 0x1937E, 0x1935A),  # Ice Beam Room
            DoorIdentifier(RIGHT, 0, 2, 0x19366, 0x19282),  # Ice Beam Acid Room
        ],
    ),
    Room(
        name='Ice Beam Room',
        rom_address=0x7A890,
        map=[[1]],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x1935A, 0x1937E),  # Ice Beam Snake Room
        ],
    ),
    Room(
        name='Ice Beam Tutorial Room',
        rom_address=0x7A865,
        map=[[1, 1]],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x19342, 0x19372),  # Ice Beam Snake Room
            DoorIdentifier(RIGHT, 1, 0, 0x1934E, 0x19312),  # Ice Beam Gate Room
        ],
    ),
    Room(
        name='Crumble Shaft',
        rom_address=0x7A8F8,
        map=[
            [1],
            [1],
            [1],
            [1],
        ],
        door_ids=[
            DoorIdentifier(RIGHT, 0, 0, 0x1938A, 0x19336),  # Ice Beam Gate Room
            DoorIdentifier(RIGHT, 0, 3, 0x19396, 0x193A2),  # Crocomire Speedway
        ],
    ),
    Room(
        name='Nutella Refill',
        rom_address=0x7B026,
        map=[[1]],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x19786, 0x19756),  # Acid Snakes Tunnel
            DoorIdentifier(RIGHT, 0, 0, 0x19792, 0x1976E),  # Spiky Acid Snakes Tunnel
        ],
    ),
    Room(
        name='Spiky Acid Snakes Tunnel',
        rom_address=0x7AFFB,
        map=[[1, 1, 1, 1]],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x1976E, 0x19792),  # Nutella Refill
            DoorIdentifier(RIGHT, 3, 0, 0x1977A, 0x1968A),  # Kronic Boost Room
        ],
    ),
    Room(
        name='Kronic Boost Room',
        rom_address=0x7AE74,
        map=[
            [0, 1],
            [1, 1],
            [0, 1],
        ],
        door_ids=[
            DoorIdentifier(LEFT, 1, 0, 0x19666, 0x196A2),  # Magdollite Tunnel
            DoorIdentifier(LEFT, 0, 1, 0x1968A, 0x1977A),  # Spiky Acid Snakes Tunnel
            DoorIdentifier(LEFT, 1, 2, 0x1967E, 0x196D2),  # Lava Dive Room
            DoorIdentifier(RIGHT, 1, 0, 0x19672, 0x1965A),  # Volcano Room
        ],
    ),
    Room(
        name='Magdollite Tunnel',
        rom_address=0x7AEB4,
        map=[[1, 1, 1]],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x19696, 0x196BA),  # Purple Shaft
            DoorIdentifier(RIGHT, 2, 0, 0x196A2, 0x19666),  # Kronic Boost Room
        ],
    ),
    Room(
        name='Lava Dive Room',
        rom_address=0x7AF14,
        map=[
            [1, 1, 1, 1],
            [0, 1, 1, 1],
            [0, 1, 1, 0],
        ],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x196DE, 0x196EA),  # Lower Norfair Elevator
            DoorIdentifier(RIGHT, 3, 0, 0x196D2, 0x1967E),  # Kronic Boost Room
        ],
    ),
    Room(
        name='Volcano Room',
        rom_address=0x7AE32,
        map=[
            [0, 0, 1],
            [0, 0, 1],
            [1, 1, 1],
        ],
        door_ids=[
            DoorIdentifier(LEFT, 2, 0, 0x1964E, 0x19642),  # Spiky Platforms Tunnel
            DoorIdentifier(LEFT, 0, 2, 0x1965A, 0x19672),  # Kronic Boost Room
        ],
    ),
    Room(
        name='Spiky Platforms Tunnel',
        rom_address=0x7AE07,
        map=[[1, 1, 1, 1]],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x19636, 0x195EE),  # Single Chamber
            DoorIdentifier(RIGHT, 3, 0, 0x19642, 0x1964E),  # Volcano Room
        ],
    ),
    Room(
        name='Red Pirate Shaft',
        rom_address=0x7B139,
        map=[
            [1],
            [1],
            [1],
        ],
        door_ids=[
            DoorIdentifier(RIGHT, 0, 0, 0x197F2, 0x19726),  # Upper Norfair Farming Room
            DoorIdentifier(DOWN, 0, 2, 0x197FE, 0x19762),  # Acid Snakes Tunnel
        ],
    ),
    Room(
        name='Acid Snakes Tunnel',
        rom_address=0x7AFCE,
        map=[[1, 1, 1, 1]],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x1974A, 0x193C6),  # Crocomire Speedway
            DoorIdentifier(RIGHT, 3, 0, 0x19756, 0x19786),  # Nutella Refill
            DoorIdentifier(UP, 3, 0, 0x19762, 0x197FE),  # Red Pirate Shaft
        ],
    ),
    Room(
        name='Crocomire Speedway',
        rom_address=0x7A923,
        map=[
            [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x193A2, 0x19396),  # Crumble Shaft
            DoorIdentifier(LEFT, 12, 0, 0x193AE, 0x1940E),  # Crocomire Escape
            DoorIdentifier(RIGHT, 12, 1, 0x193BA, 0x19822),  # Crocomire Save Room
            DoorIdentifier(RIGHT, 12, 2, 0x193C6, 0x1974A),  # Acid Snakes Tunnel
            DoorIdentifier(DOWN, 12, 2, 0x193D2, 0x193EA),  # Crocomire's Room
        ],
        parts=[[0], [1, 2, 3, 4]],
        transient_part_connections=[(0, 1)],  # speed blocks
        missing_part_connections=[(1, 0)],
    ),
    Room(
        name='Crocomire Escape',
        rom_address=0x7AA0E,
        map=[
            [1, 1, 1, 1],
            [1, 1, 1, 1],
        ],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x19402, 0x192E2),  # Business Center
            DoorIdentifier(RIGHT, 3, 1, 0x1940E, 0x193AE),  # Crocomire Speedway
        ],
        parts=[[0], [1]],
        transient_part_connections=[(1, 0)],  # unglitchable green gate
        missing_part_connections=[(0, 1)],
    ),
    Room(
        name="Crocomire's Room",
        rom_address=0x7A98D,
        map=[[1, 1, 1, 1, 1, 1, 1, 1]],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x193DE, 0x19432),  # Post Crocomire Farming Room
            DoorIdentifier(UP, 3, 0, 0x193EA, 0x193D2),  # Crocomire Speedway
        ],
        parts=[[0], [1]],
        durable_part_connections=[(1, 0)],  # spike blocks cleared after Crocomire defeated
        missing_part_connections=[(0, 1)],
    ),
    Room(
        name='Post Crocomire Farming Room',
        rom_address=0x7AA82,
        map=[
            [1, 1],
            [1, 1],
        ],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x1943E, 0x1946E),  # Post Crocomire Power Bomb Room
            DoorIdentifier(RIGHT, 1, 0, 0x19432, 0x193DE),  # Crocomire's Room
            DoorIdentifier(RIGHT, 1, 1, 0x19456, 0x19462),  # Post Crocomire Save Room
            DoorIdentifier(DOWN, 0, 1, 0x1944A, 0x1947A),  # Post Crocomire Shaft
        ],
    ),
    Room(
        name='Post Crocomire Power Bomb Room',
        rom_address=0x7AADE,
        map=[[1]],
        door_ids=[
            DoorIdentifier(RIGHT, 0, 0, 0x1946E, 0x1943E),  # Post Crocomire Farming Room
        ],
    ),
    Room(
        name='Post Crocomire Shaft',
        rom_address=0x7AB07,
        map=[
            [1],
            [1],
            [1],
            [1],
            [1],
        ],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x19486, 0x194C2),  # Grapple Tutorial Room 3
            DoorIdentifier(RIGHT, 0, 3, 0x19492, 0x194AA),  # Post Crocomire Missile Room
            DoorIdentifier(DOWN, 0, 4, 0x1949E, 0x194CE),  # Post Crocomire Jump Room
            DoorIdentifier(UP, 0, 0, 0x1947A, 0x1944A),  # Post Crocomire Farming Room
        ],
    ),
    Room(
        name='Post Crocomire Missile Room',
        rom_address=0x7AB3B,
        map=[[1, 1, 1, 1]],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x194AA, 0x19492),  # Post Crocomire Shaft
        ],
    ),
    Room(
        name='Post Crocomire Jump Room',
        rom_address=0x7AB8F,
        map=[
            [1, 1, 1, 1, 1, 0, 0, 0],
            [1, 1, 1, 1, 1, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1],
        ],
        door_ids=[
            DoorIdentifier(LEFT, 0, 1, 0x194DA, 0x19516),  # Grapple Beam Room
            DoorIdentifier(UP, 6, 2, 0x194CE, 0x1949E),  # Post Crocomire Shaft
        ],
    ),
    Room(
        name='Grapple Beam Room',
        rom_address=0x7AC2B,
        map=[
            [1],
            [1],
            [1],
        ],
        door_ids=[
            DoorIdentifier(RIGHT, 0, 0, 0x19522, 0x194FE),  # Grapple Tutorial Room 1
            DoorIdentifier(RIGHT, 0, 2, 0x19516, 0x194DA),  # Post Crocomire Jump Room
        ],
    ),
    Room(
        name='Grapple Tutorial Room 1',
        rom_address=0x7AC00,
        map=[[1, 1]],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x194FE, 0x19522),  # Grapple Beam Room
            DoorIdentifier(RIGHT, 1, 0, 0x1950A, 0x194E6),  # Grapple Tutorial Room 2
        ],
    ),
    Room(
        name='Grapple Tutorial Room 2',
        rom_address=0x7ABD2,
        map=[
            [1],
            [1],
            [1],
        ],
        door_ids=[
            DoorIdentifier(LEFT, 0, 2, 0x194E6, 0x1950A),  # Grapple Tutorial Room 1
            DoorIdentifier(RIGHT, 0, 0, 0x194F2, 0x194B6),  # Grapple Tutorial Room 3
        ],
    ),
    Room(
        name='Grapple Tutorial Room 3',
        rom_address=0x7AB64,
        map=[
            [1, 1, 1],
            [1, 1, 1],
        ],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x194B6, 0x194F2),  # Grapple Tutorial Room 2
            DoorIdentifier(RIGHT, 2, 0, 0x194C2, 0x19486),  # Post Crocomire Shaft
        ],
        parts=[[0], [1]],  # assuming that green gate glitch is not necessarily in logic
        transient_part_connections=[(0, 1)],  # glitchable green gate
        missing_part_connections=[(1, 0)],
    ),
    Room(
        name='Crocomire Save Room',
        rom_address=0x7B192,
        map=[[1]],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x19822, 0x193BA)  # Crocomire Speedway
        ],
    ),
    Room(
        name='Post Crocomire Save Room',
        rom_address=0x7AAB5,
        map=[[1]],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x19462, 0x19456)  # Post Crocomire Farming Room
        ],
    ),
    Room(
        name='Lower Norfair Elevator',
        rom_address=0x7AF3F,
        map=[[1]],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x19702, 0x1982E),  # Lower Norfair Elevator Save Room
            DoorIdentifier(RIGHT, 0, 0, 0x196EA, 0x196DE),  # Lava Dive Room
            DoorIdentifier(DOWN, 0, 0, 0x196F6, 0x1986A, ELEVATOR),  # Main Hall
        ],
    ),
    Room(
        name='Lower Norfair Elevator Save Room',
        rom_address=0x7B1BB,
        map=[[1]],
        door_ids=[
            DoorIdentifier(RIGHT, 0, 0, 0x1982E, 0x19702),  # Lower Norfair Elevator
        ],
    ),
    Room(
        name='Main Hall',
        rom_address=0x7B236,
        map=[
            [0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1],
        ],
        door_ids=[
            DoorIdentifier(LEFT, 0, 2, 0x19852, 0x19846),  # Acid Statue Room
            DoorIdentifier(RIGHT, 7, 2, 0x1985E, 0x198E2),  # Fast Pillars Setup Room
            DoorIdentifier(UP, 4, 0, 0x1986A, 0x196F6, ELEVATOR),  # Lower Norfair Elevator
        ],
    ),
    Room(
        name='Fast Pillars Setup Room',
        rom_address=0x7B3A5,
        map=[
            [1],
            [1],
            [1],
        ],
        door_ids=[
            DoorIdentifier(LEFT, 0, 1, 0x198E2, 0x1985E),  # Main Hall
            DoorIdentifier(LEFT, 0, 2, 0x19906, 0x1989A),  # Fast Ripper Room
            DoorIdentifier(RIGHT, 0, 0, 0x198EE, 0x1992A),  # Mickey Mouse Room
            DoorIdentifier(RIGHT, 0, 2, 0x19912, 0x19942),  # Pillar Room
        ],
    ),
    Room(
        name='Pillar Room',
        rom_address=0x7B457,
        map=[[1, 1, 1, 1]],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x19942, 0x19912),  # Fast Pillars Setup Room
            DoorIdentifier(RIGHT, 3, 0, 0x1994E, 0x1998A),  # The Worst Room In The Game
        ],
    ),
    Room(
        name='The Worst Room In The Game',
        rom_address=0x7B4AD,
        map=[
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
        ],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x19972, 0x19936),  # Mickey Mouse Room
            DoorIdentifier(LEFT, 0, 5, 0x1998A, 0x1994E),  # Pillar Room
            DoorIdentifier(RIGHT, 0, 1, 0x1997E, 0x19996),  # Amphitheatre
        ],
    ),
    Room(
        name='Amphitheatre',
        rom_address=0x7B4E5,
        map=[
            [0, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
        ],
        door_ids=[
            DoorIdentifier(LEFT, 0, 1, 0x19996, 0x1997E),  # The Worst Room In The Game
            DoorIdentifier(RIGHT, 3, 0, 0x199A2, 0x199F6),  # Red Kihunter Shaft
        ],
        parts=[[0], [1]],  # assuming that acid damage is not necessarily in logic
        transient_part_connections=[(0, 1)],  # climbing while acid rises
        missing_part_connections=[(1, 0)],
    ),
    Room(
        name='Red Kihunter Shaft',
        rom_address=0x7B585,
        map=[
            [1, 0, 0],
            [1, 0, 0],
            [1, 0, 0],
            [1, 0, 0],
            [1, 1, 1],
        ],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x199F6, 0x199A2),  # Amphitheatre
            DoorIdentifier(RIGHT, 0, 0, 0x19A02, 0x19AAA),  # Lower Norfair Fireflea Room
            DoorIdentifier(RIGHT, 0, 3, 0x19A0E, 0x19AB6),  # Red Kihunter Shaft Save Room
            DoorIdentifier(DOWN, 2, 4, 0x199EA, 0x19A26),  # Wasteland
        ],
    ),
    Room(
        # TODO: add this to wiki.supermetroid.run/List_of_rooms because it is missing.
        name='Red Kihunter Shaft Save Room',
        rom_address=0x7B741,
        map=[[1]],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x19AB6, 0x19A0E),  # Red Kihunter Shaft
        ],
    ),
    Room(
        name='Wasteland',
        rom_address=0x7B5D5,
        map=[
            [1, 1, 1, 1, 1, 1],
            [0, 1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
        ],
        door_ids=[
            DoorIdentifier(LEFT, 1, 2, 0x19A1A, 0x19A3E),  # Metal Pirates Room
            DoorIdentifier(UP, 5, 0, 0x19A26, 0x199EA),  # Red Kihunter Shaft
        ],
    ),
    Room(
        name='Metal Pirates Room',
        rom_address=0x7B62B,
        map=[[1, 1, 1]],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x19A32, 0x19966),  # Plowerhouse Room
            DoorIdentifier(RIGHT, 2, 0, 0x19A3E, 0x19A1A),  # Wasteland
        ],
    ),
    Room(
        name='Plowerhouse Room',
        rom_address=0x7B482,
        map=[[1, 1, 1]],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x1995A, 0x198D6),  # Lower Norfair Farming Room
            DoorIdentifier(RIGHT, 2, 0, 0x19966, 0x19A32),  # Metal Pirates Room
        ],
    ),
    Room(
        name='Lower Norfair Farming Room',
        rom_address=0x7B37A,
        map=[[1, 1, 1]],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x198CA, 0x198BE),  # Ridley's Room
            DoorIdentifier(RIGHT, 2, 0, 0x198D6, 0x1995A),  # Plowerhouse Room
        ],
    ),
    Room(
        name="Ridley's Room",
        rom_address=0x7B32E,
        map=[
            [1],
            [1],
        ],
        door_ids=[
            DoorIdentifier(LEFT, 0, 1, 0x198B2, 0x19A62),  # Ridley Tank Room
            DoorIdentifier(RIGHT, 0, 0, 0x198BE, 0x198CA),  # Lower Norfair Farming Room
        ],
    ),
    Room(
        name='Ridley Tank Room',
        rom_address=0x7B698,
        map=[[1]],
        door_ids=[
            DoorIdentifier(RIGHT, 0, 0, 0x19A62, 0x198B2),  # Ridley's Room
        ],
    ),
    Room(
        name='Mickey Mouse Room',
        rom_address=0x7B40A,
        map=[
            [0, 0, 0, 1],
            [0, 0, 1, 1],
            [0, 0, 0, 1],
            [1, 1, 1, 1],
        ],
        door_ids=[
            DoorIdentifier(LEFT, 0, 3, 0x1992A, 0x198EE),  # Fast Pillars Setup Room
            DoorIdentifier(RIGHT, 3, 0, 0x19936, 0x19972),  # The Worst Room In The Game
        ],
        parts=[[0], [1]],
        transient_part_connections=[(1, 0)],  # crumble blocks
        missing_part_connections=[(0, 1)],
    ),
    Room(
        name='Lower Norfair Fireflea Room',
        rom_address=0x7B6EE,
        map=[
            [1, 1, 0],
            [0, 1, 0],
            [0, 1, 0],
            [0, 1, 1],
            [0, 1, 1],
            [0, 1, 1],
        ],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x19A92, 0x199BA),  # Lower Norfair Spring Ball Maze Room
            DoorIdentifier(LEFT, 1, 3, 0x19AAA, 0x19A02),  # Red Kihunter Shaft
            DoorIdentifier(RIGHT, 1, 0, 0x19A9E, 0x199D2),  # Lower Norfair Escape Power Bomb Room
        ],
    ),
    Room(
        name='Lower Norfair Spring Ball Maze Room',
        rom_address=0x7B510,
        map=[
            [1, 1, 1, 1, 1],
            [1, 1, 0, 0, 0],
        ],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x199AE, 0x19A56),  # Three Musketeers' Room
            DoorIdentifier(RIGHT, 1, 1, 0x199BA, 0x19A92),  # Lower Norfair Fireflea Room
            DoorIdentifier(DOWN, 4, 0, 0x199C6, 0x199DE),  # Lower Norfair Escape Power Bomb Room
        ],
        parts=[[0, 1], [2]],
        transient_part_connections=[(0, 1)],  # crumble block
        missing_part_connections=[(1, 0)],
    ),
    Room(
        name='Lower Norfair Escape Power Bomb Room',
        rom_address=0x7B55A,
        map=[[1]],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x199D2, 0x19A9E),  # Lower Norfair Fireflea Room
            DoorIdentifier(UP, 0, 0, 0x199DE, 0x199C6),  # Lower Norfair Spring Ball Maze Room
        ],
        parts=[[0], [1]],
        transient_part_connections=[(1, 0)],  # crumble block
        missing_part_connections=[(0, 1)],
    ),
    Room(
        name="Three Musketeers' Room",
        rom_address=0x7B656,
        map=[
            [0, 1, 0, 0],
            [0, 1, 0, 0],
            [1, 1, 1, 1],
        ],
        door_ids=[
            DoorIdentifier(LEFT, 1, 0, 0x19A4A, 0x195FA),  # Single Chamber
            DoorIdentifier(RIGHT, 3, 2, 0x19A56, 0x199AE),  # Lower Norfair Spring Ball Maze Room
        ],
    ),
    Room(
        name='Acid Statue Room',
        rom_address=0x7B1E5,
        map=[
            [1, 1, 0],
            [1, 1, 0],
            [1, 1, 1],
        ],
        door_ids=[
            DoorIdentifier(RIGHT, 1, 0, 0x19846, 0x19852),  # Main Hall
            DoorIdentifier(RIGHT, 2, 2, 0x1983A, 0x19876),  # Golden Torizo's Room
        ],
        parts=[[0], [1]],
        durable_part_connections=[(0, 1)],  # acid drain by morphing in statue with space jump
        missing_part_connections=[(1, 0)],
    ),
    Room(
        name="Golden Torizo's Room",
        rom_address=0x7B283,
        map=[
            [1, 1],
            [1, 1],
        ],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x19876, 0x1983A),  # Acid Statue Room
            DoorIdentifier(RIGHT, 1, 1, 0x19882, 0x19A86),  # Screw Attack Room
        ],
        parts=[[0], [1]],
        transient_part_connections=[(0, 1)],  # crumble blocks
        missing_part_connections=[(1, 0)],
    ),
    Room(
        name='Screw Attack Room',
        rom_address=0x7B6C1,
        map=[
            [1],
            [1],
            [1],
        ],
        door_ids=[
            DoorIdentifier(LEFT, 0, 2, 0x19A86, 0x19882),  # Golden Torizo's Room
            DoorIdentifier(RIGHT, 0, 0, 0x19A6E, 0x1988E),  # Fast Ripper Room
            DoorIdentifier(RIGHT, 0, 1, 0x19A7A, 0x198A6),  # Golden Torizo Energy Recharge
        ],
    ),
    Room(
        name='Golden Torizo Energy Recharge',
        rom_address=0x7B305,
        map=[[1]],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x198A6, 0x19A7A),  # Screw Attack Room
        ],
    ),
    Room(
        name='Fast Ripper Room',
        rom_address=0x7B2DA,
        # # TODO: fix this back.
        # map=[[1, 1, 1]],
        # door_ids=[
        #     DoorIdentifier(LEFT, 0, 0, 0x1988E, 0x19A6E),  # Screw Attack Room
        #     DoorIdentifier(RIGHT, 2, 0, 0x1989A, 0x19906),  # Fast Pillars Setup Room
        # ],
        map=[[1, 1, 1, 1]],
        door_ids=[
            DoorIdentifier(LEFT, 0, 0, 0x1988E, 0x19A6E),  # Screw Attack Room
            DoorIdentifier(RIGHT, 3, 0, 0x1989A, 0x19906),  # Fast Pillars Setup Room
        ],
        parts=[[0], [1]],  # assuming that green gate glitch is not necessarily in logic
        transient_part_connections=[(0, 1)],  # glitchable green gate
        missing_part_connections=[(1, 0)],
    ),
]

for room in rooms:
    room.area = Area.NORFAIR
    room.sub_area = SubArea.UPPER_NORFAIR
