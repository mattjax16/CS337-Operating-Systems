
import multiprocessing
import time

def send_msgs(conn, msgs):
    for msg in msgs:
        conn.send(msg)
    conn.close()
    
def recv_msg(conn):
    while 1:
        msg = conn.recv()
        if msg == "END":
            break
        print(msg)

def main():

    msgs = ["Hey", "Hello", "Hru?", "END"]
    parent_conn, child_conn = multiprocessing.Pipe()

    p1 = multiprocessing.Process(target=send_msgs, args=(parent_conn, msgs))
    p2 = multiprocessing.Process(target=recv_msg, args=(child_conn,))
    
    p1.start()
    p2.start()
    p2.join()
    p1.join()


if __name__ == '__main__':
    main()