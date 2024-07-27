# Multi thread file copy
from multiprocessing import Pool, Manager
import os


# name文件名，queue队列
def copyFileTask(name, oldFolderName, newFolderName, queue):
    fr = open(oldFolderName + "/" + name, 'rb')
    fw = open(newFolderName + "/" + name, 'wb')
    content = fr.read()
    fw.write(content)
    fr.close()
    fw.close()
    queue.put(name)  # queue.put()Add a value to the series


def main():
    oldFolderName = input("源文件夹绝对路径：")
    newFolderName = oldFolderName + '[copy]'
    os.mkdir(newFolderName)
    # 2.Get the names of all files in the old folder
    fileNames = os.listdir(oldFolderName)
    print(fileNames)
    # 3.Copy all files in the original folder to the new folder in a multi process manner
    # Multiprocessing provides Pool() for creating process pools
    # Size Specifies the number of processes contained in the process pool
    size = 3
    pool = Pool(size)
    # Create a queue. No parameter indicates unlimited number of queues
    queue = Manager().Queue()
    # fileNames:List of files in the folder
    for name in fileNames:
        # Pool.apply will block, apply_ Async asynchronous non blocking, parallel execution
        # Pool.apply将阻塞，apply_async并行执行

        pool.apply_async(copyFileTask,
                         args=(name, oldFolderName, newFolderName, queue))
    # Close the process pool. After closing, the pool will not receive new requests
    pool.close()  # 不再创建新进程，不是消除进程
    # file_numNumber of folder files
    file_num = len(fileNames)
    # copy_ok_numNumber of copied files
    copy_ok_num = 0
    # The while below is used to display the progress,
    # which is an additional function
    while True:
        # name = queue.get()
        copy_ok_num += 1
        print("\r完成进度:%.2f " % (copy_ok_num * 100 / file_num), end='')
        if copy_ok_num >= file_num:
            break
    # Wait for all child processes in the pool to complete execution,
    # which must be placed after the close statement
    pool.join()
    print("拷贝完成")


global name
if __name__ == '__main__':
    main()
