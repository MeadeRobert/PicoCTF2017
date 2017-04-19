# Encrypted Shell

```
This service gives a shell, but it's password protected! We were able intercept this
 encrypted traffic which may contain a successful password authentication. Can you
 get shell access and read the contents of flag.txt?
The service is running at shell2017.picoctf.com:30754.
HINTS
Are any of the parameters used in the key exchange weaker than they should be?
```

Looking at the [pcap file](https://www.cloudshark.org/captures/b5746ddb4a3b) for the network traffic, we notice a tcp stream. Looking inside of it revealed some interesting data sent between the client and server involving the letters ```p, g, A```. Additional analysis of the provided source code reveals some kind of public key exchange to securely start an AES 256 encrypted shell session. The file is called ```dhshell.py```. What could DH stand for? A quick google search for the letters and public key cryptography reveals an algorithm called a [Diffie Hellman Exchange](https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange), another public key encryption algorithm that, much like RSA, relies on the difficulty of the discrete log problem.

So doing some research on attacks on Diffie Hellman we found a log about precomputed tables to crack 1024 bit possibly being in the hands of the NSA, making the whole algorithm questionable and issues with certificate authority because each exchange involves a different random number selected for exponent ```a``` unlike RSA which uses the same public key everytime. We found that it is vulnerable only to brute force and a man in the middle attack unless there is an issue with the implementation. We searched for things that didn't seem quite right. We wondered why the prime ```p``` and base ```g``` were the same every time as they were loaded from a file, but this appeared to be a dead end. The other thing that stood out was the limit on the size of the value ```a```. Why did they choose ```2^46``` instead of ```2^64``` as the exclusive upper bound?

It turns out that for a value of this size we can do a meet in the middle attack, not to be confused with a man in the middle attack which involves impersonating the server for the client and the client for the server in order to control the public key exchange which must be done when both parties are trying to communicate, not after the communications have been completed. We will use a special ```sqrt(n)``` time and space complexity algorithm that offloads some of the computation via the use of a hashmap or, in our case, a python dictionary. The algorithm that we will be using to do this is called the [Baby-step Giant-step Algorithm](https://en.wikipedia.org/wiki/Baby-step_giant-step)

