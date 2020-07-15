import os
import re
import json

all_lines = []
total = 0

for file in os.listdir('../moles-access-logs'):
    with open(os.path.join('../moles-access-logs', file)) as reader:
        lines = reader.readlines()

    output = []

    pattern = re.compile(r'^(?P<ip>[0-9.]+)\s'
                         r'(?P<identity>[\w.-]+)\s'
                         r'(?P<userid>[\w.-]+)\s'
                         r'\[(?P<date>.+)]\s'
                         r'\"(?P<request>GET[\w\s/\-\.?=&,+%*\']+)\"\s'
                         r'(?P<status_code>\d{3})\s'
                         r'(?P<response_bytes>\d+|-)\s'
                         r'\"(?P<referer>[\w\s/\-\.?=&:,%+*\']+)\"')

    # Filter lines
    for line in lines:
        if not any(x in line for x in
                   ['static', 'Googlebot', 'bingbot', 'Barkrowler', 'api', 'robots', 'DotBot', 'nagios-plugins',
                    'monitoring-plugins', 'Baiduspider', 'BUbiNG','Qwantify','YandexBot','MJ12bot','Sogou web spider',
                    'setup.php','export/xml','favicon.ico','AhrefsBot','baidu','SeznamBot','Gluten Free Crawler',
                    '/admin','YandexMobileBot','BingPreview','Gh0st']):

            m = pattern.search(line)
            if m and m.group('referer') != '-':
                if 'uuid' not in m.group('request') or 'http://catalogue.ceda.ac.uk/?q' not in m.group('referer'): continue
                output.append(json.dumps({
                    'ip': m.group('ip'),
                    'date': m.group('date'),
                    'request': m.group('request'),
                    'referer': m.group('referer')
                })+'\n')


    total += len(lines)
    all_lines.extend(output)

print 'Total input: {} Output lines: {} Shrink: {}%'.format(total, len(all_lines),
                                                            100 - round((float(len(all_lines)) / total) * 100, 3))
with open('output_logs.txt', 'w') as writer:
    writer.writelines(all_lines)
