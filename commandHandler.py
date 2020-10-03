dict = {}

if __name__ != "__main__":

    class discordCommandHandler:
        def new_command(self, **kwargs):
            global dict

            if kwargs['name'] and kwargs['description']:
                dict[kwargs['name']] = kwargs['description']

            else:

                raise Exception("Failed to add new command in {}".format(__file__))

        def ret_comm(self): 
            if dict:
                return dict
            else:
                raise Exception("No commands have been added to the database.")

        def dict_keys(self, dict):
            tempLog = []

            if dict:
                for i in dict.keys():
                    tempLog.append(i)
                return tempLog
            else: raise Exception("Please provide a dictionary to retrieve the keys from.")

else : 
    
    raise Exception("Please import {} instead of running the file directly.".format(__file__))