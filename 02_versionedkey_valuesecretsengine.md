

Display all the enabled secrets engine.



```
$ vault secrets list --detailed
```


write secrets ....
```
$ vault kv put secret/customer/acme customer_name="ACME Inc." contact_email="john.smith@acme.com"

$ vault kv put --mount=secret customer/bjss customer_name="GodSaveTheKinks"  contact_email="ray.davies@theKinks.com"


$ vault kv get secret/customer/acme

$ vault kv get secret/customer/bjss
```

an example of an update ... patch in Vault nomenclature

```
# below is a patch to update email only ...
$ vault kv patch secret/customer/acme contact_email="admin@acme.com"

# now lets verify it
$ vault kv get secret/customer/acme

```


now, adding custom metadata ...

```commandline
# lets add some metadata to the customer
$ vault kv metadata put --custom-metadata=Membership="Platinum" secret/customer/bjss


# verify by reading back:
$ vault kv get secret/customer/bjss

# now upgrade the metadata ...
$ vault kv metadata put --custom-metadata=Membership="Gold" secret/customer/bjss

# verify by reading back:
$ vault kv get secret/customer/bjss

# now add more metadata ...
$ vault kv metadata put --custom-metadata=CreditLevel="AAA" secret/customer/bjss

# ah, only one single field to Metadata .... ugh, now we know
```


storing [ Database secrets ] ( https://www.vaultproject.io/docs/secrets/databases )

```commandline
# you must configure DB secrets engine
$ vault secrets enable database


$ vault write database/config/position_db \
    plugin_name="..." \
    connection_url="..." \
    allowed_roles="..." \
    username="..." \
    password="..." \

# Vault will use the user specified here to create/update/revoke database credentials. That user must have the appropriate permissions to perform actions upon other database users (create, update credentials, delete, etc.).
# This secrets engine can configure multiple database connections. For details on the specific configuration options, please see the database-specific documentation.

# 
$ vault write -force database/rotate-root/position_db


$ vault write database/roles/risk_engine_app \
    db_name=position_db \
    creation_statements="..." \
    default_ttl="1h" \
    max_ttl="24h"

```

Usage:

```commandline

vault read database/creds/risk_engine_app

```
