# contriboard-populator
Contains contriboard database populator scripts written in python and using
Fabric framework

# Dependencies
- fabric
- pymongo
- loremipsum
- requests

# Use
```
fab populate

fab populate_random

fab clear_database

fab take_snapshot

fab list_snapshots

fab restore
```

# Configure
Change conf in `conf.yml`
