# Don't use
from .utils import string_to_key
from .utils import isdecimal
from typing import Optional
from typing import Union
from enum import IntEnum
from enum import IntFlag
from enum import Enum

class Bookmark:
    def __init__(self, time_stamp: int) -> None:
        self.time_stamp = time_stamp

class CurvePoint:
    def __init__(self, x: int, y: int) -> None:
        self.x = x 
        self.y = y
    
    @classmethod
    def from_str(cls, s: str) -> 'CurvePoint':
        x,y = s.split(':')
        return cls(int(x), int(y))

class CurveType(Enum):
    Bezier = 'B'
    Centripetal_Catmull_Rom = 'C'
    Linear = 'L'
    Perfect_Circle = 'P'

class HitSample:
    def __init__(
        self, normal_set: int,
        addition_set: int,
        index: int,
        volume: int,
        filename: str
    ) -> None:
        self.normal_set = normal_set
        self.addition_set = addition_set
        self.index = index
        self.volume = volume
        self.filename = filename

class HitObject:
    def __init__(self) -> None:
        self.x: int
        self.y: int
        self._type: int
        self.type: HitObjectType
        self.time_when_object_hit: int
        self.params: Optional[ObjectParams]

class HitObjectType(IntFlag):
    HIT_CIRCLE = 1 << 0
    SLIDER = 1 << 1
    NEW_COMBO = 1 << 2
    SPINNER = 1 << 3
    SKIP_ONE = 1 << 4
    SKIP_TWO = 1 << 5
    SKIP_THREE = 1 << 6
    MANIA_HOLD = 1 << 7

class ObjectParams:
    def __init__(self) -> None:
        ...
    
    @classmethod
    def from_raw_params(
        cls, type: HitObjectType, 
        params: str
    ) -> 'ObjectParams':
        obj = cls()
        print
        """
        if type & HitObjectType.SPINNER:
            obj.end_time = int(params)
        elif (
            type & HitObjectType.Slider or
            type & HitObjectType.New_Combo and # Check this one later
            not type & HitObjectType.Spinner and
            not type & HitObjectType.Color_Skip1 and
            not type &  HitObjectType.Color_Skip2 and
            not type & HitObjectType.Color_Skip3
        ):
            obj.curve_type = params[0]
            params = params[1:].split(',', 1)
            
            obj.curve_points = [CurvePoint.from_str(x) for x in params[0].split('|') if x]
            params = params[1].split(',', 2)
            slides, length, _ = params
            obj.slides = int(slides)
            obj.length = float(length)
            params = params[2].split(',')
            obj.edge_sounds = list(map(int, params[0].split('|')))
            obj.edge_sets = []
            for x in params[1].split('|'):
                normal_set, addition_set = x.split(':', 1)
                obj.edge_sets.append(
                    (int(normal_set), int(addition_set))
                )
        else:
            print
        """

        return obj

class HitSound(IntFlag):
    Normal = 1 << 0
    Whistle = 1 << 1
    Finish = 1 << 2
    Clap = 1 << 3

class Effects(IntFlag):
    Kiai_Enabled = 1 << 0
    Barline = 1 << 3

class SampleSet(IntEnum):
    Default = 0
    Normal = 1
    Soft = 2
    Drum = 3

class TimingPoint:
    def __init__(
        self, start_time: int,
        beat_length: float,
        meter: int,
        sample_set: SampleSet,
        sample_index: int,
        volume: int,
        uninherited: bool,
        effects: Effects
    ) -> None:
        self.start_time = start_time
        self.beat_length = beat_length
        self.meter = meter
        self.sample_set = sample_set
        self.sample_index = sample_index
        self.volume = volume
        self.uninherited = uninherited
        self.effects = effects

class EventType(IntEnum):
    Background = 0
    Video = 1
    Breaks = 2
    Sample = 3
    Sprite = 4

    @classmethod
    def from_str(cls, s: str) -> 'EventType':
        return cls({
            'background': 0,
            'video': 1,
            'breaks': 2,
            'sample': 3,
            'sprite': 4
        }[s.lower()])

