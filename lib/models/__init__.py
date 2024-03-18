#!/usr/bin/env python3

import sqlite3

CONN = sqlite3.connect('restaurant.db')
CURSOR = CONN.cursor()