# Sphinx Documentation Notes

1. Add docstring after the parameter to add documentation as shown below or use the special formatting '#:' used below.
```
    flox = 1.5   #: Doc comment for Foo.flox. One line only.

    baz = 2
    """Docstring for class attribute Foo.baz."""
```

2. For classes and exceptions, members inherited from base classes will be left out when documenting all members, unless you give the inherited-members option, in addition to members:
```
    .. autoclass:: Noodle
        :members:
        :inherited-members:
```