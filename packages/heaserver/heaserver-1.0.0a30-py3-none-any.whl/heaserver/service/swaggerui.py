"""
This module implements a simple API for launching a swagger UI for trying out a HEA microservice's REST APIs.
"""

from testcontainers.mongodb import MongoDbContainer
from heaserver.service import runner, wstl, db
from aiohttp_swagger3 import SwaggerDocs, SwaggerUiSettings
from aiohttp import web
from importlib.metadata import version
from typing import Any, Dict, List, Tuple, Callable, Iterable
from types import ModuleType
from urllib.request import urlopen
import os
from tempfile import NamedTemporaryFile
import bson


def run(project_slug: str,
        fixtures: Dict[str, List[Dict[str, Any]]],
        module: ModuleType,
        routes: Iterable[Tuple[str, Callable]]) -> None:
    """
    Launches a swagger UI for trying out the given HEA APIs. It downloads the HEA OpenAPI spec from gitlab.com,
    launches a MongoDB database in a Docker container, inserts the given HEA objects into it, and makes the given
    routes available to query in swagger.

    :param project_slug: the Gitlab project slug of interest. Required.
    :param fixtures: a mapping of mongo collection -> list of HEA objects as dicts. Required.
    :param module: the microservice's service module.
    :param routes: a list of two-tuples containing the path and collable of each route of interest.
    :raises OSError: If an error occurred accessing the OpenAPI spec.
    """

    def download_openapi_spec():
        """
        Downloads HEA's OpenAPI spec file into a temporary file.
        :return: the path of the temp file.
        :raises OSError: if an error occurred downloading and writing the spec to a temporary file.
        """
        with NamedTemporaryFile(delete=False) as tmpfile:
            with urlopen(
                'https://gitlab.com/huntsman-cancer-institute/risr/hea/hea-openapi-specs/-/raw/master/openapi.yaml') as url:
                tmpfile.write(url.read())
            return tmpfile.name

    done = False
    openapi_spec_file = download_openapi_spec()
    try:
        with MongoDbContainer('mongo:4.2.2') as mongo_:
            config_file = f"""
[MongoDB]
ConnectionString = mongodb://test:test@{mongo_.get_container_host_ip()}:{mongo_.get_exposed_port(27017)}/test?authSource=admin
"""
            config = runner.init(config_string=config_file)
            _insert_fixtures_into_db(mongo_, fixtures)
            app = runner.get_application(db.mongo.Mongo,
                                         wstl_builder_factory=wstl.builder_factory(module.__package__, href='/'),
                                         config=config)
            swagger = SwaggerDocs(app,
                                  swagger_ui_settings=SwaggerUiSettings(path="/docs"),
                                  title=project_slug,
                                  version=version(project_slug),
                                  components=openapi_spec_file)
            swagger.add_routes([web.get(r[0], r[1]) for r in routes])
        done = True
        os.remove(openapi_spec_file)
    finally:
        if not done:
            try:
                os.remove(openapi_spec_file)
            except OSError:
                pass
    web.run_app(app)


def _insert_fixtures_into_db(mongo_: MongoDbContainer, fixtures: Dict[str, List[Dict[str, Any]]]) -> None:
    db_ = mongo_.get_connection_client().test
    for k in fixtures or {}:
        lst = []
        for f in fixtures[k]:
            if 'id' in f:
                f_ = dict(f)
                f_['_id'] = bson.ObjectId(f_.pop('id', None))
                lst.append(f_)
            else:
                lst.append(f)
        db_[k].insert_many(lst)
