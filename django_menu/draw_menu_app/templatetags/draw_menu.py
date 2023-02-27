from django import template

from draw_menu_app.models import Item


register = template.Library()


@register.inclusion_tag('menu_tree.html', takes_context=True)
def draw_menu(context, menu):
    """
    Функция отрисовки древовидного меню.
    Принимает название таблицы.
    """
    all_menu_items = Item.objects.filter(menu__name=menu)
    items = []
    primary_menu_items = all_menu_items.filter(parent=None)

    chosen_menu_item_id = context['request'].GET.get(menu, None)
    if not chosen_menu_item_id:
        items = [item for item in primary_menu_items.values()]
    else:
        chosen_menu_item = all_menu_items.filter(id=int(chosen_menu_item_id)).first()
        ancestors_ids = get_ancestors_ids(all_menu_items, chosen_menu_item)
        for item in primary_menu_items:
            if item.id in ancestors_ids:
                item.child_items = get_childs(all_menu_items, item, ancestors_ids)
            items.append(item)

    menu_query = {
        'menu': menu,
        'items': items,
    }

    return menu_query


def get_ancestors_ids(all_menu_items, item):
    """
    Возвращает список ID всех предков полученного объекта.
    """
    ancestors_ids = [item.id, ]
    while item.parent:
        ancestors_ids.append(item.parent.id)
        item = all_menu_items.filter(id=item.parent.id).first()

    return ancestors_ids


def get_childs(all_menu_items, parent, ancestors_ids):
    """
    Возвращает список всех детей полученного объекта.
    Если эти дети в списке родителей - рекурсивно вызывает себя для поиска их детей.
    """
    child_items = []
    for item in all_menu_items.filter(parent=parent.id):
        if item.id in ancestors_ids:
            item.child_items = get_childs(all_menu_items, item, ancestors_ids)
        child_items.append(item)
    return child_items
