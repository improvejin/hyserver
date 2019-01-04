from base.models.base import MatchCinemaBase


class MatchCinemaLM2MT(MatchCinemaBase):

    class Meta:
        db_table = 'match_cinema_lm2mt'
        managed = False


class MatchCinemaTB2MT(MatchCinemaBase):

    class Meta:
        db_table = 'match_cinema_tb2mt'
        managed = False

