# unathenticaed and updated every 5 minutes
# https://presearch.org/extsearch?term=can+i+count+the+number+of+bitcoin+nodes
# https: // bitnodes.io / api / v1 / snapshots / < TIMESTAMP > /
# https://bitnodes.io/api/v1/snapshots/<TIMESTAMP>/
# curl -H "Accept: application/json; indent=4" https://bitnodes.io/api/v1/snapshots/latest/


# (bcn) bash-4.3$ curl -H "Accept: application/json; indent=4" https://bitnodes.io/api/v1/snapshots/latest/
# {
#     "timestamp": 1625070387,
#     "total_nodes": 10490,
#     "latest_height": 689232,
#     "nodes": {
#         "nesxfmano25clfvn.onion:8333": [
#             70015,
#             "/Satoshi:0.20.0/",
#             1624749001,
#             1037,
#             689229,
#             null,
#             null,
#             null,
#             0.0,
#             0.0,
#             null,
#             "TOR",
#             "Tor network"
#         ],
#         "37.59.47.27:8333": [
#             70015,
#             "/Satoshi:0.17.99/",
#             1623616365,
#             1037,
#             689232,
#             "ns335655.ip-37-59-47.eu",
#             null,
#             "FR",
#             48.8582,
#             2.3387,
#             "Europe/Paris",
#             "AS16276",
#             "OVH SAS"
#         ],
#         "ogjpukmw3w6l5wmt.onion:8333": [
#             70015,
#             "/Satoshi:0.20.1/",
#             1625065406,
#             1033,
#             689232,
#             null,
#             null,
#             null,
#             0.0,
#             0.0,
#             null,
#             "TOR",
#             "Tor network"
#         ],
#         "185.25.48.184:8333": [
#             70016,
#             "/Satoshi:0.21.0/",
#             1623616016,
#             1037,
#             689232,
#             "185-25-48-184.bacloud.com",
#             null,
#             "LT",
#             56.0,
#             24.0,
#             "Europe/Vilnius",
#             "AS61272",
#             "Informacines sistemos ir technologijos, UAB"
#         ],
