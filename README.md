# Encrypted-Password-Manager
Simple project for a SHA512 Encrypted password manager

Requirements:

    MySql
    pickel
    cryptograpyhy
    base64
    mysqlconnecter-python
    functools
    customtkinter

## Breif Explanation
This code creates a databse for each new user in mysql with the password given the first time a user enters their usename, after that the user can add/delete records of their passwords, these passwords are highly secure behind a SHA-512 encryption algorithm with an addition of a 16bit randomly generaed salt, the username and password both are encrypted before storing
