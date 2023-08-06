from heaserver.service.testcase import mockmongotestcase, expectedvalues
from heaserver.service import wstl, requestproperty, appproperty
from heaserver.folder import service
from heaobject import user
from yarl import URL
from aiohttp import hdrs
from typing import Dict, Any, List
import copy

db_values = {service.MONGODB_ITEMS_COLLECTION: [{
    'created': None,
    'derived_by': None,
    'derived_from': [],
    'description': None,
    'display_name': 'Reximus',
    'id': '666f6f2d6261722d71757578',
    'invites': [],
    'modified': None,
    'name': 'reximus',
    'owner': user.NONE_USER,
    'shares': [],
    'source': None,
    'type': 'heaobject.folder.Item',
    'version': None,
    'actual_object_type_name': 'heaobject.folder.Folder',
    'actual_object_id': '666f6f2d6261722d71757579',
    'folder_id': 'root'
},
    {
        'created': None,
        'derived_by': None,
        'derived_from': [],
        'description': None,
        'display_name': 'Reximus',
        'id': '0123456789ab0123456789ab',
        'invites': [],
        'modified': None,
        'name': 'reximus',
        'owner': user.NONE_USER,
        'shares': [],
        'source': None,
        'type': 'heaobject.folder.Item',
        'version': None,
        'actual_object_type_name': 'heaobject.folder.Folder',
        'actual_object_id': '0123456789ab0123456789ac',
        'folder_id': 'root'
    }
], service.MONGODB_FOLDER_COLLECTION: [{
    'created': None,
    'derived_by': None,
    'derived_from': [],
    'description': None,
    'display_name': 'Reximus',
    'id': '666f6f2d6261722d71757579',
    'invites': [],
    'modified': None,
    'name': 'reximus',
    'owner': user.NONE_USER,
    'shares': [],
    'source': None,
    'type': 'heaobject.folder.Folder',
    'version': None,
    'mime_type': 'application/x.folder'
},
    {
        'created': None,
        'derived_by': None,
        'derived_from': [],
        'description': None,
        'display_name': 'Reximus',
        'id': '0123456789ab0123456789ac',
        'invites': [],
        'modified': None,
        'name': 'reximus',
        'owner': user.NONE_USER,
        'shares': [],
        'source': None,
        'type': 'heaobject.folder.Folder',
        'version': None,
        'mime_type': 'application/x.folder'
    }
]}


def create_expected() -> Dict[str, Any]:
    result = copy.deepcopy(db_values)
    for item in result[service.MONGODB_ITEMS_COLLECTION]:
        item['actual_object'] = next(
            obj for obj in result[service.MONGODB_FOLDER_COLLECTION] if obj['id'] == item['actual_object_id'])
    return result


db_values_expected = create_expected()

ItemPostTestCase = \
    mockmongotestcase.get_test_case_cls(
        href='/folders/666f6f2d6261722d71757578/items?type=heaobject.folder.Folder',
        wstl_package=service.__package__,
        fixtures=db_values,
        body_post=expectedvalues.body_post(fixtures=db_values,
                                           coll=service.MONGODB_ITEMS_COLLECTION))

