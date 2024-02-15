# Python Script Description

This Python script uses the `asyncio` library along with a `ThreadPoolExecutor` to make HTTP GET requests to a list of URLs in parallel. The script is divided into several parts:

1. **Imports and Constants**: The script imports necessary modules and defines a constant `MAX_THREADS` which sets the maximum number of threads to use.

2. **Utility Function**: The `twod` function is a utility function that truncates a float to two decimal places.

3. **Request Thread Function**: The `request_thread` function makes a GET request to a given URL in a separate thread and returns a dictionary containing the status code, URL, thread ID, and request duration.

4. **Fetch Coroutine**: The `fetch` coroutine uses `asyncio.to_thread` to run the `request_thread` function in a separate thread. It returns a dictionary with additional information such as wait duration and total duration.

5. **Main Coroutine**: The `main` coroutine is where the script's main logic resides. It creates a `ThreadPoolExecutor` and sets it as the default executor for the event loop. It then creates a list of URLs to fetch and creates an asyncio task for each URL. The coroutine waits for the tasks to complete, processes the completed tasks, and prints out the total duration and other statistics.

6. **Script Execution**: If the script is run directly (not imported as a module), the `main` coroutine is run using `asyncio.run(main())`.

This script demonstrates how to use `asyncio` and `ThreadPoolExecutor` to perform IO-bound tasks (like making HTTP requests) in parallel, which can significantly improve performance when dealing with a large number of such tasks.