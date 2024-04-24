import requests

def fetch_delays(station_id, duration=60):
    api_url = f'https://v6.db.transport.rest/stops/{station_id}/departures?duration={duration}'
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        departures = data if isinstance(data, list) else data.get('departures', [])
        return departures
    except requests.RequestException as e:
        print(f"Fehler bei der API-Anfrage für Station {station_id}: {e}")
        return []

def fetch_connections(station_id):
    departures = fetch_delays(station_id)
    print(f"\nVerbindungen für Station ID {station_id}:")
    for departure in departures:
        line_name = departure.get('line', {}).get('name', 'Unbekannt')
        direction = departure.get('direction', 'Unbekannte Richtung')
        # Verspätung extrahieren und in Minuten umrechnen, Standardwert ist 0, wenn keine Verspätung vorhanden ist
        delay_seconds = departure.get('delay')
        delay_minutes = delay_seconds // 60 if delay_seconds is not None else 0  # Verspätung von Sekunden in Minuten umrechnen

        # Überprüfen, ob eine Verspätung vorliegt und entsprechend formatieren
        delay_info = f", Verspätung: {delay_minutes} Minuten" if delay_seconds is not None and delay_seconds > 0 else ", pünktlich"

        print(f"Linie: {line_name}, Ziel: {direction}{delay_info}")


def main():
    station_names = {
        '8002549': 'Berlin Hbf',
        '8000207': 'Hamburg Hbf',
        '8000105': 'München Hbf',
        '8000152': 'Frankfurt am Main Hbf',
        '8000026': 'Köln Hbf',
        '8000284': 'Stuttgart Hbf',
        '8010205': 'Leipzig Hbf',
        '8000096': 'Düsseldorf Hbf',
        '8003200': 'Hannover Hbf',
        '8000191': 'Bremen Hbf',
    }

    gesamt_verspaetungsminuten_aller_bahnhoefe = 0
    gesamt_abgefragte_linien = 0

    for station_id in station_names:
        departures = fetch_delays(station_id)
        station_verspaetungsminuten = sum(departure.get('delay', 0) for departure in departures if departure.get('delay') is not None) // 60
        gesamt_verspaetungsminuten_aller_bahnhoefe += station_verspaetungsminuten
        gesamt_abgefragte_linien += len(departures)
        print(f"\n{station_names[station_id]} (Station ID {station_id}): Gesamte Verspätungsminuten = {station_verspaetungsminuten}, Abgefragte Linien: {len(departures)}")

    # Gesamtbilanz der Verspätungsminuten und der abgefragten Linien über alle Bahnhöfe ausgeben
    print(f"\nGesamte Verspätungsminuten über alle abgefragten Bahnhöfe: {gesamt_verspaetungsminuten_aller_bahnhoefe} Minuten.")
    print(f"Gesamtanzahl der abgefragten Linien: {gesamt_abgefragte_linien}")
    test_station_id = '8000105'  # Beispiel: Berlin Hbf
    fetch_connections(test_station_id)

if __name__ == '__main__':
    main()
