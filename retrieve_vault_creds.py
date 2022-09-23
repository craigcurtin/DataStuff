import hvac
import logging
import os


# https://hvac.readthedocs.io/en/stable/overview.html#getting-started

def retrieve_vault_creds(db_tag=None):
    """retrieve_vault_creds(tag) goes and gets credentials"""
    vault_url, vault_token, vault_path = get_vault_configs(db_tag)
    try:
        logging.debug(f"{__name__}: calling hvac.Client({vault_url}, {vault_token})")
        client = hvac.Client(url=vault_url, token=vault_token)

        res = client.is_authenticated()
        assert res, 'uh, oh .. Vault not authenticated!'

        logging.debug(f"{__name__}: authenticate {res}")

        secrets_list = client.secrets.kv.read_secret(
            path=vault_path
        )
        logging.info(f"Reading credentials from HVAC Vault: {vault_url}, {vault_path} with {vault_token} as token")
    except Exception as ex:
        ex_message = f"Exception: {ex} reading from HVAC Vault"
        logging.exception(ex_message)
        raise RuntimeError(ex_message) from ex

    # ok, now we got the secrets ... make sure the data is in proper JSON keys
    try:
        host = secrets_list['data']['data']['host']
        uid = secrets_list['data']['data']['username']
        pw = secrets_list['data']['data']['password']
        dbname = secrets_list['data']['data']['database']
        logging.info(f"assigning credentials HVAC Vault: json data")
    except Exception as ex:
        ex_message = f"Exception: {ex} parsing JSON data returend from HVAC Vault"
        logging.exception(ex_message)
        raise RuntimeError(ex_message) from ex

    return host, uid, pw, dbname

def get_vault_configs(db_tag=None):
    """get_vault_configs(db_tag) generally returns token/url with tag specific path"""
    vault_token = os.environ.get('VAULT_TOKEN', 'dev_root')
    vault_url = os.environ.get('VAULT_URL', 'http://127.0.0.1:8200')

    if db_tag == "hni":
        vault_path = os.environ.get('VAULT_PATH', 'database/config/mssql-database')
    else:
        vault_path = os.environ.get('VAULT_PATH', 'database/config/mssql-database')
    return vault_url, vault_token, vault_path
