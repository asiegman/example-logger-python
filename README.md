# example-logger-python

I needed an image I could use to output log messages and test loosely structured logging formats.

So this does that, utilizing `pythonjsonlogger`

It also serves as an example of how to use `pythonjsonlogger` to have stdout messages appear in standardized JSON
so you can easily pick them up and parse via `fluentd` or `logstash` or some other log aggregator.
