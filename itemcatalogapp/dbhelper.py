#!/usr/bin/python
# Filename: dbhelper.py

# Import classes and dbsession
from itemcatalog.models import Category, Item
from users.models import User
from data import dbsession

from sqlalchemy import desc

###################
# Read ############
###################

# Categories ######
def getAllCategories():
	return dbsession.query(Category).all()

def getCategoryFromID(categoryID):
	return dbsession.query(Category).filter_by(id = categoryID).one()
	
def getCategoryUserFromID(categoryID):
	return dbsession.query(Category).join(Category.usertable).filter(Category.id == categoryID).one()

	
# Items ###########
def getItemFromID(item_id):
	return dbsession.query(Item).filter(Item.id == item_id).one()

def getItemsFromCategoryID(categoryID):
	return dbsession.query(Item).filter_by(category_id = categoryID).all()

def getItemsForHomePage(home_item_num):
	return dbsession.query(Item).join(Item.category).join(Item.usertable).order_by(desc(Item.insertDateTime)).limit(home_item_num).all()

def getItemsUserCategoryFromCategoryID(categoryID):
	return dbsession.query(Item).join(Item.category).join(Item.usertable).filter(Item.category_id == categoryID).all()

def getItemUserCategoryFromItemID(itemID):
	return dbsession.query(Item).join(Item.usertable).join(Item.category).filter(Item.id == itemID).one()


# Users ###########
def getUserFromEmail(user_email):
	return dbsession.query(User).filter_by(email = user_email).one()

def getUserFromID(user_id):
	return dbsession.query(User).filter_by(id = user_id).one()

	
###################
# Add #############
###################

def add(object):
	dbsession.add(object)
	dbsession.commit()

###################
# Delete ##########
###################

def delete(object):
	dbsession.delete(object)
	dbsession.commit()

def deleteNoCommit(object):
	dbsession.delete(object)

version = '0.1'

# End of dbhelper.py
