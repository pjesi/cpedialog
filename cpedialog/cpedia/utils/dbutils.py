# -*- coding: utf-8 -*-
from google.appengine.ext import db
from django.http import Http404

def get_filters(*filters):
    """Helper method for get_filtered."""
    if len(filters) % 2 == 1:
        raise ValueError('You must supply an even number of arguments!')
    return zip(filters[::2], filters[1::2])

def get_filtered(data, *filters):
    """Helper method for get_xxx_or_404."""
    for filter in get_filters(*filters):
        data.filter(*filter)
    return data

def get_object_or_404(model, *filters_or_key, **kwargs):
    if kwargs.get('key_name'):
        item = model.get_by_key_name(kwargs.get('key_name'))
    elif kwargs.get('id'):
        item = model.get_by_id(kwargs.get('id'))
    elif len(filters_or_key) > 1:
        item = get_filtered(model.all(), *filters_or_key).get()
    else:
        item = model.get(filters_or_key[0])
    if not item:
        raise Http404('Object does not exist!')
    return item

def get_list_or_404(model, filters):
    data = get_filtered(model.all(), *filters)
    if not data.get():
        raise Http404('No objects found!')
    return data

def generate_key_name(*values):
    """
    Escapes a string such that it can be used safely as a key_name.
    
    You can pass multiple values in order to build a path.
    """
    return 'k' + '/'.join([value.replace('%', '%1').replace('/', '%2')
                           for value in values])

def transaction(func):
    """Decorator that always runs the given function in a transaction."""
    def _transaction(*args, **kwargs):
        return db.run_in_transaction(func, *args, **kwargs)
    return _transaction

@transaction
def db_add(model, key_name, parent=None, **kwargs):
    """
    This function creates an object transactionally if it does not exist in
    the datastore. Otherwise it returns None.
    """
    existing = model.get_by_key_name(key_name)
    if not existing:
        new_entity = model(parent=parent, key_name=key_name, **kwargs)
        new_entity.put()
        return new_entity
    return None

class KeyReferenceProperty(object):
    """
    Creates a cached accessor for the object referenced by a string property
    that stores a str(key) or key_name. This is useful if you need to work with
    the key of a referenced object, but mustn't get() it from the datastore.
    """
    def __init__(self, name, model, use_key_name=True):
        self.name = name
        self.model = model
        self.use_key_name = use_key_name

    def __get__(self, instance, _):
        if instance is None:
            return self
        attr = getattr(instance, self.name)
        cache = getattr(instance, '_ref_cache_for_' + self.name, None)
        if not cache:
            cache_key = cache
        elif self.use_key_name:
            cache_key = cache.key().name()
        else:
            cache_key = str(cache.key())
        if attr != cache_key:
            if self.use_key_name:
                cache = self.model.get_by_key_name(attr)
            else:
                cache = self.model.get(attr)
            setattr(instance, '_ref_cache_for_' + self.name, cache)
        return cache
