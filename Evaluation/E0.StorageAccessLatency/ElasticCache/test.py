import time

import requests
import json

url = ""
sizes = ["1KB", "4KB", "1MB", "10MB", "100MB"]
stats = {
    "get": {
        "1KB": [],
        "4KB": [],
        "1MB": [],
        "10MB": [],
        "100MB": []
    },
    "set": {
        "1KB": [],
        "4KB": [],
        "1MB": [],
        "10MB": [],
        "100MB": []
    }
}
num_requests = 1

headers = {
    "Content-Type": "application/json",
}


def main():
    for size in sizes:
        for _ in range(num_requests):
            for op in ["set", "get"]:
                data = {"size": size, "op": op}
                response = requests.post(url, json=data, headers=headers)
                response_data = json.loads(response.text)

                stats[op][size].append(response_data[op])
                print("{} {} data used: {:.3f} ms".format(op, size, response_data[op]))
                time.sleep(1)

    filename = f"results/summary"
    with open(filename, "w") as f:
        for get_1KB, get_4KB, get_1MB, get_10MB, get_100MB, set_1KB, set_4KB, set_1MB, set_10MB, set_100MB in zip(
                stats["get"]["1KB"], stats["get"]["4KB"], stats["get"]["1MB"], stats["get"]["10MB"],
                stats["get"]["100MB"],
                stats["set"]["1KB"], stats["set"]["4KB"], stats["set"]["1MB"], stats["set"]["10MB"],
                stats["set"]["100MB"]):
            f.write("{},{},{},{},{}, , ,{},{},{},{},{}\n".format(get_1KB, get_4KB, get_1MB, get_10MB, get_100MB,
                                                                 set_1KB, set_4KB, set_1MB, set_10MB, set_100MB))


if __name__ == '__main__':
    main()
