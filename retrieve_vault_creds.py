import hvac
import logging


def retrieve_vault_creds( tag = None):
    vault_token = 'dev_root'    # Copying my token from vault
    vault_url = 'https://127.0.0.1:8200'

    logging.debug(f"{__name__}: calling hvac.Client()")
    client = hvac.Client(url=vault_url, token=vault_token)

    res = client.is_authenticated()

    logging.debug(f"{__name__}: authenticate {res}")

    secrets_list = client.secrets.kv.v1.read_secret(
        path = 'databases/creds/azure-mssql'
    )

    #logging.debug(f"{__name__}: {secrets list}: secrets_list['username']")

    return ( host, uid, pw, dbname )
