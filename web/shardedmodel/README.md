## Design Docs URL: [Design Doc](https://docs.google.com/document/d/1PrYXJseTim2uXs_CEQpyBu3VX9WzG1DHMAZJ9H7zzeU/edit?ts=5dd1ec19#)

### Project Scope

We developed a scalable model class that inherits from the Django model class. This class supports the following functionalities. It can look up the shard key automatically from the user-defined model to do a horizontal partition (sharding).

The project also implemented a router class to support this feature. The router needs to support migration when a host no longer has enough storage to hold the logical shards in it. It allows the user to specify a host where the logical shards will reside in after migration. The router also directs read/write operations to the corresponding host based on the shard key. During the migration, read operations will only be directed to the original host whereas writes commands will be directed to both hosts, which is called a dual-write process.

A web-based dashboard was also implemented that allows users to initiate the sharding process and visualize the dual write query routing strategy during the migration. 

