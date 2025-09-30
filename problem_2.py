import random
import math

def exponential(mean):
    """Generate exponential random variable with given mean."""
    u = random.random()
    return -mean * math.log(1 - u)

def simulate_servers(years=20, mtbf=500, restore_time=10):
    """
    Part (a): simulate 20 years of operation for two mirrored servers.
    Records all failure and restoration intervals for each server.
    """
    horizon = years * 365 * 24  # total hours
    events = {"server1": [], "server2": []}

    # Next scheduled failure times for each server
    t1 = exponential(mtbf)
    t2 = exponential(mtbf)
    current_time = 0

    while current_time < horizon:
        if t1 < t2:
            fail_time = t1
            restore_end = fail_time + restore_time
            if fail_time < horizon:
                events["server1"].append((round(fail_time, 2), round(restore_end, 2)))
            # move server1’s next failure past restoration
            current_time = restore_end
            t1 = current_time + exponential(mtbf)
        else:
            fail_time = t2
            restore_end = fail_time + restore_time
            if fail_time < horizon:
                events["server2"].append((round(fail_time, 2), round(restore_end, 2)))
            current_time = restore_end
            t2 = current_time + exponential(mtbf)

    return events

def simulate_system_lifetime(mtbf=500, restore_time=10):
    t1 = exponential(mtbf)
    t2 = exponential(mtbf)
    current_time = 0
    while True:
        if t1 < t2:
            fail_time = t1
            if t2 <= fail_time + restore_time:
                return t2
            else:
                current_time = fail_time + restore_time
                t1 = current_time + exponential(mtbf)
        else:
            fail_time = t2
            if t1 <= fail_time + restore_time:
                return t1
            else:
                current_time = fail_time + restore_time
                t2 = current_time + exponential(mtbf)


def system_failure_times(trials=50, mtbf=500,restore_time=10):
    results = []
    for _ in range(trials):
        lifetime = simulate_system_lifetime(mtbf, restore_time)
        results.append(lifetime)
    #return sum(fail_times)/len(fail_times)
    return sum(results)/len(results)


if __name__ == "__main__":
    random.seed(42)

    events = simulate_servers()
    print("Server1 failures:", events["server1"][:5], "...")
    print("Server2 failures:", events["server2"][:5], "...")

    avg_failure_time = system_failure_times()
    print("\nExpected system failure time:", round(avg_failure_time, 2), "hours")
    print("In years:", round(avg_failure_time/(24*365), 2), "years")
    