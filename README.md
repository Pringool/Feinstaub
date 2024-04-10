# Feinstaub!

## 1. Einleitung:
   - **Projektziel:** Entwicklung einer Anwendung zur Auswertung von Feinstaubanalysen der TBS1.
   - **Hintergrund:** Der Hintergrund des Projekts ist ein Schulprojekt.

## 2. Anforderungen an die Software:
   ### 2.1 Funktionale Anforderungen:
   - **2.1.1** Download von CSV-Feinstaubdaten von einem Server auf das lokale Gerät.
   - **2.1.2** Import der zuvor heruntergeladenen Daten in eine SQLite-Datenbank.
   - **2.1.3** Grafische Oberfläche zum Herunterladen und Hochladen in einem bestimmten Zeitraum.
   - **2.1.4** Visualisierung von Daten in der grafischen Oberfläche.
   
   ### 2.2 Nicht-funktionale Anforderungen:
   - **2.2.1** Performanceverbesserung des Herunterladens durch Multi-Threading.

## 3. GUI (Graphical User Interface):
   - **3.1** Eingabefeld für Start- und Enddatum des Downloadzeitraums.
   - **3.2** Eingabefeld für Start- und Enddatum des Auswertungszeitraums.
   - **3.3** Grafische Anzeige des zuvor definierten Auswertungszeitraums.
   - **3.4** Daten via Knopfdruck in die Datenbank importieren.
   - **3.5** Daten via Knopfdruck lokal löschen.
   - **3.6** Knopfdruck für den Start des Downloads.
   - **3.7** Knopfdruck für den Start der Auswertung.
   - **3.8** Visualisierung des Downloadfortschritts als Ladebalken.

## 4. Verwendete Libraries:
   ### 4.1 Externe Libraries:
   - **4.1.1** [tqdm](https://pypi.org/project/tqdm/) wird verwendet, um den Downloadfortschritt zu visualisieren.
   - **4.1.2** Mit [PyQt6](https://pypi.org/project/PyQt6/) erstellen wir die GUI.
   - **4.1.3** [Matplotlib](https://matplotlib.org/) verwenden wir, um die Daten als grafische Darstellung anzuzeigen.
   
   ### 4.2 Python-interne Libraries:
   - **4.2.1** [sqlite3](https://docs.python.org/3/library/sqlite3.html) - das Datenbanksystem zum Speichern der Analysen.
   - **4.2.2** [os](https://docs.python.org/3/library/os.html) wird verwendet, um auf das lokale Betriebssystem zuzugreifen und Funktionen anzuwenden.
   - **4.2.3** [glob](https://docs.python.org/3/library/glob.html) wird verwendet, um die Dateien zu finden und darauf zuzugreifen.
   - **4.2.4** [requests](https://requests.readthedocs.io/en/latest/) - es wird hiermit eine Anfrage an den Server gesendet, um eine Verbindung aufzubauen.
   - **4.2.5** [calendar](https://docs.python.org/3/library/calendar.html) damit wird ein konkretes Datum verwendet können.
   - **4.2.6** [concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html) benutzen wir, um das Multi-Threading zu ermöglichen.
