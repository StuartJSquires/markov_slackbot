import pandas as pd
from os import path, listdir


class Data(object):
    def __init__(self):
        messages_dir = path.join(path.pardir, 'data', 'messages')
        self.messages_file = open(path.join(messages_dir, 'messages.txt'), 'a')
        self.messages_file.seek(0)
        self.messages_file.truncate()

    def clean_data(self, data):
        """
        function will remove all messages that contain subtypes /ie. not clean
         messages (comments, file uploads)
        """
        # regex will clean all reaction from messages
        messages = data[(data['type'] == 'message') &
                        ('subtype' not in data.columns)]

        # replace in line sections (ie ``` code ```)
        messages['text'] = messages['text'].str.replace(r'(```)[^;]*(```)', '')
        # replace reaction in text
        messages['text'] = messages['text'].str.replace(r'(:)[^<>]*(:)', '')
        # replace every <>
        messages['text'] = messages['text'].str.replace(r'(<)[^<>]*(>)', '')
        # replace &gt;
        messages['text'] = messages['text'].str.replace('&gt;', '')
        # replace &amp;
        messages['text'] = messages['text'].str.replace('&amp;', '')
        # encode to string
        return messages['text'].str.encode('UTF-8').astype(str)

    def write_to_file(self, messages):
        # open file and append messages to txt
        messages_file = open(path.join(path.pardir, 'data', 'messages',
                             'messages.txt'), 'a')
        for message in messages:
            if ((not message.endswith('.') or
                not message.endswith('?') or
               not message.endswith('!')) and
               len(message) > 0):
                message += '. '
            messages_file.write(message + '\n')
        messages_file.close

    def get_data(self):
        folders = listdir(path.join(path.pardir, 'data'))
        print(folders)
        for folder in folders:
            if folder == 'messages':
                continue
            files = listdir(path.join(path.pardir, 'data', folder))
            for file in files:
                file = pd.read_json(path.join(path.pardir, 'data', folder,
                                    file))
                messages = self.clean_data(file)
                self.write_to_file(messages)


def main():
    data = Data()
    data.get_data()


if __name__ == "__main__":
    main()
