
from datetime import datetime


def getDownloaded(group):

    dataId = []
    try:
        with open('/config/downloaded.txt','r') as f: 
            for line in f: 
                #process(line) 
                data = line.replace('\n','').split(";")

                if data[0] == group:
                    #print(f'read [{data}]',flush=True)
                    dataId.append(int(data[1]))
        return dataId

    except Exception as e:
        return dataId
        print('ERROR getDownloaded', e)
        return False



def setDownloaded(group, message_id):

    try:
        now = datetime.now() # current date and time
        date_time = now.strftime("%Y-%m-%d %H:%M:%S")

        file_object = open('/config/downloaded.txt', 'a')
        # Append 'hello' at the end of file
        file_object.write(f'{group};{message_id};{date_time}\n')
        # Close the file
        file_object.close()


        return True

    except Exception as e:
        print('ERROR setDownloaded', e)
        return False

            



if __name__ == "__main__":

    print('__name__')
    print(getDownloaded('hastaencontrarte'))
    print(setDownloaded('hastaencontrarte',11))
    print(getDownloaded('hastaencontrarte'))