ItemGetTestCase = \
    mockmongotestcase.get_test_case_cls(href='http://localhost:8080/folders/root/items/',
                                        wstl_package=service.__package__,
                                        fixtures=db_values,
                                        expected_all=expectedvalues.expected_all(fixtures={
                                            service.MONGODB_ITEMS_COLLECTION: [
                                                db_values_expected[service.MONGODB_ITEMS_COLLECTION][0]]},
                                            coll=service.MONGODB_ITEMS_COLLECTION,
                                            wstl_builder=wstl.builder(
                                                package=service.__package__,
                                                href='http://localhost:8080/folders/root/items/'),
                                            get_all_actions=[
                                                expectedvalues.ActionSpec(
                                                    name='heaserver-folders-folder-get-properties',
                                                    rel=['properties']),
                                                expectedvalues.ActionSpec(
                                                    name='heaserver-folders-folder-open',
                                                    url='http://localhost:8080/folders/root/items/{id}/opener',
                                                    rel=['opener']),
                                                expectedvalues.ActionSpec(
                                                    name='heaserver-folders-item-move',
                                                    url='http://localhost:8080/folders/root/items/{id}/mover',
                                                    rel=['mover']),
                                                expectedvalues.ActionSpec(
                                                    name='heaserver-folders-folder-duplicate',
                                                    url='http://localhost:8080/folders/root/items/{id}/duplicator',
                                                    rel=['duplicator'])],
                                            include_root=True) +
                                                     expectedvalues.expected_all(fixtures={
                                                         service.MONGODB_ITEMS_COLLECTION: [
                                                             db_values_expected[service.MONGODB_ITEMS_COLLECTION][1]]},
                                                         coll=service.MONGODB_ITEMS_COLLECTION,
                                                         wstl_builder=wstl.builder(
                                                             package=service.__package__,
                                                             href='http://localhost:8080/folders/root/items/'),
                                                         get_all_actions=[
                                                             expectedvalues.ActionSpec(
                                                                 name='heaserver-folders-folder-get-properties',
                                                                 rel=['properties']),
                                                             expectedvalues.ActionSpec(
                                                                 name='heaserver-folders-folder-open',
                                                                 url='http://localhost:8080/folders/root/items/{id}/opener',
                                                                 rel=['opener']),
                                                             expectedvalues.ActionSpec(
                                                                 name='heaserver-folders-item-move',
                                                                 url='http://localhost:8080/folders/root/items/{id}/mover',
                                                                 rel=['mover']),
                                                             expectedvalues.ActionSpec(
                                                                 name='heaserver-folders-folder-duplicate',
                                                                 url='http://localhost:8080/folders/root/items/{id}/duplicator',
                                                                 rel=['duplicator'])],
                                                         include_root=True),
                                        expected_one=expectedvalues.expected_one(fixtures=db_values_expected,
                                                                                 coll=service.MONGODB_ITEMS_COLLECTION,
                                                                                 wstl_builder=wstl.builder(
                                                                                     package=service.__package__,
                                                                                     href='http://localhost:8080/folders/root/items'),
                                                                                 get_actions=[
                                                                                     expectedvalues.ActionSpec(
                                                                                         name='heaserver-folders-folder-get-properties',
                                                                                         rel=['properties']),
                                                                                     expectedvalues.ActionSpec(
                                                                                         name='heaserver-folders-folder-open',
                                                                                         url='http://localhost:8080/folders/root/items/{id}/opener',
                                                                                         rel=['opener']),
                                                                                     expectedvalues.ActionSpec(
                                                                                         name='heaserver-folders-item-move',
                                                                                         url='http://localhost:8080/folders/root/items/{id}/mover',
                                                                                         rel=['mover']),
                                                                                     expectedvalues.ActionSpec(
                                                                                         name='heaserver-folders-folder-duplicate',
                                                                                         url='http://localhost:8080/folders/root/items/{id}/duplicator',
                                                                                         rel=['duplicator'])],
                                                                                 include_root=True),
                                        expected_one_duplicate_form=expectedvalues.expected_one_duplicate_form(
                                            fixtures=db_values_expected,
                                            coll=service.MONGODB_ITEMS_COLLECTION,
                                            duplicate_action_name='heaserver-folders-folder-duplicate-form',
                                            include_root=True,
                                            wstl_builder=wstl.builder(package=service.__package__,
                                                                      href='http://localhost:8080/folders/root/items/')),
                                        body_put=expectedvalues.body_put(fixtures=db_values_expected,
                                                                         coll=service.MONGODB_ITEMS_COLLECTION))


async def mock_type_to_resource_url(request, type_or_type_name):
    return URL('http://' + request.headers[hdrs.HOST]).with_path('/folders')


