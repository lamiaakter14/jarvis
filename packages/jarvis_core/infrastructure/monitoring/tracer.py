"""Tracer for request tracing and context tracking."""

import uuid
from contextvars import ContextVar
from datetime import datetime
from typing import Any, Dict, Optional

# Context variable for storing trace context
_trace_context: ContextVar[Optional[Dict[str, Any]]] = ContextVar("trace_context", default=None)


class Tracer:
    """Request tracer for tracking execution context.

    Provides distributed tracing capabilities to track requests
    across different components and layers of the application.
    """

    def __init__(self, enabled: bool = True):
        """Initialize tracer.

        Args:
            enabled: Whether tracing is enabled
        """
        self.enabled = enabled

    def start_trace(
        self,
        operation_name: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Start a new trace.

        Args:
            operation_name: Name of the operation being traced
            metadata: Optional metadata for the trace

        Returns:
            Trace ID
        """
        if not self.enabled:
            return ""

        trace_id = str(uuid.uuid4())

        trace_context = {
            "trace_id": trace_id,
            "operation_name": operation_name,
            "start_time": datetime.now().isoformat(),
            "metadata": metadata or {},
            "spans": [],
        }

        _trace_context.set(trace_context)
        return trace_id

    def start_span(
        self,
        span_name: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Start a new span within the current trace.

        Args:
            span_name: Name of the span
            metadata: Optional metadata for the span

        Returns:
            Span ID
        """
        if not self.enabled:
            return ""

        trace_context = _trace_context.get()
        if not trace_context:
            # No active trace, start one
            return self.start_trace(span_name, metadata)

        span_id = str(uuid.uuid4())

        span = {
            "span_id": span_id,
            "span_name": span_name,
            "start_time": datetime.now().isoformat(),
            "metadata": metadata or {},
            "end_time": None,
            "duration": None,
            "status": "in_progress",
        }

        trace_context["spans"].append(span)
        return span_id

    def end_span(
        self,
        span_id: str,
        status: str = "success",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """End a span.

        Args:
            span_id: ID of the span to end
            status: Final status of the span
            metadata: Optional additional metadata
        """
        if not self.enabled:
            return

        trace_context = _trace_context.get()
        if not trace_context:
            return

        # Find and update the span
        for span in trace_context["spans"]:
            if span["span_id"] == span_id:
                end_time = datetime.now()
                span["end_time"] = end_time.isoformat()
                span["status"] = status

                # Calculate duration
                start_time = datetime.fromisoformat(span["start_time"])
                span["duration"] = (end_time - start_time).total_seconds()

                # Merge additional metadata
                if metadata:
                    span["metadata"].update(metadata)

                break

    def end_trace(
        self,
        status: str = "success",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Optional[Dict[str, Any]]:
        """End the current trace.

        Args:
            status: Final status of the trace
            metadata: Optional additional metadata

        Returns:
            Trace context if tracing is enabled
        """
        if not self.enabled:
            return None

        trace_context = _trace_context.get()
        if not trace_context:
            return None

        end_time = datetime.now()
        trace_context["end_time"] = end_time.isoformat()
        trace_context["status"] = status

        # Calculate duration
        start_time = datetime.fromisoformat(trace_context["start_time"])
        trace_context["duration"] = (end_time - start_time).total_seconds()

        # Merge additional metadata
        if metadata:
            trace_context["metadata"].update(metadata)

        # Clear context
        _trace_context.set(None)

        return trace_context

    def get_current_trace_id(self) -> Optional[str]:
        """Get the current trace ID.

        Returns:
            Current trace ID or None
        """
        if not self.enabled:
            return None

        trace_context = _trace_context.get()
        return trace_context["trace_id"] if trace_context else None

    def get_current_trace_context(self) -> Optional[Dict[str, Any]]:
        """Get the current trace context.

        Returns:
            Current trace context or None
        """
        if not self.enabled:
            return None

        return _trace_context.get()

    def add_metadata(self, key: str, value: Any) -> None:
        """Add metadata to the current trace.

        Args:
            key: Metadata key
            value: Metadata value
        """
        if not self.enabled:
            return

        trace_context = _trace_context.get()
        if trace_context:
            trace_context["metadata"][key] = value

    def add_tag(self, tag: str) -> None:
        """Add a tag to the current trace.

        Args:
            tag: Tag to add
        """
        if not self.enabled:
            return

        trace_context = _trace_context.get()
        if trace_context:
            if "tags" not in trace_context["metadata"]:
                trace_context["metadata"]["tags"] = []
            trace_context["metadata"]["tags"].append(tag)

    def record_error(self, error: Exception) -> None:
        """Record an error in the current trace.

        Args:
            error: Exception that occurred
        """
        if not self.enabled:
            return

        trace_context = _trace_context.get()
        if trace_context:
            if "errors" not in trace_context["metadata"]:
                trace_context["metadata"]["errors"] = []

            trace_context["metadata"]["errors"].append(
                {
                    "type": type(error).__name__,
                    "message": str(error),
                    "timestamp": datetime.now().isoformat(),
                }
            )

    def create_child_context(self) -> Dict[str, Any]:
        """Create a child trace context for propagation.

        Returns:
            Dictionary with trace context for propagation
        """
        if not self.enabled:
            return {}

        trace_context = _trace_context.get()
        if not trace_context:
            return {}

        return {
            "trace_id": trace_context["trace_id"],
            "parent_operation": trace_context["operation_name"],
        }

    def inject_context(self, headers: Dict[str, str]) -> Dict[str, str]:
        """Inject trace context into headers for propagation.

        Args:
            headers: Headers dictionary to inject context into

        Returns:
            Headers with trace context
        """
        if not self.enabled:
            return headers

        trace_id = self.get_current_trace_id()
        if trace_id:
            headers["X-Trace-ID"] = trace_id

        return headers

    def extract_context(self, headers: Dict[str, str]) -> Optional[str]:
        """Extract trace context from headers.

        Args:
            headers: Headers dictionary to extract context from

        Returns:
            Trace ID if present
        """
        if not self.enabled:
            return None

        return headers.get("X-Trace-ID")
