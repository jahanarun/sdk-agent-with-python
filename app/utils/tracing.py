from opentelemetry import trace
from functools import wraps

# Initialize the tracer
tracer = trace.get_tracer(__name__)

def trace_with_span(span_name: str = None):
    """Decorator to trace a function with a custom span name."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_span_name = span_name if span_name else func.__name__
            with tracer.start_as_current_span(current_span_name) as span:
                # Optionally, add attributes to the span
                span.set_attribute("function.name", func.__name__)
                return await func(*args, **kwargs)
        return wrapper
    return decorator
