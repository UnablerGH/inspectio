Feature: Endpoints hospitacji

  Scenario: Pobieranie hospitacji dla pracownika
    Given aplikacja jest uruchomiona
    When wysyłam żądanie GET do "/api/hospitacje/1"
    Then otrzymuję status 200
    And odpowiedź zawiera "termin"

  Scenario: Pobieranie szczegółów hospitacji
    Given aplikacja jest uruchomiona
    When wysyłam żądanie GET do "/api/hospitacja/1"
    Then otrzymuję status 200
    And odpowiedź zawiera "przedmiot_nazwa"

  Scenario: Zatwierdzanie hospitacji
    Given aplikacja jest uruchomiona
    When wysyłam żądanie POST do "/api/hospitacja/1/zaakceptuj"
    Then otrzymuję status 200
    And odpowiedź zawiera "message"
