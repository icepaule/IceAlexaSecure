# Architektur

## Vorher: Alexa im geteilten IoT-WLAN

Beide Alexa-Geräte hingen im "Bad!Net"-WLAN (VLAN 666) — dem alten, unsegmentierten IoT-Netz, gemeinsam mit anderen, noch nicht migrierten IoT-Geräten. Keine geräteklassen-spezifischen Firewall-Regeln, volles Internet ohne Einschränkung.

```mermaid
flowchart LR
    subgraph WLAN["WLAN Bad!Net (VLAN 666)"]
        Show["Echo Show 8<br/>192.168.178.126"]
        Dot["Echo Dot 3.Gen<br/>192.168.178.149"]
        Other["… weitere IoT-Geräte"]
    end
    WLAN -->|"uneingeschränkt"| USG[UniFi USG-Pro-4]
    USG --> Internet((Internet))
```

## Nachher: dediziertes VLAN14 mit Default-Deny

Ein neues, ausschließlich für Alexa reserviertes VLAN — eigene Firewall-Zone auf pfSense, minimale Ports-Allowlist, kein Zugriff auf andere interne Netze.

```mermaid
flowchart TB
    subgraph VLAN14["VLAN14 — Alexa-Secure (10.10.14.0/24)"]
        Show["Echo Show 8<br/>10.10.14.10"]
        Dot["Echo Dot 3.Gen<br/>10.10.14.11"]
    end

    VLAN14 -->|"nur Allowlist-Ports"| PF[pfSense OPT3<br/>10.10.14.2]

    PF -->|"DNS 53"| AdGuard["AdGuard<br/>192.168.178.145"]
    PF -->|"443 · 3478 · 49152-65535<br/>123 · 4070 · 33434 · 40317 · 49317"| Internet((Internet / Amazon))
    PF -.->|"blockiert"| Other["andere VLANs<br/>10.0.0.0/8 · 172.16.0.0/12 · 192.168.0.0/16"]

    style Other stroke-dasharray: 5 5
```

## Firewall-Regelreihenfolge (first-match-wins)

Die Reihenfolge ist entscheidend: spezifische Allows zuerst, dann der Block für private Netze, dann die generischen Internet-Allows. So kann AdGuard (eine private IP) erreicht werden, während Zugriff auf alle anderen internen Netze blockiert bleibt.

```mermaid
flowchart TD
    A[Paket von VLAN14] --> B{Ziel = AdGuard :53?}
    B -->|ja| P1[PASS]
    B -->|nein| C{Ziel = pfSense self :53?}
    C -->|ja| P2[PASS]
    C -->|nein| D{Ziel = VLAN14 :5353 mDNS?}
    D -->|ja| P3[PASS]
    D -->|nein| E{Ziel ∈ RFC1918?}
    E -->|ja| BLOCK[BLOCK + LOG]
    E -->|nein| F{Port ∈ Allowlist?}
    F -->|443 / 3478 / 49152-65535 / 123 / 4070 / 33434 / 40317 / 49317| P4[PASS]
    F -->|sonst| IMPLICIT[Implizit BLOCK]
```

## Port-Allowlist

| Ziel/Zweck | Protokoll | Port |
|---|---|---|
| Amazon-Endpunkte (Signaling, App) | TCP | 443 |
| STUN/TURN (Anrufe, Intercom) | TCP+UDP | 3478 |
| SRTP-Audio | UDP | 49152–65535 |
| NTP | UDP | 123 |
| mDNS (nur lokal, VLAN14-intern) | UDP | 5353 |
| Amazon Custom-Dienste | TCP+UDP | 4070, 33434, 40317, 49317 |

Quelle: Amazon Developer Docs "Alexa Smart Properties — Networking Best Practices" (Enterprise-Kontext, community-bestätigt für Consumer-Echo, siehe [00-ausgangslage.md](00-ausgangslage.md)).

## Physische Topologie

```mermaid
flowchart LR
    subgraph prox2["prox2 (Proxmox, Single-NIC Router-on-a-Stick)"]
        pfSense["pfSense VM100<br/>vtnet4 = VLAN14 (OPT3)"]
    end

    prox2 -->|"vmbr0 Trunk<br/>+VLAN14"| Backbone[CRS305 Backbone]

    Backbone --> AP1["U6+ Wohnzimmer<br/>Echo Show"]
    Backbone --> AP2["U6+ Office<br/>Echo Dot"]

    AP1 -.->|"neue SSID<br/>Alexa-Secure"| Show2[Echo Show 8]
    AP2 -.->|"neue SSID<br/>Alexa-Secure"| Dot2[Echo Dot 3.Gen]
```
