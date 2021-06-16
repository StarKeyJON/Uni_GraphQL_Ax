# python3
import os, shutil, csv, re
import time
import store_data
from subprocess import check_output


def get_time():
    check_output(['node', './timeSets.js'])
    time.sleep(.3)


def default_Q():
    check_output(['node', './defaultQ.js'])
    time.sleep(2)


def get_csv_data(csv_file, row, cell):
    ls = []
    with open(csv_file, newline='') as csvfile:
        csv_file = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for rows in csv_file:
            ls.append(str(rows[0]).split(","))
        if cell is not None:
            return re.sub(r'\W+', '', str(ls[row - 1]).split(",")[cell - 1])
        else:
            return ls[row - 1]


def check_time():
    # check if directories exist, if not create
    # If a datasets directory doesn't exist, make a new one
    is_directory = os.path.isdir('./datasets')
    dataset_dir = 'datasets'
    mkdir = 'mkdir {0}'.format(dataset_dir)
    if is_directory == False:
        pass

        # if a dataset directory exists, check to see if it is empty
    else:
        if len(os.listdir('./datasets')) != 0:
            store_data.store_data()

        else:
            for file in os.listdir(os.getcwd()):
                if file.endswith('.csv'):
                    os.remove(os.getcwd() + '/' + dataset_dir + '/' + file)

    is_new_directory = os.path.isdir('./newtimesets')
    newtimeset_dir = 'newtimesets'
    mkdir1 = 'mkdir {0}'.format(newtimeset_dir)
    if is_new_directory == False:
        try:
            os.system(mkdir1)
            print('successfully created new times directory')
        except:
            pass

    new_time_path = os.listdir('./newtimesets')
    is_old_directory = os.path.isdir('./oldtimesets')

    oldtimeset_dir = 'oldtimesets'
    mkdir2 = 'mkdir {0}'.format(oldtimeset_dir)
    if is_old_directory == False:
        try:
            os.system(mkdir2)
            print('successfully created old time directory')
        except:
            pass

    # check to see if timestamp.csv files exist in directory
    new_time = []
    old_time = []
    graph = []
    if len(new_time_path) == 0:
        print('there are no new times, let me get some')
        # if no new times exist, get new times
        get_time()
        check_time()
    # if new times exist but old do not, move new files to old dir and get new timesets, execute default_Q and store_data
    else:
        if len(os.listdir('./oldtimesets')) == 0:
            print('%' * 8)
            print('''
                There are now new times but there are no old times. 
                This apears to be the first cycle,
                allow me to fetch new times and store the default schema.
                ''')
            print('%' * 8)
            for file in new_time_path:
                shutil.move(newtimeset_dir + '/' + file, oldtimeset_dir)
            get_time()
            default_Q()
            store_data.store_data()
            check_time()


        else:  # if new and old timesets exist, then we can compare them!
            for file in os.listdir('./oldtimesets'):
                if file.endswith('timestamp.csv'):
                    old_time.append(file)
            for file in new_time_path:
                if file.endswith('timestamp.csv'):
                    new_time.append(file)

                # compare the new ids against the old time_sets,
                # append graph query list with inconsistencies for next batch of queries
                num_swap = 0
                for i in range(50):
                    a = get_csv_data('./newtimesets' + '/' + file, i, 1)
                    b = get_csv_data('./oldtimesets' + '/' + file, i, 1)
                    if a != b:
                        num_swap += 1
                        if file not in graph:
                            graph.append(file)

                print(' DEX=> ' + file)
                for j in range(7):
                    j += 1
                    print(' ' * 4 + get_csv_data('./newtimesets' + '/' + file, j, 1) + ' index: '+str(j)+' --> new id')
                print(' ' * 2, '*' * 12, ' ' * 2)
                for i in range(7):
                    i += 1
                    print(' ' * 4 + get_csv_data('./oldtimesets' + '/' + file, i, 1) + ' index: '+str(i)+' --> old id')
                print('_' * 20)
                
            # formatting the graph list for js queries
            graph = [
                "'UNIv2'" + ':' + "'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2'" if i == 'UNIv2timestamp.csv' else i
                for i in graph]
            graph = [
                "'MDEX'" + ':' + "'https://api.thegraph.com/subgraphs/name/wetitpig-cross-chain/mdex-bsc'" if i == 'MDEXtimestamp.csv' else i
                for i in graph]
            graph = [
                "'PANCAKE'" + ':' + "'https://api.thegraph.com/subgraphs/name/depayfi/pancake-v2-exchange'" if i == 'PANCAKEtimestamp.csv' else i
                for i in graph]
            graph = [
                "'SUSHI'" + ':' + "'https://api.thegraph.com/subgraphs/name/sushiswap/exchange'" if i == 'SUSHItimestamp.csv' else i
                for i in graph]
            graph = [
                "'QUICK'" + ':' + "'https://api.thegraph.com/subgraphs/name/sameepsi/quickswap'" if i == 'QUICKtimestamp.csv' else i
                for i in graph]
            graph = [
                "'HONEY'" + ':' + "'https://api.thegraph.com/subgraphs/name/1hive/honeyswap-v2'" if i == 'HONEYtimestamp.csv' else i
                for i in graph]

            sources = graph

            if len(sources) == 0:
                for new_file in os.listdir('./oldtimesets'):
                    try:
                        os.remove(oldtimeset_dir + '/' + new_file)
                        print("Removed " + (oldtimeset_dir + new_file) + ' since there are no new times to fetch. ')
                    except Exception:
                        print('Error: deletion failed 1')
                        time.sleep(10)
                        break
                for file in new_time_path:
                    shutil.move(newtimeset_dir + '/' + file, oldtimeset_dir)
                get_time()
                check_time()
            else:
                try:
                    print('-' * 18)
                    print(' ' * 10)
                    print('Current query: ' + str(graph))
                    print('_' * 20)
                    # delete oldtimesets
                    for new_file in os.listdir('./oldtimesets'):
                        try:
                            os.remove(oldtimeset_dir + '/' + new_file)
                        except Exception:
                            print('Error: deletion failed 2')
                            time.sleep(10)
                            break

                    # move new times to old times directory
                    for file in new_time_path:
                        shutil.move(newtimeset_dir + '/' + file, oldtimeset_dir)

                    get_time()

                    # write the newly created query to js file
                    # passing the slate the first time prevents errors of appending existing data
                        # that may have been left from a shutdown and sending a false schema
                    with open('./time_slate.js', 'w') as file:
                        pass
                    with open('./time_slate.js', 'r+') as file:
                        file.write('const sources={')
                        for k in sources:
                            file.write(k + ', \n')
                        file.write('};\n' + 'module.exports = { sources };')
                    with open('./new_query.js', 'w') as file:
                        pass
                    
                    # write the function to generate a specfic schema to query using numswap variable as amount of swaps
                    try:
                        with open('./new_query.js', 'r+') as file:
                            file.write("const axios = require('axios');\nconst ObjectsToCsv = require('objects-to-csv');"+
                            "\nconst { sources } = require('./time_slate.js');\nconst fs = require('fs');"+
                            "\n\nfunction GATHER() {\n  Object.entries(sources).forEach(([key, value]) => {\n    MAIN = async () => {"+
                            "\n      try {\n      const result = await axios.post(\n         value,\n          {\n              query: `"+
                            "\n              {\n                swaps(first: " + str(num_swap) + ", orderBy: timestamp, orderDirection: desc){\n                      timestamp"+
                            "\n                pair {\n                  token0 {\n                      name\n                  }\n                }\n                sender"+
                            "\n                amount0In\n                amount1In\n                amount0Out\n                amount1Out\n                to\n                amountUSD"+
                            "\n                }\n              }\n              `\n          }\n        )"+
                            "\n        const csv = new ObjectsToCsv(result.data.data.swaps)\n        console.log('Successfully uploaded custom schema query of recent swap logs')\n        await csv.toDisk(`./${" + "key" + "}.csv`)\n"+
                            "\n        } catch (err) {\n          console.log(err);\n        }\n      };\n    MAIN();\n  })}\nGATHER();\n")
                    except Exception:
                        print('Error: Rewrite the js code')
                        sys.exit()

                    # execute the newly formed query
                    print('Executing newly formed schema...')
                    try:
                        check_output(['node', './new_query.js'])
                    except Exception:
                        print('Error executing custom query' + Exception)
                        sys.exit

                    time.sleep(2)

                    # clear time slate
                    with open('./time_slate.js', 'w') as file:
                        pass

                    # # delete query slate
                    # with open('./new_query.js', 'w') as file:
                    #     pass

                    # store the newly gathered data
                    print('storing the gathered data')
                    store_data.store_data()

                    # repeat
                    check_time()
                except:
                    print('error storing modified list')
                    sys.exit()


check_time()

