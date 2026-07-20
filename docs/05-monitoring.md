# Traffic-Monitoring

Realistischer Umfang gemäß [Ausgangsrecherche](00-ausgangslage.md): Metadaten-Sichtbarkeit (Volumen, Ziele, Timing), **kein** Klartext-Inhalt. Traffic-Timing-Angriffe mit hoher Genauigkeit (siehe Ausgangsrecherche) nutzen trainierte ML-Modelle — ein selbstgebautes Dashboard erkennt grobe Anomalien, keine einzelnen Sprachbefehle.

## Ebene 1: pfSense-native Firewall-Logs

Die Regeln in [pfSense-Setup](02-pfsense-setup.md) haben Logging auf den sicherheitsrelevanten Einträgen aktiv:

- **Block-Regeln** (Zugriff auf andere VLANs) — jeder Versuch wird geloggt, sollte im Normalbetrieb **nie** auftreten. Ein Treffer hier ist ein starkes Anomalie-Signal (kompromittiertes Gerät, Fehlkonfiguration, oder ein Skill/Feature, das mehr Zugriff braucht als erwartet).
- **HTTPS-443-Pass-Regel** — geloggt für Volumen-Trending.

Einsehbar unter *Status → System Logs → Firewall*, gefiltert auf Interface `VLAN14_Alexa`.

## Ebene 2: Interface-Traffic-Graphen (RRD)

*Status → Traffic Graph → VLAN14_Alexa* — eingebaut, sofort nutzbar, zeigt Durchsatz in Echtzeit. *Status → Monitoring* für historische RRD-Graphen (Bandbreite über Zeit).

## Ebene 3: Suricata (SNI-Sichtbarkeit ohne Entschlüsselung)

Optionaler nächster Schritt, noch nicht umgesetzt: Suricata läuft aktuell nur auf `WAN` (IDS-Modus, siehe bestehende pfSense-Doku — **nicht** IPS, nach einem dokumentierten False-Positive-Vorfall). Eine zweite Suricata-Instanz auf `VLAN14_Alexa` würde TLS-SNI-Metadaten sichtbar machen (welcher Amazon-Host wird wann/wie oft kontaktiert), ohne den Traffic zu entschlüsseln.

**Wichtig, falls umgesetzt:** IDS-Modus (`blockoffenders=off`), nicht IPS — der dokumentierte Vorfall vom 29.06.2026 zeigt, dass automatisches Blocken auf Basis von ET-Open-Regeln zu False-Positives auf legitimen Zielen führen kann.

## Ebene 4: TLS-Interception

**Bewusst nicht umgesetzt.** Siehe [Ausgangsrecherche](00-ausgangslage.md) — nur durch physische Hardware-Modifikation demonstriert, für den Produktivbetrieb nicht praktikabel. Für Forschungszwecke am Echo Dot 3. Gen siehe [Root-Zugriff-Recherche](04-dot-3gen-recherche.md).
