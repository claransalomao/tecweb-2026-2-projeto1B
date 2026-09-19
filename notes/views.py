from django.shortcuts import render, redirect, get_object_or_404
from .models import Note, Tag


def _parse_tags(tags_text):
    names = [name.strip() for name in (tags_text or '').split(',')]
    tags = []
    seen = set()
    for name in names:
        if not name or name in seen:
            continue
        seen.add(name)
        tag, _ = Tag.objects.get_or_create(name=name)
        tags.append(tag)
    return tags


def index(request):
    if request.method == 'POST':
        title = request.POST.get('titulo')
        content = request.POST.get('detalhes')
        # TAREFA: Utilize o title e content para criar um novo Note no banco de dados
        note = Note.objects.create(title=title, content=content)
        note.tags.set(_parse_tags(request.POST.get('tags')))
        return redirect('index')
    else:
        all_notes = Note.objects.all()
        return render(request, 'notes/index.html', {'notes': all_notes})


def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    note.delete()
    return redirect('index')


def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if request.method == 'POST':
        note.title = request.POST.get('titulo')
        note.content = request.POST.get('detalhes')
        note.save()
        note.tags.set(_parse_tags(request.POST.get('tags')))
        return redirect('index')
    else:
        tags_text = ', '.join(tag.name for tag in note.tags.all())
        return render(request, 'notes/edit.html', {'note': note, 'tags_text': tags_text})


def tags_list(request):
    all_tags = Tag.objects.all()
    return render(request, 'notes/tags_list.html', {'tags': all_tags})


def tag_detail(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    notes = tag.notes.all()
    return render(request, 'notes/tag_detail.html', {'tag': tag, 'notes': notes})