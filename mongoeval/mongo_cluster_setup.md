# Cluster setup for measuring distributed Mongodb with YCSB 

On 4 machines with 512 GB SSDs and 32GB RAM, 8 cores each (gpu3, gpu4, gpu5, gpu6).

#### Start the 4 shard cluster data nodes:

gpu3: (192.168.0.3)

    $ sudo mkdir /home/mongodata
    $ sudo mkdir /home/mongodata3
    $ sudo mkdir /home/mongodata4
    $ sudo mongod --port 27111 --replSet data1 --shardsvr --dbpath /home/mongodata --wiredTigerCacheSizeGB 6
    $ sudo mongod --port 27133 --replSet data3 --shardsvr --dbpath /home/mongodata3 --wiredTigerCacheSizeGB 6
    $ sudo mongod --port 27142 --replSet data4 --shardsvr --dbpath /home/mongodata4 --wiredTigerCacheSizeGB 6

gpu4: (192.168.0.4)

    $ sudo mkdir /home/mongodata
    $ sudo mkdir /home/mongodata2
    $ sudo mkdir /home/mongodata4
    $ sudo mongod --port 27112 --replSet data1 --shardsvr --dbpath /home/mongodata --wiredTigerCacheSizeGB 6
    $ sudo mongod --port 27121 --replSet data2 --shardsvr --dbpath /home/mongodata2 --wiredTigerCacheSizeGB 6
    $ sudo mongod --port 27144 --replSet data4 --shardsvr --dbpath /home/mongodata4 --wiredTigerCacheSizeGB 6

gpu5: (192.168.0.5)

    $ sudo mkdir /home/mongodata
    $ sudo mkdir /home/mongodata2
    $ sudo mkdir /home/mongodata3
    $ sudo mongod --port 27113 --replSet data1 --shardsvr --dbpath /home/mongodata --wiredTigerCacheSizeGB 6
    $ sudo mongod --port 27122 --replSet data2 --shardsvr --dbpath /home/mongodata2 --wiredTigerCacheSizeGB 6
    $ sudo mongod --port 27131 --replSet data3 --shardsvr --dbpath /home/mongodata3 --wiredTigerCacheSizeGB 6

gpu6: (192.168.0.6)

    $ sudo mkdir /home/mongodata2
    $ sudo mkdir /home/mongodata3
    $ sudo mkdir /home/mongodata4
    $ sudo mongod --port 27123 --replSet data2 --shardsvr --dbpath /home/mongodata2 --wiredTigerCacheSizeGB 6
    $ sudo mongod --port 27132 --replSet data3 --shardsvr --dbpath /home/mongodata3 --wiredTigerCacheSizeGB 6
    $ sudo mongod --port 27141 --replSet data4 --shardsvr --dbpath /home/mongodata4 --wiredTigerCacheSizeGB 6


#### Initialize the 4 shards as Replica Sets

##### Init shard 1 (data1)

From the gpu3 machine, connect to MongoDb data1_srv1 (this will be the primary of this shard's replica set)

    $ mongo --port 27111

You'll get a mongo shell, type into it: 

    > rs.initiate()

Then add the two other container's addresses to this replica set as secondaries (data1_srv2 and data1_srv3):

    > rs.add("192.168.0.4:27112")
    > rs.add("192.168.0.5:27113")
    
Check: 

    > rs.status()
    
Should print 3 members of this replica set.

Now we need to re-config the primary of the replica set to have a name that is its ip address, not the docker container's random generated name:

    > cfg = rs.conf()
    > cfg.members[0].host = "192.168.0.3:27111"
    > rs.reconfig(cfg)
    > rs.status()
    
Prints OK at the end :)

##### Init shard 2 (data2)

From the gpu4 machine, connect to MongoDb data2_srv1 (this will be the primary of this shard's replica set)

    $ mongo --port 27121

You'll get a mongo shell, type into it to add the two other container's addresses to this replica set as secondaries (data2_srv2 and data2_srv3):

    > rs.initiate()
    > rs.add("192.168.0.5:27122")
    > rs.add("192.168.0.6:27123")
    > cfg = rs.conf()
    > cfg.members[0].host = "192.168.0.4:27121"
    > rs.reconfig(cfg)
    > rs.status()

Should print OK at the end.

##### Init shard 3 (data3)

Very similar to the previous two... But now, from the gpu5 machine, connect to MongoDb data3_srv1 (this will be the primary of this shard's replica set)

    $ mongo --port 27131
    > rs.initiate()
    > rs.add("192.168.0.3:27133")
    > rs.add("192.168.0.6:27132")
    > cfg = rs.conf()
    > cfg.members[0].host = "192.168.0.5:27131"
    > rs.reconfig(cfg)
    > rs.status()
    

##### Init shard 4 (data4)

Again.. From the gpu6 machine, connect to MongoDb data4_srv1 (this will be the primary of this shard's replica set)

    $ mongo --port 27141
    > rs.initiate()
    > rs.add("192.168.0.3:27142")
    > rs.add("192.168.0.4:27144")
    > cfg = rs.conf()
    > cfg.members[0].host = "192.168.0.6:27141"
    > rs.reconfig(cfg)
    > rs.status()


#### Create a Config Server

Now we create one MongoDB config server, (which will be a replica set of 3 nodes) to manage our shard's metadata. 
Its primary node will be on the gpu4 machine. Secondaries on gpu5 and gpu6.

So, on gpu4:

    $ sudo mkdir /home/mongocfg
    $ sudo mongod --port 27151 --configsvr --replSet config --dbpath /home/mongocfg --wiredTigerCacheSizeGB 6

On gpu5:

    $ sudo mkdir /home/mongocfg
    $ sudo mongod --port 27152 --configsvr --replSet config --dbpath /home/mongocfg --wiredTigerCacheSizeGB 6
    
On gpu6:

    $ sudo mkdir /home/mongocfg
    $ sudo mongod --port 27153 --configsvr --replSet config --dbpath /home/mongocfg --wiredTigerCacheSizeGB 6
 
Then, on gpu4 connect them to form a new replica set:

    $ mongo --port 27151
    > rs.initiate()
    > rs.add("192.168.0.5:27152")
    > rs.add("192.168.0.6:27153")
    > cfg = rs.conf()
    > cfg.members[0].host = "192.168.0.4:27151"
    > rs.reconfig(cfg)
    > rs.status()
    
    
#### Create a MongoDB router (mongos)

Last step! Starting "mongos" on gpu3 (where the ycsb client will run), using the default mongodb port 27017.
Note: after the "--configdb" you have to specify <replica set name of the config server>/<address of one member of the config server Replica Set>

On gpu3:

    $ sudo mongos --port 27017 --configdb config/192.168.0.4:27151




    
    
    
    