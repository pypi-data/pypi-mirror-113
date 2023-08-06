# Iris - Verwaltung von Events

## Event

```__init__```: Konstruktor, der eine beliebige Anzahl an Funktionspointern nimmt, die ans Event gebunden werden.


```add_function```: Bindet neue Funktionen an das Event.


```remove_function```: Entbindet Funktionen vom Event.


```emit```: Löst das Event aus und ruft alle Funktionen nacheinaner auf mit den dieser Funktion gegebenen Argumenten auf.


```__iadd__```: Selbe Funktion wie ```add_function```


```__isub```: Selbe Funktion wie ```remove_function```


```__call__```: Selbe Funktion wie ```emit```


```__repr_```: Representationsstring des Events mit den gebundenen Funktionen.


```function```: Property-Attribut, das die Liste der gebundenen Funktionen liefert zur einfachen Manipulation.


## Handler

```__init__```: Konstruktor, der den Handler initialisiert.


```get_event_names```: Liefert die Namen aller erstellten Events.


```remove```: Löscht das Event mit dem gegebenem Namen.


```__repr__```: Representationsstring mit den Namen der Events


Möglichkeiten ein neues Event zu erstellen mit:
- Dem Namen des Events
- Den zu bindenen Funktionen

* ```new```
* ```__setitem__```

Möglichkeiten ein Event zu löschen:

* ```remove```
* ```__delitem__```
* ```__delattr__```

Möglichkeiten ein Event von seinem Namen her zu erhalten:

* ```__getitem__```
* ```__getattr__```
