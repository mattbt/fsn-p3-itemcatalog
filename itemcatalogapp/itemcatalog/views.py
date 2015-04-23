import datetime
from flask import Blueprint, render_template, url_for, request, redirect
from flask import flash, jsonify

# Blueprint declaration
itemcatalogbp = Blueprint("itemcatalogbp", __name__)

# Import classes and dbhelper
from models import Category, Item
from .. import dbhelper

#session data: Flask-Login
from flask.ext.login import login_required, current_user 

# Import Forms
from .forms import CategoryForm, ItemForm

# decorators
from ..decorators import requires_roles

##################
# API endpoint ###
##################

@itemcatalogbp.route('/catalog.json')
def catalogJSON():
    categories = dbhelper.getAllCategories()
    return jsonify(Categories=[c.get_dict(items = dbhelper
                                          .getItemsFromCategoryID(c.id))
                               for c in categories])

				   
							   
##########
# Home ###
##########

@itemcatalogbp.route('/')
@itemcatalogbp.route('/catalog/')
def catalog():
    # number of last items to be displayed in homepage
    home_item_num = 9
    #print dbhelper.getRolesFromUserID(1)
    # render home page
    categories = dbhelper.getAllCategories()
    itemslist = dbhelper.getItemsForHomePage(home_item_num)
    return render_template('home.html', itemslist = itemslist,
                           categories = categories, categorySelected = None,
                           home_item_num = home_item_num)


################
# Categories ###
################

@itemcatalogbp.route('/catalog/new/', methods=['GET', 'POST'])
@login_required # no access if user not logged
@requires_roles('ad')
def categoryNew():

    # create form object
    category_form = CategoryForm()

    # if valid form submitted
    if category_form.validate_on_submit():  

        # get data from form
        name = category_form.name.data
        insertDateTime = datetime.datetime.now()

        # insert new Category
        newCategory = Category(name = name,
                               user_id = current_user.id,
                               insertDateTime = insertDateTime)
        dbhelper.add(newCategory)
        
        flash('New category %s inserted' % name)
        return redirect(url_for('.catalog'))
    else:
        # if GET or not valid POST request, simply render page
        categories = dbhelper.getAllCategories()
        return render_template('categorynew.html',
                               categories = categories,
                               categorySelected = None,
                               category_form = category_form)

@itemcatalogbp.route('/catalog/<int:category_id>/edit/', methods=['GET', 'POST'])
@login_required # no access if user not logged
def categoryEdit(category_id):
     
    # create form object
    category_form = CategoryForm()

    # if valid form submitted
    if category_form.validate_on_submit():

        # get Category from db and edit if data changed
        categorySelected = dbhelper.getCategoryFromID(category_id)
        if category_form.name.data:
            categorySelected.name = category_form.name.data
        dbhelper.add(categorySelected)
        
        flash('Category %s successfully modified' % categorySelected.name)
        return redirect(url_for('.categoryItems', category_id = category_id))
    else:
        # if GET or not valid POST request, simply render page
        # get data for page render
        categorySelected = dbhelper.getCategoryUserFromID(category_id)
        categoryFormObj = dbhelper.getCategoryFromID(category_id)
        categories = dbhelper.getAllCategories()
        category_form = CategoryForm(obj=categoryFormObj)
        return render_template('categoryedit.html',
                               categories = categories,
                               categorySelected = categorySelected,
                               category_form = category_form)

@itemcatalogbp.route('/catalog/<int:category_id>/delete/',
                     methods=['GET', 'POST'])
@login_required # no access if user not logged
def categoryDelete(category_id):     
    
    # create form object
    category_form = CategoryForm()

    # if valid form submitted
    if category_form.validate_on_submit():

        # delete selected Category and all children Items
        categorySelected = dbhelper.getCategoryFromID(category_id)
        categoryItems = dbhelper.getItemsFromCategoryID(category_id)
        name = categorySelected.name
        for categoryItem in categoryItems:
            dbhelper.deleteNoCommit(categoryItem)
        dbhelper.delete(categorySelected)
        
        flash('Category %s deleted' % name)
        return redirect(url_for('.catalog'))
    else:
        # if GET or not valid POST request, simply render page
        # get data for page render
        categorySelected = dbhelper.getCategoryUserFromID(category_id)
        categoryFormObj = dbhelper.getCategoryFromID(category_id)
        categories = dbhelper.getAllCategories()
        category_form = CategoryForm(obj=categoryFormObj)
        return render_template('categorydelete.html',
                               categories = categories,
                               categorySelected = categorySelected,
                               category_form = category_form)
        
@itemcatalogbp.route('/catalog/<int:category_id>/')
@itemcatalogbp.route('/catalog/<int:category_id>/items/')
def categoryItems(category_id):
    categories = dbhelper.getAllCategories()
    categorySelected = dbhelper.getCategoryFromID(category_id)
    itemsFilteredList = dbhelper.getItemsUserCategoryFromCategoryID(category_id)
    return render_template('categorypage.html',
                           categories = categories,
                           categorySelected = categorySelected,
                           itemslist = itemsFilteredList)


