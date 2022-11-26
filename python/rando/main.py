# TODO: Clean up this whole thing (it's a mess right now). Split stuff up into modules in some reasonable way.
import flask
from typing import List
from dataclasses import dataclass
from io import BytesIO
import numpy as np
import random
import graph_tool
import graph_tool.inference
import graph_tool.topology
from collections import defaultdict
import zipfile
import pprint

from rando.sm_json_data import SMJsonData, GameState, Link, DifficultyConfig
from rando.items import Randomizer
from logic.rooms.all_rooms import rooms
from maze_builder.types import Room, SubArea
from maze_builder.display import MapDisplay
import json
import ips_util

VERSION = 0

import logging
from maze_builder.types import reconstruct_room_data, Direction, DoorSubtype
import logic.rooms.all_rooms
import pickle

logging.basicConfig(format='%(asctime)s %(message)s',
                    level=logging.INFO,
                    handlers=[logging.FileHandler("train.log"),
                              logging.StreamHandler()])

import io
import os

from flask import Flask

app = Flask(__name__)

sm_json_data_path = "sm-json-data/"
sm_json_data = SMJsonData(sm_json_data_path)
map_dir = 'maps/session-2022-06-03T17:19:29.727911.pkl-bk30'
file_list = sorted(os.listdir(map_dir))


def get_tech_description(name):
    desc = sm_json_data.tech_json_dict[name].get('note')
    if isinstance(desc, str):
        return desc
    elif isinstance(desc, list):
        return ' '.join(desc)
    else:
        return ''


def get_tech_inputs():
    return '\n'.join(f'''
        <div class="row">
            <div class="col-sm-3 form-check">
              <input type="checkbox" class="form-check-input" id="tech-{tech}" onchange="techChanged()" name="tech-{tech}" value="{tech}">
              <label class="form-check-label" for="{tech}"><b>{tech}</b></label>
            </div>
        </div>
        <div class="row">
            <div class="col-sm-12">
              {get_tech_description(tech)}
            </div>
        </div>
        '''
                     for tech in sorted(sm_json_data.tech_name_set))


presets = [
    ('Beginner', {
        'shinesparkTiles': 32,
        'resourceMultiplier': 3.0,
        'tech': [],
    }),
    ('Easy', {
        'shinesparkTiles': 28,
        'resourceMultiplier': 2.0,
        'tech': [
            'canIBJ',
            'canWalljump',
            'canShinespark',
            'canCrouchJump',
            'canCrystalFlash',
            'canDownGrab',
            'canHeatRun',
            'canSuitlessMaridia']
    }),
    ('Medium', {
        'shinesparkTiles': 24,
        'resourceMultiplier': 1.5,
        'tech': [
            'canBombAboveIBJ',
            'canManipulateHitbox',
            'canUseEnemies',
            'canCrystalFlashForceStandup',
            'canDamageBoost',
            'canGateGlitch',
            'canGGG',
            'canGravityJump',
            'canMockball',
            'canMachball',
            'canMidAirMockball',
            'canSpringBallJump',
            'canUseFrozenEnemies',
            'canMochtroidClimb',
            'canStationarySpinJump',
            'canMoonfall',
            'canMochtroidClip',
            'canCeilingClip',
            'canIframeSpikeJump',
            'canSingleHBJ',
            'canSnailClimb',
            'canXRayStandUp',
            'canCrumbleJump',
            'canBlueSpaceJump']
    }),
    ('Hard', {
        'shinesparkTiles': 20,
        'resourceMultiplier': 1.2,
        'tech': [
            'canUseSpeedEchoes',
            'canTrickyJump',
            'canSuitlessLavaDive',
            'canSuitlessLavaWalljump',
            'canPreciseWalljump',
            'canHitbox',
            'canPlasmaHitbox',
            'canUnmorphBombBoost',
            'canHeatedGateGlitch',
            'canHeatedGGG',
            'canLavaGravityJump',
            'can3HighMidAirMorph',
            'canTurnaroundAimCancel',
            'canStationaryMidAirMockball',
            'canTrickyUseFrozenEnemies',
            'canCrabClimb',
            'canMetroidAvoid',
            'canSandMochtroidClimb',
            'canShotBlockOverload',
            'canMaridiaTubeClip',
            'canQuickLowTideWalljumpWaterEscape',
            'canGrappleJump',
            'canDoubleHBJ',
            'canSnailClip',
            'canBombJumpBreakFree',
            'canSuperReachAround',
            'canWrapAroundShot',
            'canTunnelCrawl',
            'canSpringBallJumpMidAir',
            'canCrumbleSpinJump',
            'canIceZebetitesSkip']}),
    ('Expert', {
        'shinesparkTiles': 16,
        'resourceMultiplier': 1.0,
        'tech':
         [
             'canTrickyDashJump',
             'canCWJ',
             'canDelayedWalljump',
             'canIframeSpikeWalljump',
             'canFlatleyTurnaroundJump',
             'canContinuousDboost',
             'canReverseGateGlitch',
             'canGravityWalljump',
             'can2HighWallMidAirMorph',
             'canPixelPerfectIceClip',
             'canWallIceClip',
             'canBabyMetroidAvoid',
             'canSunkenDualWallClimb',
             'canBreakFree',
             'canHerdBabyTurtles',
             'canSandIBJ',
             'canFastWalljumpClimb',
             'canDraygonGrappleJump',
             'canGrappleClip',
             'canManipulateMellas',
             'canMorphlessTunnelCrawl',
             'canSpringwall',
             'canDoubleSpringBallJumpMidAir',
             'canXRayClimb',
             'canQuickCrumbleEscape',
             'canSpeedZebetitesSkip',
             'canRemorphZebetiteSkip',
             'canBePatient',
             'canInsaneWalljump',
             'canNonTrivialIceClip',
             'canBeetomClip',
             'canWallCrawlerClip',
             'canPuyoClip',
             'canMultiviolaClip',
             'canRightFacingDoorXRayClimb']
     })
]

