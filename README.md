graphite-stomp-tools
====================

(This was sat in a branch of https://github.com/bodgit/graphite-amqp-tools however as I'm using this in production it made sense to break it out as its own separate project.)

Basically gluing libevent2, https://github.com/bodgit/libevent-stomp and https://github.com/bodgit/libevent-graphite together to make the following daemons that should be reasonably efficient and have low memory usage:

* graphite-enqueue - provides the graphite TCP line receiver protocol and forwards all received messages on to a given STOMP destination.

* graphite-dequeue - does the opposite, receives messages from a given STOMP source and posts them on to a given graphite TCP line receiver.

* graphite-rewrite - reads from a STOMP source, applies PCRE rewrite rules to the metric names and sends back to a given STOMP destination. Useful for removing the need to use carbon-aggregator if all you need to do is rewrite metrics, such as those fed from collectd.

All daemons can use SSL to connect to the STOMP server and also periodically send their own various statistics to a given graphite TCP destination.
