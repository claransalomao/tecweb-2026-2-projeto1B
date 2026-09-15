from django.shortcuts import render, redirect, get_object_or_404
from .models import Note, Tag


def _get_or_create_tag(tag_name):
    tag_name = (tag_name or '').strip()
    if not tag_name:
        return None
    tag, _ = Tag.objects.get_or_create(name=tag_name)
    return tag


def index(request):
    if request.method == 'POST':
        title = request.POST.get('titulo')
        content = request.POST.get('detalhes')
        tag = _get_or_create_tag(request.POST.get('tag'))
        # TAREFA: Utilize o title e content para criar um novo Note no banco de dados
        Note.objects.create(title=title, content=content, tag=tag)
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
        note.tag = _get_or_create_tag(request.POST.get('tag'))
        note.save()
        return redirect('index')
    else:
        return render(request, 'notes/edit.html', {'note': note})


def tags_list(request):
    all_tags = Tag.objects.all()
    return render(request, 'notes/tags_list.html', {'tags': all_tags})


def tag_detail(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    notes = tag.notes.all()
    return render(request, 'notes/tag_detail.html', {'tag': tag, 'notes': notes})