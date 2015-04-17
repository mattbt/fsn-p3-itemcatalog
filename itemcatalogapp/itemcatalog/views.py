import datetime
from flask import Blueprint, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy import desc

# Blueprint declaration
itemcatalogbp = Blueprint("itemcatalogbp", __name__)

# Import classes and dbsession
from models import Category, Item, User
from ..data import dbsession

# Import session data
from ..users.views import login_session

# Import Forms
from .forms import CategoryForm, ItemForm


#API endpoint
@itemcatalogbp.route('/catalog.json')
def catalogJSON():
        categories = dbsession.query(Category).all()
        return jsonify(Categories=[c.get_dict(items = dbsession.query(Item).filter_by(category_id=c.id).all()) for c in categories])


#routing
@itemcatalogbp.route('/')
@itemcatalogbp.route('/catalog/')
def catalog():
        # number of last items to be displayed in homepage
        home_item_num = 9

        # render home page
        categories = dbsession.query(Category).all()
        itemslist = dbsession.query(Item).join(Item.category).join(Item.usertable).order_by(desc(Item.insertDateTime)).limit(home_item_num).all()
	return render_template('home.html', itemslist = itemslist, categories = categories, categorySelected = None, home_item_num = home_item_num)


################
# Categories ###
################

@itemcatalogbp.route('/catalog/new/', methods=['GET', 'POST'])
def categoryNew():

        # no access if user not logged
        if 'username' not in login_session:
		return redirect('/login')

        # create form object
	category_form = CategoryForm()

        # if valid form submitted
	if category_form.validate_on_submit():	

                # get data from form
                name = category_form.name.data
                insertDateTime = datetime.datetime.now()

                # insert new Category
		newCategory = Category(name = name, user_id = login_session['user_id'], insertDateTime = insertDateTime)
		dbsession.add(newCategory)
		dbsession.commit()
		flash('New category %s inserted' % name)
		return redirect(url_for('.catalog'))
        else:
                # if GET or not valid POST request, simply render page
                categories = dbsession.query(Category).all()
                return render_template('categorynew.html', categories = categories, categorySelected = None, category_form = category_form)

@itemcatalogbp.route('/catalog/<int:category_id>/edit/', methods=['GET', 'POST'])
def categoryEdit(category_id):

        # no access if user not logged
        if 'username' not in login_session:
		return redirect('/login')

        # create form object
        category_form = CategoryForm()

        # if valid form submitted
        if category_form.validate_on_submit():

                # get Category from db and edit if data changed
                categorySelected = dbsession.query(Category).filter_by(id = category_id).one()
                if category_form.name.data:
                        categorySelected.name = category_form.name.data
		dbsession.add(categorySelected)
		dbsession.commit()
		flash('Category %s successfully modified' % categorySelected.name)
		return redirect(url_for('.categoryItems', category_id = category_id))
        else:
                # if GET or not valid POST request, simply render page
                # get data for page render
                categorySelected = dbsession.query(Category, User).join(User).filter(Category.id == category_id).one()
                categoryFormObj = dbsession.query(Category).filter(Category.id == category_id).one()
                categories = dbsession.query(Category).all()
                category_form = CategoryForm(obj=categoryFormObj)
                return render_template('categoryedit.html', categories = categories, categorySelected = categorySelected, category_form = category_form)

@itemcatalogbp.route('/catalog/<int:category_id>/delete/', methods=['GET', 'POST'])
def categoryDelete(category_id):     

        # no access if user not logged
        if 'username' not in login_session:
		return redirect('/login')

        # create form object
        category_form = CategoryForm()

        # if valid form submitted
        if category_form.validate_on_submit():

                # delete selected Category and all children Items
                categorySelected = dbsession.query(Category).filter_by(id = category_id).one()
                categoryItems = dbsession.query(Item).filter_by(category_id = category_id).all()
                name = categorySelected.name
                for categoryItem in categoryItems:
                        dbsession.delete(categoryItem)
		dbsession.delete(categorySelected)
		dbsession.commit()
		flash('Category %s deleted' % name)
		return redirect(url_for('.catalog'))
        else:
                # if GET or not valid POST request, simply render page
                # get data for page render
                categorySelected = dbsession.query(Category, User).join(User).filter(Category.id == category_id).one()
                categories = dbsession.query(Category).all()
                categoryFormObj = dbsession.query(Category).filter(Category.id == category_id).one()
                category_form = CategoryForm(obj=categoryFormObj)
                return render_template('categorydelete.html', categories = categories, categorySelected = categorySelected, category_form = category_form)
        
@itemcatalogbp.route('/catalog/<int:category_id>/')
@itemcatalogbp.route('/catalog/<int:category_id>/items/')
def categoryItems(category_id):
        categories = dbsession.query(Category).all()
        categorySelected = dbsession.query(Category).filter_by(id = category_id).one()
        itemsFilteredList = dbsession.query(Item).join(Item.category).join(Item.usertable).filter(Item.category_id == category_id).all()
        return render_template('categorypage.html', categories = categories, categorySelected = categorySelected, itemslist = itemsFilteredList)


###########
# Items ###
###########

