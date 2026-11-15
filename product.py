"""
product.py
----------
Python equivalent of Product.java (the Remote Interface).

In Java RMI, `Product` is an interface that extends `java.rmi.Remote`.
It declares the methods a client is allowed to call on a remote object,
and every method can throw `RemoteException`.

Python has no `interface` keyword, so we use an Abstract Base Class (ABC).
Any class that implements Product (see ProductImpl in server.py) MUST
provide all three methods. In Pyro5, network errors are raised on the
client side as `Pyro5.errors.CommunicationError` (the RemoteException
equivalent).
"""

from abc import ABC, abstractmethod

# Shared network settings (same values used in the Java version:
# LocateRegistry.getRegistry("127.0.0.1", 9000))
HOST = "127.0.0.1"
REGISTRY_PORT = 9000


class Product(ABC):
    """Remote interface: defines product behaviour (methods)."""

    @abstractmethod
    def get_name(self) -> str:
        """Equivalent to: public String getName() throws RemoteException;"""

    @abstractmethod
    def get_description(self) -> str:
        """Equivalent to: public String getDescription() throws RemoteException;"""

    @abstractmethod
    def get_price(self) -> float:
        """Equivalent to: public double getPrice() throws RemoteException;"""
