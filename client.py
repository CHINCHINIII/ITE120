"""
client.py
---------
Python equivalent of Client.java.

Java RMI  ->  Pyro5 mapping
  LocateRegistry.getRegistry("127.0.0.1", 9000)  ->  Pyro5.api.locate_ns(HOST, 9000)
  (Product) registry.lookup("laptop")            ->  Pyro5.api.Proxy("PYRONAME:laptop@...")

Usage:
  python client.py            # looks up "laptop" (same as the Java client)
  python client.py bag        # looks up any other bound name: laptop, ram, bag, charger
"""

import sys

import Pyro5.api

from product import HOST, REGISTRY_PORT


def main():
    object_name = sys.argv[1] if len(sys.argv) > 1 else "laptop"
    try:
        # Get the registry.
        registry = Pyro5.api.locate_ns(host=HOST, port=REGISTRY_PORT)

        # Look up the remote object and assign it to a proxy (the "stub").
        uri = registry.lookup(object_name)
        with Pyro5.api.Proxy(uri) as laptop:
            laptop_name = laptop.get_name()
            laptop_description = laptop.get_description()
            price = laptop.get_price()

        print("Name:" + laptop_name)
        print("Description: " + laptop_description)
        print("Price: " + str(price))

    except Exception as e:
        print("Exception in client side", e)


if __name__ == "__main__":
    main()
