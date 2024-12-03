# Copyright The Cloud Custodian Authors.
# SPDX-License-Identifier: Apache-2.0
import json
from pickle import FALSE

from pytest_terraform import terraform

from .common import BaseTest


# class AppSyncWafV2(BaseTest):

@terraform('appsync', replay=False)
def test_graphql_api_filter_wafv2(test, appsync):
    factory = test.record_flight_data("test_graphql_api_filter_wafv2")
    p = test.load_policy(
        {
            "name": "filter-graphql-api-wafv2",
            "resource": "graphql-api",
            "filters": [{"type": "wafv2-enabled", "state": True}]
        },
        session_factory=factory,
    )
    resources = p.run()
    test.assertEqual(len(resources), 2)

    p = test.load_policy(
        {
            "name": "filter-graphql-api-wafv2",
            "resource": "graphql-api",
            "filters": [{"type": "wafv2-enabled", "state": True,
                         "web-acl": ".*FMManagedWebACLV2-?FMS-.*"}]
        },
        session_factory=factory,
    )
    resources = p.run()
    test.assertEqual(len(resources), 1)

    p = test.load_policy(
        {
            "name": "filter-graphql-api-wafv2",
            "resource": "graphql-api",
            "filters": [{"type": "wafv2-enabled", "state": False}]
        },
        session_factory=factory,
    )
    resources = p.run()
    test.assertEqual(len(resources), 1)

    p = test.load_policy(
        {
            "name": "filter-graphql-api-wafv2",
            "resource": "graphql-api",
            "filters": [{"type": "wafv2-enabled", "state": False,
                         "web-acl": ".*FMManagedWebACLV2-?FMS-.*"}]
        },
        session_factory=factory,
    )
    resources = p.run()
    test.assertEqual(len(resources), 2)

@terraform('appsync', replay=False)
def test_graphql_api_filter_wafv2_value(test, appsync):
    factory = test.record_flight_data("test_graphql_api_filter_wafv2_value")

    p = test.load_policy(
        {
            "name": "filter-graphql-api-wafv2",
            "resource": "graphql-api",
            "filters": [{"type": "wafv2-enabled", "key": "Rules", "value": "empty"}]
        },
        session_factory=factory,
    )
    resources = p.run()
    # mock WAF has 1 rule
    test.assertEqual(len(resources), 0)

    p = test.load_policy(
        {
            "name": "filter-graphql-api-wafv2",
            "resource": "graphql-api",
            "filters": [{
                "type": "wafv2-enabled",
                "key": "length(Rules[?contains(keys(Statement), 'RateBasedStatement')])",
                "op": "gte",
                "value": 1
            }]
        },
        session_factory=factory,
    )
    resources = p.run()
    # mock WAF rule has single RateBasedStatement
    test.assertEqual(len(resources), 1)

@terraform('appsync', replay=False)
def test_graphql_api_action_wafv2(test, appsync):
    factory = test.record_flight_data("test_graphql_api_action_wafv2")
    p = test.load_policy(
        {
            "name": "action-graphql-api-wafv2",
            "resource": "graphql-api",
            "filters": [{"type": "wafv2-enabled", "state": False,
                         "web-acl": ".*FMManagedWebACLV2-?FMS-.*"}],
            "actions": [{"type": "set-wafv2", "state": True,
                         "web-acl": ".*FMManagedWebACLV2-?FMS-.*"}]
        },
        session_factory=factory,
    )
    resources = p.run()
    test.assertEqual(len(resources), 2)

    p = test.load_policy(
        {
            "name": "action-graphql-api-wafv2",
            "resource": "graphql-api",
            "filters": [{"type": "wafv2-enabled", "state": True,
                         "web-acl": ".*FMManagedWebACLV2-?FMS-.*"}],
            "actions": [{"type": "set-wafv2", "state": False,
                         "force": True}]
        },
        session_factory=factory,
    )
    resources = p.run()
    test.assertEqual(len(resources), 1)

    p = test.load_policy(
        {
            "name": "action-graphql-api-wafv2",
            "resource": "graphql-api",
            "filters": [{"type": "wafv2-enabled", "state": True,
                         "web-acl": ".*FMManagedWebACLV2-?FMS-.*"}],
            "actions": [{"type": "set-wafv2", "state": True, "force": True,
                         "web-acl": ".*FMManagedWebACLV2-?FMS-TEST.*"}]
        },
        session_factory=factory,
    )
    resources = p.run()
    test.assertEqual(len(resources), 1)

@terraform('appsync', replay=False)
def test_graphql_api_action_wafv2_regex_multiple_webacl_match(test, appsync):
    factory = test.record_flight_data(
        "test_graphql_api_action_wafv2_regex_multiple_webacl_match")
    p = test.load_policy(
        {
            "name": "action-graphql-api-wafv2",
            "resource": "graphql-api",
            "filters": [{"type": "wafv2-enabled", "state": False,
                         "web-acl": ".*FMManagedWebACLV2-?FMS-.*"}],
            "actions": [{"type": "set-wafv2", "state": True,
                         "web-acl": ".*FMManagedWebACLV2-?FMS-.*"}]
        },
        session_factory=factory,
    )
    with test.assertRaises(ValueError) as ctx:
        p.run()
    test.assertIn('matching to none or multiple webacls', str(
        ctx.exception))


# class TestAppSyncApiCache(BaseTest):
@terraform('appsync', replay=False)
def test_graphql_api_cache_filter(test, appsync):
    factory = test.record_flight_data(
        "test_graphql_api_cache_filter")

    p = test.load_policy(
        {
            "name": "graphql-api-cache-filter",
            "resource": "graphql-api",
            "filters": [{"type": "api-cache",
                         "key": "apiCachingBehavior",
                         "value": "FULL_REQUEST_CACHING"
                         }],
        },
        session_factory=factory,
    )

    resources = p.run()
    test.assertEqual(len(resources), 1)

@terraform('appsync', replay=False)
def test_delete_appsync_api(test, appsync):
    factory = test.record_flight_data("test_delete_appsync_api")
    p = test.load_policy(
        {
            "name": "appsync-delete",
            "resource": "graphql-api",
            "filters": [{"name": "My AppSync App"}],
            "actions": [{"type": "delete"}],
        },
        session_factory=factory,
    )
    resources = p.run()
    test.assertEqual(len(resources), 1)
    test.assertEqual(resources[0]['name'], "My AppSync App")
    client = factory().client("appsync")
    test.assertEqual(len(client.list_graphql_apis()["graphqlApis"]),0)
