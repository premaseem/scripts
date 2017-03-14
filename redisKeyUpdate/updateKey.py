# ~*~ coding: utf-8 ~*~
from redis import StrictRedis
from argparse import ArgumentParser


class RedisUpdateException(Exception):
    """class RedisUpdateException."""

    pass


class UpdateRedisKey(object):
    """class UpdateRedisKey."""

    def __init__(self, host, key, path):
        """__init__ method.

        :param host: str
        :return: void
        """
        if not host:
            raise RedisUpdateException("Failed to provide a host")
        self.__redis = StrictRedis(host)

        data = self.get_data_from_file(path)

        self.updateprocess(key, data)

    def updateprocess(self, key, data):
        """updateprocess, updates  process.

        :param data: str
        :return: void
        """
        if not data or not key:
            raise RedisUpdateException(
                "Failed to provide a valid data payload and or key.")
        try:
            print("Going to add data into key {}".format(key))
            self.__redis.set(key, data)
        except Exception as e:
            raise RedisUpdateException(str(e))

    def get_data_from_file(self, path):
        """get_data_from_file returns data from a file, given a path.

        :param path: str
        :return: string
        """
        data = None
        if not path:
            raise RedisUpdateException("Failed to provide a path")

        try:
            with open(path, 'r') as _file:
                data = _file.read()
                print("Retrieved data from {}".format(path))
        except Exception as e:
            print(str(e))
            raise RedisUpdateException(
                "Failed to open file in location {}".format(path))
        return data


if __name__ == '__main__':
    parser = ArgumentParser(description='Redis process updater')
    parser.add_argument('-r', '--redis', help='Redis host')
    parser.add_argument(
        '-k', '--key', help='Redis key to be used to add data into')
    # Need to specify a location for a file. If we try to add data from the
    # command line we encounter weird issues; the shell is trying to
    # interpret the string as a command instead of just seeing it as a string.
    parser.add_argument(
        '-p',
        '--path',
        help='Path to the file that contains the value to be added')

    args = parser.parse_args()
    # -h cannot work because it is already being used by the module itself.
    host = args.redis
    key = args.key
    path = args.path

    UpdateRedisKey(host, key, path)
