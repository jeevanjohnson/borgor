import lzma
import struct
from enum import Enum
from enum import unique 
from enum import IntFlag
from textwrap import wrap
from typing import Optional

str_to_num = {
    'osu': 0,
    'taiko': 1,
    'fruits': 2,
    'mania': 3
}

@unique
class Gamemode(Enum):
    STD = 'osu'
    Taiko = 'taiko'
    Ctb = 'fruits'
    Mania = 'mania'

    def _as_int(self) -> int:
        """Use this if `Gamemode.as_int` doesn't work"""
        return str_to_num[self._value_]

    @property
    def as_int(self) -> int:
        return str_to_num[self._value_]
    
    @classmethod
    def from_int(cls, i: int) -> 'Gamemode':
        return (cls.STD, cls.Taiko, cls.Ctb, cls.Mania)[i]

@unique
class Mods(IntFlag):
    NOMOD = 0
    NOFAIL = 1 << 0
    EASY = 1 << 1
    TOUCHSCREEN = 1 << 2 # old: 'NOVIDEO'
    HIDDEN = 1 << 3
    HARDROCK = 1 << 4
    SUDDENDEATH = 1 << 5
    DOUBLETIME = 1 << 6
    RELAX = 1 << 7
    HALFTIME = 1 << 8
    NIGHTCORE = 1 << 9
    FLASHLIGHT = 1 << 10
    AUTOPLAY = 1 << 11
    SPUNOUT = 1 << 12
    AUTOPILOT = 1 << 13
    PERFECT = 1 << 14
    KEY4 = 1 << 15
    KEY5 = 1 << 16
    KEY6 = 1 << 17
    KEY7 = 1 << 18
    KEY8 = 1 << 19
    FADEIN = 1 << 20
    RANDOM = 1 << 21
    CINEMA = 1 << 22
    TARGET = 1 << 23
    KEY9 = 1 << 24
    KEYCOOP = 1 << 25
    KEY1 = 1 << 26
    KEY3 = 1 << 27
    KEY2 = 1 << 28
    SCOREV2 = 1 << 29
    MIRROR = 1 << 30

    def __repr__(self) -> str:
        """
        Return a string with readable std mods.
        Used to convert a mods number for oppai
        :param m: mods bitwise number
        :return: readable mods string, eg HDDT
        """

        if not self:
            return 'NM'

        # dt/nc is a special case, as osu! will send
        # the mods as 'DTNC' while only NC is applied.
        if self & Mods.NIGHTCORE:
            self &= ~Mods.DOUBLETIME

        return ''.join(v for k, v in mod_to_str.items() if self & k)

    @classmethod
    def from_str(cls, s: str):
        final_mods = 0
        for m in wrap(s.lower(), 2):
            if m not in str_to_mod:
                continue
            
            final_mods += str_to_mod[m]
        
        return cls(final_mods)

str_to_mod = {
    'nm': Mods.NOMOD,
    'ez': Mods.EASY,
    'td': Mods.TOUCHSCREEN,
    'hd': Mods.HIDDEN,
    'hr': Mods.HARDROCK,
    'sd': Mods.SUDDENDEATH,
    'dt': Mods.DOUBLETIME,
    'rx': Mods.RELAX,
    'ht': Mods.HALFTIME,
    'nc': Mods.NIGHTCORE,
    'fl': Mods.FLASHLIGHT,
    'au': Mods.AUTOPLAY,
    'so': Mods.SPUNOUT,
    'ap': Mods.AUTOPILOT,
    'pf': Mods.PERFECT,
    'k1': Mods.KEY1, 
    'k2': Mods.KEY2, 
    'k3': Mods.KEY3, 
    'k4': Mods.KEY4, 
    'k5': Mods.KEY5, 
    'k6': Mods.KEY6, 
    'k7': Mods.KEY7, 
    'k8': Mods.KEY8, 
    'k9': Mods.KEY9,
    'fi': Mods.FADEIN,
    'rn': Mods.RANDOM,
    'cn': Mods.CINEMA,
    'tp': Mods.TARGET,
    'v2': Mods.SCOREV2,
    'co': Mods.KEYCOOP,
    'mi': Mods.MIRROR
}

