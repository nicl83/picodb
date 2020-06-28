from importlib import reload
import json
import time

with open("config.json") as config:
    refreshtime = json.load(config)["refreshtime"]

print (f"========== Welcome to picoDB, set to fresh every {refreshtime} seconds! ==========")


print ("===== Running sources to sources_to_picodbinfo =====\n")
import sources_to_picodbinfo

print ("\n===== Now running picodbinfo_to_html =====\n")
import picodbinfo_to_html

print ("\n===== Refreshed HTMl, waiting! =====\n")

time.sleep(refreshtime)

while True:
    print ("===== Running sources to sources_to_picodbinfo =====\n")
    reload(sources_to_picodbinfo)

    print ("\n===== Now running picodbinfo_to_html =====\n")
    reload(picodbinfo_to_html)

    print ("\n===== Refreshed HTMl, waiting! =====\n")

    with open("config.json") as config:
        refreshtime = json.load(config)["refreshtime"]

    time.sleep(refreshtime)