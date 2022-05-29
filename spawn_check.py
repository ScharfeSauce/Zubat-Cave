def spawn_check(group, offset): # kann für ander Gruppen, oder auch zukünftige Programme eingesetzt werden
    if len(group) > 1:
        list = group.sprites()
        for i in list:
            if i == list[len(group) - 1]:
                break
            if (list[len(group) - 1].rect.left - offset) < i.rect.right:          # Prüfung nach Zusammenstößen, mit einem variablen Sicherheitsabstand 
                if i.rect.left < (list[len(group) - 1].rect.right + offset):
                    if (list[len(group) - 1].rect.top - offset) < i.rect.bottom:
                        if i.rect.top < (list[len(group) - 1].rect.bottom + offset):
                            group.remove(list[len(group) - 1])