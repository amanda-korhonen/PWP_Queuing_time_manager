## Runnin client on localhost
```
python -m http.server 8000
```

## Helpful links for testing
Create new place -> http://localhost:8000/templates/create.html?type=place

Edit place (for example: Bar1) ->  http://localhost:8000/templates/edit.html?type=place&place=Bar1

Create new queue for place (for example: Bar1) ->  http://localhost:8000/templates/create.html?type=queue&place=Bar1

edit queue in place (for example: Bar1 queue=General) -> http://localhost:8000/templates/edit.html?type=queue&place=Bar1&queue=General

## Test Client
To get client code quality using ESLint: 

Note: you need Node.js with this.
```
npm run lint
```