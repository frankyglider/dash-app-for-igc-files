Projektbeschreibung: IGC-Datei-Visualisierung und -Speicherung mit AWS RDS und Dash

IGC-Datei-Visualisierung

Beschreibung:
Das IGC-Datei-Visualisierungsprojekt mit AWS RDS, Dash und AWS Lambda ermöglicht die einfache Aufzeichnung und grafische Darstellung von Flugdaten aus IGC-Dateien. Die Anwendung bietet zwei Hauptfunktionen: das Speichern von Flugdaten in einer AWS RDS-Datenbank mithilfe von Drag & Drop oder einem direkten API-POST-Anforderungsprozess und die Visualisierung dieser Daten in einer Dash-Webanwendung. Eine AWS Lambda-Funktion, die mit AWS API Gateway verbunden ist, erleichtert die Datenbankinteraktion.

Funktionsweise:

    Datenbank-Setup:
        Das Projekt nutzt Amazon RDS (Relational Database Service) zur Speicherung von Flugdaten. Die RDS-Datenbank wird so konfiguriert, dass sie IGC-Dateien aufnehmen kann.

    AWS Lambda und API Gateway:
        Eine AWS Lambda-Funktion wird eingerichtet und mit AWS API Gateway verknüpft. Diese Funktion nimmt die IGC-Dateien über HTTP POST-Anfragen entgegen, verarbeitet sie und speichert die Daten in der RDS-Datenbank.

    Dash Webanwendung:
        Die Dash-Webanwendung stellt eine benutzerfreundliche Oberfläche zur Verfügung.
        Benutzer können IGC-Dateien per Drag & Drop in die Anwendung hochladen oder direkte API-Anfragen senden, um die Daten zu speichern.
        

    Datenvisualisierung:
        
        Ein Höhendiagramm zeigt die Änderungen der Flughöhe über der Zeit an.
        Eine interaktive Karte zeigt die Flugbahn.

Projektvorteile:

    Einfache Datenerfassung: Benutzer können Flugdaten problemlos per Drag & Drop in die Anwendung hochladen oder direkte API-Anforderungen senden.

    Datenvisualisierung: Die Anwendung erstellt interaktive Höhendiagramme und Flugbahnen, um die Flugdaten ansprechend darzustellen.

    AWS-Integration: Die AWS-Plattform bietet eine zuverlässige und skalierbare Lösung zur Speicherung und Verarbeitung von Flugdaten.

Projektverwendung:

    Luftsportarten: Dieses Projekt ist ideal für Piloten und Enthusiasten von Luftsportarten, die ihre Flüge aufzeichnen und analysieren möchten.

    Flugüberwachung: Flugüberwachungsdienste können von dieser Anwendung profitieren, um Flugverläufe und -daten effizient zu erfassen und zu analysieren.

    Luftfahrtausbildung: Schulen und Ausbildungsstätten für Luftfahrt können dieses Tool zur Veranschaulichung und Analyse von Schulungsflügen nutzen.
