# IceAlexaSecure

Netzwerk-Isolation und Datenschutz-Härtung für Amazon-Alexa-Geräte im Heimnetz, plus Hobby-Forschung zu Root-Zugriff auf Echo-Hardware.

Zwei unabhängige Teilprojekte:

1. **[Netzwerk-Isolation](docs/01-architektur.md)** — dediziertes VLAN14 für beide Alexa-Geräte (Echo Show 8, Echo Dot 3. Gen), Default-Deny-Firewall mit minimaler Ports-Allowlist, DNS über AdGuard, Traffic-Monitoring. Umgesetzt auf pfSense + UniFi.
2. **[Root-Zugriff-Recherche](docs/04-dot-3gen-recherche.md)** — vertiefte, quellenbelegte Recherche zu Root-/Code-Execution-Möglichkeiten auf dem Echo Dot 3. Gen (MT8516, "Donut"), als Grundlage für ein eigenes Hobby-Reverse-Engineering-Projekt.

## Hintergrund

Amazon Echo-Geräte sind Cloud-gebundene Mikrofone. Eine vollständige DSGVO-Konformität ist technisch nicht erreichbar (siehe [Ausgangsrecherche](docs/00-ausgangslage.md)) — Ziel dieses Projekts ist realistische Risikominimierung: Netzwerkseitige Isolation als Defense-in-Depth, plus optionale Forschung zu weitergehender Kontrolle über eigene Hardware.

## Inhalt

| Dokument | Inhalt |
|---|---|
| [00-ausgangslage.md](docs/00-ausgangslage.md) | Zusammenfassung der Grundlagenrecherche (Datenschutz, Traffic-Analyse-Forschung, Grenzen) |
| [01-architektur.md](docs/01-architektur.md) | Netzwerk-Architektur, Mermaid-Diagramme (vorher/nachher) |
| [02-pfsense-setup.md](docs/02-pfsense-setup.md) | Schritt-für-Schritt: VLAN14-Interface, Firewall-Regeln, DHCP |
| [03-unifi-setup.md](docs/03-unifi-setup.md) | Schritt-für-Schritt: neues WLAN, Geräte-Migration |
| [04-dot-3gen-recherche.md](docs/04-dot-3gen-recherche.md) | Root-Zugriff-Recherche Echo Dot 3. Gen |
| [05-monitoring.md](docs/05-monitoring.md) | Traffic-Sichtbarkeit (pfSense-Graphen, Suricata) |

## Status

- [x] pfSense: VLAN14-Interface (OPT3), Firewall-Regelsatz, DHCP
- [ ] UniFi: neues WLAN + Geräte-Migration (manueller Schritt, siehe [03-unifi-setup.md](docs/03-unifi-setup.md))
- [x] Root-Zugriff-Recherche Echo Dot 3. Gen

## Nicht enthalten

Keine Zugangsdaten, Tokens oder Passwörter — alle Beispiele in dieser Doku sind mit Platzhaltern versehen.
