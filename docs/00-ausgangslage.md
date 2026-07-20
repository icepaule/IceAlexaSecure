# Ausgangslage — Grundlagenrecherche

Zusammenfassung der Recherche, auf der dieses Projekt aufbaut. Details/Quellen siehe Commit-Historie des begleitenden Dossiers.

## Kernbefund

Vollständige DSGVO-Sicherheit für Alexa-Geräte ist **technisch nicht erreichbar**. Vier peer-reviewte akademische Arbeiten (ACM WiSec 2020, ACM IMC 2023 Best Paper, PETS 2020, ACM TOSN/BuildSys 2024) zeigen:

- **Traffic-Timing-Analyse** kann Sprachbefehle aus verschlüsseltem Netzwerkverkehr mit bis zu 92,89 % Genauigkeit rekonstruieren — allein aus Paketgröße/Timing, ohne Entschlüsselung. Ein VPN schützt davor **nicht** (MCC 0,84 für Befehlskategorien, auch durch VPN hindurch).
- **Unbeabsichtigtes Mithören** ist empirisch belegt (21-Tage-Feldstudie: 30–38 % der Fehlaktivierungen waren echte private Gespräche).
- **TLS-Interception** wurde nur durch physische Hardware-Modifikation (UART-Zugriff, Custom-Firmware) eines Echo-Geräts der 1. Generation demonstriert — reines Netzwerk-MITM scheitert an Certificate Pinning.
- **Skills sind ein aktiver Datenabfluss-Kanal**: Drittanbieter-Werbetreibende erzielen bis zu 30× höhere Ad-Auktions-Gebote basierend auf Alexa-Interaktionsdaten.

## Konsequenz für die Architektur

Netzwerk-Isolation ist **Defense-in-Depth**, kein vollständiger Schutz. Sie reduziert Angriffsfläche und ermöglicht grobe Anomalie-Erkennung (Volumen, Zielserver), verhindert aber nicht, dass Amazon selbst über den legitimen verschlüsselten Kanal Interaktionsmuster ableiten kann.

Realistische Risikominimierung kombiniert drei Ebenen:

1. Alexa-eigene Privacy-Einstellungen (Sprachaufnahme-Auto-Löschung, Mikrofon-Mute, Skill-Audit, Werbe-Opt-out)
2. **Striktes Netzwerksegment** mit minimaler Allowlist — Gegenstand dieses Projekts
3. Lokale Sprachpipeline (Home Assistant Assist + Wyoming-Protokoll) als Ersatz für datenschutzkritische Räume — separates Projekt, siehe [IceHomeAssist](https://github.com/icepaule/IceHomeAssist)

## Wichtig: Was NICHT stimmt

Folgende naheliegende Annahmen wurden in der Recherche explizit **widerlegt**:

- Amazon empfiehlt selbst eine dedizierte SSID/VLAN-Isolation für Alexa — **falsch**, keine offizielle Empfehlung gefunden.
- Amazon publiziert eine feste Domain-Allowlist für Consumer-Firewalls — **falsch**, die in diesem Projekt genutzte Port-Liste stammt aus Amazons Enterprise-Dokumentation ("Alexa Smart Properties") und wurde nur indirekt über Community-Praxisberichte auf Consumer-Echo übertragen. Behandle sie als Startpunkt, nicht als Garantie.
- Ein VPN schützt vor Traffic-Analyse-basiertem Mithör-Rückschluss — **falsch** (siehe oben).
