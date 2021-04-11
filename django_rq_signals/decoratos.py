import django_rq


def django_rq_signal_receiver(signal, **kwargs):
    """
    A decorator for connecting receivers(which are run in django_rq worker to signals.
    Used by passing in the signal (or list of signals) and keyword arguments to connect::

        @django_rq_receiver(post_save, sender=MyModel)
        def signal_receiver(sender, **kwargs):
            ...

        @django_rq_receiver([post_save, post_delete], sender=MyModel)
        def signals_receiver(sender, **kwargs):
            ...
    """
    def _decorator(func):
        func = django_rq.job(func)

        def enqueue(*args, **kargs):
            django_rq.enqueue(func, *args, **kargs)

        if isinstance(signal, (list, tuple)):
            for s in signal:
                s.connect(enqueue, **kwargs)
        else:
            signal.connect(enqueue, **kwargs)
        return func
    return _decorator
