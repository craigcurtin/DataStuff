### note: using mermaid extentions for markdown ...

### notes on using the free Vault for some desktop development


[ hashicorp getting started ] (https://developer.hashicorp.com/vault/tutorials/getting-started/getting-started-intro)

1. we will use the free HashiCorp version for our samples,
1. please install the free version from the [ link ] (https://www.vaultproject.io/downloads)

this was an OK, YT video for getting a qucik overview, mostly the guy wants to sell his advanced course but I'm not biting - HashiCorp Vault 101 - Certified Vault Associate TeKanAid

Install Vault for your operating system, for MacOs:
```
$ brew tap hashicorp/tap
$ brew install hashicorp/tap/vault
$ brew upgrade hashicorp/tap/vault
```

verify the install:
```
$ vault --version
Vault v1.11.3 (17250b25303c6418c283c95b1d5a9c9f16174fe8), built 2022-08-26T10:27:10Z
```

we will use --dev mode alot, this does not persist anything .... good to experiment with!

```commandline
$ vault server --dev
(omitted for brevity)
```
set up the ENV variable, 
```commandline
export VAULT_ADDR='http://127.0.0.1:8200'

# get root token value from your -dev output ... and paste it below, don't use this value ;-)
export VAULT_TOKEN="s.XmpNPoi9sRhYtdKHaQhkHP6x"
```

verify the server is running
```commandline
$ vault status
(omitted for brevity)
```

to work with the k/v secrets engine:
Use the `$ vault kv <subcommand> [options] [args]` command to interact with K/V secrets engine.


| subcommands |  |
|--|--|
| delete / undelete  |  |
| destroy |  |
| enable-versioning |  |
| get / put |  |
| destroy |  |
| list |  | 
| metadata |  | 
| patch |  | 
| patch |  |  
| destroy |  | 
| rollback |  | 


### write a secret:
```commandline
$ vault kv put --mount=secret hello foo=world

```
you can even write multiple in a single command
```commandline
$ vault kv put --mount=secret hello foo=world excited=yes
```
to read a secret:
```commandline
$ vault kv get --mount=secret hello
```

To print only the value of a given field, use the -field=<key_name> flag.
```commandline
$ vault kv get --mount=secret --field=excited hello
```

Optional JSON output is very useful for scripts.
```commandline
$ vault kv get --mount=secret --format=json hello | jq -r .data.data.excited
```
to delete a secret:
```commandline
$ vault kv delete --mount=secret hello
```

to read the secret you just deleted ...
```commandline
$ vault kv get --mount=secret hello
```

undelete secret
```commandline
$ vault kv undelete --mount=secret --versions=2 hello

```


