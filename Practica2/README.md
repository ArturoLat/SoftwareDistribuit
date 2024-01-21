# Practica2
Codi de la Practica2 Software Distribuit

## Taula de continguts

* [Testing](#Testing)
* [Docker](#Docker)
* [Explicacio Codi](#Explicacio)
* [Modificacio per la Reavaluació](#Reavaluacio)
* [Execució Codi](#Execució)


## Testing

En la sessió de testing vem arribar sense la S6 implementada però encara així vem poder probar el nostre programa per poder veure alguns errors:
- Es podia comprar entrades amb diners en negatiu.
- Es podia comprar entrades sense compte iniciada.
- Els servidors amb la ip de la universitat no ens anaven.

Vem anar mirant els projectes de els nostres companys i molta gent no havia avançat per poder fer un bon testing. Els companys que la tenien més o menys feta tenien bones implementacions o sense error a primera vista. 

## Docker

  - Backend: https://hub.docker.com/repository/docker/arturolat/practica-2-b10-backend/general
  - Frontend: https://hub.docker.com/repository/docker/arturolat/practica-2-b10-frontend/general

## Explicacio

- Aquesta práctica ha estat feta conjuntament per trucades per la aplicació "Discord" i treballat setmana a setmana durant les sessions de classe. Hem fet una bona implementació tant del backend com del frontend. Al final  no hem protegit tants mètodes, ja que en la nostra implementació no ha fet falta.
- A la creacio de matches, es obligatori passar una url que sigui de les que estan a la llista url_llist, que son imatges que estan a frontend/static. 
- Totes les alertes estan controlades per $alert, que es una alerta de vue, no una alerta cutre predeterminada
- Sessió 4 exercici 3, modificat per a que retorni una llista dels orders per un usuari
- Hem fet que els botons + i - de la cesta, desapareguin si no tens el ratoli per sobre. I si no tens una compta iniciada de sessio, no et deixa afegir matches al carrito

## Reavaluacio

- Hem afegit uns ifs per la creació de matches, en cas que no hi haguin equips locals existents i competicions, no es podra crear.
- Hem arreglat el get_matches_by_details, ja que sempre donava que existia.
- Hem afegit al requeriments.txt els RUN pip installs que teniem al docker, i els hem eliminat d'alla.
- Creació del https per la prova de la reavaluació. On es crea dos teams, una competició i un matches.

## Execució
1) Fem la comanda per executar el docker: docker-compose up -d --build
