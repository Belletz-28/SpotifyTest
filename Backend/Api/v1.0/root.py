import ujson
import pandas as pd
import uuid
import os
import config
from cacher import CacheFile
from typing import AsyncContextManager, Optional
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse, RedirectResponse
import spotipy as sp
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware

# APP CONFIG
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=config.MIDDLEWARE_SESSION_TOKEN)
#app.add_middleware(HTTPSRedirectMiddleware)
app.add_middleware(TrustedHostMiddleware, allowed_hosts = ["*"])
app.add_middleware(GZipMiddleware, minimum_size = 1000)


if not os.path.exists(config.CACHES_FOLDER):
    os.makedirs(config.CACHES_FOLDER)
    
#cache cleaner, sub process on start: delay 1 min

def createSessionFile(uuid : str) -> None:
    if not os.path.exists(config.CACHES_FOLDER + uuid +".parquet"):
       data = pd.DataFrame(columns=['Name', 'Value','Domain','Path', 'Expires','Secure','SameSite'])
       data.to_parquet(config.CACHES_FOLDER + uuid +".parquet",compression='gzip')
       del(data)

@app.get("/artistid={artistid}")
async def read_artist_album(artistid, request : Request) -> JSONResponse:
    """[summary]

    Args:
        artistid ([type]): [description]
        request (Request): [description]
        code (str): [description]
        state (str): [description]

    Returns:
        JSONResponse: [description]
    """ 
    validation = checkLogin(request=request)
    if type(validation) == type({}):
        birdy_uri = f'spotify:artist:{artistid}'
        spotify = sp.Spotify(client_credentials_manager=SpotifyClientCredentials(
            client_id=config.CLIENT_ID, client_secret=config.CLIENT_SECRET))
        results = spotify.artist_top_tracks(birdy_uri)
        albums = results['items']
        return JSONResponse(albums)
    else:
        return validation

@app.get("/home")
async def main(request : Request, response : Response):
    return "HELLO"

@app.get("/login")
async def userlogin(request:Request, response : Response) -> RedirectResponse:
    """[summary]

    Returns:
        RedirectResponse: [description]
    """
    if not request.session.get('session'):
        uuid_session = str(uuid.uuid4())
        auth = SpotifyOAuth(
            client_id=config.CLIENT_ID,
            client_secret=config.CLIENT_SECRET,
            redirect_uri=config.REDIRECT_URI,
            scope="user-read-currently-playing playlist-modify-private",
            open_browser=True,
            show_dialog=True)
        return RedirectResponse(auth.get_authorize_url(uuid_session))
    else:
        return RedirectResponse("/Home")
    


@app.get("/callback")
async def callback(request: Request, response : Response) -> Response:
    """[summary]

    Args:
        request (Request): [description]
        response (Response): [description]

    Returns:
        Response: [description]
    """
    # check for middleware session and add the access token + middleware
    if not request.session.get('session'):
        cacheFile = CacheFile(filename = request.query_params.get('state'))
        cacheFile.createSessionFile(config.CACHES_FOLDER + cacheFile.filename)
        cacheFile.append(["DELETE",config.CACHES_FOLDER + request.query_params.get('state'), "Spotify", "/", 3600, "Yes", "Yes"])
        cacheFile.append(["APISESSION",request.query_params.get('state'), "Spotify", "/", 3600, "Yes", "Yes"])
        cacheFile.append(["ACCESSTOKEN",request.query_params.get('code'), "Spotify", "/", 3600, "Yes", "Yes"])
        cacheFile.save()
        response.set_cookie(key = "APISESSION", value = request.query_params.get('state'), max_age=3600, expires=3600)
        response.set_cookie(key = "ACCESSTOKEN", value = request.query_params.get('code'), max_age=3600, expires=1000)
    return response.status_code

@app.get("/checkLogin")
def checkLogin(request: Request):
    try:
        if request.session.get('session'): 
            cacheFile = CacheFile(filename = request.cookies.get('APISESSION'))
            if not cacheFile.checkSessionFile() == None:
                return {"Session": cacheFile.filename, "Verified": True}
        else:
            return RedirectResponse("/login")
    except Exception as e:
        print(e)