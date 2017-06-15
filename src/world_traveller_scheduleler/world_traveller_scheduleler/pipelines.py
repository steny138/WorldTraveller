# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
import time
import json
import logging
import leveldb
from unqlite import UnQLite
from scrapy.conf import settings

from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
from model import WorldViews, db_connect, create_tables
from scrapy.exceptions import NotConfigured

class WorldTravellerSchedulelerPipeline(object):
    def process_item(self, item, spider):
        review = WorldViews(**item)
        self.add_item_to_database(review)
        return item

    def add_item_to_database(self, db_item):
        session = self.Session()
        try:
            session.add(db_item)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def __init__(self):
        engine = db_connect()
        create_tables(engine)
        self.Session = sessionmaker(bind=engine)
        

class PostgrePipeline(object):
    """docstring for PostgrePipeline"""
    def process_item(self, item, spider):
        return item

class UnqlitePipeline(object):
    def process_item(self, item, spider):
        keyPrefix = 'views'
        
        try:
            records = self.db.collection(keyPrefix)
            if not records.exists():
                logging.info("%s records collection created." % keyPrefix)
                records.create()

            self.db.begin()
            records.store(dict(item), return_id=True)
            self.db.commit()
            
        except Exception, e:
            logging.warning(e)
            print e
            isOK = False
            for i in range(1, 10):
                logging.warning("1.catch database lock exception: %d" % i) 
                
                time.sleep(1)

                logging.warning("2.catch database lock exception: %d" % i) 
                self.db = UnQLite(settings['UNQLITE_PATH'], open_database=False)
                logging.warning("3.catch database lock exception: %d" % i) 
                try:
                    logging.warning("4.catch database lock exception: %d" % i) 
                    self.db.begin()
                    logging.warning("5.catch database lock exception: %d" % i) 
                    records.store(dict(item), return_id=True)
                    logging.warning("6.catch database lock exception: %d" % i) 
                    self.db.commit()
                    logging.warning("7.catch database lock exception: %d" % i) 
                except Exception as exc:
                    logging.warning("8.catch database lock exception: %d" % i) 
                    pass
                else:
                    logging.warning("9.catch database lock exception: %d" % i) 
                    isOK = True
                    break
            if not isOK:
                self.db.rollback()
        finally:
            logging.log(logging.INFO, 'Question added to Unqlite database!')
        return item
    def __init__(self):
        try:
            print "create pipeline"
            self.db = UnQLite(settings['UNQLITE_PATH'])
        except Exception, e:
            print "init: " 
            print e
            logging.warning(e)