preset_dict = {}
preset_tech_list = []
for preset_name, preset_tech in presets:
    preset_tech_list = preset_tech_list + preset_tech['tech']
    preset_dict[preset_name] = {**preset_tech, 'tech': preset_tech_list}


def preset_buttons():
    return '\n'.join(f'''
      <input type="radio" class="btn-check" name="preset" id="preset{name}" autocomplete="off" onclick="presetChanged()" {'checked' if i == 0 else ''}>
      <label class="btn btn-outline-primary" for="preset{name}">{name}</label>
    ''' for i, name in enumerate(preset_dict.keys()))


def preset_change_script():
    script_list = []
    for name, preset in preset_dict.items():
        script_list.append(f'''
            if (document.getElementById("preset{name}").checked) {{
                document.getElementById("shinesparkTiles").value = {preset["shinesparkTiles"]};
                document.getElementById("resourceMultiplier").value = {preset["resourceMultiplier"]};
                {';'.join(f'document.getElementById("tech-{tech}").checked = {"true" if tech in preset["tech"] else "false"}' for tech in sm_json_data.tech_name_set)}
            }}
        ''')
    return '\n'.join(script_list)


def tech_change_script():
    return '\n'.join(f'document.getElementById("preset{name}").checked = false;' for name in preset_dict.keys())


def encode_difficulty(difficulty: DifficultyConfig):
    x = 0
    x = x * 22 + (difficulty.shine_charge_tiles - 12)
    x = x * 91 + int(difficulty.multiplier * 10) - 10
    for tech in sorted(sm_json_data.tech_name_set):
        x *= 2
        if tech in difficulty.tech:
            x += 1
    return x


@app.route("/")
def home():
    # TODO: Put this somewhere else instead of inline here.
    return f'''<!DOCTYPE html>
    <html lang="en-US">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Super Metroid Map Randomizer</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">
      </head>
      <body>
        <div class="container">
            <div class="row">
                <div class="col-9">
                    <h1>Super Metroid Map Randomizer</h1>
                </div>
                <div class="col-3" align=right>
                    <small>Version: {VERSION}</small>
                </div>
            </div>
            <form method="POST" enctype="multipart/form-data" action="/randomize">
                <div class="form-group row">
                  <label class="col-sm-2 col-form-label" for="rom">Input ROM</label>
                  <input class="col-sm-10 form-control-file" type="file" id="rom" name="rom">
                </div>
                <div class="form-group row">
                  <label class="col-sm-2 col-form-label" for="preset">Difficulty preset</label>
                  <div class="col-sm-10 btn-group" role="group">
                    {preset_buttons()}
                 </div>
                </div>
                <div class="accordion p-2" id="accordion">
                  <div class="accordion-item">
                    <h2 class="accordion-header" id="flush-headingOne">
                      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseOne" aria-expanded="false" aria-controls="flush-collapseOne">
                        Customize difficulty requirements
                      </button>
                    </h2>
                    <div id="flush-collapseOne" class="accordion-collapse collapse" aria-labelledby="flush-headingOne" data-bs-parent="#accordionFlushExample">
                      <div class="form-group row p-2">
                        <label for="shinesparkTiles" class="col-sm-6 col-form-label">Shinespark tiles<br>
                        <small>(Smaller values assume ability to short-charge over shorter distances)</small>
                        </label>
                        <div class="col-sm-2">
                          <input type="text" class="form-control" name="shinesparkTiles" id="shinesparkTiles" value="32">
                        </div>
                      </div>
                      <div class="form-group row p-2">
                        <label for="resourceMultiplier" class="col-sm-6 col-form-label">Resource multiplier<br>
                        <small>(Leniency factor on assumed energy & ammo usage)</small>
                        </label>
                        <div class="col-sm-2">
                          <input type="text" class="form-control" name="resourceMultiplier" id="resourceMultiplier" value="3.0">
                        </div>
                      </div>
                      <div class="card p-2">
                        <div class="card-header">
                          Tech
                        </div>
                        <div class="card-body">
                          {get_tech_inputs()}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="form-group row p-2">
                  <label for="randomSeed" class="col-sm-2 col-form-label">Random seed</label>
                  <div class="col-sm-3">
                    <input type="text" class="form-control" name="randomSeed" id="randomSeed" value="">
                  </div>
                </div>
                <div class="form-group row p-2">
                    <input type="submit" class="col-sm-3 btn btn-primary" value="Generate ROM" />
                </div>
            </form>
            <div class="row">
                <div class="card">
                    <div class="card-header">Known issues</div>
                    <div class="card-body">
                        <ul>
                        <li>ROM may take a few minutes to generate. For fastest results, click "Generate ROM" once and wait patiently. If it times out, try again with a different random seed.
                        <li>Even if the tech is not selected, wall jumps and crouch-jump/down-grabs may be required in some places.
                        <li>Entering the Mother Brain room or Crocomire Room from the left causes a soft-lock.
                        <li>After the Kraid fight, graphics will generally be glitched (pause & unpause to fix). 
                        <li>For some seeds, using the Aqueduct toilet causes a soft-lock or glitched graphics.
                        <li>The demo graphics (before the start of the game) are messed up.
                        <li>The map in the loading sequence (from saved file) appears wrong.
                        <li>Some map tiles associated with elevators do not appear correctly.
                        <li>Door transitions generally have some minor graphical glitches.
                        <li>The escape timer is not tailored to the seed (but should be generous enough to be possible to beat).
                        <li>No door color randomization yet. To simplify things they're all just turned blue for now, except for in the Pit Room to keep a way to awaken Zebes.
                        <li>The end credits are vanilla.
                        </ul>
                    </div>
                </div>
            </div>
        <small>This is an early preview, so bugs are expected. If you encounter a problem, feedback is welcome on <a href="https://github.com/blkerby/MapRandomizer/issues">GitHub issues</a>.</small>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-kenU1KFdBIe4zVF0s0G1M5b4hcpxyD9F7jL+jjXkk+Q2h455rYXK/7HAuoJl+0I4" crossorigin="anonymous"></script>        
        <script>
        document.getElementById("randomSeed").value = Math.floor(Math.random() * 0x7fffffff);        
        function presetChanged() {{
            {preset_change_script()}
        }}
        function techChanged() {{
            {tech_change_script()}
        }}
        </script>
      </body>
    </html>
    '''


