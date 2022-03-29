# Data2410-PortfolioAssignment

## Run
The server expects a portnumber and the client expects host, port and botname.
To run a "bot" as a user choose a botname that does not correspond to any bots
```bash
  python Server.py [Portnumber]
  python Client.py [IP/host] [Portnumber] [Botname]
```

Example:
````bash
  python Server.py 5000
  python Client.py localhost 5000 alice
  python Client.py localhost 5000 bob
  python Client.py localhost 5000 Kader
  python Client.py localhost 5000 dora
````
