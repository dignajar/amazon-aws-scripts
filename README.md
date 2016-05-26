# Amazon AWS scripts

## snapshot.py
Create and delete old snapshot.
When execute the script this will be create an snapshot of a volumeID, on the description of the snapshot will appear expiration date.

### Variables configuration
Edit the variables inside the file.

```
# Volume ID for snapshot
volumenID = "vol-XXXX"

# Username with permissions, credentials are in .aws/credentials
username = "snapshot"

# Region name
region = "us-east-1"

# Amount of snapshot
snapshotAmount = 2
```

For example if you create an snapshot on 25 May 2016, the snapshot will expire on 27 May 2016, the variable `snapshotAmount` has the expiration amount of day.

