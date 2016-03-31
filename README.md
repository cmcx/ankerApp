The AnkerApp (or AnchorApp) computes the necessary rode lengths for different wind situations, taking into account the data of your individual setup (boatlength, chainlength, chain diameter, anchorweight, type of anchor) and situation (depth, seabed quality, windspeed). The initial formulas were taken from the Excel sheet created by Alain Fraysse. 

The rodeanch_diagrams program computes a set of diagrams showing necessary rode lengths for different windspeeds and different water depths and some other useful combinations that can be printed out and used when needed. 


Das erste Programm der AnkerApp (ankerApp.py) berechnet die nötigen Geschirrlängen für unterschiedliche Gegebenheiten auf der Grundlage individueller Schiffsdaten und bestimmter Eigenschaften des Ankerplatzes. Die Last, die auf das Ankergeschirr wirkt, wird aus der Bootslänge abgeleitet. Das Ankergeschirr ist definiert durch Kettenlänge, Kettendurchmesser, Ankergewicht und Ankertyp (Anker mit High Holding Power oder klassischer Anker). Die Eigenschaften des Ankerplatzes sind Tiefe, Ankergrund und Windgeschwindigkeit. 
Das Programm berechnet aus diesen Daten die richtige Länge des Ankergeschirrs für nur Kette und Kette mit Leine bei einem gegebenen Zugwinkel der Kette am Anker (hier sind fünf Grad ein guter Wert). Außerdem liefert das Programm eine minimale Geschirrlänge, die die (theoretische) Haltekraft des Ankers voll ausreizt. Diese Information ist interessant, um mit dem eigenen Geschirr zu experimentieren und wenn der Schwojkreis begrenzt ist.

Das Szenario für Kette ohne Leine ist in erster Linie für schwachwindige Situationen interessant. Ein Geschirr, das nur aus Anker und Kette besteht, erzeugt deutlich höhere Lasten als ein Geschirr mit Kette und Leine. Selbst wenn ausreichend Kette zur Verfügung steht sollte also eine wenigstens sechs Meter lange Entlastungsleine ins Ankergeschirr integriert werden.

Die gesamte Mathematik wurde aus einer Excel-Tabelle von Alain Fraysse (http://alain.fraysse.free.fr) übernommen.
**Disclaimer:** Die berechneten Diagramme basieren auf theoretischen Annahmen und können höchstens bei einer Einschätzung helfen, sind aber keine zuverlässigen Vorgaben für spezifische Situationen!

### Diagramme

Das zweite Programm der AnkerApp (ankerApp_diagrams.py) erzeugt eine Reihe von Diagrammen mit Informationen zu Lasten und Geschirrlängen, abgestimmt auf die individuellen Schiffsdaten. Der Vorteil der Diagramme ist, dass sich hier die nötige Geschirrlänge für mehrere Situationen an einem Schaubild ablesen lässt, sodass die Daten nur einmal eingegeben werden müssen. Die Diagramme liefern außerdem einen guten Überblick über die möglichen Grenzfälle des eigenen Geschirrs.

Das erste Diagramm zeigt die nötige Geschirrlänge für Tiefen von 4-10 Metern. Die Tiefe setzt sich zusammen aus Wassertiefe und Freibord! 
Bei einer Wassertiefe von 7 Metern und einem Freibord von 1 Meter ist also der Wert für eine Tiefe von 8 Metern ausschlaggebend.
Das zweite Diagramm zeigt die nötige Geschirrlänge für Tiefen von 12-24 Metern. Auch hier gilt Tiefe = Wassertiefe plus Freibord.
Das dritte Diagramm zeigt die theoretische Last auf dem Ankergeschirr, die dynamische Last (Kette plus Leine) und die Last, wenn nur Kette verwendet wird.
Das vierte und fünfte Diagramm zeigen Vergleichswerte für verschiedene Bootslängen und dienen eher einer Einschätzung der Berechnungsgrundlage als dem praktischen Nutzen an Bord.
Das sechste Diagramm zeigt das minimale Ankergewicht bei einer optimalen Zugrichtung (max. 5 Grad) der Kette am Anker für verschiedene Windgeschwindigkeiten und verschiedene Haltekoeffizienten des Ankergrunds (exzellent bis schlechter Ankergrund).


