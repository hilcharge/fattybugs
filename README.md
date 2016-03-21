# fattybugs
This is a basic python module and scripts for working with sqlite3 bug tracking database. This is a really easy way to level up on the JOEL test, because it has the 5 required fields and only requires having python. The scripts are very compatible with Unix commands such as `grep` and `awk`. This is made especially for a small team of programmers, with the main goal of being able to deploy and use a bug tracking system within minutes.

It includes scripts for basic tasks, and a module with a basic API for anyone who is interested in building a larger application. 

It has not been tested with any teams larger than one (myself). Larger teams or teams with trust issues should probably consider a more feature rich tool set, although everyone is free to, and encouraged to try to use this as a starting point for any larger applications, but please do not blame me if it turns out not to work.

Any feedback is greatly appreciated.


Install
--------

    $ git clone https://github.com/hilcharge/fattybugs
    $ cd fattybugs
    $ python setup.py install


Synopsis
------------

Build a bug database

    $ fbdb_build_bug_db /path/to/bug_db.db

Add a bug to the database, following command prompts

    $ fbdb_add_bug
    Enter reproduction steps (input ends after a blank line):
    Try to do something amazing

    Enter expected behavior (input ends after a blank line):
    Something amazing happens

    Enter observerd behavior (input ends after a blank line):
    The program tells me I am weak. 
    That is not amazing. I am told that everyday.

    Enter the bug name > nothing amazing happens

    Enter the assigned person > Hilcharge


List the bugs in the database
(Note: This is perfect for Unix tools like `grep` and `awk`)

    $ fbdb_list_bugs    
    ************
    nothing-amazing-happens	date_created	2016-03-21 08:54:01.237387
    nothing-amazing-happens	bug_name	nothing-amazing-happens
    nothing-amazing-happens	reproduction_steps	Try to do something amazing
    nothing-amazing-happens	fixed	0
    nothing-amazing-happens	assigned_to	Hilcharge
    nothing-amazing-happens	observed_behavior	The program tells me I am weak. ;; That is not amazing. I am told that everyday.
    nothing-amazing-happens	expected_behavior	Something amazing happens
    ************

Fix a bug
    
    $ fbdb_fix_bug nothing-amazing-happens

    $ fbdb_list_bugs
    $ ## No more bugs!

Reassign the bug

    $ fbdb_reassign_bug nothing-amazing-happens "Luke Skywalker"


Summary
--------

Module for dealing with a very simple sqlite bug-tracking database

The database is just a table with seven columns as follows:

* The five JOEL test columns:
    * reproduction_steps
    * expected_behavior
    * observed_behavior
    * assigned_to
    * fixed
* Identifier:
    * bug_name
* The two following date columns, which are handled automatically
    * date_created
    * date_fixed


NO OTHER COLUMNS should be relied on. This is made as a basic way to level up in the JOEL test for software development.

If you want to add more columns to the table, that is fine, but do not rely on this module.

Ok, now let's look at how to use this

Module usage
--------------

### Make a bug database ###
   
    > from fattybugs import fattybugs
    > db_file="/path/to/shared/bug_db.db
    > bdb=fattybugs.build_db(db_file,write_config=True)
    # Setting write_config=True will cause a ".fattybugs" file to bewritten in your $HOME directory

### Create a connection ###

Connect to the default BugDB as follows:

    > bdb=fattybugs.default_BugDB()

This will create a connection to the bug database defined in your .fattybugs
If you have some different bug database, you can use the following sequence:

    > bugdb=fattybugs.BugDB(DB_FILENAME)

DB_FILENAME can be retrieved from your configuration file if you wish:
    > DB_FILENAME=fattybugs.default_bug_db()

You can use a different configuration file too:
    > DB_FILENAME=fattybugs.default_bug_db("other_config_file")
    ## Each config file needs only a "bug_db" section with a "db_file" option in it specifying the path


### List all the unfixed bugs ###

Use the list_bugs method

    > bugdb.list_bugs()


### Create a new bug via prompts ### 

    > bugdb.new_bug()


You can include values in the input to this method to avoid prompting

    > bugdb.new_bug(reproduction_steps="...",expected_behavior="...",observed_behavior="...",assigned_to="...",bug_name="...")


### Fix a bug ###

    > bugdb.fix_bug(bug_name="...")

If no bug_name is input, then you can choose from the list


### Retrieve details about a bug ###

    > bugdb.bug_data(bug_name="my-bug-name")

OR
 
    > bugdb.bug_data(bug_id=2)
 

### Display details about a bug ### 

    > bugdb.bug_details_display(bug_name="my-bug-name")

OR
 
    > bugdb.bug_details_display(bug_id=2) 



### Reassign a bug ###

    > bugdb.reassign("New Person",bug_id=2)    


