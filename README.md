# cthulhu

A distributed system testing framework that is portable and easy to use.

> The cthulhu test framework is a distributed testing framework that should be
> used for correctness testing, not performance testsing, as the underlying bin
> packing, deployment, and monitoring system offered by this framework uses
> Docker under the hood.

Nearly all distributed system testing frameworks do *too much* and don't expose
the hooks you need to test your distributed system. Often, the testing
framework itself requires that you write in a particular language, using a
particular sytax, using a custom framework. What's more, if you're application
isn't written in a way that lends itself to inspection, you're mostly out of
luck.

The cthulhu distributed system testing frameworks seeks to keep it simple by
exposing your distributed system as a filesystem.

## getting started

To create a cthulhu test fixture, build the Python project and run the main
command.

```
cthulhu -h
```

You'll see that the framework creates a fixture on disk for you that you can
leverage in your correctness tests using a system such as bats.

```
cthulhu-fixture/
├── 172.17.0.2
│   ├── bindmounts
│   │   ├── etc
│   │   │   └── config.json
│   │   └── var
│   │       └── i001.log
│   ├── control
│   └── pid.txt
├── 172.17.0.3
│   ├── bindmounts
│   │   ├── etc
│   │   │   └── config.json
│   │   └── var
│   │       └── i002.log
│   ├── control
│   └── pid.txt
├── 172.17.0.4
│   ├── bindmounts
│   │   ├── etc
│   │   │   └── config.json
│   │   └── var
│   │       └── i003.log
│   ├── control
│   └── pid.txt
├── control
├── i001 -> /home/ubuntu/workspace/gallocy/cthulhu-fixture/172.17.0.2
├── i002 -> /home/ubuntu/workspace/gallocy/cthulhu-fixture/172.17.0.3
└── i003 -> /home/ubuntu/workspace/gallocy/cthulhu-fixture/172.17.0.4
```

## about

I started cthulhu to test [https://github.com/sholsapp/gallocy](gallocy), a
distributed shared memory system. Other distributed system testing frameworks
suffered from the problems I mentioned above, so I caved in and wrote my own.

I know the documentation sucks. If you're interested in learning more about
this tool, please open an issue so I know you're curious, and I'll happily
update the document further.
