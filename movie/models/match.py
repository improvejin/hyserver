from base.models.base import MatchMovieBase


class MatchMovieMT2DB(MatchMovieBase):

    class Meta:
        db_table = 'match_movie_lm2db'
        managed = False


class MatchMovieLM2DB(MatchMovieBase):

    class Meta:
        db_table = 'match_movie_lm2db'
        managed = False


class MatchMovieTB2DB(MatchMovieBase):

    class Meta:
        db_table = 'match_movie_tb2db'
        managed = False

