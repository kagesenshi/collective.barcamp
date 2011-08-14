Introduction
============

This is a full-blown functional test. The emphasis here is on testing what
the user may input and see, and the system is largely tested as a black box.
We use PloneTestCase to set up this test as well, so we have a full Plone site
to play with. We *can* inspect the state of the portal, e.g. using 
self.portal and self.folder, but it is often frowned upon since you are not
treating the system as a black box. Also, if you, for example, log in or set
roles using calls like self.setRoles(), these are not reflected in the test
browser, which runs as a separate session.

Being a doctest, we can tell a story here.

First, we must perform some setup. We use the testbrowser that is shipped
with Five, as this provides proper Zope 2 integration. Most of the 
documentation, though, is in the underlying zope.testbrower package.

    >>> from Products.Five.testbrowser import Browser
    >>> browser = Browser()
    >>> portal_url = self.portal.absolute_url()

The following is useful when writing and debugging testbrowser tests. It lets
us see all error messages in the error_log.

    >>> self.portal.error_log._ignored_exceptions = ()

With that in place, we can go to the portal front page and log in. We will
do this using the default user from PloneTestCase:

    >>> from Products.PloneTestCase.setup import portal_owner, default_password

Because add-on themes or products may remove or hide the login portlet, this test will use the login form that comes with plone.  

    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()

Here, we set the value of the fields on the login form and then simulate a
submit click.  We then ensure that we get the friendly logged-in message:

    >>> "You are now logged in" in browser.contents
    True

Finally, let's return to the front page of our site before continuing

    >>> browser.open(portal_url)

-*- extra stuff goes here -*-
The BarcampParticipant content type
===============================

In this section we are tesing the BarcampParticipant content type by performing
basic operations like adding, updadating and deleting BarcampParticipant content
items.

Adding a new BarcampParticipant content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'BarcampParticipant' and click the 'Add' button to get to the add form.

    >>> browser.getControl('BarcampParticipant').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'BarcampParticipant' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'BarcampParticipant Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'BarcampParticipant' content item to the portal.

Updating an existing BarcampParticipant content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New BarcampParticipant Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New BarcampParticipant Sample' in browser.contents
    True

Removing a/an BarcampParticipant content item
--------------------------------

If we go to the home page, we can see a tab with the 'New BarcampParticipant
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New BarcampParticipant Sample' in browser.contents
    True

Now we are going to delete the 'New BarcampParticipant Sample' object. First we
go to the contents tab and select the 'New BarcampParticipant Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New BarcampParticipant Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New BarcampParticipant
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New BarcampParticipant Sample' in browser.contents
    False

Adding a new BarcampParticipant content item as contributor
------------------------------------------------

Not only site managers are allowed to add BarcampParticipant content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'BarcampParticipant' and click the 'Add' button to get to the add form.

    >>> browser.getControl('BarcampParticipant').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'BarcampParticipant' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'BarcampParticipant Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new BarcampParticipant content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The BarcampSession content type
===============================

In this section we are tesing the BarcampSession content type by performing
basic operations like adding, updadating and deleting BarcampSession content
items.

Adding a new BarcampSession content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'BarcampSession' and click the 'Add' button to get to the add form.

    >>> browser.getControl('BarcampSession').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'BarcampSession' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'BarcampSession Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'BarcampSession' content item to the portal.

Updating an existing BarcampSession content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New BarcampSession Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New BarcampSession Sample' in browser.contents
    True

Removing a/an BarcampSession content item
--------------------------------

If we go to the home page, we can see a tab with the 'New BarcampSession
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New BarcampSession Sample' in browser.contents
    True

Now we are going to delete the 'New BarcampSession Sample' object. First we
go to the contents tab and select the 'New BarcampSession Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New BarcampSession Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New BarcampSession
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New BarcampSession Sample' in browser.contents
    False

Adding a new BarcampSession content item as contributor
------------------------------------------------

Not only site managers are allowed to add BarcampSession content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'BarcampSession' and click the 'Add' button to get to the add form.

    >>> browser.getControl('BarcampSession').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'BarcampSession' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'BarcampSession Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new BarcampSession content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The BarcampEvent content type
===============================

In this section we are tesing the BarcampEvent content type by performing
basic operations like adding, updadating and deleting BarcampEvent content
items.

Adding a new BarcampEvent content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'BarcampEvent' and click the 'Add' button to get to the add form.

    >>> browser.getControl('BarcampEvent').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'BarcampEvent' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'BarcampEvent Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'BarcampEvent' content item to the portal.

Updating an existing BarcampEvent content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New BarcampEvent Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New BarcampEvent Sample' in browser.contents
    True

Removing a/an BarcampEvent content item
--------------------------------

If we go to the home page, we can see a tab with the 'New BarcampEvent
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New BarcampEvent Sample' in browser.contents
    True

Now we are going to delete the 'New BarcampEvent Sample' object. First we
go to the contents tab and select the 'New BarcampEvent Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New BarcampEvent Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New BarcampEvent
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New BarcampEvent Sample' in browser.contents
    False

Adding a new BarcampEvent content item as contributor
------------------------------------------------

Not only site managers are allowed to add BarcampEvent content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'BarcampEvent' and click the 'Add' button to get to the add form.

    >>> browser.getControl('BarcampEvent').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'BarcampEvent' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'BarcampEvent Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new BarcampEvent content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)



