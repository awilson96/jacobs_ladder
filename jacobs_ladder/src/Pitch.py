import struct
from dataclasses import dataclass

@dataclass
class PitchInfo:
    analog_value_abs: int = 8192
    analog_value_rel: int = 0
    ratio: str = "1/1"
    cents: float = 0.0
    direction: str = "none"
    note_order: int = -1

    def serialize(self) -> bytes:
        """Convert the PitchInfo into bytes for sending over UDP.

        Format:
        - analog_value_abs: 2 bytes unsigned short
        - analog_value_rel: 2 bytes signed short
        - cents: 4 bytes float
        - note_order: 2 bytes signed short
        - ratio: 10 bytes ASCII, padded with spaces
        - direction: 1 byte ('u', 'd', or 'n')
        Total: 21 bytes
        """

        if self.direction == "up":
            dir_byte = b"u"
        elif self.direction == "down":
            dir_byte = b"d"
        else:
            dir_byte = b"n"

        ratio_bytes = self.ratio.encode("ascii", errors="ignore")[:10].ljust(10, b" ")

        core = struct.pack(
            ">Hhfh10s",
            self.analog_value_abs,
            self.analog_value_rel,
            self.cents,
            self.note_order,
            ratio_bytes,
        )

        return core + dir_byte


pitches = {
    "minor_second_up": PitchInfo(8673, 8673 - 8192, "16/15", +11.731, "up"),
    "major_second_up": PitchInfo(8352, 8352 - 8192, "9/8", +3.910, "up"),
    "major_second_harmonic_up": PitchInfo(9469, 9469 - 8192, "8/7", +31.173, "up"),
    "major_second_flat_up": PitchInfo(7471, 7471 - 8192, "10/9", -17.596, "up"),
    "major_second_half_flat_up": PitchInfo(6355, 6355 - 8192, "35/32", -55.140, "up"),
    "minor_third_up": PitchInfo(8833, 8833 - 8192, "6/5", +15.641, "up"),
    "minor_third_harmonic_up": PitchInfo(6835, 6835 - 8192, "7/6", -33.129, "up"),
    "major_third_up": PitchInfo(7631, 7631 - 8192, "5/4", -13.686, "up"),
    "perfect_fourth_up": PitchInfo(8112, 8112 - 8192, "4/3", -1.955, "up"),
    "perfect_fourth_sharp_up": PitchInfo(8993, 8993 - 8192, "27/20", +19.551, "up"),
    "tritone_up": PitchInfo(7792, 7792 - 8192, "45/32", -9.776, "up"),
    "tritone_sharp_up": PitchInfo(8592, 8592 - 8192, "64/45", +9.776, "up"),
    "perfect_fifth_up": PitchInfo(8272, 8272 - 8192, "3/2", +1.955, "up"),
    "minor_sixth_up": PitchInfo(8753, 8753 - 8192, "8/5", +13.686, "up"),
    "major_sixth_up": PitchInfo(7551, 7551 - 8192, "5/3", -15.641, "up"),
    "major_sixth_sharp_up": PitchInfo(8432, 8432 - 8192, "27/16", +5.865, "up"),
    "major_sixth_half_flat_up": PitchInfo(6435, 6435 - 8192, "105/64", +57.095, "up"),
    "minor_seventh_up": PitchInfo(8913, 8913 - 8192, "9/5", +17.596, "up"),
    "minor_harmonic_seventh_up": PitchInfo(6915, 6915 - 8192, "7/4", -31.173, "up"),
    "minor_seventh_symetric_up": PitchInfo(8032, 8032 - 8192, "16/9", -3.910, "up"),
    "major_seventh_up": PitchInfo(7711, 7711 - 8192, "15/8", -11.731, "up"),
    "minor_second_down": PitchInfo(7711, 7711 - 8192, "15/16", -11.731, "down"),
    "major_second_down": PitchInfo(8032, 8032 - 8192, "8/9", -3.910, "down"),
    "major_second_harmonic_down": PitchInfo(6915, 6915 - 8192, "7/8", -31.173, "down"),
    "major_second_flat_down": PitchInfo(8913, 8913 - 8192, "9/10", +17.596, "down"),
    "major_second_half_flat_down": PitchInfo(10029, 10029 - 8192, "32/35", +55.140, "down"),
    "minor_third_down": PitchInfo(7551, 7551 - 8192, "5/6", -15.641, "down"),
    "minor_third_harmonic_down": PitchInfo(9549, 9549 - 8192, "6/7", +33.129, "down"),
    "major_third_down": PitchInfo(8753, 8753 - 8192, "4/5", +13.686, "down"),
    "perfect_fourth_down": PitchInfo(8272, 8272 - 8192, "3/4", +1.955, "down"),
    "perfect_fourth_sharp_down": PitchInfo(7391, 7391 - 8192, "20/27", -19.551, "down"),
    "tritone_down": PitchInfo(8592, 8592 - 8192, "32/45", +9.776, "down"),
    "tritone_sharp_down": PitchInfo(7792, 7792 - 8192, "45/64", -9.776, "down"),
    "perfect_fifth_down": PitchInfo(8112, 8112 - 8192, "2/3", -1.955, "down"),
    "minor_sixth_down": PitchInfo(7631, 7631 - 8192, "5/8", -13.686, "down"),
    "major_sixth_down": PitchInfo(8833, 8833 - 8192, "3/5", +15.641, "down"),
    "major_sixth_sharp_down": PitchInfo(7952, 7952 - 8192, "16/27", -5.865, "down"),
    "major_sixth_half_flat_down": PitchInfo(9949, 9949 - 8192, "64/105", -57.095, "down"),
    "minor_seventh_down": PitchInfo(7471, 7471 - 8192, "5/9", -17.596, "down"),
    "minor_harmonic_seventh_down": PitchInfo(9469, 9469 - 8192, "4/7", +31.173, "down"),
    "minor_seventh_symetric_down": PitchInfo(8352, 8352 - 8192, "9/16", +3.910, "down"),
    "major_seventh_down": PitchInfo(9153, 9153 - 8192, "8/15", +11.731, "down"),
    "octave": PitchInfo(8192, 8192 - 8192, "2/1", 0.0, "up"),
}

# Map absolute analog value -> pitch name
analog_to_name = {info.analog_value_abs: name for name, info in pitches.items()}

def get_preferred_interval_name(analog_value: int) -> str | None:
    """Return the pitch name given an absolute analog value."""
    return analog_to_name.get(analog_value)