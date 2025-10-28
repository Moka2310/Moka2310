"""
Configuration complète des serveurs brokers MT4/MT5
Liste exhaustive des serveurs les plus populaires
"""

# Liste complète des serveurs brokers MT4/MT5
BROKER_SERVERS = {
    "GlobalPrime": {
        "name": "GlobalPrime",
        "servers": [
            "GlobalPrime-Demo",
            "GlobalPrime-Live",
            "GlobalPrime-Live2",
            "GlobalPrime-Live3",
            "GlobalPrimeForex-Demo",
            "GlobalPrimeForex-Live"
        ]
    },
    "ICMarkets": {
        "name": "IC Markets",
        "servers": [
            "ICMarkets-Demo",
            "ICMarkets-Demo02",
            "ICMarkets-Demo03",
            "ICMarkets-Live",
            "ICMarkets-Live01",
            "ICMarkets-Live02",
            "ICMarkets-Live03",
            "ICMarketsEU-Demo",
            "ICMarketsEU-Live"
        ]
    },
    "XM": {
        "name": "XM",
        "servers": [
            "XM.COM-Demo",
            "XM.COM-Demo 2",
            "XM.COM-Demo 3",
            "XM.COM-Demo 4",
            "XM.COM-Real",
            "XM.COM-Real 2",
            "XM.COM-Real 3",
            "XM.COM-Real 4",
            "XMGlobal-MT4",
            "XMGlobal-MT4 2"
        ]
    },
    "Pepperstone": {
        "name": "Pepperstone",
        "servers": [
            "Pepperstone-Demo",
            "Pepperstone-Live",
            "Pepperstone-Live01",
            "Pepperstone-Live02",
            "PepperstoneUK-Demo",
            "PepperstoneUK-Live"
        ]
    },
    "FXTM": {
        "name": "FXTM (ForexTime)",
        "servers": [
            "FXTM-Demo",
            "FXTM-Demo02",
            "FXTM-Real",
            "FXTM-Real02",
            "FXTM-ECN",
            "ForexTimeFXTM-Demo",
            "ForexTimeFXTM-Real"
        ]
    },
    "FBS": {
        "name": "FBS",
        "servers": [
            "FBS-Demo",
            "FBS-Real",
            "FBS-Real-1",
            "FBS-Real-2",
            "FBS-Real-3"
        ]
    },
    "Exness": {
        "name": "Exness",
        "servers": [
            "Exness-Demo",
            "Exness-Real",
            "Exness-Real2",
            "Exness-Real3",
            "Exness-Real4",
            "ExnessEU-Demo",
            "ExnessEU-Real"
        ]
    },
    "Alpari": {
        "name": "Alpari",
        "servers": [
            "Alpari-Demo",
            "Alpari-Real",
            "AlpariInternational-Demo",
            "AlpariInternational-Server"
        ]
    },
    "HotForex": {
        "name": "HotForex (HF Markets)",
        "servers": [
            "HotForex-Demo",
            "HotForex-Real",
            "HotForex-Real01",
            "HotForex-Real02",
            "HFMarkets-Demo",
            "HFMarkets-Real"
        ]
    },
    "AvaTrade": {
        "name": "AvaTrade",
        "servers": [
            "AvaTrade-Demo",
            "AvaTrade-Live",
            "AvaTradeEU-Demo",
            "AvaTradeEU-Live"
        ]
    },
    "OANDA": {
        "name": "OANDA",
        "servers": [
            "OANDA-Demo",
            "OANDA-Live",
            "OANDAv20-Demo",
            "OANDAv20-Live"
        ]
    },
    "AdmiralMarkets": {
        "name": "Admiral Markets",
        "servers": [
            "AdmiralMarkets-Demo",
            "AdmiralMarkets-Live",
            "Admirals-Demo",
            "Admirals-Live"
        ]
    },
    "ThinkMarkets": {
        "name": "ThinkMarkets",
        "servers": [
            "ThinkMarkets-Demo",
            "ThinkMarkets-Live",
            "ThinkForex-Demo",
            "ThinkForex-Live"
        ]
    },
    "FxPro": {
        "name": "FxPro",
        "servers": [
            "FxPro-Demo",
            "FxPro-Live",
            "FxPro.com-Demo",
            "FxPro.com-Real"
        ]
    },
    "Tickmill": {
        "name": "Tickmill",
        "servers": [
            "Tickmill-Demo",
            "Tickmill-Live",
            "TickmillEU-Demo",
            "TickmillEU-Live"
        ]
    },
    "RoboForex": {
        "name": "RoboForex",
        "servers": [
            "RoboForex-Demo",
            "RoboForex-Pro",
            "RoboForex-ECN"
        ]
    },
    "OctaFX": {
        "name": "OctaFX",
        "servers": [
            "OctaFX-Demo",
            "OctaFX-Real",
            "OctaFX-Real-1",
            "OctaFX-Real-2"
        ]
    },
    "LiteForex": {
        "name": "LiteForex",
        "servers": [
            "LiteForex-Demo",
            "LiteForex-Classic",
            "LiteForex-ECN"
        ]
    },
    "InstaForex": {
        "name": "InstaForex",
        "servers": [
            "InstaForex-Demo",
            "InstaForex-Server",
            "InstaForex-Contest"
        ]
    },
    "FPMarkets": {
        "name": "FP Markets",
        "servers": [
            "FPMarkets-Demo",
            "FPMarkets-Live",
            "FirstPrudential-Demo",
            "FirstPrudential-Live"
        ]
    }
}

def get_all_servers_list():
    """Retourne une liste plate de tous les serveurs"""
    servers = []
    for broker_data in BROKER_SERVERS.values():
        servers.extend(broker_data["servers"])
    return sorted(servers)

def get_servers_by_broker():
    """Retourne les serveurs groupés par broker"""
    return BROKER_SERVERS

def search_server(query: str):
    """Recherche un serveur par nom partiel"""
    query = query.lower()
    results = []
    for broker, data in BROKER_SERVERS.items():
        for server in data["servers"]:
            if query in server.lower():
                results.append({
                    "broker": data["name"],
                    "server": server
                })
    return results