@app.route("/randomize", methods=['POST'])
def randomize():
    uploaded_rom_file = flask.request.files['rom']
    input_buf = uploaded_rom_file.stream.read(10_000_000)

    if len(input_buf) < 3145728 or len(input_buf) > 8388608:
        return flask.Response("Invalid input ROM", status=400)

    try:
        shine_charge_tiles = int(flask.request.form.get('shinesparkTiles'))
        assert shine_charge_tiles >= 12 and shine_charge_tiles <= 33
    except:
        return flask.Response("Invalid shinesparkTiles", status=400)

    try:
        resource_multiplier = float(flask.request.form.get('resourceMultiplier'))
        resource_multiplier = round(resource_multiplier * 10) / 10
        assert 1.0 <= resource_multiplier <= 10.0
    except:
        return flask.Response("Invalid resourceMultiplier", status=400)

    try:
        random_seed = int(flask.request.form.get('randomSeed'))
    except:
        return flask.Response("Invalid randomSeed", status=400)

    tech = set(tech for tech in sm_json_data.tech_name_set if flask.request.form.get('tech-' + tech) != None)
    difficulty = DifficultyConfig(tech=tech, shine_charge_tiles=shine_charge_tiles, multiplier=resource_multiplier)
    output_file_prefix = f'smmr-v{VERSION}-{random_seed}-{encode_difficulty(difficulty)}'
    logging.info(f"Starting {output_file_prefix}: random_seed={random_seed}, difficulty={difficulty}, ROM='{uploaded_rom_file.filename}' (hash={hash(input_buf)})")
    max_map_attempts = 100
    max_item_attempts = 200
    np.random.seed(random_seed % (2 ** 32))
    random.seed(random_seed)

    for _ in range(max_map_attempts):
        map_i = int(np.random.randint(0, len(file_list)))
        map_filename = file_list[map_i]
        map_file = '{}/{}'.format(map_dir, map_filename)
        map = json.load(open(map_file, 'r'))
        logging.info("{}".format(map_file))

        randomizer = Randomizer(map, sm_json_data, difficulty)
        for i in range(max_item_attempts):
            success = randomizer.randomize()
            if success:
                break
        else:
            continue
        break
    else:
        return flask.Response("Too many failed item randomization attempts", status=500)

    logging.info("Done with item randomization")
    spoiler_data = {
        'difficulty': {
            'tech': list(sorted(difficulty.tech)),
            'shine_charge_tiles': difficulty.shine_charge_tiles,
            'multiplier': difficulty.multiplier,
        },
        'route': randomizer.spoiler_route,
    }

    for room in rooms:
        room.populate()
    xs_min = np.array([p[0] for p in map['rooms']])
    ys_min = np.array([p[1] for p in map['rooms']])
    xs_max = np.array([p[0] + rooms[i].width for i, p in enumerate(map['rooms'])])
    ys_max = np.array([p[1] + rooms[i].height for i, p in enumerate(map['rooms'])])

    door_room_dict = {}
    for i, room in enumerate(rooms):
        for door in room.door_ids:
            door_pair = (door.exit_ptr, door.entrance_ptr)
            door_room_dict[door_pair] = i
    edges_list = []
    for conn in map['doors']:
        src_room_id = door_room_dict[tuple(conn[0])]
        dst_room_id = door_room_dict[tuple(conn[1])]
        edges_list.append((src_room_id, dst_room_id))

    room_graph = graph_tool.Graph(directed=True)
    for (src, dst) in edges_list:
        room_graph.add_edge(src, dst)
        room_graph.add_edge(dst, src)

    num_areas = 6
    area_arr = np.array(map['area'])

    # Ensure that Landing Site is in Crateria:
    area_arr = (area_arr - area_arr[1] + num_areas) % num_areas

    display = MapDisplay(72, 72, 20)

    color_map = {
        0: (0x80, 0x80, 0x80),  # Crateria
        1: (0x80, 0xff, 0x80),  # Brinstar
        2: (0xff, 0x80, 0x80),  # Norfair
        3: (0xff, 0xff, 0x80),  # Wrecked ship
        4: (0x80, 0x80, 0xff),  # Maridia
        5: (0xc0, 0xc0, 0xc0),  # Tourian
    }

    colors = [color_map[i] for i in area_arr]
    display.display(rooms, xs_min, ys_min, colors)
    map_png_file = io.BytesIO()
    display.image.save(map_png_file, "png")
    map_png_bytes = map_png_file.getvalue()

    color_map = {
        SubArea.CRATERIA_AND_BLUE_BRINSTAR: (0x80, 0x80, 0x80),
        SubArea.GREEN_AND_PINK_BRINSTAR: (0x80, 0xff, 0x80),
        SubArea.RED_BRINSTAR_AND_WAREHOUSE: (0x60, 0xc0, 0x60),
        SubArea.UPPER_NORFAIR: (0xff, 0x80, 0x80),
        SubArea.LOWER_NORFAIR: (0xc0, 0x60, 0x60),
        SubArea.OUTER_MARIDIA: (0x80, 0x80, 0xff),
        SubArea.INNER_MARIDIA: (0x60, 0x60, 0xc0),
        SubArea.WRECKED_SHIP: (0xff, 0xff, 0x80),
        SubArea.TOURIAN: (0xc0, 0xc0, 0xc0),
    }

    colors = [color_map[room.sub_area] for room in rooms]
    display.display(rooms, xs_min, ys_min, colors)
    map_orig_png_file = io.BytesIO()
    display.image.save(map_orig_png_file, "png")
    map_orig_png_bytes = map_orig_png_file.getvalue()

    class Rom:
        def __init__(self, file):
            self.bytes_io = BytesIO(file.read())
            self.byte_buf = self.bytes_io.getbuffer()

        def read_u8(self, pos):
            return self.byte_buf[pos]

        def read_u16(self, pos):
            return self.read_u8(pos) + (self.read_u8(pos + 1) << 8)

        def read_u24(self, pos):
            return self.read_u8(pos) + (self.read_u8(pos + 1) << 8) + (self.read_u8(pos + 2) << 16)

        def read_n(self, pos, n):
            return self.byte_buf[pos:(pos + n)]

        def write_u8(self, pos, value):
            self.byte_buf[pos] = value

        def write_u16(self, pos, value):
            self.byte_buf[pos] = value & 0xff
            self.byte_buf[pos + 1] = value >> 8

        def write_n(self, pos, n, values):
            self.byte_buf[pos:(pos + n)] = values

        def save(self, filename):
            file = open(filename, 'wb')
            file.write(self.bytes_io.getvalue())

    area_map_ptrs = {
        0: 0x1A9000,  # Crateria
        1: 0x1A8000,  # Brinstar
        2: 0x1AA000,  # Norfair
        3: 0x1AB000,  # Wrecked ship
        4: 0x1AC000,  # Maridia
        5: 0x1AD000,  # Tourian
        6: 0x1AE000,  # Ceres
    }

    @dataclass
    class Door:
        door_ptr: int
        dest_room_ptr: int
        bitflag: int
        direction: int
        door_cap_x: int
        door_cap_y: int
        screen_x: int
        screen_y: int
        dist_spawn: int

    @dataclass
    class RoomState:
        event_ptr: int  # u16
        event_value: int  # u8
        state_ptr: int  # u16
        level_data_ptr: int  # u24
        tile_set: int  # u8
        song_set: int  # u8
        play_index: int  # u8
        fx_ptr: int  # u16
        enemy_set_ptr: int  # u16
        enemy_gfx_ptr: int  # u16
        bg_scrolling: int  # u16
        room_scrolls_ptr: int  # u16
        unused_ptr: int  # u16
        main_asm_ptr: int  # u16
        plm_set_ptr: int  # u16
        bg_ptr: int  # u16
        setup_asm_ptr: int  # u16

    class RomRoom:
        def __init__(self, rom: Rom, room: Room):
            room_ptr = room.rom_address
            self.room = room
            self.room_ptr = room_ptr
            self.area = rom.read_u8(room_ptr + 1)
            self.x = rom.read_u8(room_ptr + 2)
            self.y = rom.read_u8(room_ptr + 3)
            self.width = rom.read_u8(room_ptr + 4)
            self.height = rom.read_u8(room_ptr + 5)
            self.map_data = self.load_map_data(rom)
            self.doors = self.load_doors(rom)
            # self.load_states(rom)

        def load_map_data(self, rom):
            map_row_list = []
            for y in range(self.y, self.y + self.room.height):
                map_row = []
                for x in range(self.x, self.x + self.room.width):
                    cell = rom.read_u16(self.xy_to_map_ptr(x, y))
                    # if self.room.map[y - self.y][x - self.x] == 0:
                    #     cell = 0x1F  # Empty tile
                    map_row.append(cell)
                map_row_list.append(map_row)
            return map_row_list

        def load_single_state(self, rom, event_ptr, event_value, state_ptr):
            return RoomState(
                event_ptr=event_ptr,
                event_value=event_value,
                state_ptr=state_ptr,
                level_data_ptr=rom.read_u24(state_ptr),
                tile_set=rom.read_u8(state_ptr + 3),
                song_set=rom.read_u8(state_ptr + 4),
                play_index=rom.read_u8(state_ptr + 5),
                fx_ptr=rom.read_u16(state_ptr + 6),
                enemy_set_ptr=rom.read_u16(state_ptr + 8),
                enemy_gfx_ptr=rom.read_u16(state_ptr + 10),
                bg_scrolling=rom.read_u16(state_ptr + 12),
                room_scrolls_ptr=rom.read_u16(state_ptr + 14),
                unused_ptr=rom.read_u16(state_ptr + 16),
                main_asm_ptr=rom.read_u16(state_ptr + 18),
                plm_set_ptr=rom.read_u16(state_ptr + 20),
                bg_ptr=rom.read_u16(state_ptr + 22),
                setup_asm_ptr=rom.read_u16(state_ptr + 24),
            )

        def load_states(self, rom) -> List[RoomState]:
            ss = []
            for i in range(400):
                ss.append("{:02x} ".format(rom.read_u8(self.room_ptr + i)))
                if i % 16 == 0:
                    ss.append("\n")
            # print(''.join(ss))
            pos = 11
            states = []
            while True:
                ptr = rom.read_u16(self.room_ptr + pos)
                # print("{:x}".format(ptr))
                if ptr == 0xE5E6:
                    # This is the standard state, which is the last one
                    event_value = 0  # Dummy value
                    state_ptr = self.room_ptr + pos + 2
                    states.append(self.load_single_state(rom, ptr, event_value, state_ptr))
                    break
                elif ptr in (0xE612, 0xE629):
                    # This is an event state
                    event_value = rom.read_u8(self.room_ptr + pos + 2)
                    state_ptr = 0x70000 + rom.read_u16(self.room_ptr + pos + 3)
                    states.append(self.load_single_state(rom, ptr, event_value, state_ptr))
                    pos += 5
                else:
                    event_value = 0  # Dummy value
                    state_ptr = 0x70000 + rom.read_u16(self.room_ptr + pos + 2)
                    states.append(self.load_single_state(rom, ptr, event_value, state_ptr))
                    pos += 4
            return states

        def load_doors(self, rom):
            self.doors = []
            door_out_ptr = 0x70000 + rom.read_u16(self.room_ptr + 9)
            while True:
                door_ptr = 0x10000 + rom.read_u16(door_out_ptr)
                if door_ptr < 0x18000:
                    break
                door_out_ptr += 2

                dest_room_ptr = rom.read_u16(door_ptr)
                bitflag = rom.read_u8(door_ptr + 2)
                direction = rom.read_u8(door_ptr + 3)
                door_cap_x = rom.read_u8(door_ptr + 4)
                door_cap_y = rom.read_u8(door_ptr + 5)
                screen_x = rom.read_u8(door_ptr + 6)
                screen_y = rom.read_u8(door_ptr + 7)
                dist_spawn = rom.read_u16(door_ptr + 8)
                door_asm = rom.read_u16(door_ptr + 10)
                self.doors.append(Door(
                    door_ptr=door_ptr,
                    dest_room_ptr=dest_room_ptr,
                    # horizontal=direction in [2, 3, 6, 7],
                    bitflag=bitflag,
                    direction=direction,
                    screen_x=screen_x,
                    screen_y=screen_y,
                    door_cap_x=door_cap_x,
                    door_cap_y=door_cap_y,
                    dist_spawn=dist_spawn,
                ))
                # print(f'{dest_room_ptr:x} {bitflag} {direction} {door_cap_x} {door_cap_y} {screen_x} {screen_y} {dist_spawn:x} {door_asm:x}')

        def save_doors(self, rom):
            for door in self.doors:
                door_ptr = door.door_ptr
                rom.write_u16(door_ptr, door.dest_room_ptr)
                rom.write_u8(door_ptr + 2, door.bitflag)
                rom.write_u8(door_ptr + 3, door.direction)
                rom.write_u8(door_ptr + 4, door.door_cap_x)
                rom.write_u8(door_ptr + 5, door.door_cap_y)
                rom.write_u8(door_ptr + 6, door.screen_x)
                rom.write_u8(door_ptr + 7, door.screen_y)
                rom.write_u16(door_ptr + 8, door.dist_spawn)

        def xy_to_map_ptr(self, x, y):
            base_ptr = area_map_ptrs[self.area]
            y1 = y + 1
            if x < 32:
                offset = (y1 * 32 + x) * 2
            else:
                offset = ((y1 + 32) * 32 + x - 32) * 2
            return base_ptr + offset

        def write_map_data(self, rom):
            # rom.write_u8(self.room_ptr + 1, self.area)
            rom.write_u8(self.room_ptr + 2, self.x)
            rom.write_u8(self.room_ptr + 3, self.y)

            for y in range(self.room.height):
                for x in range(self.room.width):
                    ptr = self.xy_to_map_ptr(x + self.x, y + self.y)
                    if self.room.map[y][x] == 1:
                        rom.write_u16(ptr, self.map_data[y][x])

    orig_rom = Rom(io.BytesIO(input_buf))
    rom = Rom(io.BytesIO(input_buf))

    # Change Aqueduct map y position, to include the toilet (for the purposes of the map)
    old_y = orig_rom.read_u8(0x7D5A7 + 3)
    orig_rom.write_u8(0x7D5A7 + 3, old_y - 4)

    # # Change door asm for entering mother brain room
    orig_rom.write_u16(0x1AAC8 + 10, 0xEB00)
    # rom.write_u16(0x1956A + 10, 0xEB00)

    # Area data: --------------------------------
    area_index_dict = defaultdict(lambda: {})
    for i, room in enumerate(rooms):
        orig_room_area = orig_rom.read_u8(room.rom_address + 1)
        room_index = orig_rom.read_u8(room.rom_address)
        assert room_index not in area_index_dict[orig_room_area]
        area_index_dict[orig_room_area][room_index] = area_arr[i]
    # Handle twin rooms
    aqueduct_room_i = [i for i, room in enumerate(rooms) if room.name == 'Aqueduct'][0]
    area_index_dict[4][0x18] = area_arr[aqueduct_room_i]  # Set Toilet to same area as Aqueduct
    pants_room_i = [i for i, room in enumerate(rooms) if room.name == 'Pants Room'][0]
    area_index_dict[4][0x25] = area_arr[pants_room_i]  # Set East Pants Room to same area as Pants Room
    west_ocean_room_i = [i for i, room in enumerate(rooms) if room.name == 'West Ocean'][0]
    area_index_dict[0][0x11] = area_arr[west_ocean_room_i]  # Set Homing Geemer Room to same area as West Ocean
    # Write area data
    area_sizes = [max(area_index_dict[i].keys()) + 1 for i in range(num_areas)]
    cumul_area_sizes = [0] + list(np.cumsum(area_sizes))
    area_data_base_ptr = 0x7E99B  # LoRom $8F:E99B
    area_data_ptrs = [area_data_base_ptr + num_areas * 2 + cumul_area_sizes[i] for i in range(num_areas)]
    assert area_data_ptrs[-1] <= 0x7EB00
    for i in range(num_areas):
        rom.write_u16(area_data_base_ptr + 2 * i, (area_data_ptrs[i] & 0x7FFF) + 0x8000)
        for room_index, new_area in area_index_dict[i].items():
            rom.write_u8(area_data_ptrs[i] + room_index, new_area)

    # print("{:x}".format(area_data_ptrs[-1] + area_sizes[-1]))

    # Write map data:
    # first clear existing maps
    for area_id, area_ptr in area_map_ptrs.items():
        for i in range(64 * 32):
            # if area_id == 0:
            #     rom.write_u16(area_ptr + i * 2, 0x0C1F)
            # else:
            rom.write_u16(area_ptr + i * 2, 0x001F)

    area_start_x = []
    area_start_y = []
    for i in range(num_areas):
        ind = np.where(area_arr == i)
        area_start_x.append(np.min(xs_min[ind]) - 2)
        area_start_y.append(np.min(ys_min[ind]) - 1)

    for i, room in enumerate(rooms):
        rom_room = RomRoom(orig_rom, room)
        area = area_arr[i]
        rom_room.area = area
        rom_room.x = xs_min[i] - area_start_x[area]
        rom_room.y = ys_min[i] - area_start_y[area]
        rom_room.write_map_data(rom)
        if room.name == 'Aqueduct':
            # Patch map tile in Aqueduct to replace Botwoon Hallway with tube/elevator tile
            cell = rom.read_u16(rom_room.xy_to_map_ptr(rom_room.x + 2, rom_room.y + 2))
            rom.write_u16(rom_room.xy_to_map_ptr(rom_room.x + 2, rom_room.y + 3), cell)

    def write_door_data(ptr, data):
        if ptr in (0x1A600, 0x1A60C):
            # Avoid overwriting the door ASM leaving the toilet room. Otherwise Samus will be stuck,
            # unable to be controlled. This is only quick hack because by not applying the door ASM for
            # the next room, this can mess up camera scrolls and other things. (At some point,
            # maybe figure out how we can patch both ASMs together.)
            rom.write_n(ptr, 10, data[:10])
        else:
            rom.write_n(ptr, 12, data)
        bitflag = data[2] | 0x40
        rom.write_u8(ptr + 2, bitflag)
        # print("{:x}".format(bitflag))

    def write_door_connection(a, b):
        a_exit_ptr, a_entrance_ptr = a
        b_exit_ptr, b_entrance_ptr = b
        if a_entrance_ptr is not None and b_exit_ptr is not None:
            # print('{:x},{:x}'.format(a_entrance_ptr, b_exit_ptr))
            a_entrance_data = orig_rom.read_n(a_entrance_ptr, 12)
            write_door_data(b_exit_ptr, a_entrance_data)
            # rom.write_n(b_exit_ptr, 12, a_entrance_data)
        if b_entrance_ptr is not None and a_exit_ptr is not None:
            b_entrance_data = orig_rom.read_n(b_entrance_ptr, 12)
            write_door_data(a_exit_ptr, b_entrance_data)
            # rom.write_n(a_exit_ptr, 12, b_entrance_data)
            # print('{:x} {:x}'.format(b_entrance_ptr, a_exit_ptr))

    for (a, b, _) in list(map['doors']):
        write_door_connection(a, b)

    save_station_ptrs = [
        0x44C5,
        0x44D3,
        0x45CF,
        0x45DD,
        0x45EB,
        0x45F9,
        0x4607,
        0x46D9,
        0x46E7,
        0x46F5,
        0x4703,
        0x4711,
        0x471F,
        0x481B,
        0x4917,
        0x4925,
        0x4933,
        0x4941,
        0x4A2F,
        0x4A3D,
    ]

    area_save_ptrs = [0x44C5, 0x45CF, 0x46D9, 0x481B, 0x4917, 0x4A2F]

    orig_door_dict = {}
    for room in rooms:
        for door in room.door_ids:
            orig_door_dict[door.exit_ptr] = door.entrance_ptr
            # if door.exit_ptr is not None:
            #     door_asm = orig_rom.read_u16(door.exit_ptr + 10)
            #     if door_asm != 0:
            #         print("{:x}".format(door_asm))

    door_dict = {}
    for (a, b, _) in map['doors']:
        a_exit_ptr, a_entrance_ptr = a
        b_exit_ptr, b_entrance_ptr = b
        if a_exit_ptr is not None and b_exit_ptr is not None:
            door_dict[a_exit_ptr] = b_exit_ptr
            door_dict[b_exit_ptr] = a_exit_ptr

    # Fix save stations
    for ptr in save_station_ptrs:
        orig_entrance_door_ptr = orig_rom.read_u16(ptr + 2) + 0x10000
        exit_door_ptr = orig_door_dict[orig_entrance_door_ptr]
        entrance_door_ptr = door_dict[exit_door_ptr]
        rom.write_u16(ptr + 2, entrance_door_ptr & 0xffff)
    #
    # # Fix save stations
    # room_ptr_to_idx = {room.rom_address: i for i, room in enumerate(rooms)}
    # area_save_idx = {x: 0 for x in range(6)}
    # area_save_idx[0] = 1  # Start Crateria index at 1 since we keep ship save station as is.
    # for ptr in save_station_ptrs:
    #     room_ptr = orig_rom.read_u16(ptr) + 0x70000
    #     if room_ptr != 0x791F8:  # The ship has no Save Station PLM for us to update (and we don't need to since we keep the ship in Crateria)
    #         room_obj = Room(orig_rom, room_ptr)
    #         states = room_obj.load_states(orig_rom)
    #         plm_ptr = states[0].plm_set_ptr + 0x70000
    #         plm_type = orig_rom.read_u16(plm_ptr)
    #         assert plm_type == 0xB76F  # Check that the first PLM is a save station
    #
    #         area = cs[room_ptr_to_idx[room_ptr]]
    #         idx = area_save_idx[area]
    #         rom.write_u16(plm_ptr + 4, area_save_idx[area])
    #         area_save_idx[area] += 1
    #
    #         orig_save_station_bytes = orig_rom.read_n(ptr, 14)
    #         dst_ptr = area_save_ptrs[area] + 14 * idx
    #         rom.write_n(dst_ptr, 14, orig_save_station_bytes)
    #     else:
    #         area = 0
    #         dst_ptr = ptr
    #
    #     orig_entrance_door_ptr = rom.read_u16(dst_ptr + 2) + 0x10000
    #     exit_door_ptr = orig_door_dict[orig_entrance_door_ptr]
    #     entrance_door_ptr = door_dict[exit_door_ptr] & 0xffff
    #     rom.write_u16(dst_ptr + 2, entrance_door_ptr & 0xffff)

    # item_dict = {}
    for room_obj in rooms:
        room = RomRoom(orig_rom, room_obj)
        states = room.load_states(rom)
        for state in states:
            if room_obj.name == 'Pit Room' and state == 0xE652:
                # Leave grey doors in post-Missile Pit Room intact, to leave a way to trigger Zebes becoming awake.
                continue
            ptr = state.plm_set_ptr + 0x70000
            while True:
                plm_type = orig_rom.read_u16(ptr)
                if plm_type == 0:
                    break
                # if plm_type in (0xC842, 0xC848, 0xC84E, 0xC854):
                #     print('{}: {:04x} {:04x}'.format(room_obj.name, rom.read_u16(ptr + 2), rom.read_u16(ptr + 4)))
                #     rom.write_u8(ptr + 5, 0x0)  # main boss dead
                #     # rom.write_u8(ptr + 5, 0x0C)  # enemies dead

                # # Collect item ids
                # if (plm_type >> 8) in (0xEE, 0xEF):
                #     item_type_index = rando.conditions.get_plm_type_item_index(plm_type)
                #     print("{}: {}".format(room_obj.name, rando.conditions.item_list[item_type_index]))
                #     item_dict[ptr] = plm_type
                #     # print("{:x} {:x} {:x}".format(ptr, plm_type, item_id))

                # Turn non-blue doors blue
                if plm_type in (0xC88A, 0xC842, 0xC85A, 0xC872):  # right grey/yellow/green door
                    # print('{}: {:x} {:x} {:x}'.format(room_obj.name, rom.read_u16(ptr), rom.read_u16(ptr + 2), rom.read_u16(ptr + 4)))
                    # rom.write_u16(ptr, 0xC88A)  # right pink door
                    rom.write_u16(ptr, 0xB63B)  # right continuation arrow (should have no effect, giving a blue door)
                    rom.write_u16(ptr + 2, 0)  # position = (0, 0)
                elif plm_type in (0xC890, 0xC848, 0xC860, 0xC878):  # left grey/yellow/green door
                    # rom.write_u16(ptr, 0xC890)  # left pink door
                    rom.write_u16(ptr, 0xB63B)  # right continuation arrow (should have no effect, giving a blue door)
                    rom.write_u16(ptr + 2, 0)  # position = (0, 0)
                elif plm_type in (0xC896, 0xC84E, 0xC866, 0xC87E):  # down grey/yellow/green door
                    # rom.write_u16(ptr, 0xC896)  # down pink door
                    rom.write_u16(ptr, 0xB63B)  # right continuation arrow (should have no effect, giving a blue door)
                    rom.write_u16(ptr + 2, 0)  # position = (0, 0)
                elif plm_type in (0xC89C, 0xC854, 0xC86C, 0xC884):  # up grey/yellow/green door
                    # rom.write_u16(ptr, 0xC89C)  # up pink door
                    rom.write_u16(ptr, 0xB63B)  # right continuation arrow (should have no effect, giving a blue door)
                    rom.write_u16(ptr + 2, 0)  # position = (0, 0)
                elif plm_type in (0xDB48, 0xDB4C, 0xDB52, 0xDB56, 0xDB5A, 0xDB60):  # eye doors
                    rom.write_u16(ptr, 0xB63B)  # right continuation arrow (should have no effect, giving a blue door)
                    rom.write_u16(ptr + 2, 0)  # position = (0, 0)
                elif plm_type in (0xC8CA,):  # wall in Escape Room 1
                    rom.write_u16(ptr, 0xB63B)  # right continuation arrow (should have no effect, giving a blue door)
                    rom.write_u16(ptr + 2, 0)  # position = (0, 0)
                ptr += 6

    def item_to_plm_type(item_name, orig_plm_type):
        item_list = [
            "ETank",
            "Missile",
            "Super",
            "PowerBomb",
            "Bombs",
            "Charge",
            "Ice",
            "HiJump",
            "SpeedBooster",
            "Wave",
            "Spazer",
            "SpringBall",
            "Varia",
            "Gravity",
            "XRayScope",
            "Plasma",
            "Grapple",
            "SpaceJump",
            "ScrewAttack",
            "Morph",
            "ReserveTank",
        ]
        i = item_list.index(item_name)
        old_i = ((orig_plm_type - 0xEED7) // 4) % 21
        return orig_plm_type + (i - old_i) * 4

    # Place items
    for i in range(len(randomizer.item_placement_list)):
        ptr = randomizer.item_placement_list[i]
        item_name = randomizer.item_sequence[i]
        orig_plm_type = orig_rom.read_u16(ptr)
        plm_type = item_to_plm_type(item_name, orig_plm_type)
        rom.write_u16(ptr, plm_type)

    # Make whole map revealed (after getting map station), i.e. no more "secret rooms" that don't show up in map.
    for i in range(0x11727, 0x11D27):
        rom.write_u8(i, 0xFF)

    # print(randomizer.item_sequence[:5])
    # print(randomizer.item_placement_list[:5])
    # sm_json_data.node_list[641]

    # # Randomize items
    # item_list = list(item_dict.values())
    # item_perm = np.random.permutation(len(item_dict.values()))
    # for i, ptr in enumerate(item_dict.keys()):
    #     item = item_list[item_perm[i]]
    #     rom.write_u16(ptr, item)

    # rom.write_u16(0x78000, 0xC82A)
    # rom.write_u8(0x78002, 40)
    # rom.write_u8(0x78003, 68)
    # rom.write_u16(0x78004, 0x8000)

    # ---- Fix twin room map x & y:
    # Aqueduct:
    old_aqueduct_x = rom.read_u8(0x7D5A7 + 2)
    old_aqueduct_y = rom.read_u8(0x7D5A7 + 3)
    rom.write_u8(0x7D5A7 + 3, old_aqueduct_y + 4)
    # Toilet:
    rom.write_u8(0x7D408 + 2, old_aqueduct_x + 2)
    rom.write_u8(0x7D408 + 3, old_aqueduct_y)
    # East Pants Room:
    pants_room_x = rom.read_u8(0x7D646 + 2)
    pants_room_y = rom.read_u8(0x7D646 + 3)
    rom.write_u8(0x7D69A + 2, pants_room_x + 1)
    rom.write_u8(0x7D69A + 3, pants_room_y + 1)
    # Homing Geemer Room:
    west_ocean_x = rom.read_u8(0x793FE + 2)
    west_ocean_y = rom.read_u8(0x793FE + 3)
    rom.write_u8(0x7968F + 2, west_ocean_x + 5)
    rom.write_u8(0x7968F + 3, west_ocean_y + 2)

    # Apply patches
    patches = [
        'vanilla_bugfixes',
        'new_game',
        # 'new_game_extra',
        'music',
        'crateria_sky',
        'everest_tube',
        'sandfalls',
        'escape_room_1',
        'saveload',
        'map_area',
        'mb_barrier',
        'mb_barrier_clear',
        # Seems to incompatible with fast_doors due to race condition with how level data is loaded (which fast_doors speeds up)?
        # 'fast_doors',
        'elevators_speed',
        'boss_exit',
        'itemsounds',
        'progressive_suits',
        'disable_map_icons',
        'escape',
    ]
    for patch_name in patches:
        patch = ips_util.Patch.load('patches/ips/{}.ips'.format(patch_name))
        rom.byte_buf = patch.apply(rom.byte_buf)

    # rom.write_u16(0x79213 + 24, 0xEB00)
    # rom.write_u16(0x7922D + 24, 0xEB00)
    # rom.write_u16(0x79247 + 24, 0xEB00)
    # rom.write_u16(0x79247 + 24, 0xEB00)
    # rom.write_u16(0x79261 + 24, 0xEB00)

    # Connect bottom left landing site door to mother brain room, for testing
    # mb_door_bytes = orig_rom.read_n(0X1AAC8, 12)
    # rom.write_n(0x18916, 12, mb_door_bytes)

    # Change setup asm for Mother Brain room
    rom.write_u16(0x7DD6E + 24, 0xEB00)

    # Change door exit asm for boss rooms (TODO: do this better, in case entrance asm is needed in next room)
    boss_exit_asm = 0xF7F0
    # Kraid:
    rom.write_u16(0x191CE + 10, boss_exit_asm)
    rom.write_u16(0x191DA + 10, boss_exit_asm)
    # Draygon:
    rom.write_u16(0x1A978 + 10, boss_exit_asm)
    rom.write_u16(0x1A96C + 10, boss_exit_asm)

    memory_file = BytesIO()
    files = [
        (output_file_prefix + '.sfc', rom.byte_buf),
        (output_file_prefix + '.json', json.dumps(spoiler_data, indent=2)),
        (output_file_prefix + '.png', map_png_bytes),
        (output_file_prefix + '-orig.png', map_orig_png_bytes),
    ]
    with zipfile.ZipFile(memory_file, 'w') as zf:
        for file_name, file_data in files:
            data = zipfile.ZipInfo(file_name)
            data.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(data, file_data)
    memory_file.seek(0)
    return flask.send_file(memory_file, download_name=output_file_prefix + '.zip')

    # return flask.send_file(io.BytesIO(rom.byte_buf), mimetype='application/octet-stream', download_name=output_filename)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
