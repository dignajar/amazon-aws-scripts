#!/usr/bin/python

# Edit this variables
# ------------------------------------------------------------------------------

# Volume ID for snapshot
volumenID = "vol-eb194f49"

# Username with permissions, credentials are in .aws/credentials
username = "snapshot"

# Region name
region = "us-east-1"

# Amount of snapshot, each snapshot it's per day
snapshotAmount = 2

# Libraries
# ------------------------------------------------------------------------------
import boto3
import json
from datetime import datetime, timedelta

# Today and tomorrow date
# ------------------------------------------------------------------------------
todayDate = datetime.today()
tomorrowDate = todayDate + timedelta(days=snapshotAmount)

# Session
# ------------------------------------------------------------------------------
session = boto3.Session(profile_name=username)

# IAM session
# ------------------------------------------------------------------------------
iam = session.client("iam")
iamOwenerID = iam.get_user()['User']['Arn'].split(':')[4]

# EC2 session
# ------------------------------------------------------------------------------
ec2 = session.client("ec2", region_name=region)

# Create snapshot
# ------------------------------------------------------------------------------

# All snapshot has the description "backup_delete_on:Tomorrow date"
description = "backup_delete_on:"+tomorrowDate.strftime("%Y-%m-%d")

# Launch create snapshot
print "Creating snapshot..."
print ec2.create_snapshot(VolumeId=volumenID, Description=description)
print ""

# Delete old snapshots
# ------------------------------------------------------------------------------

# snapshot list
snapshotList = ec2.describe_snapshots(OwnerIds=[iamOwenerID])
for snap in snapshotList['Snapshots']:

    # snapshot ID
    snapID = snap['SnapshotId']

    # snapshot descripton
    snapDescription = snap['Description']

    # if the snapshot description has "backup_delete_on"
    if snapDescription.split(":")[0] == "backup_delete_on":

        # get the snapshot date
        snap_date = datetime.strptime(snapDescription.split(":")[1], "%Y-%m-%d")

        # if the snapshot date is today, delete them
        if snap_date < todayDate:
            print "Deleting snapshot: ID "+snapID+", Date "+snapDescription.split(":")[1]
            print ec2.delete_snapshot(SnapshotId=snapID)
            print ""