###########
# Items ###
###########

@itemcatalogbp.route('/catalog/<int:category_id>/new/', methods=['GET', 'POST'])
@login_required # no access if user not logged
def categoryNewItem(category_id):

    # create form object
    item_form = ItemForm()
    categories = dbhelper.getAllCategories()
    item_form.category_id.choices = [(c.id, c.name) for c in categories]

    # if valid form submitted
    if item_form.validate_on_submit():  

        # get data from form
        name = item_form.name.data
        category_id = item_form.category_id.data 
        description = item_form.description.data 
        insertDateTime = datetime.datetime.now()

        # create and add new Item
        newItem = Item(name = name,
                       category_id = category_id,
                       description = description,
                       user_id = current_user.id,
                       insertDateTime = insertDateTime)
        dbhelper.add(newItem)

        flash('New item %s inserted' % name)
        return redirect(url_for('.categoryItems', category_id = category_id))
    else:
        # if GET or not valid POST request, simply render page
        categorySelected = None
        # if adding from a category page, preselect category from dropdown
        if (0 != category_id):
            categorySelected = dbhelper.getCategoryFromID(category_id)
            item_form.category_id.default = category_id
            item_form.process()
                
        return render_template('itemnew.html', categories = categories,
                               categorySelected = categorySelected,
                               item_form=item_form)

@itemcatalogbp.route('/catalog/<int:category_id>/items/<int:item_id>/')
def itemDetail(category_id, item_id):
    categories = dbhelper.getAllCategories()
    itemSelected = dbhelper.getItemUserCategoryFromItemID(item_id)
    categorySelected = dbhelper.getCategoryFromID(category_id)
    return render_template('itemdetailpage.html',
                           categories = categories,
                           categorySelected = categorySelected,
                           itemSelected = itemSelected)

@itemcatalogbp.route('/catalog/<int:category_id>/items/<int:item_id>/edit',
                     methods=['GET', 'POST'])
@login_required # no access if user not logged
def itemEdit(category_id, item_id):

    # create form object
    item_form = ItemForm()
    categories = dbhelper.getAllCategories()
    item_form.category_id.choices = [(c.id, c.name) for c in categories]

    ## print item_form.data
    # if valid form submitted
    if item_form.validate_on_submit():

        # get Item from db and edit if data changed
        itemSelected = dbhelper.getItemFromID(item_id)
        if item_form.name.data :
            itemSelected.name = item_form.name.data 
        if item_form.category_id.data:
            itemSelected.category_id = item_form.category_id.data
        if item_form.description.data:
            itemSelected.description = item_form.description.data

        dbhelper.add(itemSelected)
        flash('Item %s successfully modified' % itemSelected.name)
        return redirect(url_for('.itemDetail',
                                category_id = itemSelected.category_id,
                                item_id = itemSelected.id))
    else:
        # if GET or not valid POST request, simply render page
        # get data for page render
        itemSelected = dbhelper.getItemUserCategoryFromItemID(item_id)
        categories = dbhelper.getAllCategories()
        categorySelected = dbhelper.getCategoryFromID(category_id)

        # prepopulate form
        itemFormObj = dbhelper.getItemFromID(item_id)
        item_form = ItemForm(obj=itemFormObj)
        item_form.category_id.choices = [(c.id, c.name) for c in categories]
                
                 
        return render_template('itemedit.html', categories = categories,
                               categorySelected = categorySelected,
                               itemSelected = itemSelected,
                               item_form = item_form)

@itemcatalogbp.route('/catalog/<int:category_id>/items/<int:item_id>/delete',
                     methods=['GET', 'POST'])
@login_required # no access if user not logged
def itemDelete(category_id, item_id):

    # create form object
    item_form = ItemForm()
    categories = dbhelper.getAllCategories()
    item_form.category_id.choices = [(c.id, c.name) for c in categories]

    # if valid form submitted
    if item_form.validate_on_submit():     

        # get and delete selected Item
        itemSelected = dbhelper.getItemFromID(item_id)
        name = itemSelected.name
        dbhelper.delete(itemSelected)
        
        flash('Item %s deleted' % name)
        return redirect(url_for('.categoryItems', category_id = category_id))
    else:
        # if GET or not valid POST request, simply render page
        # get data for page render
        itemSelected = dbhelper.getItemUserCategoryFromItemID(item_id)
        categories = dbhelper.getAllCategories()
        categorySelected = dbhelper.getCategoryFromID(category_id)

        # prepopulate form
        itemFormObj = dbhelper.getItemFromID(item_id)
        item_form = ItemForm(obj=itemFormObj)
        item_form.category_id.choices = [(c.id, c.name) for c in categories]
                
        return render_template('itemdelete.html',
                               categories = categories,
                               categorySelected = categorySelected,
                               itemSelected = itemSelected,
                               item_form = item_form)
