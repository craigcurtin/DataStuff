

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