mod_to_str = {
    Mods.NOFAIL: 'NF',
    Mods.EASY: 'EZ',
    Mods.TOUCHSCREEN: 'TD',
    Mods.HIDDEN: 'HD',
    Mods.HARDROCK: 'HR',
    Mods.SUDDENDEATH: 'SD',
    Mods.DOUBLETIME: 'DT',
    Mods.RELAX: 'RX',
    Mods.HALFTIME: 'HT',
    Mods.NIGHTCORE: 'NC',
    Mods.FLASHLIGHT: 'FL',
    Mods.AUTOPLAY: 'AU',
    Mods.SPUNOUT: 'SO',
    Mods.AUTOPILOT: 'AP',
    Mods.PERFECT: 'PF',
    Mods.KEY4: 'K4',
    Mods.KEY5: 'K5',
    Mods.KEY6: 'K6',
    Mods.KEY7: 'K7',
    Mods.KEY8: 'K8',
    Mods.FADEIN: 'FI',
    Mods.RANDOM: 'RN',
    Mods.CINEMA: 'CN',
    Mods.TARGET: 'TP',
    Mods.KEY9: 'K9',
    Mods.KEYCOOP: 'CO',
    Mods.KEY1: 'K1',
    Mods.KEY3: 'K3',
    Mods.KEY2: 'K2',
    Mods.SCOREV2: 'V2',
    Mods.MIRROR: 'MI'
}

@unique
class Key(IntFlag):
    M1    = 1 << 0
    M2    = 1 << 1
    K1    = 1 << 2
    K2    = 1 << 3
    Smoke = 1 << 4

class LifeBar:
    def __init__(self, delta_time: int, current_hp: float) -> None:
        self.delta_time = delta_time
        self.current_hp = current_hp

    @classmethod
    def from_raw_bar(cls, raw_bar: str) -> 'LifeBar':
        hp = 1.0
        if ',' not in raw_bar:
            return cls(int(raw_bar), hp)
        
        hp, vtime = raw_bar.split(',')
        return cls(int(vtime or 0), float(hp))

class Frame:
    def __init__(
        self, delta_time: float, 
        x: float, y: float, 
        key: Key
    ) -> None:
        self.delta_time = delta_time
        self.x = x
        self.y = y
        self.pressed = key

    @classmethod
    def from_raw_frame(cls, raw_frame: bytes) -> 'Frame':
        w, x, y, z = raw_frame.decode().split('|')
        return cls(
            float(w), float(x), 
            float(y), Key(int(z))
        )

