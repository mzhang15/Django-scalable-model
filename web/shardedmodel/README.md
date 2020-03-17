## Design Docs URL: [Design Doc](https://docs.google.com/document/d/1PrYXJseTim2uXs_CEQpyBu3VX9WzG1DHMAZJ9H7zzeU/edit?ts=5dd1ec19#)

### Project Scope

We are writing a scalable model class that inherits from the Django model class. This class supports the following functionalities. It can look up the shard key automatically from the users-defined models to do a horizontal partition (sharding).

We are also implementing a router class to support this feature. The router needs to support migration when a host no longer has enough storage to hold the logical shards in it. We will allow the user to specify which host each logical shard will reside in after migration. The router will also direct read/write operations to the corresponding host based on the shard key. During migration, read commands will only be directed to the original host whereas writes commands will be directed to both hosts.

We will implement a web-based dashboard that allows users to initiate the sharding process and visualize the dual write query routing strategy during the migration. 

