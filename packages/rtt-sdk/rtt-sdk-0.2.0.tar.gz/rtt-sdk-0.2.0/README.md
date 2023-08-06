# RTT Platform Python SDK

This is the formally maintained Python SDK for interacting with a Red Team Toolkit (RTT) Platform C2 server.

**This project is currently in BETA status and subject to significant change until finalized**

This SDK is based on models generated from the OpenAPI specification for the latest platform server. It will
continue to be updated and expanded as more features are finalized in the platform server.

Additional information can be found [here](https://www.netspi.com/company/news/netspi-relaunches-red-team-toolkit/)

## Installation

```
> pip install rtt-sdk
```

## Examples

Collecting current session information

```python
import asyncio
import rtt_sdk

async def main():
    client = rtt_sdk.SlingshotClient()
    user = await client.context_user(True)
    process = await client.context_process()
    print(f"Running as {user.username} in {process.process_id}")

asyncio.run(main())
```

## Asyncronous Code

This SDK makes use of `asyncio` for executing tasks and returning results. Almost every function exposed
on API clients is an asyncronous co-routine and requires an event loop for execution. The easiest way
to accomplish this is to define a wrapper `async main()` function and use the new `asyncio.run()` function
to establish an event loop, and execute your code within (as seen in the examples section)

Some useful primitives that can be used as part of `async`:

```python
results = await foo()
await asyncio.waitfor(foo(), timeout=10)
await asyncio.gather([foo(), bar()])
```

More information can be found [here](https://docs.python.org/3/library/asyncio.html)

## Requirements

- Active RTT license and deployed RTT platform server
- Python 3.7+
