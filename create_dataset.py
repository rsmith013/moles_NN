import os
import re
import json

all_lines = []
total = 0

for file in os.listdir('input_logs'):
    print(file)
    with open(os.path.join('input_logs', file)) as reader:
        lines = reader.readlines()

    output = []

    pattern = re.compile(
        r'^(?P<ip>[0-9.]+)\s(?P<identity>[\w.-]+)\s(?P<userid>[\w.-]+)\s\[(?P<date>.+)]\s\"(?P<request>GET[\w\s/\-\.?=&,+%*\']+)\"\s(?P<status_code>\d{3})\s(?P<response_bytes>\d+|-)\s\"(?P<referer>[\w\s/\-\.?=&:,%+*\']+)\"')

    # Filter lines
    for line in lines:
        if not any(x in line for x in
                   ['static', 'Googlebot', 'bingbot', 'Barkrowler', 'api', 'robots', 'DotBot', 'nagios-plugins',
                    'monitoring-plugins', 'Baiduspider', 'BUbiNG','Qwantify','YandexBot','MJ12bot','Sogou web spider',
                    'setup.php','export/xml','favicon.ico','AhrefsBot','baidu','SeznamBot','Gluten Free Crawler',
                    '/admin','YandexMobileBot','BingPreview','Gh0st']):

            m = pattern.search(line)
            if m and m.group('referer') != '-':

                if 'uuid' not in m.group('request') or 'https://catalogue.ceda.ac.uk/?q' not in m.group('referer'): continue
                output.append(json.dumps({
                    # 'ip': m.group('ip'),
                    'date': m.group('date'),
                    'request': m.group('request'),
                    'referer': m.group('referer')
                }) + '\n')

    total += len(lines)
    all_lines.extend(output)

print('Total input: {} Output lines: {} Shrink: {}%'.format(total, len(all_lines),
                                                            100 - round((float(len(all_lines)) / total) * 100, 3)))
with open('output_logs1.txt', 'w') as writer:
    writer.writelines(all_lines)
