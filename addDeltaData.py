#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import re
import shutil

base_url = "https://www.friidrott.se/rs/arsbasta.aspx"
seasons  = [46] # Inomhus 2020
classes  = ["p14","p15","p16","p17","p19","m22","m","f14","f15","f16","f17","f19","k22","k"]

def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

# Open data file and start adding new posts
f = open("data/DeltaData.json","w")

# Write the columns
f.write("{\n")
f.write("  \"cols\":[\n")
f.write("    {\"id\":\"A\",\"label\":\"Säsong\",\"type\":\"string\"},\n")
f.write("    {\"id\":\"B\",\"label\":\"Klass\",\"type\":\"string\"},\n")
f.write("    {\"id\":\"C\",\"label\":\"Gren\",\"type\":\"string\"},\n")
f.write("    {\"id\":\"D\",\"label\":\"Placering\",\"type\":\"string\"},\n")
f.write("    {\"id\":\"E\",\"label\":\"Resultat\",\"type\":\"string\"},\n")
f.write("    {\"id\":\"F\",\"label\":\"Namn\",\"type\":\"string\"},\n")
f.write("    {\"id\":\"G\",\"label\":\"Född\",\"type\":\"string\"},\n")
f.write("    {\"id\":\"H\",\"label\":\"Klubb\",\"type\":\"string\"},\n")
f.write("    {\"id\":\"I\",\"label\":\"Plats\",\"type\":\"string\"},\n")
f.write("    {\"id\":\"J\",\"label\":\"Datum\",\"type\":\"string\"},\n")
f.write("    {\"id\":\"K\",\"label\":\"Notering\",\"type\":\"string\"}\n")
f.write("  ],\n")

# Write the rows
f.write("  \"rows\":[\n")
first = True

for season_no in seasons:
    for cl in classes:
        target_url = base_url + "?season=" + str(season_no) + "&class=" + cl
        # print target_url
        data = urllib.urlopen(target_url)

        for line in data:
            line = line.strip()
            if '<h2>' in line or 'class="rubrik"' in line:
                season = remove_html_tags(line)
                if 'Inget årsbästa finns' in season:
                    continue
                print str(season_no) + ": " + season
            if 'colspan="4"' in line and 'img' not in line:
                if 'notis' not in line:
                    event = remove_html_tags(line)
                    place = 1
                    notis = ""
                else:
                    notis = remove_html_tags(line)
            if 'class="notis"' in line:
                if 'width="50"' in line:
                    result = remove_html_tags(line)
                if 'width="230"' in line:
                    info = remove_html_tags(line).split()
                    name = ""
                    year = ""
                    club = ""
                    for i in info:
                        if i.isdigit():
                            if int(i) > 30:
                                year = "19" + i
                            else:
                                year = "20" + i
                        elif not year:
                            name = name + i + " "
                        else:
                            club = club + i + " "
                if 'width="120"' in line:
                    city = remove_html_tags(line)
                if 'width="40"' in line:
                    date = remove_html_tags(line)
                    # All data received, print the line
                    if 'Hanviken' not in club and \
                       'Alunda' not in club and \
                       'Bromma' not in club and \
                       'Danderyd' not in club and \
                       'Falun' not in club and \
                       'Hammarby' not in club and \
                       'Hellas' not in club and \
                       'Huddinge' not in club and \
                       'Hässelby' not in club and \
                       'Tureberg' not in club and \
                       'Tyresö' not in club and \
                       'Täby' not in club:
                        place += 1
                        continue
                    cl = cl.upper()
                    season = season.replace(" " + cl,"")
                    if not first:
                        f.write(",\n")                    
                    f.write("    {\"c\":[\n")
                    f.write("      {\"v\": \"" + season + "\"},\n")
                    f.write("      {\"v\": \"" + cl + "\"},\n")
                    f.write("      {\"v\": \"" + event + "\"},\n")
                    f.write("      {\"v\": \"" + str(place) + "\"},\n")
                    f.write("      {\"v\": \"" + result + "\"},\n")
                    f.write("      {\"v\": \"" + name + "\"},\n")
                    f.write("      {\"v\": \"" + year + "\"},\n")
                    f.write("      {\"v\": \"" + club + "\"},\n")
                    f.write("      {\"v\": \"" + city + "\"},\n")
                    f.write("      {\"v\": \"" + date + "\"},\n")
                    f.write("      {\"v\": \"" + notis + "\"}\n")
                    f.write("    ]}")
                    first = False
                    place += 1
f.close()

print "Concat DataOldSeasons.json and DeltaData.json into Data.json"
with open('data/Data.json','wb') as wfd:
    for f in ['data/DeltaData.json','data/DataOldSeasons.json']:
        with open(f,'rb') as fd:
            shutil.copyfileobj(fd, wfd)


