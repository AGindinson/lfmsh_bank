from enum import Enum


class AttendanceTypeEnum(Enum):
    workout = 'workout'
    seminar_pass = 'seminar_pass'
    seminar_attend = 'seminar_attend'
    fac_attend = 'fac_attend'
    fac_pass = 'fac_pass'
    lecture_attend = 'lecture_attend'
    lecture_miss = 'lecture_miss'
