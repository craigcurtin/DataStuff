### https://www.vaultproject.io/docs/secrets/databases/mssql

##Capabilities

| Plugin Name |	Root Credential Rotation	| Dynamic Roles	| Static Roles |	Username Customization |
|----         | ---------                   |	---	        | ---          | ---	|
| mssql-database-plugin |	Yes	| Yes	 | Yes	| Yes (1.7+) |


## Setup 1. database, 2. role
```
# below is config for MS-SQL instance
$ vault write database/config/my-mssql-database \
    plugin_name=mssql-database-plugin \
    connection_url='sqlserver://{{username}}:{{password}}@localhost:1433' \
    allowed_roles="my-role" \
    username="vaultuser" \
    password="yourStrong(!)Password"

# setup role for MS-SQL instance
$ vault write database/roles/risk_engine_app \
    db_name=my-mssql-database \
    creation_statements="CREATE LOGIN [{{name}}] WITH PASSWORD = '{{password}}';\
        CREATE USER [{{name}}] FOR LOGIN [{{name}}];\
        GRANT SELECT ON SCHEMA::dbo TO [{{name}}];" \
    default_ttl="1h" \
    max_ttl="24h"

```

# usage:
# after 

Generate a new credential by reading from the /creds endpoint with the name of the role:

```commandline
$ vault read database/creds/my-role
```

# ms-sql plug-in page .... for more details
https://www.vaultproject.io/api-docs/secret/databases/mssql

Sample Payload
```commandline
$ TMP_FILE=/tmp/payload.json

$ cat > ${TMP_FILE} <<End-of-message
{
  "plugin_name": "mssql-database-plugin",
  "allowed_roles": "readonly",
  "connection_url": "sqlserver://{{username}}:{{password}}@localhost:1433",
  "max_open_connections": 5,
  "max_connection_lifetime": "5s",
  "username": "sa",
  "password": "yourStrong(!)Password"
}
End-of-message
```

sample post (using curl)
```commandline
$ curl \
    --header "X-Vault-Token: ..." \
    --request POST \
    --data @${TMP_FILE} \
    http://127.0.0.1:8200/v1/database/config/mssql
    
# perhaps verify success from curl cmd
$ rm ${TMP_FILE}

```
