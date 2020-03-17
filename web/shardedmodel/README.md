## Design Docs URL: [Design Doc](https://docs.google.com/document/d/1PrYXJseTim2uXs_CEQpyBu3VX9WzG1DHMAZJ9H7zzeU/edit?ts=5dd1ec19#)

### Project Scope

We developed a scalable model class that inherits from the Django model class. This class supports the following functionalities. It can look up the shard key automatically from the user-defined model to do a horizontal partition (sharding).

The project also implemented a router class to support this feature. The router needs to support migration when a host no longer has enough storage to hold the logical shards in it. It allows the user to specify a host where the logical shards will reside in after migration. The router also directs read/write operations to the corresponding host based on the shard key. During the migration, read operations will only be directed to the original host whereas writes commands will be directed to both hosts, which is called a dual-write process.

A web-based dashboard was also implemented that allows users to initiate the sharding process and visualize the dual write query routing strategy during the migration. 

### Demo
Demo link: http://35.223.59.213:8080/mapping (use http instead of https)
Project Github link: https://github.com/mzhang15/Django-scalable-model/tree/master/web/shardedmodel
If you don’t want to read the detailed demo explanation, please go straight to Do a sharding migration
If anything goes wrong during the demo, please try clicking Reset and Populate or Reset and delete to reset the demo app to a clean state. Also, I will be available for questions/troubleshooting via email or google hangout at yz3359@nyu.edu.

#### 1.Demo setup:
- a.Models that require sharding in demo app inherits from ShardModel in Scalable and Specify its is_root field:

Root models such as User needs to set is_root to True, and its child models needs to set is_root to False

- b.User needs to set the CUSTOMIZED_MODEL_MODULE and SHARDABLE_MODELS variable in the setting.py file.

CUSTOMIZED_MODEL_MODULE defines the model file to import and  SHARDABLE_MODELS specifies models that are shardable from the model file. 
The SHARDABLE_MODELS is a comma delimited string.

In our demo, the models are from models.py of demo app and the two Shardable models are User and Post. If you have a model such as auth that you do not wish to use the ShardRouter, DON’T specify the model in SHARDABLE_MODELS string
- c. User needs to add 'scalable.apps.ScalableConfig' to their settings.py file.
- d. During django migration, user has to use:
$ python manage.py migrate --database ‘db_name’ (e.g. db1)
To migrate to each registered database
#### 2. Demo Usage:
Bold font feature text indicates which app the feature belongs to, only expect
Sharded-Model features when you are building your own app with Sharded-Model

- a. View current mapping and Migrate data from one database to another Sharded-Model feature:
Mappings url:  http://35.223.59.213:8080/mapping



Please see Generate logical shard number and mapping from shard to host for the explanation of this mapping table.

Reset and Delete Button(Use for testing with customized data): Resets the Mapping to its initial state of only having one database db1 and deletes all model instances. 
Reset and Populate Button (Use for testing with pre-populated data) : Resets the Mapping to its initial state of only having one database db1 then deletes and re-populates all model instances. We will have some sample users and sample posts ready. The sample Users have names as their primary key, however, they should not be duplicates. (The Reset and Populate is not a feature of sharded-model, it's just for easier demo)

Migrate Button: The Migrate Button opens up a modal for the user to input the name of their target database for migration. 
The only supported db names are: db2, db3, db4, db5. (Unfortunately, if you type anything other than these database names, you will need to click the Reset and Delete Button button to reset) 
We only support migration to empty databases, so if you have already migrated to db2, please don’t migrate to it again. 

- b. View Users in each database Demo feature:
Entry point urls: 
http://35.223.59.213:8080/demo/users/db1
http://35.223.59.213:8080/demo/users/db2
http://35.223.59.213:8080/demo/users/db3
http://35.223.59.213:8080/demo/users/db4
http://35.223.59.213:8080/demo/users/db5

The ADD USER button acts as a register button on a website’s home page, it does not indicate that you are adding to db1 if you are on db1’s display page. The User added will be assigned a shard number based on the hash of the primary key and saved to proper db based on the shard number calculated. 

Note: to get a specific user, click the GET USER button and enter the primary key of the user and click save changes button. If the user is found in the database, the primary key will stay in the form. Otherwise, it will be cleared out in the form. 

Each url shows the users that are stored in each database from db1 to db5

Our recommendation is to open these 5 urls in 5 different tabs before the migration so you can view the change in database data prior/post data-sharding migration. (You need to refresh the page after you do migration on mapping page)

The implementation of the view for this page is as below
Link to code

The GET request calls User.objects.using method with the db from request to get all instance of the object from the requested db. Thus the page is actually displaying models stored in each database.

- c. View and add Posts to each user Demo feature:

Entry point urls: http://35.223.59.213:8080/demo/posts/<user_pimary_key>
Or You can simply click on the name of the User to see all of its posts and use add post button to add a post.
Link to code
The code for getting post also uses the real get method of Post.objects with shard_key as a parameter.




- d. Let’s do a sharding migration

  - 1. Go to the mapping page and click Reset and Populate to reset mappings and data in all dbs http://35.223.59.213:8080/mapping

  - 2. Go to db1 display page to see all data stored in db1: 
Click on the Database 1 link on webpage or
Go to http://35.223.59.213:8080/demo/users/db1

There should be 6 users with randomly generated posts in db1.
You can see their posts by clicking on their names

    - 3. Go to db2 display page to see all data stored in db2:
Click on the Database 2 link on webpage or 
Go to http://35.223.59.213:8080/demo/users/db2
 
There should be no users


    - 4. Go to the mapping page and click on migrate button to initiate a migration.
Type db2 as the target db and click save changes in the modal:

  - 5. Now the Mapping table shows the read and write state of dbs during migration:

The read with permission 1 will always go to db1, and writes with permission db2 will alway dual write to both db1 and db2. (We were not able to change the django code to perform dual writes) 
Please wait for 5s for the mapping table to refresh and show 4 rows, and that indicates the migration is completed:


  - 6. Go to db1 display page and refresh: http://35.223.59.213:8080/demo/users/db1
Some of the Users should be deleted and has been migrated to db2. The distribution of users might not be exactly half and half because we are using hashing to distribute users.

  - 7. Go to db2 display page and refresh: http://35.223.59.213:8080/demo/users/db2
Db2 should have the rest of the users 

  - 8. Check to see that the posts of each user are migrated them.

  - 9. You can also use the Reset and delete button to delete all users, and use add user button on any db page to add your custom users (primary key must be unique). And use add post button on each user’s page to add your custom posts to that user.

Note: The ADD USER button acts as a register button on a website’s home page, it does not indicate that you are adding to db1 if you are on db1’s display page. The User added will be assigned a shard number based on the hash of the primary key and saved to proper db based on the shardModel router. 

Note: to get a specific user, click the GET USER button and enter the primary key(Username) of the user and click save changes button. If the user is found in the database the current url points to, the primary key will stay in the form. Otherwise, it will be cleared out of the form. 



