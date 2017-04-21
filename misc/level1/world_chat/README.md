# WorldChat

```
We think someone is trying to transmit a flag over WorldChat. Unfortunately, there are so many other people talking that we can't really keep track of what is going on! Go see if you can find the messenger at shell2017.picoctf.com:61161. Remember to use Ctrl-C to cut the connection if it overwhelms you!
HINTS
There are cool command line tools that can filter out lines with specific keywords in them. Check out 'grep'! You can use the '|' character to put all the output into another process or command (like the grep process)
```

For this problem our initial approach was connect to the application but pipe the output to a grep command searching simply for the string "flag". There is excess noise still involving that word, so we added additional components to the filter string based on useful output we observed.

Here is the search for 'flag.'

```
$ nc shell2017.picoctf.com 61161 | grep flag
02:54:52 whatisflag: I has attacked my toes to drink your milkshake
02:54:52 noihazflag: A silly panda is our best chance to make a rasberry pie
02:54:52 noihazflag: A silly panda wants to steal my sloth to help me spell 'raspberry' correctly
02:54:53 noihazflag: my homegirlz need to meet up for the future of humanity
02:54:54 personwithflag: My sworn enemy will never understand me for the future of humanity
02:54:54 flagperson: this is part 1/8 of the flag - 1a2e
02:54:54 noihazflag: Cats with hats have demanded my presence to generate fusion power
02:54:54 ihazflag: that girl from that movie gives me hope to generate fusion power
02:54:55 noihazflag: my homegirlz will never be able to generate fusion power
02:54:55 personwithflag: We need to meet up to create a self driving car
^C
$ 
```

Clearly the useful flag fragments contain flag - in addition to just flag so we'll search for that instead. We could have been more elegant and used regex to get the parts of the flag out in order, but we just manually concatenated them. Here is the results of the new search and the concatenated flag below.

```
$ nc shell2017.picoctf.com 61161 | grep 'flag -'
02:55:59 flagperson: this is part 1/8 of the flag - 1a2e
02:56:01 flagperson: this is part 2/8 of the flag - 3d0a
02:56:07 flagperson: this is part 3/8 of the flag - 6310
02:56:09 flagperson: this is part 4/8 of the flag - 682c
02:56:10 flagperson: this is part 5/8 of the flag - 6be0
02:56:15 flagperson: this is part 6/8 of the flag - e319
02:56:21 flagperson: this is part 7/8 of the flag - d1b5
02:56:23 flagperson: this is part 8/8 of the flag - 2f53
^C
$ 
```

```
flag: 1a2e3d0a6310682c6ve0e319d1b52f53 
```