
import time
import statistics
import httpx

BASE_URL = "http://127.0.0.1:8000"
TOTAL_REQUESTS = 20

latencies = []
successful_requests = 0
failed_requests = 0

print("Starting CampusAssist AI performance test...\n")

with httpx.Client(timeout=10) as client:

    for i in range(TOTAL_REQUESTS):
        start_time = time.perf_counter()

        try:
            response = client.get(f"{BASE_URL}/health")

            elapsed = (time.perf_counter() - start_time) * 1000
            latencies.append(elapsed)

            if response.status_code == 200:
                successful_requests += 1
            else:
                failed_requests += 1

            print(
                f"Request {i + 1}: "
                f"Status {response.status_code} | "
                f"{elapsed:.2f} ms"
            )

        except httpx.RequestError as error:
            failed_requests += 1
            print(f"Request {i + 1}: Failed - {error}")


average_latency = (
    statistics.mean(latencies) if latencies else 0
)

maximum_latency = max(latencies) if latencies else 0

success_rate = (successful_requests / TOTAL_REQUESTS) * 100
error_rate = (failed_requests / TOTAL_REQUESTS) * 100

print("\n========== PERFORMANCE REPORT ==========")
print("Total Requests:", TOTAL_REQUESTS)
print("Successful Requests:", successful_requests)
print("Failed Requests:", failed_requests)
print(f"Success Rate: {success_rate:.2f}%")
print(f"Error Rate: {error_rate:.2f}%")
print(f"Average Response Time: {average_latency:.2f} ms")
print(f"Maximum Response Time: {maximum_latency:.2f} ms")
print("========================================")
