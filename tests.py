import queue

q = queue.Queue(maxsize=1000)

for i in range(100):
    q.put(i)




while True:
    try:
        e = q.get(timeout=10)
        print(e)
    except:
        print("acabou a musica")
        break

print("saiu")