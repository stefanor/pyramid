from pyramid.httpexceptions import HTTPBadRequest, HTTPForbidden, HTTPNotFound

NotFound = HTTPNotFound  # bw compat
Forbidden = HTTPForbidden  # bw compat


class BadCSRFOrigin(HTTPBadRequest):
    """
    This exception indicates the request has failed cross-site request forgery
    origin validation.
    """

    title = "Bad CSRF Origin"
    explanation = (
        "Access is denied. This server can not verify that the origin or "
        "referrer of your request matches the current site. Either your "
        "browser supplied the wrong Origin or Referrer or it did not supply "
        "one at all."
    )


class BadCSRFToken(HTTPBadRequest):
    """
    This exception indicates the request has failed cross-site request
    forgery token validation.
    """

    title = 'Bad CSRF Token'
    explanation = (
        'Access is denied.  This server can not verify that your cross-site '
        'request forgery token belongs to your login session.  Either you '
        'supplied the wrong cross-site request forgery token or your session '
        'no longer exists.  This may be due to session timeout or because '
        'browser is not supplying the credentials required, as can happen '
        'when the browser has cookies turned off.'
    )


class PredicateMismatch(HTTPNotFound):
    """
    This exception is raised by multiviews when no view matches
    all given predicates.

    This exception subclasses the :class:`HTTPNotFound` exception for a
    specific reason: if it reaches the main exception handler, it should
    be treated as :class:`HTTPNotFound`` by any exception view
    registrations. Thus, typically, this exception will not be seen
    publicly.

    However, this exception will be raised if the predicates of all
    views configured to handle another exception context cannot be
    successfully matched.  For instance, if a view is configured to
    handle a context of ``HTTPForbidden`` and the configured with
    additional predicates, then :class:`PredicateMismatch` will be
    raised if:

    * An original view callable has raised :class:`HTTPForbidden` (thus
      invoking an exception view); and
    * The given request fails to match all predicates for said
      exception view associated with :class:`HTTPForbidden`.

    The same applies to any type of exception being handled by an
    exception view.
    """


class URLDecodeError(UnicodeDecodeError):
    """
    This exception is raised when :app:`Pyramid` cannot
    successfully decode a URL or a URL path segment.  This exception
    behaves just like the Python builtin
    :exc:`UnicodeDecodeError`. It is a subclass of the builtin
    :exc:`UnicodeDecodeError` exception only for identity purposes,
    mostly so an exception view can be registered when a URL cannot be
    decoded.
    """


class ConfigurationError(Exception):
    """Raised when inappropriate input values are supplied to an API
    method of a :term:`Configurator`"""


class ConfigurationConflictError(ConfigurationError):
    """Raised when a configuration conflict is detected during action
    processing"""

    def __init__(self, conflicts):
        self._conflicts = conflicts

    def __str__(self):
        r = ["Conflicting configuration actions"]
        for discriminator, infos in self._conflicts.items():
            r.append(f"  For: {discriminator}")
            for info in infos:
                for line in str(info).rstrip().split('\n'):
                    r.append("    " + line)

        return '\n'.join(r)


class ConfigurationExecutionError(ConfigurationError):
    """An error occurred during execution of a configuration action"""

    def __init__(self, etype, evalue, info):
        self.etype, self.evalue, self.info = etype, evalue, info

    def __str__(self):
        return f"{self.etype}: {self.evalue}\n  in:\n  {self.info}"


class CyclicDependencyError(Exception):
    """The exception raised when the Pyramid topological sorter detects a
    cyclic dependency."""

    def __init__(self, cycles):
        self.cycles = cycles

    def __str__(self):
        L = []
        cycles = self.cycles
        for cycle in cycles:
            dependent = cycle
            dependees = cycles[cycle]
            L.append(f'{dependent!r} sorts before {dependees!r}')
        msg = 'Implicit ordering cycle:' + '; '.join(L)
        return msg
