sleep 5
mongosh --host "mongodb-primary" --port "27017" --username "user" --password "password" --eval 'rs.initiate({
    "_id": "rs",
    "protocolVersion": 1,
    "version": 1,
    "members": [
        {
            "_id": 0,
            "host": "mongodb-primary:27017",
            "priority": 5
        },
        {
            "_id": 1,
            "host": "mongodb-secondary:27017",
            "priority": 1
        },
        {
            "_id": 2,
            "host": "mongodb-arbiter:27017",
            "priority": 0
        }
    ],settings: {chainingAllowed: true}
},
{
  force: true
})'
mongosh --host "mongodb-primary" --port "27017" --username "user" --password "password" --eval 'rs.status()'