class EventParams:
    def __init__(self) -> None:
        # Background
        self.file_name: str
        self.offset_x: int
        self.offset_y: int

        # Video
        ...

        # Breaks
        self.end_time: int

        # Storyboards
        ...
    
    @classmethod
    def from_raw_event_params(
        cls, type: Union[str, int], 
        raw_params: str
    ) -> 'EventParams':
        ep = cls()

        if type == EventType.Background:
            split = raw_params.split(',')
            if len(split) == 1:
                ep.file_name = split[0].strip('"')
            else:
                file_name, offset_x, offset_y = split
                ep.file_name = file_name
                ep.offset_x = int(offset_x)
                ep.offset_y = int(offset_y)
        elif type == EventType.Video:
            ep.file_name = raw_params.strip('"')
        elif type == EventType.Breaks:
            ep.end_time = int(raw_params)
        elif type == EventType.Sample:
            num1, file_name, num2 = raw_params.split(',')
            ep.file_name = file_name
            ep.num1 = float(num1)
            ep.num2 = float(num2)
        else:
            print
        
        return ep

class Event:
    def __init__(
        self, event_type: EventType,
        start_time: int, event_params: EventParams
    ) -> None:
        self.event_type = event_type
        self.start_time = start_time
        self.event_params = event_params

class Beatmap:
    def __init__(self, content: bytes) -> None:
        self.map = content.decode().splitlines()
        self.file_version: int
        self.audio_filename: str
        self.audio_lead_in: int = 0
        self.preview_time: int = -1
        self.countdown: int = 0
        self.sample_set: str = 'Normal'
        self.stack_leniency: float = 0.7
        self.mode: int = 0
        self.letterbox_in_breaks: int = 0
        self.use_skin_sprites: int = 0
        self.overlay_position: str = 'NoChange'
        self.skin_preference: str
        self.epilepsy_warning: int = 0
        self.countdown_offset: int = 0
        self.special_style: int = 0
        self.widescreen_storyboard: int = 0
        self.samples_match_playback_rate: int = 0
        self.bookmarks: list[int] = []
        self.distance_spacing: float
        self.beat_divisor: float
        self.grid_size: int
        self.timeline_zoom: float
        self.title: str
        self.title_unicode: str
        self.artist: str
        self.artist_unicode: str
        self.creator: str
        self.version: str
        self.source: str
        self.tags: list[str] = []
        self.beatmap_id: int
        self.beatmap_set_id: int
        self.hp_drain_rate: float
        self.circle_size: float
        self.overall_difficulty: float
        self.approach_rate: float
        self.slider_multiplier: float
        self.slider_tick_rate: float
        self.combo_colors: list[tuple[int]] = []
        self.slider_track_colors: list[tuple[int]] = []
        self.slider_border_colors: list[tuple[int]] = [] 
        self.events: list[Event] = []
        self.timing_points: list[TimingPoint] = []
        self.hit_objects: list[HitObject] = []
        self.parse()
    
    def modify_metadata(self) -> None:
        self.tags = self.tags.split()

    def parse_file_version(self) -> None:
        version = []
        for char in self.map[0]:
            if char.isdecimal() or char == '.':
                version.append(char)
            
        self.file_version = float(''.join(version))

    def modify_editor(self) -> None:
        if not self.bookmarks:
            return
        elif isinstance(self.bookmarks, int):
            self.bookmarks = [self.bookmarks]
        else:
            self.bookmarks = [Bookmark(int(x)) for x in self.bookmarks.split(',')]

    def parse(self) -> None:
        self.parse_file_version()
        self.parse_section('[General]')
        
        self.parse_section('[Editor]')
        self.modify_editor()

        self.parse_section('[Metadata]')
        self.modify_metadata()

        self.parse_section('[Difficulty]')
        self.parse_section('[Colours]')
        
        self.parse_events()
        self.parse_timing_points()
        self.parse_hit_objects()

    def parse_hit_objects(self) -> None:
        index = self.map.index('[HitObjects]') + 1
        for line in self.map[index:]:
            if not line:
                break
            
            if line[:2] == '//':
                continue

            line = line.split(',', 5)

            obj = HitObject()

            obj.x = int(line[0])
            obj.y = int(line[1])
            obj.time_when_object_hit = int(line[2])
            obj.type = type = int(line[3])
            obj.hit_sound = HitSound(int(line[4]))

            if type & HitObjectType.HIT_CIRCLE:
                if len(line) < 6:
                    obj.hit_sample = HitSample(0, 0, 0, 0, '')
                    obj.params = None
                else:
                    ns, ads, i, volume, filename = line[5].split(':')
                    obj.hit_sample = HitSample(
                        int(ns), int(ads), int(i),
                        int(volume), filename
                    )
                    obj.params = None
            
            elif type & HitObjectType.SLIDER:
                params = ObjectParams()
                _line = line[5].split(',')
                params.curve = CurveType(_line[0][0])
                params.curve_points = []
                for x in _line[0][2:].split('|'):
                    params.curve_points.append(CurvePoint.from_str(x))
                
                params.slides = int(_line[1])
                params.length = float(_line[2])
                params.edge_sounds = []
                params.edge_sets = []
                
                len__line = len(_line)
                if len__line > 3:
                    params.edge_sounds = list(map(int, _line[3].split('|')))
                    
                    if len__line > 4:
                        params.edge_sets = [
                            tuple(map(int, x.split(':', 1))) for x in _line[4].split('|')
                        ]
                
                    
                    if not len__line < 6:
                        ns, ads, i, volume, filename = _line[5].split(':')
                        obj.hit_sample = HitSample(
                            int(ns), int(ads), int(i),
                            int(volume), filename
                        )
                else:
                    obj.hit_sample = HitSample(
                        None, None, None,
                        None, None
                    )
                
                obj.params = params

            elif type & HitObjectType.SPINNER:
                params = ObjectParams()
                
                split = line[5].split(',', 1)
                if len(split) == 1:
                    end_time = split[0]
                    hit_sample = '0:0:0:0:'
                else:
                    end_time, hit_sample = split

                params.end_time = int(end_time)
                ns, ads, i, volume, filename = hit_sample.split(':')
                obj.hit_sample = HitSample(
                    int(ns), int(ads), int(i),
                    int(volume), filename
                )
                obj.params = params
            
            elif type & HitObjectType.MANIA_HOLD:
                params = ObjectParams()
                end_time, hit_sample = line[5].split(':', 1)
                params.end_time = int(end_time)
                ns, ads, i, volume, filename = hit_sample.split(':')
                obj.hit_sample = HitSample(
                    int(ns), int(ads), int(i),
                    int(volume), filename
                )
                obj.params = params

            self.hit_objects.append(obj)

    def parse_timing_points(self) -> None:
        index = self.map.index('[TimingPoints]') + 1
        for line in self.map[index:]:
            if not line:
                break
            
            if line[:2] == '//':
                continue
            
            line = line.split(',')
            start_time = float(line[0])
            beat_length = float(line[1])
            meter = int(line[2])
            sample_set = SampleSet(int(line[3]))
            sample_index = int(line[4])
            volume = int(line[5])
            uninherited = bool(int(line[6]))
            effects = Effects(int(line[7]))

            self.timing_points.append(
                TimingPoint(
                    start_time, beat_length,
                    meter, sample_set,
                    sample_index, volume,
                    uninherited, effects
                )
            )

    def parse_events(self) -> None:
        index = self.map.index('[Events]') + 1
        for line in self.map[index:]:
            if not line:
                break
            
            if line[:2] == '//':
                continue

            event_type, start_time, params = line.split(',', 2)
            if event_type.isdecimal():
                event_type = EventType(int(event_type))
            else:
                event_type = EventType.from_str(event_type)
            
            self.events.append(
                Event(
                    event_type, int(start_time), 
                    EventParams.from_raw_event_params(event_type, params)
                )
            )

    def parse_section(self, section: str) -> None:
        if section not in self.map:
            return
        
        index = self.map.index(section) + 1
        for line in self.map[index:]:
            if not line:
                break
            
            if line[:2] == '//':
                continue

            k, v = line.split(':', 1)
            k = k.strip()
            v = v.strip()

            if v.isdecimal():
                v = int(v)
            elif isdecimal(v):
                v = float(v)
            elif section == '[Colours]':
                rgb = tuple(map(int, v.split(',')))
                if 'Combo' in k:
                    self.combo_colors.append(rgb)
                elif 'track' in k:
                    self.slider_track_colors.append(rgb)
                else:
                    self.slider_border_colors.append(rgb)
                
                continue

            self.__dict__[string_to_key(k)] = v

import os
song_folder = '/mnt/c/Users/imeas/AppData/Local/osu!/Songs'
for map_path in os.listdir(song_folder):
    for m in os.listdir(f'{song_folder}/{map_path}'):
        if not m.endswith('.osu'):
            continue

        with open(f'{song_folder}/{map_path}/{m}', 'rb') as f: 
            balls = Beatmap(f.read())