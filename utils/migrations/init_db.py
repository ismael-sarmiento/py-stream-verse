from sqlalchemy.schema import CreateTable

from common.database import engine
from common.models import User, Movie, Series, UserFavorite, UserWatched

for tbl in [User.__table__, Movie.__table__, Series.__table__,
            UserFavorite.__table__, UserWatched.__table__]:
    print(str(CreateTable(tbl).compile(engine)))