class Replay:
    def __init__(self, raw_replay: bytes) -> None:
        """https://osu.ppy.sh/wiki/en/osu%21_File_Formats/Osr_%28file_format%29"""
        self._data = raw_replay
        self.offset = 0

        self.mode: Optional[Gamemode] = None
        self.version: Optional[int] = None
        self.beatmap_md5: Optional[str] = None
        self.replay_md5: Optional[str] = None
        self.player_name: Optional[str] = None
        self.n300: Optional[int] = None
        self.n100: Optional[int] = None
        self.n50: Optional[int] = None
        self.geki: Optional[int] = None
        self.katu: Optional[int] = None
        self.miss: Optional[int] = None
        self.total_score: Optional[int] = None
        self.combo: Optional[int] = None
        self.perfect: Optional[int] = None
        self.mods: Optional[Mods] = None
        self.bar_graph: Optional[list[LifeBar]] = None
        self.timestamp: Optional[int] = None
        self.score_id: Optional[int] = None
        self.additional_mods: Optional[Mods] = None
        self.frames: Optional[list[Frame]] = None
    
    @property
    def data(self) -> bytes:
        return self._data[self.offset:]
    
    @classmethod
    def from_file(cls, path: str) -> 'Replay':
        with open(path, 'rb') as f:
            replay = cls(f.read())
            replay.parse()
            return replay
    
    @classmethod
    def from_content(cls, content: bytes) -> 'Replay':
        replay = cls(content)
        replay.parse()
        return replay
    
    def parse(self) -> None:
        self.mode = Gamemode.from_int(self.read_byte())
        self.version = self.read_int()
        self.beatmap_md5 = self.read_string()
        self.player_name = self.read_string()
        self.replay_md5 = self.read_string()
        self.n300 = self.read_short()
        self.n100 = self.read_short()
        self.n50 = self.read_short()
        self.geki = self.read_short()
        self.katu = self.read_short()
        self.miss = self.read_short()
        self.total_score = self.read_int()
        self.combo = self.read_short()
        self.perfect = self.read_byte()
        self.mods = Mods(self.read_int())
        self.bar_graph = [LifeBar.from_raw_bar(x) for x in self.read_string().split('|')]
        self.timestamp = self.read_long_long()
        raw_frames: list[bytes] = lzma.decompress(self.read_raw(self.read_int())).split(b',')
        self.frames = [Frame.from_raw_frame(x) for x in raw_frames if x]

        self.scoreid = self.read_long_long()
        
        if self.mods & Mods.TARGET:
            self.additional_mods = self.read_double()

    def build(self) -> bytes:
        buffer = bytearray()
        buffer += self.write_byte(self.mode._value_)
        buffer += self.write_int(self.version)
        buffer += self.write_string(self.beatmap_md5)
        buffer += self.write_string(self.player_name)
        buffer += self.write_string(self.replay_md5)
        buffer += self.write_short(self.n300)
        buffer += self.write_short(self.n100)
        buffer += self.write_short(self.n50)
        buffer += self.write_short(self.geki)
        buffer += self.write_short(self.katu)
        buffer += self.write_short(self.miss)
        buffer += self.write_int(self.total_score)
        buffer += self.write_short(self.combo)
        buffer += self.write_byte(self.perfect)
        buffer += self.write_int(self.mods._value_)
        
        bar_graph = '0,|' + '|'.join([
            f'{lifebar.current_hp},{lifebar.delta_time}' 
            for lifebar in self.bar_graph
        ])
        
        buffer += self.write_string(bar_graph)
        buffer += self.write_long_long(self.timestamp)

        raw_frames = lzma.compress(
            b','.join([
                f'{frame.delta_time}|{frame.x}|{frame.y}|{int(frame.pressed)}'.encode() 
                for frame in self.frames
            ])
        )

        buffer += self.write_int(len(raw_frames))
        buffer += raw_frames
        
        buffer += self.write_long_long(self.score_id or 0)

        if self.mods & Mods.TARGET:
            buffer += self.write_double(self.additional_mods)

        if (d := bytes(buffer) )== self._data:
            print
        else:
            p = len(self._data)
            print

        return bytes(buffer)
    
    def read_byte(self) -> int:
        val, = struct.unpack('<b', self.data[:1])
        self.offset += 1
        return val

    def read_short(self) -> int:
        val, = struct.unpack('<h', self.data[:2])
        self.offset += 2
        return val

    def read_int(self) -> int:
        val, = struct.unpack('<i', self.data[:4])
        self.offset += 4
        return val

    def read_long_long(self) -> int:
        val, = struct.unpack('<q', self.data[:8])
        self.offset += 8
        return val

    def read_double(self) -> int:
        val, = struct.unpack('<d', self.data[:8])
        self.offset += 8
        return val

    def read_uleb128(self) -> int:
        val = shift = 0

        while True:
            b = self.data[0]
            self.offset += 1

            val |= ((b & 0b01111111) << shift)
            if (b & 0b10000000) == 0:
                break


            shift += 7

        return val

    def read_string(self) -> str:
        if self.read_byte() == 0x0b:
            return self.read_raw(self.read_uleb128()).decode()

        return ''

    def read_raw(self, length: int) -> bytes:
        val = self.data[:length]
        self.offset += length
        return val

    def write_double(self, i: int) -> int:
        return struct.pack('<d', i)

    def write_uleb128(self, num: int) -> bytes:
        if num == 0:
            return bytearray(b'\x00')

        ret = bytearray()
        length = 0

        while num > 0:
            ret.append(num & 0b01111111)
            num >>= 7
            if num != 0:
                ret[length] |= 0b10000000
            length += 1

        return bytes(ret)

    def write_string(self, string: str) -> bytes:
        s = string.encode()
        return b'\x0b' + self.write_uleb128(len(s)) + s

    def write_int(self, i: int) -> bytes:
        return struct.pack('<i', i)

    def write_unsigned_int(self, i: int) -> bytes:
        return struct.pack('<I', i)

    def write_float(self, f: float) -> bytes:
        return struct.pack('<f', f)

    def write_byte(self, b: int) -> bytes:
        return struct.pack('<b', b)

    def write_unsigned_byte(self, b: int) -> bytes:
        return struct.pack('<B', b)

    def write_short(self, s: int) -> bytes:
        return struct.pack('<h', s)

    def write_long_long(self, l: int) -> bytes:
        return struct.pack('<q', l)