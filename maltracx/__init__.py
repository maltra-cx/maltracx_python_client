'''
maltracx

Official maltra.cx REST API client
'''

__title__ = 'maltracx'
__version__ = '0.0.1'
__all__ = ('Client',)
__author__ = 'Johan Nestaas <johan@maltra.cx>'
__license__ = 'BSD'
__copyright__ = 'Copyright 2017 Johan Nestaas'

import sys
from .client import Client


def _add_args(parser):
    parser.add_argument('--apikey-id', '-I')
    parser.add_argument('--apikey-secret', '-S')
    parser.add_argument('--root-url', '-R')


def main():
    import json
    import argparse
    parser = argparse.ArgumentParser()
    subs = parser.add_subparsers(dest='cmd')

    p = subs.add_parser('create-apikey')
    p.add_argument('username')
    p.add_argument('password')
    p.add_argument('--expires-at', '-x')
    p.add_argument('--root-url', '-R')

    p = subs.add_parser('news')
    _add_args(p)

    p = subs.add_parser('user')
    _add_args(p)

    p = subs.add_parser('report')
    subs2 = p.add_subparsers(dest='report_cmd')

    p2 = subs2.add_parser('get')
    _add_args(p2)

    p2 = subs2.add_parser('create')
    _add_args(p2)
    p2.add_argument('name')
    p2.add_argument('--description', '-d')
    p2.add_argument('--tlp', '-t', default='white')

    p = subs.add_parser('urlmon')
    subs2 = p.add_subparsers(dest='urlmon_cmd')

    p2 = subs2.add_parser('get')
    _add_args(p2)

    p2 = subs2.add_parser('create')
    _add_args(p2)
    p2.add_argument('url')
    p2.add_argument('--tlp', '-t', default='white')
    p2.add_argument('--referer', '-r')
    p2.add_argument('--user-agent', '--ua', '-u')
    p2.add_argument('--yara-rules', '-y', nargs='*')

    p2 = subs2.add_parser('delete')
    _add_args(p2)
    p2.add_argument('guids', nargs='+')

    p2 = subs2.add_parser('trigger')
    _add_args(p2)
    p2.add_argument('guids', nargs='+')

    p = subs.add_parser('yararule')
    subs2 = p.add_subparsers(dest='yararule_cmd')

    p2 = subs2.add_parser('get')
    _add_args(p2)
    p2.add_argument('--guids', '-g', nargs='*')

    p2 = subs2.add_parser('create')
    _add_args(p2)
    p2.add_argument('source')
    p2.add_argument('--tlp', '-t', default='white')

    p2 = subs2.add_parser('delete')
    _add_args(p2)
    p2.add_argument('guids', nargs='+')

    p = subs.add_parser('yaramatch')
    subs2 = p.add_subparsers(dest='yaramatch_cmd')

    p2 = subs2.add_parser('get')
    _add_args(p2)
    p2.add_argument('--guids', '-g', nargs='*')

    args = parser.parse_args()

    try:
        if hasattr(args, 'apikey_id'):
            client = Client(apikey_id=args.apikey_id,
                            apikey_secret=args.apikey_secret,
                            root_url=args.root_url)
        elif hasattr(args, 'root_url'):
            client = Client(root_url=args.root_url)
        else:
            client = Client()
    except:
        parser.print_usage()
        sys.exit(1)

    try:
        if args.cmd == 'create-apikey':
            response = client.create_apikey(args.username, args.password,
                                            expires_at=args.expires_at)
        elif args.cmd == 'news':
            response = client.get_news()
        elif args.cmd == 'user':
            response = client.get_user()
        elif args.cmd == 'report':
            if args.report_cmd == 'get':
                response = client.get_report()
            elif args.report_cmd == 'create':
                response = client.create_report(
                    args.name, description=args.description, tlp=args.tlp)
            else:
                parser.print_usage()
                sys.exit(1)
        elif args.cmd == 'urlmon':
            if args.urlmon_cmd == 'get':
                response = client.get_url_monitor()
            elif args.urlmon_cmd == 'create':
                response = client.create_url_monitor(
                    args.url, tlp=args.tlp, referer=args.referer,
                    user_agent=args.user_agent, yara_rules=args.yara_rules,
                )
            elif args.urlmon_cmd == 'delete':
                response = client.delete_url_monitor(args.guids)
            elif args.urlmon_cmd == 'trigger':
                response = client.trigger_url_monitor(args.guids)
            else:
                parser.print_usage()
                sys.exit(1)
        elif args.cmd == 'yararule':
            if args.yararule_cmd == 'get':
                response = client.get_yara_rule(guids=args.guids or None)
            elif args.yararule_cmd == 'create':
                response = client.create_yara_rule(args.source, tlp=args.tlp)
            elif args.yararule_cmd == 'delete':
                response = client.delete_yara_rule(args.guids)
        elif args.cmd == 'yaramatch':
            if args.yaramatch_cmd == 'get':
                response = client.get_yara_match(guids=args.guids or None)
        else:
            parser.print_usage()
            sys.exit(1)
    except Exception as e:
        sys.exit(str(e))

    print(json.dumps(response, indent=4))


if __name__ == '__main__':
    main()
