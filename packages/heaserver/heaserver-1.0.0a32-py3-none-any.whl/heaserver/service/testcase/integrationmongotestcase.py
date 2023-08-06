from aiohttp.web import Application
from .mongotestcase import MongoTestCase
from ..db.mongo import Mongo, replace_id_with_object_id
from .. import runner
from .. import wstl
import logging
from typing import Union, Dict, List, Any, Optional, Type, Iterable
from testcontainers.mongodb import MongoDbContainer
from testcontainers.general import DockerContainer
from contextlib import ExitStack
from yarl import URL
import os
from .expectedvalues import expected_values, ActionSpec
from heaserver.service.docker import get_bridge_ip, get_exposed_port


def get_test_case_cls(href: Union[URL, str],
                      wstl_package: str,
                      fixtures: Dict[str, List[dict]],
                      body_post: Optional[Dict[str, Dict[str, Any]]] = None,
                      body_put: Optional[Dict[str, Dict[str, Any]]] = None,
                      expected_one: Optional[Dict[str, Any]] = None,
                      expected_one_wstl: Optional[Dict[str, Any]] = None,
                      expected_one_duplicate_form: Optional[Dict[str, Any]] = None,
                      expected_all: Optional[Dict[str, Any]] = None,
                      expected_all_wstl: Optional[Dict[str, Any]] = None,
                      registry_docker_image: Optional[str] = None,
                      port: Optional[int] = None) -> Type[MongoTestCase]:
    """
    This function configures mocks. It returns a base test case class for testing a mongodb-based service with the
    provided fixtures. The test case class is a subclass of aiohttp.test_utils.AioHTTPTestCase, and the provided
    fixtures can be found in the following fields: _resource_path, _body_post, _body_put, _expected_all, and
    _expected_one.

    :param href: the resource being tested. Required.
    :param wstl_package: the name of the package containing the wstl data package. Required.
    :param fixtures: data to insert into the mongo database before running each test. Should be a dict of
    collection -> list of objects. Required.
    :param body_post: JSON dict for data to be posted.
    :param body_put: JSON dict for data to be put. If None, the value of body_post will be used for PUTs.
    :param expected_one: The expected JSON dict for GET calls. If None, the value of expected_all will be used.
    :param expected_one_wstl: The expected JSON dict for GET calls that return the
    application/vnd.wstl+json mime type.
    :param expected_one_properties_form: The expected JSON dict for GET calls that return the
    object's properties form.
    :param expected_one_duplicate_form: The expected JSON dict for GET calls that return the
    object's duplicate form.
    :param expected_all: The expected JSON dict for GET-all calls.
    :param expected_all_wstl: The expected JSON dict for GET-all calls that return the
    application/vnd.wstl+json mime type.
    :param registry_docker_image: an heaserver-registry docker image in REPOSITORY:TAG format, that will be launched
    after the MongoDB container is live.
    :param port: the port number to run aiohttp. If None, a random available port will be chosen.
    :return the base test case class.
    """

    class RealMongoTestCase(MongoTestCase):
        """
        Test case class for testing a mongodb-based service.
        """

        def __init__(self, methodName: str = 'runTest') -> None:
            """
            Initializes a test case.

            :param methodName: the name of the method to test.
            """
            super().__init__(methodName=methodName,
                             href=href,
                             body_post=body_post,
                             body_put=body_put,
                             expected_all=expected_all,
                             expected_one=expected_one or expected_all,
                             expected_one_wstl=expected_one_wstl or expected_all_wstl,
                             expected_all_wstl=expected_all_wstl,
                             expected_one_duplicate_form=expected_one_duplicate_form,
                             wstl_package=wstl_package,
                             port=port)

        def run(self, result=None):
            """
            Runs a test using a freshly created MongoDB Docker container. The container is destroyed upon concluding
            the test.

            :param result: a TestResult object into which the test's result is collected.
            :return: the TestResult object.
            """
            os.environ['MONGO_DB'] = 'hea'
            with ExitStack() as stack:
                mongo_ = stack.enter_context(MongoDbContainer('mongo:4.2.2'))
                mongo_bridge_ip = get_bridge_ip(mongo_)
                mongodb_connection_string = f'mongodb://test:test@{mongo_.get_container_host_ip()}:{get_exposed_port(mongo_, 27017)}/hea?authSource=admin'
                if registry_docker_image is None:
                    config_file = f"""
                [MongoDB]
                ConnectionString = {mongodb_connection_string}
                """
                elif registry_docker_image is not None:
                    registry_container = DockerContainer(registry_docker_image)
                    registry_container.with_env('MONGO_HOSTNAME', mongo_bridge_ip)
                    registry_container.with_env('MONGO_HEA_USERNAME', 'test')
                    registry_container.with_env('MONGO_HEA_PASSWORD', 'test')
                    registry_container.with_env('MONGO_HEA_DATABASE', 'hea')
                    registry_container.with_exposed_ports(8080)
                    registry = stack.enter_context(registry_container)
                    registry_url = f'http://{registry.get_container_host_ip()}:{get_exposed_port(registry, 8080)}'
                    config_file = f"""
                [DEFAULT]
                Registry={registry_url}

                [MongoDB]
                ConnectionString = {mongodb_connection_string}
                                """
                with self._caplog.at_level(logging.DEBUG):
                    self.__config = runner.init(config_string=config_file)
                    db = mongo_.get_connection_client().hea
                    for k in fixtures or {}:
                        db[k].insert_many(replace_id_with_object_id(f) for f in fixtures[k])
                    return super().run(result)

        async def get_application(self) -> Application:
            return runner.get_application(db=Mongo,
                                          wstl_builder_factory=wstl.builder_factory(wstl_package, href=href),
                                          config=self.__config)

    return RealMongoTestCase


def get_test_case_cls_default(coll: str,
                              wstl_package: str,
                              fixtures: Dict[str, List[Dict[str, Any]]],
                              duplicate_action_name: str,
                              include_root=False,
                              href: Optional[Union[str, URL]] = None,
                              get_actions: Optional[List[ActionSpec]] = None,
                              get_all_actions: Optional[List[ActionSpec]] = None,
                              registry_docker_image: Optional[str] = None,
                              port: Optional[int] = None) -> Type[MongoTestCase]:
    if href is None:
        href_ = URL(f'/{coll}/')
    else:
        href_ = str(href)
        if not href_.endswith('/'):
            href_ = href_ + '/'
    return get_test_case_cls(href=href, wstl_package=wstl_package, fixtures=fixtures,
                             **expected_values(fixtures, coll, wstl.builder(package=wstl_package),
                                               duplicate_action_name, href_,
                                               include_root=include_root,
                                               get_actions=get_actions, get_all_actions=get_all_actions),
                             registry_docker_image=registry_docker_image,
                             port=port
                             )
