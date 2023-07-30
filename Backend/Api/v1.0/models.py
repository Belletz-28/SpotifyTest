from typing import Optional
import datetime
from IPython.core.display import JSON
from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import List, Any

# Enum classes
class Endpoint(Enum): 
    ARTIST = "Artists"
    TRACKS = "Tracks"
    ALBUMS = "Albums"

class Album(Enum):
    COMPILATION = "compilation"
    ALBUM = "album"
    SINGLE = "single"

class Href(Enum):
    MARKET = "market"
    STRING = ""
    
class AvailableMarket(Enum):
    BR = "BR"
    CA = "CA"
    IT = "IT"

class ArtistType(Enum):
    ARTIST = "artist"



class ReleaseDatePrecision(Enum):
    YEAR = "year"

class Genre(Enum):
    GRUNGE = "Grunge"
    PROG_ROCK = "Prog rock"

#l.corsini - m.belletti - 11/08/2021 Gestione ID e URI<
class ID():
    id = str
    def __init__(self, id: str) -> None:
        self.ID = id

class URI():        #Da verificare il tipo di dati processato
    id : ID
    endpoint : Endpoint
    uri = str
    
    def __init__(self, endpoint : Endpoint, id : ID ) -> None:
        """[summary]

        Args:
            endpoint (Endpoint): [Endpoint Type]
            id (ID): [Resource ID]
        """
        self.endpoint = endpoint
        self.id = id
        self.uri = f"spotify:{endpoint}:{id}"
#l.corsini - m.belletti - 11/08/2021 Gestione ID e URI>

class Artist():
    id : ID
    def __init__(self, id) -> None:
        self.id = id

class Welcome8ExternalUrls:
    spotify: Href

    def __init__(self, spotify: Href) -> None:
        self.spotify = spotify

class Image:
    url: str
    height: int
    width: int

    def __init__(self, url: str, height: int, width: int) -> None:
        self.url = url
        self.height = height
        self.width = width

class Restrictions:
    reason: Href

    def __init__(self, reason: Href) -> None:
        self.reason = reason

class Welcome8Album:
    album_type: Album
    total_tracks: int
    available_markets: List[AvailableMarket]
    external_urls: Welcome8ExternalUrls
    href: Href
    id: ID
    images: List[Image]
    name: Href
    release_date: datetime.date
    release_date_precision: ReleaseDatePrecision
    restrictions: Restrictions
    type: Album
    uri: URI
    album_group: Album
    artists: List[Artist]

    def __init__(self, album_type: Album, total_tracks: int, available_markets: List[AvailableMarket], external_urls: Welcome8ExternalUrls, 
                 href: Href, id: ID, images: List[Image], name: Href, release_date: datetime.date, release_date_precision: ReleaseDatePrecision, 
                 restrictions: Restrictions, type: Album, uri: URI, album_group: Album, artists: List[Artist]) -> None:

        self.album_type = album_type
        self.total_tracks = total_tracks
        self.available_markets = available_markets
        self.external_urls = external_urls
        self.href = href
        self.id = id
        self.images = images
        self.name = name
        self.release_date = release_date
        self.release_date_precision = release_date_precision
        self.restrictions = restrictions
        self.type = type
        self.uri = uri
        self.album_group = album_group
        self.artists = artists



class Followers:
    href: Href
    total: int

    def __init__(self, href: Href, total: int) -> None:
        self.href = href
        self.total = total

class Welcome8Artist:
    external_urls: Welcome8ExternalUrls
    followers: Followers
    genres: List[Genre]
    href: Href
    id: Href
    images: List[Image]
    name: Href
    popularity: int
    type: ArtistType
    uri: Href

    def __init__(self, external_urls: Welcome8ExternalUrls, followers: Followers, genres: List[Genre], href: Href, id: Href, images: List[Image], name: Href, popularity: int, type: ArtistType, uri: Href) -> None:
        self.external_urls = external_urls
        self.followers = followers
        self.genres = genres
        self.href = href
        self.id = id
        self.images = images
        self.name = name
        self.popularity = popularity
        self.type = type
        self.uri = uri

class ExternalIDS:
    isrc: Href
    ean: Href
    upc: Href

    def __init__(self, isrc: Href, ean: Href, upc: Href) -> None:
        self.isrc = isrc
        self.ean = ean
        self.upc = upc

class ExternalUrlsElement:
    pass

    def __init__(self, ) -> None:
        pass
