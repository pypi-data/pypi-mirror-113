"""
The HEA Volumes Microservice provides ...
"""

from heaserver.service import response, appproperty
from heaserver.service.runner import init_cmd_line, routes, start, web
from heaserver.service.db import mongo, mongoservicelib
from heaserver.service.wstl import builder_factory, action
from heaobject.volume import Volume

MONGODB_VOLUME_COLLECTION = 'volumes'


@routes.get('/volumes/{id}')
@action('heaserver-volumes-volume-get-properties', rel='properties')
@action('heaserver-volumes-volume-open', rel='opener', path='/volumes/{id}/opener')
@action('heaserver-volumes-volume-duplicate', rel='duplicator')
async def get_volume(request: web.Request) -> web.Response:
    """
    Gets the volume with the specified id.
    :param request: the HTTP request.
    :return: the requested volume or Not Found.
    """
    return await mongoservicelib.get(request, MONGODB_VOLUME_COLLECTION)


@routes.get('/volumes/byname/{name}')
async def get_volume_by_name(request: web.Request) -> web.Response:
    """
    Gets the volume with the specified id.
    :param request: the HTTP request.
    :return: the requested volume or Not Found.
    """
    return await mongoservicelib.get_by_name(request, MONGODB_VOLUME_COLLECTION)


@routes.get('/volumes')
@routes.get('/volumes/')
@action('heaserver-volumes-volume-get-properties', rel='properties')
@action('heaserver-volumes-volume-open', rel='opener', path='/volumes/{id}/opener')
@action('heaserver-volumes-volume-duplicate', rel='duplicator')
async def get_all_volumes(request: web.Request) -> web.Response:
    """
    Gets all volumes.
    :param request: the HTTP request.
    :return: all volumes.
    """
    return await mongoservicelib.get_all(request, MONGODB_VOLUME_COLLECTION)


@routes.get('/volumes/{id}/duplicator')
@action(name='heaserver-volumes-volume-duplicate-form', path='/volumes/{id}')
async def get_volume_duplicate_form(request: web.Request) -> web.Response:
    """
    Gets a form template for duplicating the requested volume.

    :param request: the HTTP request. Required.
    :return: the requested form, or Not Found if the requested volume was not found.
    """
    return await mongoservicelib.get(request, MONGODB_VOLUME_COLLECTION)


@routes.post('/volume/duplicator')
async def post_volume_duplicator(request: web.Request) -> web.Response:
    """
    Posts the provided volume for duplication.
    :param request: the HTTP request.
    :return: a Response object with a status of Created and the object's URI in the
    """
    return await mongoservicelib.post(request, MONGODB_VOLUME_COLLECTION, Volume)


@routes.post('/volumes')
@routes.post('/volumes/')
async def post_volume(request: web.Request) -> web.Response:
    """
    Posts the provided volume.
    :param request: the HTTP request.
    :return: a Response object with a status of Created and the object's URI in the
    """
    return await mongoservicelib.post(request, MONGODB_VOLUME_COLLECTION, Volume)


@routes.put('/volumes/{id}')
async def put_volume(request: web.Request) -> web.Response:
    """
    Updates the volume with the specified id.
    :param request: the HTTP request.
    :return: a Response object with a status of No Content or Not Found.
    """
    return await mongoservicelib.put(request, MONGODB_VOLUME_COLLECTION, Volume)


@routes.delete('/volumes/{id}')
async def delete_volume(request: web.Request) -> web.Response:
    """
    Deletes the volume with the specified id.
    :param request: the HTTP request.
    :return: No Content or Not Found.
    """
    return await mongoservicelib.delete(request, MONGODB_VOLUME_COLLECTION)


def main() -> None:
    config = init_cmd_line(description='The HEA volumes service',
                           default_port=8080)
    start(db=mongo.Mongo, wstl_builder_factory=builder_factory(__package__), config=config)
