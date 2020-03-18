#!/usr/bin/python
#! -*- coding: utf-8 -*-

################################################################################
######
###
## Qbt Companion v0.1
##
## This code written for the "Qbt Companion" program
##
## This project is licensed with:
## GNU AFFERO GENERAL PUBLIC LICENSE
##
## Please refer to the LICENSE file locate in the root directory of this
## project or visit <https://www.gnu.org/licenses/agpl-3.0 for more
## information.
##
## THE COPYRIGHT HOLDERS PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY OF ANY
## KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE
## IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
## THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM IS WITH
## YOU. SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF ALL
## NECESSARY SERVICING, REPAIR OR CORRECTION.
##
## IN NO EVENT ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR
## CONVEYS THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES,
## INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING
## OUT OF THE USE OR INABILITY TO USE THE PROGRAM EVEN IF SUCH HOLDER OR OTHER
### PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
######
################################################################################


import json
import os
import pickle
import sqlite3
import sys
from datetime import datetime

import requests


class RequestError(Exception):
    pass


class DbAlreadyConnected(Exception):
    pass


class NoDatabaseConnected(Exception):
    pass


class RequestMixin:
    def login(self,url=None,credentials=None):
        url += "auth/login"
        response = requests.get(url, params=credentials)
        self.check_response(response)
        return response

    def check_response(self, response):
        if response.status_code == 200:
            return True
        else:
            raise RequestError

    def get_info(self,resp,url=None):
        if not url:
            url = self.url
        url += "torrents/info"
        cookies = resp.cookies
        response = requests.get(url, cookies=cookies)
        self.check_response(response)
        data = response.json()
        return data


class QueryMixin:

    def torrent_exists(self,table,field,value):
        row = self.select_where(table,field,value)
        if row: return True
        return False

    def log_timestamp(self,stamp):
        with SqlConnect(self.path) as cur:
            statement = f"INSERT INTO stamps VALUES (?)"
            cur.execute(statement,(stamp,))
        return

    def save_to_db(self,data,table_name):
        with SqlConnect(self.path) as cur:
            columns, values, params = self.get_save_values(data)
            stat = f"INSERT INTO {table_name} ({columns}) VALUES ({params})"
            cur.execute(stat,tuple(values))
        return

    def save_many_to_db(self,columns,commit_values,params,table_name):
        with SqlConnect(self.path) as cur:
            cmd = f"INSERT INTO {table_name} ({columns}) VALUES ({params})"
            cur.executemany(cmd,commit_values)
        return

    def select_rows(self,table):
        with SqlConnect(self.path) as cur:
            statement = f"SELECT * FROM {table}"
            r = cur.execute(statement)
            rows = r.fetchall()
        return rows

    def select_where(self,table,field,value):
        with SqlConnect(self.path) as cur:
            stmnt = f"SELECT * FROM {table} WHERE {field} == ?"
            r = cur.execute(stmnt,(value,))
            rows = r.fetchall()
        return rows

    def create_db_table(self,headers,table_name):
        with SqlConnect(self.path) as cur:
            statement = f"CREATE TABLE {table_name} ({headers})"
            cur.execute(statement)
        return


class SqlConnect:
    """ Context Manager Class for connection and cursor to the database """

    def __init__(self,path):
        self.path = path

    def __enter__(self):
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = sqlite3.Row
        self.curs = self.conn.cursor()
        return self.curs

    def __exit__(self,*args):
        self.conn.commit()
        self.curs.close()
        self.conn.close()
