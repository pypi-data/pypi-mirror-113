from collections import UserList
from multiprocessing import Pool
import json


class ASFSearchResults(UserList):
    def geojson(self):
        return {
            'type': 'FeatureCollection',
            'features': [product.geojson() for product in self]
        }

    def __str__(self):
        return json.dumps(self.geojson(), indent=2, sort_keys=True)

    def download(self, path: str, token: str = None, processes=1) -> None:
        """
        Iterates over each ASFProduct and downloads them to the specified path.

        :param path: The directory into which the products should be downloaded.
        :param token: EDL authentication token for authenticated downloads, see https://urs.earthdata.nasa.gov/user_tokens
        :param processes: Number of download processes to use. Defaults to 1 (i.e. sequential download)

        :return: None
        """

        if processes == 1:
            for product in self:
                product.download(path=path, token=token)
        else:
            pool = Pool(processes=processes)
            args = [(product, path, token) for product in self]
            pool.map(_download_product, args)
            pool.close()
            pool.join()


def _download_product(args):
    product, path, token = args
    product.download(path=path, token=token)