@itemcatalogbp.route('/catalog/<int:category_id>/new/', methods=['GET', 'POST'])
def categoryNewItem(category_id):

        # no access if user not logged
        if 'username' not in login_session:
		return redirect('/login')

        # create form object
        item_form = ItemForm()
        categories = dbsession.query(Category).all()
        item_form.category_id.choices = [(c.id, c.name) for c in categories]

        # if valid form submitted
        if item_form.validate_on_submit():	

                # get data from form
                name = item_form.name.data
                print item_form.category_id.data
                category_id = item_form.category_id.data 
                description = item_form.description.data 
                insertDateTime = datetime.datetime.now()

                # create and add new Item
		newItem = Item(name = name, category_id = category_id, description = description, user_id = login_session['user_id'], insertDateTime = insertDateTime)
		dbsession.add(newItem)
		dbsession.commit()

		flash('New item %s inserted' % name)
		return redirect(url_for('.categoryItems', category_id = category_id))
        else:
                # if GET or not valid POST request, simply render page
                categorySelected = None
                # if adding from a category page, preselect category from dropdown
                if (0 != category_id):
                       categorySelected = dbsession.query(Category).filter_by(id = category_id).one()
                       item_form.category_id.default = category_id
                       item_form.process()
                
                return render_template('itemnew.html', categories = categories, categorySelected = categorySelected, item_form=item_form)

@itemcatalogbp.route('/catalog/<int:category_id>/items/<int:item_id>/')
def itemDetail(category_id, item_id):
        categories = dbsession.query(Category).all()
        itemSelected = dbsession.query(Item).join(Item.usertable).join(Item.category).filter(Item.id == item_id).one()
        categorySelected = dbsession.query(Category).filter_by(id = category_id).one()
        return render_template('itemdetailpage.html', categories = categories, categorySelected = categorySelected, itemSelected = itemSelected)

@itemcatalogbp.route('/catalog/<int:category_id>/items/<int:item_id>/edit', methods=['GET', 'POST'])
def itemEdit(category_id, item_id):

        # no access if user not logged
        if 'username' not in login_session:
		return redirect('/login')

        # create form object
        item_form = ItemForm()
        categories = dbsession.query(Category).all()
        item_form.category_id.choices = [(c.id, c.name) for c in categories]

        ## print item_form.data
        # if valid form submitted
        if item_form.validate_on_submit():

                # get Item from db and edit if data changed
                itemSelected = dbsession.query(Item).filter(Item.id == item_id).one()
                if item_form.name.data :
                        itemSelected.name = item_form.name.data 
                if item_form.category_id.data:
                        itemSelected.category_id = item_form.category_id.data
                if item_form.description.data:
                        itemSelected.description = item_form.description.data

		dbsession.add(itemSelected)
		dbsession.commit()
		flash('Item %s successfully modified' % itemSelected.name)
		return redirect(url_for('.itemDetail', category_id = itemSelected.category_id, item_id = itemSelected.id))
        else:
                # if GET or not valid POST request, simply render page
                # get data for page render
                itemSelected = dbsession.query(Item).join(Item.category).join(Item.usertable).filter(Item.id == item_id).one()
                categories = dbsession.query(Category).all()
                categorySelected = dbsession.query(Category).filter_by(id = category_id).one()

                # prepopulate form
                itemFormObj = dbsession.query(Item).filter(Item.id == item_id).one()
                item_form = ItemForm(obj=itemFormObj)
                item_form.category_id.choices = [(c.id, c.name) for c in categories]
                
                 
                return render_template('itemedit.html', categories = categories, categorySelected = categorySelected, itemSelected = itemSelected, item_form = item_form)

@itemcatalogbp.route('/catalog/<int:category_id>/items/<int:item_id>/delete', methods=['GET', 'POST'])
def itemDelete(category_id, item_id):

        # no access if user not logged
        if 'username' not in login_session:
		return redirect('/login')

        # create form object
        item_form = ItemForm()
        categories = dbsession.query(Category).all()
        item_form.category_id.choices = [(c.id, c.name) for c in categories]

        # if valid form submitted
        if item_form.validate_on_submit():     

                # get and delete selected Item
                itemSelected = dbsession.query(Item).filter(Item.id == item_id).one()
                name = itemSelected.name
		dbsession.delete(itemSelected)
		dbsession.commit()
		flash('Item %s deleted' % name)
		return redirect(url_for('.categoryItems', category_id = category_id))
        else:
                # if GET or not valid POST request, simply render page
                # get data for page render
                itemSelected = dbsession.query(Item).join(Item.category).join(Item.usertable).filter(Item.id == item_id).one()
                categories = dbsession.query(Category).all()
                categorySelected = dbsession.query(Category).filter_by(id = category_id).one()

                # prepopulate form
                itemFormObj = dbsession.query(Item).filter(Item.id == item_id).one()
                item_form = ItemForm(obj=itemFormObj)
                item_form.category_id.choices = [(c.id, c.name) for c in categories]
                
                return render_template('itemdelete.html', categories = categories, categorySelected = categorySelected, itemSelected = itemSelected, item_form = item_form)