service.type_to_resource_url = mock_type_to_resource_url


async def mock_get_actual_item(request, wstl_builder, item, headers=None):
    actions = [
        {
            "name": "heaserver-folders-folder-open",
            "description": "Open this folder",
            "type": "safe",
            "action": "read",
            "target": "item read cj",
            "prompt": "Open",
            "href": '/folders/{folder_id}/items/{id}/opener',
            "rel": "opener"
        },
        {
            "name": "heaserver-folders-folder-get-properties",
            "description": "View and edit this folder's properties",
            "type": "unsafe",
            "target": "item cj-template",
            "action": "update",
            "prompt": "Properties",
            "href": "#",
            "rel": "properties",
            "inputs": [
                {
                    "name": "id",
                    "prompt": "Id",
                    "required": True,
                    "readOnly": True
                },
                {
                    "name": "source",
                    "prompt": "Source"
                },
                {
                    "name": "version",
                    "prompt": "Version"
                },
                {
                    "name": "display_name",
                    "prompt": "Name",
                    "required": True
                },
                {
                    "name": "description",
                    "prompt": "Description",
                    "type": "textarea"
                },
                {
                    "name": "owner",
                    "prompt": "Owner"
                },
                {
                    "name": "created",
                    "prompt": "Created",
                    "readOnly": True
                },
                {
                    "name": "modified",
                    "prompt": "Modified",
                    "readOnly": True
                },
                {
                    "name": "invites",
                    "prompt": "Share invites",
                    "readOnly": True
                },
                {
                    "name": "shares",
                    "prompt": "Shared with"
                },
                {
                    "name": "derived_by",
                    "prompt": "Derived by",
                    "readOnly": True
                },
                {
                    "name": "derived_from",
                    "prompt": "Derived from",
                    "readOnly": True
                },
                {
                    "name": "items",
                    "prompt": "Items",
                    "readOnly": True
                }
            ]
        },
        {
            "name": "heaserver-folders-folder-duplicate",
            "description": "Duplicate this folder",
            "type": "unsafe",
            "action": "append",
            "target": "item read cj",
            "prompt": "Duplicate",
            "href": "/folders/{folder_id}/items/{id}/duplicator",
            "rel": "duplicator"
        }
    ]
    _mock_add_actions(actions, wstl_builder, request)
    return _get_data([item])


def _mock_add_actions(actions, wstl_builder, request):
    for action in actions:
        if not wstl_builder.has_design_time_action(action['name']):
            wstl_builder.add_design_time_action(action)
        if not wstl_builder.has_run_time_action(action['name']):
            wstl_builder.add_run_time_action(action['name'],
                                             path=action['href'],
                                             root=request.app[appproperty.HEA_COMPONENT],
                                             rel=action.get('rel', None))


async def mock_get_actual_item_duplicate(request, wstl_builder, item, headers=None):
    actions = [
        {
            "name": "heaserver-folders-folder-duplicate-form",
            "description": "Duplicate this folder",
            "type": "unsafe",
            "target": "item cj-template",
            "action": "update",
            "prompt": "Duplicate",
            "href": '/folders/root/items/'
        }
    ]
    _mock_add_actions(actions, wstl_builder, request)
    return _get_data([item])


service._add_actual_object = mock_get_actual_item
service._add_actual_object_duplicate_form = mock_get_actual_item_duplicate


def _get_data(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    For an item, attempts to find the item's corresponding folder, and returns the copy of the item with its
    actual_object attribute set to the folder in a list of length 1.
    :param item: an Item object.
    :return: a list containing a copy of the item with the corresponding actual folder, or an empty list if the folder
    could not be found.
    """
    result = []
    for item in items:
        for folder in db_values[service.MONGODB_FOLDER_COLLECTION]:
            if item['actual_object_id'] == folder['id']:
                item['actual_object'] = folder
                result.append(item)
    return result
