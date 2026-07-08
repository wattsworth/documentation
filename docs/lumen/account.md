# Account Settings

![Account Page](../images/lumen/account/account_page.png)

Access the Account Settings page by clicking the <span class="fa-button light-gray">my account</span> button on the page header.

## Account Details
The Account Details panel allows you to change your name, e-mail, and password.
Any changes require you to enter your current password.

## Installations

Installations are listed by row. Two status icons indicate whether the installation
is online and your permission level. The icon legend is below:


|  Icon      | Description                                       |
|:----------:|:------------------------------------------------- |
|<span class="green">:fontawesome-solid-circle:</span>  | Installation is online and accepting data queries |
|<span class="red">:fontawesome-solid-circle:</span>| Installation is offline (not available)           |
| :fontawesome-solid-user-shield:   | You have administrative priveleges                |
| :fontawesome-solid-user:  | You have owner priveleges                         |
| :fontawesome-solid-eye:  | You have viewer priveleges                        |

Installations where you are an admin or owner have a <span class="fa-button gray">Manage</span>
 button. Click this button open the Installation Settings page.

Add a new installation by clicking the <span class="fa-button blue">:fontawesome-solid-plus: New Installation</span> button. This will
display the **Add New Installation Dialog** shown below.

![New Installation](../images/lumen/account/new_installation.png){ width="400"}

You must have CLI access to the target node. Run the `joule master add lumen` command and when prompted
for the key use the value shown in the dialog. This ensures Lumen can only access Joule nodes where an
authorized user has granted access. You are automatically assigned admin rights to the newly added
installation.

## Saved Views

This panel lists your data views. Click the :fontawesome-solid-close: icon to delete a view.
Click the :fontawesome-solid-edit: icon to edit a view. This will open the **Edit Saved View
Dialog** shown below:

![Saved Data Views](../images/lumen/account/edit_view.png){ width="500"}

You may change the name, description and visibility of the view. You may not
change the thumbnail or any of the data associated with the view.

If **Set as Home View?** is checked this view will load automatically when you
open the web page. The home view is indicated by a :fontawesome-solid-home: icon next to the
view name.

If **Private?** is checked the view will only be available to you. Otherwise it
is available to any user with sufficient permissions on the associated
installations.

## Groups

Groups make it easier to manage installation permissions for a large  number of
users. This panel lists the groups you own. The :fontawesome-solid-bars: icon next to group
name opens up the group management menu. This menu allows you to edit the group,
add members, or remove the group.

**Edit Group**

This dialog allows you to change the name and description of the group. The
group name must be unique.

![Edit User Group](../images/lumen/account/edit_group.png){ width="400"}

**Add Users**

This dialog allows you to add members to the group. You may add a member three
different ways.

![Add User to User Group](../images/lumen/account/group_add_user.png){ width="400"}

* **pick an existing user or group**: If the user already has an
  account you can select their name from a drop down list.
* **invite a user by e-mail**: If the user does not have an account
  you may send them an e-mail invitation. The user will not appear
  in the list until they have accepted the invitation and created an
  account.
* **create a new user**: Create a new account manually

**Create a Group**

Click the <span class="fa-button blue">:fontawesome-solid-plus: New Group</span> button to create a new group. Provide a name and
description for the group and click <span class="fa-button blue">Save</span>. The group name must be unique.

![Create a User Group](../images/lumen/account/create_group.png){ width="400"}

Groups you are a member of are listed at the bottom of the panel. You may not
edit groups that you do not own.
