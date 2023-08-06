# -*- coding: utf-8 -*-
# Copyright (c) 2016 - 2020 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
try:
    from ddtrace import constants, tracer
except ImportError:

    def retain_datadog_trace():
        # Do nothing as ddtrace is not available.
        return None, None
else:

    def retain_datadog_trace():
        span = tracer.current_span()
        if span is not None:
            span.set_tag(constants.MANUAL_KEEP_KEY)
            span.set_tag("sqreen.event", "true")
            return span.trace_id, span.span_id
        return None, None
