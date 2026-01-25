Feature: Kind Verwaltung
  Als Vereinsvertreter
  Möchte ich Kinder im System verwalten können
  Damit sie an Wettkämpfen teilnehmen können

  Scenario: Kind erfolgreich anlegen
    Given ein Verband "Bezirk Nord" existiert
    And eine Versicherung "SchutzSchwarm" existiert
    When ich ein Kind "Max Mustermann" mit Geburtsdatum "2014-05-12" anlege
    Then sollte das Kind "Max Mustermann" im System existieren
    And das Kind sollte dem Verband "Bezirk Nord" zugeordnet sein

  Scenario: Kind Liste abrufen
    Given ein Verband "Bezirk Süd" existiert
    And eine Versicherung "AquaSchutz" existiert
    And ein Kind "Anna Fischer" existiert bereits
    And ein Kind "Tom Schmidt" existiert bereits
    When ich die Liste aller Kinder abrufe
    Then sollten mindestens 2 Kinder in der Liste sein
