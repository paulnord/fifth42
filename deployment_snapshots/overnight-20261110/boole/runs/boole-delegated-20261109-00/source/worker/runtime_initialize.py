"""New-process initializer for the selected exact host optimizations."""
import speed_options


def initialize(source,cpus=()):
    speed_options.initialize(source,cpus)
