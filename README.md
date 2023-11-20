# LastResort
## A Password Management and Vault Application

LastResort is a simple password management application focusing on storing passwords and information in a centralized program. LastResort was meant to be a school prototype version which can be used as a password management application as a "Last Resort" however, there are definitely better options to explore...

*This is NOT meant to be focused on security or UI/UX friendliness but rather FUNCTIONALITY*

## Features

- Create a Master Key upon signing in
- Store usernames and passwords for various accounts
- Hashes passwords and stores it in an SQL database
- Delete old usernames and passwords that are no longer needed
- Generate unique, complex, and random passwords

LastResort is a password management and vault application for a school project. The main focus was the functionality of storing passwords in a centralized application. This was done using Python3, Tkinter, SQLite3, and hashing. Successfully stores all information in a SQL database and saves all information entered for future use.

## Tools

LastResort uses a number of open source projects to work properly:

- [Python3] - Programming Language used to create the application!
- [Tkinter] - Python Interface for a simple GUI design
- [SQLite3] - SQL database engine used to store data
- [Hashlib] - Secure hashes and message digests

## Running the Program

Run the Python program and follow the simple prompts that follow.
> Make sure to remember the master key you created

Running through a CLI:
```sh
python3 LastReort.py
```

   [Python3]: https://www.python.org/
   [Tkinter]: https://docs.python.org/3/library/tkinter.html
   [SQLite3]: https://docs.python.org/3/library/sqlite3.html
   [Hashlib]: https://docs.python.org/3/library/hashlib.html

