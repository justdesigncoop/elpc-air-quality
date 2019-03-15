rm backup/*

for table in hexagons measurements neighborhoods notes sessions streams tracts users wards zipcodes; do
    echo "creating: $table.tsv"
    mysql --user=elpcjd --password=Elpc1234 --database=elpc_air_quality --execute="SELECT * FROM $table" > backup/$table.tsv
done

zip -r backup/backup.zip backup/*.tsv

