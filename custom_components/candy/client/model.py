from dataclasses import dataclass
from enum import Enum
from typing import Optional


class MachineState(Enum):
    IDLE = 1
    RUNNING = 2
    PAUSED = 3
    DELAYED_START_SELECTION = 4
    DELAYED_START_PROGRAMMED = 5
    ERROR = 6
    FINISHED = 7

    def __str__(self):
        if self == MachineState.IDLE:
            return "Idle"
        elif self == MachineState.RUNNING:
            return "Running"
        elif self == MachineState.PAUSED:
            return "Paused"
        elif self == MachineState.DELAYED_START_SELECTION:
            return "Delayed start selection"
        elif self == MachineState.DELAYED_START_PROGRAMMED:
            return "Delayed start programmed"
        elif self == MachineState.ERROR:
            return "Error"
        elif self == MachineState.FINISHED:
            return "Finished"
        else:
            return "%s" % self


class WashProgramState(Enum):
    STOPPED = 0
    PRE_WASH = 1
    WASH = 2
    RINSE = 3
    LAST_RINSE = 4
    END = 5
    DRYING = 6
    ERROR = 7
    STEAM = 8
    GOOD_NIGHT = 9  # TODO: GN pause?
    SPIN = 10

    def __str__(self):
        if self == WashProgramState.STOPPED:
            return "Stopped"
        elif self == WashProgramState.PRE_WASH:
            return "Pre-wash"
        elif self == WashProgramState.WASH:
            return "Wash"
        elif self == WashProgramState.RINSE:
            return "Rinse"
        elif self == WashProgramState.LAST_RINSE:
            return "Last rinse"
        elif self == WashProgramState.END:
            return "End"
        elif self == WashProgramState.DRYING:
            return "Drying"
        elif self == WashProgramState.ERROR:
            return "Error"
        elif self == WashProgramState.STEAM:
            return "Steam"
        elif self == WashProgramState.GOOD_NIGHT:
            return "Spin - Good Night"
        elif self == WashProgramState.SPIN:
            return "Spin"
        else:
            return "%s" % self


class DryerProgramState(Enum):
    STOPPED = 0
    DRYING = 2
    HANG_LEVEL = 3
    IRON_LEVEL = 4

    # TODO: values

    def __str__(self):
        if self == DryerProgramState.STOPPED:
            return "Stopped"
        if self == DryerProgramState.DRYING:
            return "Drying"
        if self == DryerProgramState.HANG_LEVEL:
            return "Hang Level Reached"
        if self == DryerProgramState.IRON_LEVEL:
            return "Iron Level Reached"
        else:
            return "%s" % self

class DryLevelState(Enum):
    WET = 1 # TODO
    HANG = 2
    IRON = 3
    CLOSET = 4


    def __str__(self):
        if self == DryLevelState.WET:
            return "Wet"
        if self == DryLevelState.HANG:
            return "Ready to Hang"
        if self == DryLevelState.IRON:
            return "Ready to Iron"
        if self == DryLevelState.CLOSET:
            return "Ready for Closet"
        else:
            return "%s" % self


@dataclass
class WashingMachineStatus:
    machine_state: MachineState
    program_state: WashProgramState
    program: int
    temp: int
    spin_speed: int
    remaining_minutes: int
    remote_control: bool
    fill_percent: Optional[int]  # 0...100

    @classmethod
    def from_json(cls, json):
        return cls(
            machine_state=MachineState(int(json["MachMd"])),
            program_state=WashProgramState(int(json["PrPh"])),
            program=int(json["Pr"]),
            temp=int(json["Temp"]),
            spin_speed=int(json["SpinSp"]) * 100,
            remaining_minutes=round(int(json["RemTime"]) / 60),
            remote_control=json["WiFiStatus"] == "1",
            fill_percent=int(json["FillR"]) if "FillR" in json else None
        )


@dataclass
class TumbleDryerStatus:
    machine_state: MachineState
    dry_level_state: DryLevelState
    program_state: DryerProgramState
    program: int
    remaining_minutes: int
    remote_control: bool
    water_tank_full: bool
    clean_filter: bool

    @classmethod
    def from_json(cls, json):
        return cls(
            machine_state=MachineState(int(json["StatoTD"])),  # TODO? 
            dry_level_state=DryLevelState(int(json["DryLev"])),
            machine_state=MachineState(int(json["StatoTD"])),  # TODO?
            program_state=DryerProgramState(int(json["PrPh"])),
            program=int(json["Pr"]),
            remaining_minutes=int(json["RemTime"]),  # Its in minutes
            remote_control=json["StatoWiFi"] == "1",
            water_tank_full=json["WaterTankFull"] != "0",
            clean_filter=json["CleanFilter"] != "0",
        )


class OvenState(Enum):
    IDLE = 0
    HEATING = 1

    def __str__(self):
        if self == OvenState.IDLE:
            return "Idle"
        elif self == OvenState.HEATING:
            return "Heating"
        else:
            return "%s" % self


@dataclass
class OvenStatus:
    machine_state: OvenState
    program: int
    selection: int
    temp: float
    temp_reached: bool
    program_length_minutes: int
    remote_control: bool

    @classmethod
    def from_json(cls, json):
        return cls(
            machine_state=OvenState(int(json["StartStop"])),
            program=int(json["Program"]),
            selection=int(json["Selettore"]),
            temp=round(fahrenheit_to_celsius(int(json["TempRead"]))),
            temp_reached=json["TempSetRaggiunta"] == "1",
            program_length_minutes=int(json["TimeProgr"]),
            remote_control=json["StatoWiFi"] == "1",
        )


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    return (fahrenheit - 32) * 5.0 / 9.0
