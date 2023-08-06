#!/usr/bin/env python3

import asyncio
import json
import logging
import random
import re
import sys
import aiohttp
import pycountry
import requests
import time
import ssl
from typing import Union
from urllib.parse import urlparse, unquote

try:
    from helper import get_by_regex, ndict_to_csv, run_until_completed
except ModuleNotFoundError:
    from .helper import get_by_regex, ndict_to_csv, run_until_completed

ssl.match_hostname = lambda cert, hostname: hostname == cert["subjectAltName"][0][1]
logging.basicConfig(
    stream=sys.stdout, level=logging.INFO, format="%(levelname)s: %(message)s"
)


class M3uParser:
    """A parser for m3u files.

    It parses the contents of m3u file to a list of streams information which can be saved as a JSON/CSV file.

    :Example

    >>> url = "/home/pawan/Downloads/ru.m3u"
    >>> useragent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
    >>> parser = M3uParser(timeout=5, useragent=useragent)
    >>> parser.parse_m3u(url)
    INFO: Started parsing m3u file...
    >>> parser.remove_by_extension('mp4')
    >>> parser.filter_by('status', 'GOOD')
    >>> print(len(parser.get_list()))
    4
    >> parser.to_file('pawan.json')
    INFO: Saving to file...
    """

    def __init__(self, useragent: str = None, timeout: int = 5):
        self._streams_info = []
        self._streams_info_backup = []
        self._lines = []
        self._timeout = timeout
        self._loop = None
        self._headers = {
            "User-Agent": useragent
            if useragent
            else "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
        }
        self._check_live = False
        self._content = ""
        self._url_regex = re.compile(
            r"^(?:(?:https?|ftp)://)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!("
            r"?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,"
            r"3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){"
            r"2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*["
            r"a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*["
            r"a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:/\S*)?$"
        )
        self._file_regex = re.compile(
            r"^[a-zA-Z]:\\((?:.*?\\)*).*\.[\d\w]{3,5}$|^(/[^/]*)+/?.[\d\w]{3,5}$"
        )

    def parse_m3u(self, path: str, check_live: bool = True):
        """Parses the content of local file/URL.

        It downloads the file from the given url or use the local file path to get the content and parses line by line
        to a structured format of streams information.

        :param path: Path can be a url or local filepath
        :type path: str
        :param check_live: To check if the stream links are working or not
        :type check_live: bool
        :rtype: None

        """
        self._check_live = check_live
        if urlparse(path).scheme != "" or re.search(self._url_regex, path):
            logging.info("Started parsing m3u link...")
            try:
                self._content = requests.get(path).text
            except:
                logging.error("Cannot read anything from the url!!!")
                return
        else:
            logging.info("Started parsing m3u file...")
            try:
                with open(unquote(path), errors="ignore") as fp:
                    self._content = fp.read()
            except FileNotFoundError:
                logging.error("File doesn't exist!!!")
                return

        # splitting contents into lines to parse them
        self._lines = [
            line.strip("\n\r")
            for line in self._content.split("\n")
            if line.strip("\n\r") != ""
        ]
        if len(self._lines) > 0:
            self._parse_lines()
        else:
            logging.error("No content to parse!!!")

    @staticmethod
    async def _run_until_completed(tasks):
        for res in run_until_completed(tasks):
            _ = await res

    def _parse_lines(self):
        num_lines = len(self._lines)
        self._streams_info.clear()
        try:
            self._loop = asyncio.get_event_loop()
        except RuntimeError:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
        try:
            coros = (
                self._parse_line(line_num)
                for line_num in range(num_lines)
                if "#EXTINF" in self._lines[line_num]
            )
            self._loop.run_until_complete(self._run_until_completed(coros))
        except BaseException:
            pass
        else:
            self._streams_info_backup = self._streams_info.copy()
            self._loop.run_until_complete(asyncio.sleep(0))
            while self._loop.is_running():
                time.sleep(0.3)
                if not self._loop.is_running():
                    self._loop.close()
                    break
        logging.info("Parsing completed !!!")

    async def _parse_line(self, line_num: int):
        line_info = self._lines[line_num]
        stream_link = ""
        streams_link = []
        status = "BAD"
        try:
            for i in [1, 2]:
                if self._lines[line_num + i] and re.search(
                    self._url_regex, self._lines[line_num + i]
                ):
                    streams_link.append(self._lines[line_num + i])
                    break
                elif self._lines[line_num + i] and re.search(
                    self._file_regex, self._lines[line_num + i]
                ):
                    status = "GOOD"
                    streams_link.append(self._lines[line_num + i])
                    break
            stream_link = streams_link[0]
        except IndexError:
            pass
        if line_info and stream_link:
            try:
                temp = {}
                tvg_name = get_by_regex(r"tvg-name=\"(.*?)\"", line_info)
                tvg_id = get_by_regex(r"tvg-id=\"(.*?)\"", line_info)
                logo = get_by_regex(r"tvg-logo=\"(.*?)\"", line_info)
                category = get_by_regex(r"group-title=\"(.*?)\"", line_info)
                title = get_by_regex("[,](?!.*[,])(.*?)$", line_info)
                country = get_by_regex(r"tvg-country=\"(.*?)\"", line_info)
                language = get_by_regex(r"tvg-language=\"(.*?)\"", line_info)
                tvg_url = get_by_regex(r"tvg-url=\"(.*?)\"", line_info)
                if country:
                    country_obj = pycountry.countries.get(alpha_2=country.upper())
                    temp["country"] = {
                        "code": country,
                        "name": country_obj.name if country_obj else "",
                    }
                if language:
                    language_obj = pycountry.languages.get(name=country.capitalize())
                    temp["language"] = {
                        "code": language_obj.alpha_3 if language_obj else "",
                        "name": language,
                    }

                timeout = aiohttp.ClientTimeout(total=self._timeout)
                if self._check_live and status == "BAD":
                    try:
                        async with aiohttp.ClientSession() as session:
                            async with session.request(
                                "get",
                                stream_link,
                                headers=self._headers,
                                timeout=timeout,
                            ) as response:
                                if response.status == 200:
                                    status = "GOOD"
                    except:
                        pass
                temp.update(
                    {
                        "name": title,
                        "logo": logo,
                        "url": stream_link,
                        "category": category,
                        "tvg": {
                            "id": tvg_id,
                            "name": tvg_name,
                            "url": tvg_url,
                        },
                    }
                )
                if self._check_live:
                    temp["status"] = status
                self._streams_info.append(temp)
            except AttributeError:
                pass

    def filter_by(
        self,
        key: str,
        filters: Union[str, list],
        retrieve: bool = True,
        nested_key: bool = False,
    ):
        """Filter streams infomation.

        It retrieves/removes stream information from streams information list using filter/s on key.
        If key is not found, it will not raise error and filtering is done silently.

        :param key: Key can be single or nested. eg. key='name', key='language-name'
        :type key: str
        :param filters: List of filter/s to perform the retrieve or remove operation.
        :type filters: str or list
        :param retrieve: True to retrieve and False for removing based on key.
        :type retrieve: bool
        :param nested_key: True/False for if the key is nested or not.
        :type nested_key: bool
        :rtype: None
        """
        key_0, key_1 = [""] * 2
        if nested_key:
            try:
                key_0, key_1 = key.split("-")
            except ValueError:
                logging.error("Nested key must be in the format <key>-<nested_key>")
                return
        if not filters:
            logging.error("Filter word/s missing!!!")
            return
        if not isinstance(filters, list):
            filters = [filters]
        any_or_all = any if retrieve else all
        not_operator = lambda x: x if retrieve else not x
        try:
            self._streams_info = list(
                filter(
                    lambda stream_info: any_or_all(
                        not_operator(
                            re.search(
                                re.compile(fltr, flags=re.IGNORECASE),
                                stream_info.get(key_0, {}).get(key_1, "")
                                if nested_key
                                else stream_info.get(key, ""),
                            )
                        )
                        for fltr in filters
                    ),
                    self._streams_info,
                )
            )
        except AttributeError:
            logging.error("Key given is not nested !!!")

    def reset_operations(self):
        """Reset the stream information list to initial state before various operations.

        :rtype: None
        """
        self._streams_info = self._streams_info_backup.copy()

    def remove_by_extension(self, extension: Union[str, list]):
        """Remove stream information with certain extension/s.

        It removes stream information from streams information list based on extension/s provided.

        :param extension: Name of the extension like mp4, m3u8 etc. It can be a string or list of extension/s.
        :type extension: str or list
        :rtype: None
        """
        self.filter_by("url", extension, retrieve=False, nested_key=False)

    def retrieve_by_extension(self, extension: Union[str, list]):
        """Select only streams information with a certain extension/s.

        It retrieves the stream information based on extension/s provided.

        :param extension: Name of the extension like mp4, m3u8 etc. It can be a string or list of extension/s.
        :type extension: str or list
        :rtype: None
        """
        self.filter_by("url", extension, retrieve=True, nested_key=False)

    def remove_by_category(self, filter_word: Union[str, list]):
        """Removes streams information with category containing a certain filter word/s.

        It removes stream information based on category using filter word/s.

        :param filter_word: It can be a string or list of filter word/s.
        :type filter_word: str or list
        :rtype: None
        """
        self.filter_by("category", filter_word, retrieve=False)

    def retrieve_by_category(self, filter_word: Union[str, list]):
        """Retrieve only streams information that contains a certain filter word/s.

        It retrieves stream information based on category/categories.

        :param filter_word: It can be a string or list of filter word/s.
        :type filter_word: str or list
        :rtype: None
        """
        self.filter_by("category", filter_word, retrieve=True)

    def sort_by(self, key: str, asc: bool = True, nested_key: bool = False):
        """Sort streams information.

        It sorts streams information list sorting by key in asc/desc order.

        :param key: It can be single or nested key.
        :type key: str
        :param asc: Sort by asc or desc order
        :type asc: bool
        :param nested_key: True/False for if the key is nested or not.
        :type nested_key: bool
        :rtype: None
        """
        key_0, key_1 = [""] * 2
        if nested_key:
            try:
                key_0, key_1 = key.split("-")
            except ValueError:
                logging.error("Nested key must be in the format <key>-<nested_key>")
                return
        try:
            self._streams_info = sorted(
                self._streams_info,
                key=lambda stream_info: stream_info[key_0][key_1]
                if nested_key
                else stream_info[key],
                reverse=not asc,
            )
        except KeyError:
            logging.error("Key not found!!!")

    def get_json(self, indent: int = 4):
        """Get the streams information as json.

        :param indent: Int value for indentation.
        :type indent: int
        :return: json of the streams_info list
        :rtype: json
        """
        return json.dumps(self._streams_info, indent=indent)

    def get_list(self):
        """Get the parsed streams information list.

        It returns the streams information list.

        :return: Streams information list
        :rtype: list
        """
        return self._streams_info

    def get_random_stream(self, random_shuffle: bool = True):
        """Return a random stream information

        It returns a random stream information with shuffle if required.

        :param random_shuffle: To shuffle the streams information list before returning the random stream information.
        :type random_shuffle: bool
        :return: A random stream info
        :rtype: dict
        """
        if not len(self._streams_info):
            logging.error("No streams information so could not get any random stream.")
            return
        if random_shuffle:
            random.shuffle(self._streams_info)
        return random.choice(self._streams_info)

    def to_file(self, filename: str, format: str = "json"):
        """Save to file (CSV or JSON)

        It saves streams information as a CSV or JSON file with a given filename and format parameters.

        :param filename: Name of the file to save streams_info as.
        :type filename: str
        :param format: csv/json to save the streams_info.
        :type format: str
        :rtype: None
        """
        format = filename.split(".")[-1] if len(filename.split(".")) > 1 else format

        def with_extension(name, ext):
            name, ext = name.lower(), ext.lower()
            if ext in name:
                return name
            else:
                return name + f".{ext}"

        filename = with_extension(filename, format)
        logging.info("Saving to file: %s" % filename)
        try:
            if format == "json":
                data = json.dumps(self._streams_info, indent=4)
                with open(filename, "w") as fp:
                    fp.write(data)
                logging.info("Saved to file: %s" % filename)

            elif format == "csv":
                ndict_to_csv(self._streams_info, filename)
                logging.info("Saved to file: %s" % filename)
            else:
                logging.error("Unrecognised format!!!")
        except Exception as error:
            logging.warning(str(error))


if __name__ == "__main__":
    url = "/home/pawan/Downloads/ru.m3u"
    useragent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
    parser = M3uParser(timeout=5, useragent=useragent)
    parser.parse_m3u(url)
    parser.remove_by_extension("mp4")
    parser.filter_by("status", "GOOD")
    print(len(parser.get_list()))
    parser.to_file("pawan.json")
