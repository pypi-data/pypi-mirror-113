import os
from typing import TYPE_CHECKING

import pandas as pd
from basis.core.declarative.dataspace import DataspaceCfg
from basis.core.declarative.graph import GraphCfg
from basis.core.environment import Environment
from basis.logging import logger
from basis_modules.modules import mailchimp
from dcp.storage.database.utils import get_tmp_sqlite_db_url
from mailchimp_marketing import Client


def ensure_api_key() -> str:
    api_key = os.environ.get("TEST_MAILCHIMP_API_KEY")
    if api_key is not None:
        return api_key
    api_key = input("Enter Mailchimp API key: ")
    return api_key


def create_test_list(mailchimp: Client):
    body = {
        "permission_reminder": "You signed up for updates on our website",
        "email_type_option": False,
        "campaign_defaults": {
            "from_name": "Test",
            "from_email": "kvh@scaledscience.com",
            "subject": "Test",
            "language": "EN_US",
        },
        "name": "Test list",
        "contact": {
            "company": "Test",
            "address1": "123 test ave",
            "city": "San Francisco",
            "state": "CA",
            "zip": "94103",
            "country": "US",
        },
    }
    response = mailchimp.lists.create_list(body)
    return response["id"]


def delete_list(mailchimp: Client, id: str):
    mailchimp.lists.delete_list(id)


def test():
    api_key = ensure_api_key()
    server = api_key.split("-")[-1]  # Hack? appears to be true for new api keys
    client = Client()
    client.set_config(
        {
            "api_key": api_key,
            "server": server,
        }
    )
    # delete_list(mailchimp, "9311ebcf06")
    list_id = create_test_list(client)

    storage = get_tmp_sqlite_db_url()
    env = Environment(DataspaceCfg(metadata_storage="sqlite://", storages=[storage]))
    env.add_module(mailchimp)
    try:
        members_df = pd.DataFrame.from_records(
            [
                dict(
                    email_address="e1@scaledscience.com",
                    status="subscribed",
                    merge_fields={"f1": "v1"},
                ),
                dict(
                    email_address="e2@scaledscience.com",
                    status="subscribed",
                    merge_fields={"f1": "v2"},
                ),
                dict(
                    email_address="e3@scaledscience.com",
                    status="subscribed",
                    merge_fields={"f1": "v3"},
                ),
            ]
        )

        # Initial graph
        import_df = GraphCfg(
            key="core.import_dataframe",
            function="core.import_dataframe",
            params={"dataframe": members_df, "schema": "MailchimpMember"},
        )
        export_aud = GraphCfg(
            key="mailchimp.export_audience",
            function="mailchimp.export_audience",
            input="core.import_dataframe",
            params={"api_key": api_key, "list_id": list_id, "server": server},
        )
        g = GraphCfg(nodes=[import_df, export_aud])
        # logger.enable("basis")
        env.produce(export_aud.key, g, execution_timelimit_seconds=5)
        response = client.lists.get_list_members_info(list_id)
        assert len(response["members"]) == len(members_df)
    finally:
        delete_list(client, list_id)


if __name__ == "__main__":
    test()
