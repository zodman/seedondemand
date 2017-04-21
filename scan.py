#!/usr/bin/env python
# encoding=utf8
# made by zodman

from scraper import scrape
import yaml
import click

TRACKER="http://open.nyaatorrents.info:6544/announce"

_torrent = []

def get_torrent_from_hash(hash):
    for i in _torrent:
        if hash.lower() == i["torrent_hash"].lower():
            return i

def get_all_hashes():
    f = yaml.load(open("torrents.yaml").read())
    l = []
    torrents = f.get("torrents")
    for fansub_entries in torrents.keys():
        for torrent in torrents[fansub_entries]:
            _torrent.append(torrent)
            hash = torrent.get("torrent_hash")
            l.append(hash)
    return l



@click.command()
def scan():
    hashes = get_all_hashes()
    results = scrape(TRACKER, hashes)
    for hash, info in results.items():
        tor = get_torrent_from_hash(hash)
        if tor:
            seed, leech = info.get("seeds"), info.get("peers")
            msg = u"{} {} \U0001F51D / {} \U00002B07".format(tor["name"], leech, seed)
            click.echo(msg)


if __name__=="__main__":
    scan()
