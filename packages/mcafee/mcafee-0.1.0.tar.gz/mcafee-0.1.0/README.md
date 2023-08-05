# McAfee

Number four automated fee manager script in all of Kazakhstan.

## Prerequisites

- Open gRPC port on `localhost:10009`
- Baked macaroon file

```
$ lncli bakemacaroon offchain:read offchain:write onchain:read info:read --save_to=~/.lnd/data/chain/bitcoin/mainnet/mcafee.macaroon
```
