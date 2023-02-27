from django import template

from draw_menu_app.models import Item


register = template.Library()


@register.inclusion_tag('menu_tree.html', takes_context=True)
def draw_menu(context, menu):
    all_menu_items = Item.objects.filter(menu__name=menu)
    items = []
    primary_menu_items = all_menu_items.filter(parent=None)

    chosen_menu_item_id = context['request'].GET.get(menu, None)
    if not chosen_menu_item_id:
        items = [item for item in primary_menu_items.values()]
    else:
        chosen_menu_item = all_menu_items.filter(id=int(chosen_menu_item_id)).first()
        ancestors_ids = get_ancestors_ids(all_menu_items, chosen_menu_item)
        print('!!!ancestors_ids', ancestors_ids)
        all_family_childs = all_menu_items.filter(parent__in=ancestors_ids)
        print('!!!all_family_childs', all_family_childs)
        # for parent in all_menu_items.filter(id__in=ancestors_ids):
        #     parent.child_items = [item for item in all_menu_items.filter(parent=parent.id)]
        #     print('!!!parent.child_items', parent.child_items)
        #     items.append(parent)
        for item in primary_menu_items:
            if item.id in ancestors_ids:
                item.child_items = get_childs(all_menu_items, item, ancestors_ids)
            items.append(item)

    menu_query = {
        'menu': menu,
        'items': items,
        # 'child_items': [item for item in all_family_childs.values()],
    }

    return menu_query


def get_ancestors_ids(all_menu_items, item):
    ancestors_ids = [item.id, ]
    # parent = item.parent
    # print('!!!parent', parent)
    #
    # while parent:
    #     ancestors_ids.append(parent)
    #     print('!!!ancestors_ids.append(parent)', ancestors_ids)
    #     # parent = parent.parent
    #     parent = all_menu_items.filter(id=parent).first().parent
    while item.parent:
        ancestors_ids.append(item.parent.id)
        print('!!!ancestors_ids.append(item.parent)', ancestors_ids)
        item = all_menu_items.filter(id=item.parent.id).first()

    return ancestors_ids


def get_childs(all_menu_items, parent, ancestors_ids):
    # child_items = [item for item in all_menu_items.filter(parent=parent.id)]
    child_items = []
    for item in all_menu_items.filter(parent=parent.id):
        if item.id in ancestors_ids:
            item.child_items = get_childs(all_menu_items, item, ancestors_ids)
        child_items.append(item)
    return child_items
