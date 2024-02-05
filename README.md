# Smart Home Steuerungssystem

Diese Flask-Anwendung ermöglicht die Steuerung verschiedener Smart-Home-Geräte über ein einfaches Web-Interface. Unterstützt werden Geräte von Kasa (TP-Link), Shelly und Tapo. Zu den Funktionen gehören das Ein- und Ausschalten von Lampen, die Abfrage des aktuellen Stromverbrauchs und die Überwachung der CPU-Temperatur des Servers.

## Funktionen

- Steuerung von Shelly Geräten (Ein/Aus)
- Steuerung von Kasa Smart Plugs (Ein/Aus, Statusabfrage)
- Abfrage von CPU-Temperatur und Systeminformationen
- Abfrage der Stromaufnahme von Tapo-Geräten

## Voraussetzungen

- Python 3.x
- flask
- Kaskade
- ShellyPy
- asyncio
- tapo

## Installation

Stellen Sie sicher, dass Python 3 und pip auf Ihrem System installiert sind. Installieren Sie dann die benötigten Pakete mit

```bash
pip install flask kasa ShellyPy asyncio tapo


Die Anwendung
Die Applikation bietet verschiedene Wege, um die Smart Home Geräte zu steuern und Systeminformationen abzurufen:

GET / - Lädt die Startseite der Anwendung.
GET /wohnzimmer_deckenlampe_an/ - Schaltet die Deckenlampe im Wohnzimmer ein.
GET /wohnzimmer_deckenlampe_aus/ - Schaltet die Deckenlampe im Wohnzimmer aus.
GET /schlafzimmer_deckenlampe_an/ - Schaltet die Deckenlampe im Schlafzimmer ein.
GET /schlafzimmer_deckenlampe_aus/ - Schaltet die Deckenlampe im Schlafzimmer aus.
GET /schlafzimmer_wand_an/ - Schaltet den Wandschalter im Schlafzimmer ein (Kasa Smart Plug).
GET /schlafzimmer_wand_aus/ - Schaltet den Wandschalter im Schlafzimmer aus.
GET /cpu_temp/ - Zeigt die CPU-Temperatur und andere Systeminformationen an.
GET /plug_workstation/ - Zeigt den aktuellen Stromverbrauch der Workstation an.
GET /plug_kitchen/ - Zeigt den aktuellen Stromverbrauch der Küche an.
GET /mariadb/status - Zeigt den Status des MariaDB-Servers an.
GET /command/<cmd> - Führt einen benutzerdefinierten Befehl aus und gibt das Ergebnis zurück.
