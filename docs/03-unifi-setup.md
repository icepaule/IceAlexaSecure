# UniFi-Setup — Schritt für Schritt

**Status: manueller Schritt, noch offen.** Der Admin-Account war zum Zeitpunkt der Umsetzung durch UniFis Login-Rate-Limit gesperrt (siehe [Bekannte Probleme](#bekannte-probleme)) — hier die exakte Konfiguration zum Nachtragen über die UI.

## 1. Neues Netzwerk anlegen

*Settings → Networks → Add New Network*

| Feld | Wert |
|---|---|
| Name | `Alexa-Secure` |
| VLAN ID | `14` |
| Gateway/Subnet | `10.10.14.1/24` *(nur als UniFi-interne Referenz — das eigentliche Routing/Gateway für VLAN14 übernimmt pfSense auf `10.10.14.2`, siehe [pfSense-Setup](02-pfsense-setup.md); Network Purpose auf „VLAN Only" stellen, kein DHCP hier aktivieren — DHCP läuft bereits über pfSense)* |

## 2. Neue WLAN-SSID anlegen

*Settings → WiFi → Add New WiFi Network*

| Feld | Wert |
|---|---|
| Name (SSID) | `Alexa-Secure` |
| Security | WPA2 (nicht WPA3, Kompatibilität mit älteren Echo-Geräten) |
| Network | `Alexa-Secure` (VLAN14, aus Schritt 1) |
| Minimum Data Rate | 6 Mbps *(Standard in diesem Netz, siehe bestehende Konfiguration von Bad!Net/Bad!IoT)* |
| Broadcasting APs | **U6+ Wohnzimmer** und **U6+ Office** — das sind die beiden APs, an denen die Alexa-Geräte aktuell bereits hängen (Bad!Net), Funkabdeckung ist also schon bestätigt vorhanden |

## 3. Geräte migrieren (manuell, pro Gerät)

Das ist der einzige Schritt, der sich nicht per Script/API erledigen lässt — Alexa-Geräte haben keine fernsteuerbare WLAN-Konfiguration.

Für **beide** Geräte (Echo Show 8 in Wohnzimmer, Echo Dot 3. Gen im Office):

1. Alexa-App → Geräte → das jeweilige Gerät auswählen
2. Einstellungen → WLAN-Netzwerk ändern
3. Neues Netzwerk: `Alexa-Secure`, Passwort eingeben
4. Warten, bis das Gerät neu verbindet (LED-Ring: orange → blau/grün)

## 4. Verifikation nach der Migration

Von pfSense aus prüfen, dass die Geräte im neuen Segment auftauchen:

```
# über pf.sh (siehe /root/thw-barbeleg/pf.sh) oder GUI Status → DHCP Leases
pf_exec "cat /var/dhcpd/var/db/dhcpd.leases | grep -A5 'echo-show\|echo-dot'"
```

Erwartete IPs (statische Reservierung, siehe [pfSense-Setup](02-pfsense-setup.md)):
- `echo-show-az` → `10.10.14.10`
- `echo-dot-office` → `10.10.14.11`

Danach in *Firewall → Rules → VLAN14_Alexa* die "0/0 B"-Zähler beobachten (siehe Screenshot in [pfSense-Setup](02-pfsense-setup.md)) — sobald die Geräte über die neuen Regeln kommunizieren, steigen die Byte-Zähler der jeweils genutzten Regeln.

## Bekannte Probleme

**UniFi-Admin-Login-Sperre (2026-07-20):** Der reguläre API-Admin-Account (`claude`) geriet in eine Login-Retry-Schleife und wurde von UniFi mit `429 AUTHENTICATION_FAILED_LIMIT_REACHED` gesperrt — die Sperre hält offenbar mehrere Tage an. Workaround für lesenden Zugriff: dedizierter Read-Only-Viewer-Account (`watchdog`, Rolle „reader") — reicht für Diagnose, aber nicht für Config-Änderungen wie oben. Für schreibenden Zugriff: entweder auf Ablauf der Sperre warten, oder über die UniFi-App/GUI direkt mit dem Owner-Account einloggen (dort greift die API-Rate-Limit-Sperre nicht in gleicher Form).
