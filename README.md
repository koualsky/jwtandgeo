### Run and stop
`docker-compose up` \
`docker-compose down` \
Local: http://0.0.0.0:8002/api/geolocalization/ \
Production: https://jwtandgeo.herokuapp.com/api/geolocalization/

### Register
POST request to http://0.0.0.0:8002/api/register/ - with `username` and `password`

### Login (get token)
POST request to http://0.0.0.0:8002/api/token/ - with `username` and `password`

### Using API
Add into request headers: \
Key: `Authorization` \
Value: received from http://0.0.0.0:8002/api/token/ `access` token (e.g. `Bearer 3eyJ0eXAiOi...`)

### API
GET http://0.0.0.0:8002/api/geolocalization/ - Shows list of all IP's stored in db \
GET http://0.0.0.0:8002/api/geolocalization/?address=212.77.0.98 - Shows data for specific IP in json format \
POST http://0.0.0.0:8002/api/geolocalization/ with key `address` and value (IP or URL) `185.253.212.22` or `google.com`  - Will add Geolocalization to database for given IP \
DELETE http://0.0.0.0:8002/api/geolocalization/?address=185.253.212.22 - Will delete specific Geolocalization from database 

### Admin
https://jwtandgeo.herokuapp.com/admin 
or 
http://0.0.0.0:8002/admin \
Username: `admin` \
Password: `admin`
