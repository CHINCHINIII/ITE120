# PYTHON_RMI_LAB — Java RMI → Python Pyro5

This project translates the Java RMI project
[`nix1947/sunway_dpp/JAVA_RMI_IV`](https://github.com/nix1947/sunway_dpp/tree/master/JAVA_RMI_IV)
into a Python distributed system using **Pyro5** (Python Remote Objects).

## Project Structure

```
PYTHON_RMI_LAB/
├── product.py        # Equivalent to Product.java (Remote Interface)
├── server.py         # Equivalent to Server.java, ProductImpl.java and ServerImpl.java
├── client.py         # Equivalent to Client.java
├── requirements.txt
└── README.md
```

## Java RMI → Pyro5 Mapping

| Java RMI | Python / Pyro5 |
|---|---|
| `interface Product extends Remote` | `class Product(ABC)` with `@abstractmethod`s (`product.py`) |
| `class ProductImpl implements Product` | `@Pyro5.api.expose class ProductImpl(Product)` (`server.py`) |
| `rmiregistry 9000` | Pyro5 Name Server on `127.0.0.1:9000` (started automatically by `server.py`) |
| `UnicastRemoteObject.exportObject(obj, 0)` | `daemon.register(obj)` |
| `registry.bind("laptop", stub)` | `ns.register("laptop", uri)` |
| `LocateRegistry.getRegistry("127.0.0.1", 9000)` | `Pyro5.api.locate_ns(host="127.0.0.1", port=9000)` |
| `(Product) registry.lookup("laptop")` | `Pyro5.api.Proxy(ns.lookup("laptop"))` |
| `RemoteException` | `Pyro5.errors.CommunicationError` / `NamingError` |

> `ServerImpl.java` in the original repository is an empty file, so it has no extra logic to translate.

The server exposes four remote objects, the same as in the Java version:

| Bound name | Name | Description | Price |
|---|---|---|---|
| `laptop` | Laptop | Lenovo laptop | 800000.0 |
| `ram` | Mobile | MI 9 mobile | 24000.0 |
| `bag` | Bag | Branded bag | 800.0 |
| `charger` | Charger | MI Charger | 230.0 |

## Requirements

- Python 3.8+
- Pyro5

```bash
pip install -r requirements.txt
```

## How to Run

Open **two terminals** in the `PYTHON_RMI_LAB` folder.

**Terminal 1 — Server**

```bash
python server.py
```

Expected output:

```
Server is booting....
No registry found - starting Pyro5 Name Server on 127.0.0.1:9000 ...
NS running on 127.0.0.1:9000 (127.0.0.1)
Registry running at 127.0.0.1:9000
  bound 'laptop' -> PYRO:obj_...@127.0.0.1:xxxxx
  bound 'ram' -> PYRO:obj_...@127.0.0.1:xxxxx
  bound 'bag' -> PYRO:obj_...@127.0.0.1:xxxxx
  bound 'charger' -> PYRO:obj_...@127.0.0.1:xxxxx
Server is ready. Waiting for client requests... (Ctrl+C to stop)
```

**Terminal 2 — Client**

```bash
python client.py
```

Expected output:

```
Name:Laptop
Description: Lenovo laptop
Price: 800000.0
```

You can also look up the other remote objects:

```bash
python client.py ram
python client.py bag
python client.py charger
```

Each remote call is logged in the server terminal, for example
`[server] get_name() called on 'Laptop'`.

Press **Ctrl+C** in the server terminal to stop the server.

### Optional: run the registry separately (like `rmiregistry 9000`)

```bash
python -m Pyro5.nameserver -n 127.0.0.1 -p 9000
```

If a name server is already running on port 9000, `server.py` uses it instead of starting its own.
