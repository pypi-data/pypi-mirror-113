# TrollDB
Just a simple json database project made by Walter.

### Installing 
### You need cryptography to use trolldb.
    pip install --upgrade trolldb
    

### Example code

    import trolldb


    database = trolldb.Database(trolldb.key_by_filename('key.trolldb')) # new database
    print('Doing database on {0}'.format(database.getfilename())) 

    v = str(1)
    database.add(v, '{0}'.format(v)) # sets variable in the database
    print(database.get(v)) # get variable 
    print(database.getplainjson()) # prints the whole json

### Getting 'key'
Trolldb will write your key into file called "key.trolldb"

    import trolldb
    trolldb.genkey()

### Creating new database (or load existing database)
    import trolldb
    database = trolldb.Database("yourkeyhere")


### Creating or changing a variable's value 
    database.add("varname", "value")

### Deleting variable
    database.remove("varname")

## Using tables
note: Tables aren't finished yet.

### Creating a new table (or load an existing table)
    import trolldb
    database = trolldb.Database("yourkeyhere")
    table = trolldb.Table.new(database, "tablename")

### Adding an element into the table (or changing an existing element)
    table.add("elemname", "value")

### Getting element value
    table.get("elemname")

### Deleting element
    table.remove("elemname")

