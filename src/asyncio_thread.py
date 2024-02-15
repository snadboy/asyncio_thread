from concurrent.futures import ThreadPoolExecutor
import math
import threading
from time import perf_counter
from typing import Dict, Tuple
import requests
from requests import Response

import asyncio
from asyncio import Task

# Maximum number of threads to use
MAX_THREADS = 25

# Function to truncate a float to two decimal places
twod = lambda x: math.trunc(x * 100) / 100


# Function to make a GET request to a URL in a separate thread
# Returns a dictionary with the status code, URL, thread ID, and request duration
def request_thread(url) -> Dict[str, any]:
    start = perf_counter()
    response = requests.get(url, timeout=5), threading.get_ident()
    request_duration = twod(perf_counter() - start)
    return {
        "status": response[0].status_code,
        "url": url,
        "thread": response[1],
        "request_duration": request_duration,
    }


# Coroutine to fetch a URL
# Uses asyncio.to_thread to run request_thread in a separate thread
# Returns a dictionary with the status code, URL, thread ID, request duration, wait duration, and total duration
async def fetch(url: str) -> Response:
    start = perf_counter()
    try:
        response_dict = await asyncio.to_thread(request_thread, url)
    except Exception as e:
        raise

    fetch_duration = twod(perf_counter() - start)
    return {
        "status": response_dict["status"],
        "url": response_dict["url"],
        "thread": response_dict["thread"],
        "wait_duration": twod(fetch_duration - response_dict["request_duration"]),
        "request_duration": response_dict["request_duration"],
        "total_duration": twod(
            response_dict["request_duration"]
            + (fetch_duration - response_dict["request_duration"])
        ),
    }


# Main coroutine
async def main():
    start = perf_counter()

    # Create a ThreadPoolExecutor and set it as the default executor for the event loop
    executor = ThreadPoolExecutor(max_workers=MAX_THREADS)
    loop = asyncio.get_running_loop()
    loop.set_default_executor(executor)

    # List of URLs to fetch
    urls = [
        "tiktok.com",
        "instagram.com",
        "google.com",
        "apple.com",
        "facebook.com",
        "twitter.com",
        "cloudflare.com",
        "github.com",
        "youtube.com",
        "plex.tv",
        "yahoo.com",
        "amazon.com",
        "microsoft.com",
        "reddit.com",
        "nytimes.com",
        "visualstudio.com",
        "stackoverflow.com",
        "wikipedia.org",
        "wikimedia.org",
        "chase.com",
        "capitalone.com",
        "usaa.com",
        "navyfederal.org",
        "fidelity.com",
        "spotify.com",
        "pandora.com",
    ]

    # Create a task for each URL to fetch
    pending = set([asyncio.create_task(fetch(f"https://{url}")) for url in urls])

    ndx = 0
    total_wait_duration = 0
    total_request_duration = 0
    while True:
        # Wait for the tasks to complete, returning when the first task raises an exception or after 1 second
        results, pending = await asyncio.wait(
            pending, return_when=asyncio.FIRST_EXCEPTION, timeout=1.0
        )

        # Process the completed tasks
        for task in results:
            ndx += 1

            # If the task raised an exception, print the exception
            if task.exception():
                print(f"[{ndx}/{len(urls)}] {task.exception()}")
            else:
                # Otherwise, print the result
                print(f"[{ndx}/{len(urls)}] {task.result()}")
                total_wait_duration += task.result()["wait_duration"]
                total_request_duration += task.result()["request_duration"]

        # If there are no more pending tasks, break the loop
        if not pending:
            break

    # Print the total duration
    print("Exiting...")
    print(f"  Total Execution: {perf_counter() - start:.2f} seconds")
    print(f"  Total Wait: {total_wait_duration:.2f} seconds")
    print(f"  Total Request: {total_request_duration:.2f} seconds")
    print(
        f"  Average Request (# thread = {MAX_THREADS}): {(perf_counter() - start) / len(urls):.2f} seconds per request"
    )


# If this script is run directly, run the main coroutine
if __name__ == "__main__":
    asyncio.run(main())
