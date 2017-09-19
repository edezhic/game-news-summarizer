#!/bin/bash
#Force file syncronization and lock writes

MONGODUMP_PATH="/root/mongodump"
MONGO_HOST="104.131.65.102" #replace with your server ip
MONGO_PORT="81"
MONGO_DATABASE="meteor" #replace with your database name

TIMESTAMP=`date +%F-%H%M`
S3_BUCKET_NAME="briefslivemongobackup" #replace with your bucket name on Amazon S3
S3_BUCKET_PATH="mongodb-backups"

# Create backup
#$MONGODUMP_PATH -h $MONGO_HOST:$MONGO_PORT -d $MONGO_DATABASE
mongodump --port 81 --db meteor --out /root/mongodb_$TIMESTAMP/

# Add timestamp to backup
#mv dump mongodb-$HOSTNAME-$TIMESTAMP
tar -cf mongodb_$TIMESTAMP.tar mongodb_$TIMESTAMP

# Upload to S3
s3cmd put mongodb_$TIMESTAMP.tar s3://$S3_BUCKET_NAME

rm mongodb_$TIMESTAMP.tar
rm -r mongodb_$TIMESTAMP
