# ADR-003 - Extractor Error Handling: Timeout and Retry with Fixed Delay

## Status

Accepted

---

## Context

`extract_weather` had no error handling and no timeout. A hanging API
response would block the pipeline indefinitely, and any network failure
crashed with an unhandled exception. Because the function returned no
value on failure in the old implementation, the resulting error surfaced
downstream in `transformer.py` as a confusing `TypeError` instead of a
clear network-related message.

---

## Decision

Add an explicit request timeout (10s) and a simple retry loop (5 attempts,
3s fixed delay) directly in `extractor.py`, using `requests.exceptions.RequestException`
and `response.raise_for_status()`. If the error is caused by timeout or a HTTP error 5xx, the application tries to get the data again. If the timeout or if the 5xx errors persist after all attempts, an exception is raised to alert that the API did not return any data. If the error is in a HTTP error 4xx, the application raises an exception and shows the status HTTP that was returned. All events are registered in the log.

---

## Consequences

### Advantages

- Bounded wait time; the pipeline can no longer hang forever on a slow API
- The issues throughout the attempts of data extraction are registered in the logs, and when a failure happens,
  an exception is raised.

### Disadvantages

- Fixed delay between retries is not adaptive; a library such as `tenacity`
  would allow exponential backoff and jitter with less hand-written code —
  worth revisiting if retry needs grow more sophisticated later