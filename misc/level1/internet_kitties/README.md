# Internet Kitties

```
I was told there was something at IP shell2017.picoctf.com with port 12275. How do I get there? Do I need a ship for the port?
HINTS
Look at using the netcat (nc) command!
To figure out how to use it, you can run "man nc" or "nc -h" on the shell, or search for it on the interwebz
```

This problem requires only the use of the netcat command to connect to a network application running on the specified port. We connect and get a flag as shown below.

```
$ nc shell2017.picoctf.com 12275   
Yay! You made it!                                          
Take a flag!                                               
1e1ccf22b278d35b1977c76bb66c5e30                           
$
```
