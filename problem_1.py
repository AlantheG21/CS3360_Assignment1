import random
import math

def exponential(mean):
    """Generate an exponentially distributed random variable."""
    return -mean * math.log(1 - random.random())

def generate_processes(num_processes=1000, arrival_rates=2, service_mean=1):
    processes = []
    arrival_time = 0.0
    for pid in range(1, num_processes + 1):
        inter_arrival = exponential(1 / arrival_rates)
        arrival_time += inter_arrival
        service_time = exponential(service_mean)
        processes.append((pid, round(arrival_time,4), round(service_time,4)))
    return processes

if __name__ == "__main__":
    processes = generate_processes()
    for process in processes:
        print(process)

    total_time = processes[-1][1] + processes[-1][2]
    avg_arrival_rate = len(processes) / total_time
    avg_service_time = sum(p[2] for p in processes) / len(processes)

    print("\nActual average arrival rate:", round(avg_arrival_rate, 4))
    print("Actual average service time:", round(avg_service_time, 4))