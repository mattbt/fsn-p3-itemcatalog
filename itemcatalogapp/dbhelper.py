#!/usr/bin/python
# Filename: dbhelper.py

# Import classes and dbsession
from itemcatalog.models import Category, Item
from users.models import User, Role
from data import dbsession#, user_datastore

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
	return dbsession.query(Category).join(Category.user).filter(Category.id == categoryID).one()

	
# Items ###########
def getItemFromID(item_id):
	return dbsession.query(Item).filter(Item.id == item_id).one()

def getItemsFromCategoryID(categoryID):
	return dbsession.query(Item).filter_by(category_id = categoryID).all()

def getItemsForHomePage(home_item_num):
	return dbsession.query(Item).join(Item.category).join(Item.user).order_by(desc(Item.insertDateTime)).limit(home_item_num).all()

def getItemsUserCategoryFromCategoryID(categoryID):
	return dbsession.query(Item).join(Item.category).join(Item.user).filter(Item.category_id == categoryID).all()

def getItemUserCategoryFromItemID(itemID):
	return dbsession.query(Item).join(Item.user).join(Item.category).filter(Item.id == itemID).one()


# Users ###########
def getAllUsers():
        return dbsession.query(User).all()

def getUserFromEmail(user_email):
	return dbsession.query(User).filter_by(email = user_email).one()

def getUserFromID(user_id):
	return dbsession.query(User).filter_by(id = user_id).one()


# Roles ###########
def getAllRoles():
	return dbsession.query(Role).all()

def getRoleFromKeyword(keyword):
	return dbsession.query(Role).filter_by(name=keyword).one()
	
def getRolesFromUserID(user_id):
        #return dbsession.query(Role).join(UserRoles.role_id).all()
        return dbsession.query(User).filter_by(id=user_id).first().roles

def addCustomRoles():
	add(Role(name='admin'))
	add(Role(name='company_admin'))
	add(Role(name='risk_owner'))
###################
# Add #############
###################

def add(obj):
	dbsession.add(obj)
	dbsession.commit()
	
def addUser(user):
        '''user_datastore.create_user(password=user.password,
                                   email=user.email,
                                   picture=user.picture,
                                   name=user.name
                                   )'''
        role = getRoleFromKeyword('admin')
	user.roles.append(role)
        dbsession.add(user)
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
