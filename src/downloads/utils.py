class FileSize(str):

    """
    Allows write file sizes as strings and get de size
    in bytes.

    >>> FileSize('2.5MB').get_bytes()
    2621440
    >>> FileSize(1024).get_bytes()
    1024
    >>> FileSize('1024KB').get_bytes()
    1048576
    >>> FileSize('4RR').get_bytes()
    '4RR'
    """

    SUFFIXES = ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']

    def get_bytes(self):
        try:
            exp = self.SUFFIXES.index(self.__str__()[-2:])
            return int(float(self.__str__()[:-2])*1024**(exp+1))
        except ValueError:
            try:
                int_value = int(self.__str__())
                return int_value
            except ValueError:
                return self
