# Gestire il relogin se già loggato, in teoria con utilizzo corretto impossibile che accada.
# in caso di richiamo a endpoint redirect a dashboard se filealreadyexist


from datetime import datetime, timedelta
import config
import os
from pandas import DataFrame, Series, read_parquet
from dataclasses import dataclass


@dataclass()
class CacheFile:
    filename: str
    root: str = config.CACHES_FOLDER
    data: DataFrame = DataFrame(columns=['Name', 'Value', 'Domain', 'Path', 'Expires', 'Secure', 'SameSite'])
    expirationDate: datetime = datetime.timestamp(datetime.now()) + config.DEFAULT_EXPIRATION_TIME

    def createSessionFile(self, identifier: str) -> None:
        if not os.path.exists(config.CACHES_FOLDER + self.filename + config.CACHE_ENGINE):
            self.append([config.FIRST_CACHE_NAME, identifier, config.DOMAIN, "/", self.expirationDate])
            self.save()
        else:
            raise FileExistsError

    def checkSessionFile(self) -> datetime:
        data = self.read()
        if data[:1]["Expires"] == self.expirationDate:
            self.delete()
            return None
        else:
            return self.expirationDate

    def read(self) -> DataFrame:
        try:
            return read_parquet(config.CACHES_FOLDER + self.filename + config.CACHE_ENGINE)
        except FileNotFoundError as e:
            raise e

    def save(self) -> None:
        self.data.to_parquet(
            config.CACHES_FOLDER + self.filename + config.CACHE_ENGINE, compression='gzip')

    def delete(self) -> None:
        try:
            os.remove(config.CACHES_FOLDER +
                      self.filename + config.CACHE_ENGINE)
        except FileNotFoundError as e:
            raise e

    def append(self, values : list) -> bool:
        """[summary]

        Args:
            Name (str): [description]
            Value (str): [description]
            Domain (str): [description]
            Path (str, optional): [description]. Defaults to "/".
            Expires (int, optional): [description]. Defaults to 3600.
            Secure (str, optional): [description]. Defaults to "YES".
            Samesite (str, optional): [description]. Defaults to "YES".

        Returns:
            bool: [description]
        """
        try:
            self.data = self.read()
            self.data.loc[len(self.data.index)] = Series(
                [item for item in values], index=self.data.columns)
            return True
        except FileNotFoundError:
            return False
