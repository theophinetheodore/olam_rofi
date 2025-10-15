#!/bin/python3

import sqlite3
import subprocess
import sys
import os

theme_file = os.path.dirname(os.path.realpath(__file__)) + '/' + 'theme.rasi'

def query_word():
    search_query = subprocess.run(['rofi', '-dmenu', '-p', 'ഓളം', '-l', '0', '-theme', theme_file], stdout=subprocess.PIPE, text=True).stdout.strip()
    return search_query

def show_meanings(formatted):
    subprocess.run(['rofi', '-markup', '-theme', theme_file, '-e', formatted])

def return_search_results(conn, word):
    cursor = conn.cursor()

    query = """
    SELECT 
    CONCAT(
        CASE 
            WHEN types = '{-}' THEN "-"
            WHEN types = '{n}' THEN '<b>നാമം</b>'
            WHEN types = '{v}' THEN '<b>ക്രിയ</b>'
            WHEN types = '{a}' THEN '<b>വിശേഷണം</b>'
            WHEN types = '{idm}' THEN '<b>ഭാഷാശൈലി</b>'
            WHEN types = '{phr}' THEN '<b>ഉപവാക്യം</b>'
            WHEN types = '{adv}' THEN '<b>ക്രിയാവിശേഷണം</b>'
            WHEN types = '{prep}' THEN '<b>ഉപസര്‍ഗം</b>'
            WHEN types = '{conj}' THEN '<b>അവ്യയം</b>'
            WHEN types = '{abbr}' THEN '<b>സംക്ഷേപം</b>'
            WHEN types = '{propn}' THEN '<b>സംജ്ഞാനാമം</b>'
            WHEN types = '{interj}' THEN '<b>വ്യാക്ഷേപകം</b>'
            WHEN types = '{phrv}' THEN '<b>ഉപവാക്യ ക്രിയ</b>'
            WHEN types = '{pron}' THEN '<b>സര്‍വ്വനാമം</b>'
            WHEN types = '{auxv}' THEN '<b>പൂരകകൃതി</b>'
            WHEN types = '{pfx}' THEN '<b>പൂർവ്വപ്രത്യയം</b>'
            WHEN types = '{sfx}' THEN '<b>പ്രത്യയം</b>'
            ELSE types 
        END, 
        ': ', 
        GROUP_CONCAT(to_content, ', ')
    ) AS formatted_output
    FROM 
        dictionary
    WHERE 
        lower(from_content) = lower(?)
    GROUP BY 
        types;
    """

    cursor.execute(query, (word,))
    results = cursor.fetchall()

    text = []
    text.append(f"<span size='xx-large' weight='bold'>{word}</span>")
    text.append("")

    if len(results) != 0:
        for result in results:
                text.append(f"• {result[0]}")
    else:
        text.append("നിങ്ങള്‍ അന്വേഷിച്ച പദത്തിന്റെ അർത്ഥം കണ്ടെത്താനായില്ല.")

    text.append("")

    formatted = '\n'.join(text)

    return formatted

def main():
    conn = sqlite3.connect(os.path.dirname(os.path.realpath(__file__)) + '/' + 'olam.db')

    word = sys.argv[1] if len(sys.argv) != 1 else query_word()

    if word != "":
        meanings = return_search_results(conn, word)
        show_meanings(meanings)

    conn.close()

if __name__ == "__main__":
    main()
