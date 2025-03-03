# cash_register


This is a simple django rest app which imitates cash register.


The API receives requests in format: 

POST {{root}}/cash_machine

  {
  "items": [1,2,3]
  }

where items are the array of goods id's of the Item model.

The server generates check in pdf format. 

The check has fields:

1) For each item:
  - Name
  - Total amount
  - price
2) Total price
3) Check creation time (DD.MM.YYYY H:M)

The server saves the check, generates link to it as a QR-code which is a response to request.

Scanning QR-code will commit GET {{root}}/media/< filename >

the response to which is the file.


## Getting started
To start Docker from main directory:

```sh
$ docker compose up --build
```
