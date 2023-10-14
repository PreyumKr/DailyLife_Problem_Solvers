import csv
from time import sleep
from faker import Faker
from multiprocessing import Process
from multiprocessing import cpu_count
from multiprocessing import Semaphore

# Generates a total of 14000000 rows with 400 columns of data in seperate 700 CSVs with 20000 rows each

fake = Faker()
rows = []

def thread(i, sema):
    if sema is not None:
          sema.acquire()
    print("Thread {} running".format(i));
    f = open('./testClean'+ str(i) +'.csv', 'w+')
    writer = csv.writer(f)
    for j in range(20000):
        row = [fake.name().split()[0], fake.name().split()[1], fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.name().split()[0], fake.name().split()[1], fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.name().split()[0], fake.name().split()[1], fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.name().split()[0], fake.name().split()[1], fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.name().split()[0], fake.name().split()[1], fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.name().split()[0], fake.name().split()[1], fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.name().split()[0], fake.name().split()[1], fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.name().split()[0], fake.name().split()[1], fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.name().split()[0], fake.name().split()[1], fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.name().split()[0], fake.name().split()[1], fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.name().split()[0], fake.name().split()[1], fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.name().split()[0], fake.name().split()[1], fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.name().split()[0], fake.name().split()[1], fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.name().split()[0], fake.name().split()[1], fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.name().split()[0], fake.name().split()[1], fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.name().split()[0], fake.name().split()[1], fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.name().split()[0], fake.name().split()[1], fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.name().split()[0], fake.name().split()[1], fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.name().split()[0], fake.name().split()[1], fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.name().split()[0], fake.name().split()[1], fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.name().split()[0], fake.name().split()[1], fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.name().split()[0], fake.name().split()[1], fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.name().split()[0], fake.name().split()[1], fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.name().split()[0], fake.name().split()[1], fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.name().split()[0], fake.name().split()[1], fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.name().split()[0], fake.name().split()[1], fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.name().split()[0], fake.name().split()[1], fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.name().split()[0], fake.name().split()[1], fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.name().split()[0], fake.name().split()[1], fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.name().split()[0], fake.name().split()[1], fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.name().split()[0], fake.name().split()[1], fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.name().split()[0], fake.name().split()[1], fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.name().split()[0], fake.name().split()[1], fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.name().split()[0], fake.name().split()[1], fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.name().split()[0], fake.name().split()[1], fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.name().split()[0], fake.name().split()[1], fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.name().split()[0], fake.name().split()[1], fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.name().split()[0], fake.name().split()[1], fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.name().split()[0], fake.name().split()[1], fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.name().split()[0], fake.name().split()[1], fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address(),fake.address() ]
        writer.writerow(row)
        print("Currently thread {} in row: {}".format(i, j))
    f.close()
    if sema is not None:
          sema.release()

# thread(2)

# Runs at semaphore 2
# You can change the value according to CPU load you need
sema = Semaphore(cpu_count() - cpu_count() + 2)

if __name__ == "__main__":
    processes = []
    for i in range(700):
            p=Process(target=thread,args=(i,sema,))
            p.start()
            processes.append(p)
    #sleep an increment of time until all processes are done
    while len(p for p in processes if p.is_alive()) > 0:
            sleep(0.1)
            print("Waiting!!!")