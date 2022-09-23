import hvac
import logging
import os


# https://hvac.readthedocs.io/en/stable/overview.html#getting-started

def retrieve_vault_creds(tag=None):
    vault_token = os.environ.get('VAULT_TOKEN', 'dev_root')
    vault_url = os.environ.get('VAULT_URL', 'http://127.0.0.1:8200')
    vault_path = os.environ.get('VAULT_PATH', 'database/config/mssql-database')
    try:
        logging.debug(f"{__name__}: calling hvac.Client()")
        client = hvac.Client(url=vault_url, token=vault_token)

        res = client.is_authenticated()
        assert res, 'uh, oh .. cannot talk to the Vault!'

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
        # logging.debug(f"{__name__}: {secrets list}: secrets_list['username']")
        # host = f"""{secrets_list['data']['data']['host']}:{secrets_list['data']['data']['port']}"""
        host = f"""{secrets_list['data']['data']['host']}"""
        uid = secrets_list['data']['data']['username']
        pw = secrets_list['data']['data']['password']
        dbname = secrets_list['data']['data']['database']
    except Exception as ex:
        ex_message = f"Exception: {ex} parsing JSON data returend from HVAC Vault"
        logging.exception(ex_message)
        raise RuntimeError(ex_message) from ex

    return host, uid, pw, dbname
