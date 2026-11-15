"""
server.py
---------
Python equivalent of ProductImpl.java, Server.java and ServerImpl.java.

Java RMI  ->  Pyro5 mapping
  rmiregistry 9000                      ->  Pyro5 Name Server on 127.0.0.1:9000
  ProductImpl implements Product        ->  class ProductImpl(Product) + @expose
  UnicastRemoteObject.exportObject(p,0) ->  daemon.register(p)
  registry.bind("laptop", stub)         ->  ns.register("laptop", uri)

(ServerImpl.java in the original repository is empty, so there is
nothing extra to translate for it.)
"""

import threading
import time

import Pyro5.api
import Pyro5.errors
import Pyro5.nameserver

from product import HOST, REGISTRY_PORT, Product


# ---------------------------------------------------------------------------
# ProductImpl.java
# ---------------------------------------------------------------------------
@Pyro5.api.expose          # makes the methods callable from remote clients
class ProductImpl(Product):
    """Implements all the methods defined in the Product interface."""

    # Parametrized constructor.
    def __init__(self, new_name: str, new_description: str, new_price: float):
        self.name = new_name
        self.description = new_description
        self.price = new_price

    def get_name(self) -> str:
        print(f"[server] get_name() called on '{self.name}'")
        return self.name

    def get_description(self) -> str:
        print(f"[server] get_description() called on '{self.name}'")
        return self.description

    def get_price(self) -> float:
        print(f"[server] get_price() called on '{self.name}'")
        return self.price


# ---------------------------------------------------------------------------
# Registry (equivalent of running `rmiregistry 9000` in Java)
# ---------------------------------------------------------------------------
def get_registry():
    """Locate the name server on 127.0.0.1:9000, starting one if needed."""
    try:
        return Pyro5.api.locate_ns(host=HOST, port=REGISTRY_PORT)
    except Pyro5.errors.NamingError:
        print(f"No registry found - starting Pyro5 Name Server on {HOST}:{REGISTRY_PORT} ...")
        threading.Thread(
            target=Pyro5.nameserver.start_ns_loop,
            kwargs={"host": HOST, "port": REGISTRY_PORT, "enableBroadcast": False},
            daemon=True,
        ).start()
        for _ in range(50):                      # wait up to ~5 s
            try:
                return Pyro5.api.locate_ns(host=HOST, port=REGISTRY_PORT)
            except Pyro5.errors.NamingError:
                time.sleep(0.1)
        raise


# ---------------------------------------------------------------------------
# Server.java
# ---------------------------------------------------------------------------
def main():
    try:
        print("Server is booting....")

        # We create objects from ProductImpl class and share them.
        p1 = ProductImpl("Laptop", "Lenovo laptop", 800000.0)
        p2 = ProductImpl("Mobile", "MI 9 mobile", 24000.0)
        p3 = ProductImpl("Bag", "Branded bag", 800.0)
        p4 = ProductImpl("Charger", "MI Charger", 230.0)

        # Export all p1, p2, p3 and p4 objects (equivalent of
        # UnicastRemoteObject.exportObject). The daemon listens on a
        # random free port, just like exportObject(obj, 0).
        daemon = Pyro5.api.Daemon(host=HOST)
        uri1 = daemon.register(p1)
        uri2 = daemon.register(p2)
        uri3 = daemon.register(p3)
        uri4 = daemon.register(p4)

        # Get the registry.
        registry = get_registry()

        # Bind the exported objects in the registry so that clients can
        # look them up and call the object methods.
        # (Java's bind() fails if the name exists; we use safe=False so the
        #  server can be restarted without restarting the registry.)
        registry.register("laptop", uri1, safe=False)
        registry.register("ram", uri2, safe=False)
        registry.register("bag", uri3, safe=False)
        registry.register("charger", uri4, safe=False)

        print(f"Registry running at {HOST}:{REGISTRY_PORT}")
        for name, uri in registry.list().items():
            if name != "Pyro.NameServer":
                print(f"  bound '{name}' -> {uri}")
        print("Server is ready. Waiting for client requests... (Ctrl+C to stop)")

        daemon.requestLoop()

    except KeyboardInterrupt:
        print("\nServer shutting down.")
    except Exception as e:
        print("Server error", e)


if __name__ == "__main__":
    main()
