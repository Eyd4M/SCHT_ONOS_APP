import pandas as pd

def read_iperf(file_path):
    data = []
    # Reads txt file
    with open(file_path, 'r') as file:
        for line in file:
            #Spliting line into list of words
            words = line.split()

            #Dictionary for storing parameters
            params = {}

            #it goes through words and and parameters into dictionary
            i = 0
            while i < len(words):
                #it checks if word beggins with "-"
                if words[i].startswith('-'):
                    key = words[i][1:]
                    i += 1

                    #it cheks if it is the last word in line
                    if i < len(words) and (not words[i].startswith('-')):
                        value = words[i]

                        if i + 1 < len(words) and (not words[i + 1].startswith('-')):
                            value += words[i + 1]
                            i += 1

                        params[key] = value
                i += 1

            data.append({**params, 'start': words[0]})

    df = pd.DataFrame(data)
    return df

print(read_iperf(r'C:\Users\Piotrek\PycharmProjects\SCHT_ONOS_APP2\resources\iperfs.txt'))

