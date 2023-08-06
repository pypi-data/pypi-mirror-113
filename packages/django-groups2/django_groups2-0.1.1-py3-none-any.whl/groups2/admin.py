from django.contrib import admin
from .models import Group2, Group2Kind
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from django.template.response import TemplateResponse
from django.urls import path
from django.shortcuts import get_object_or_404
from . import forms
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _


class Group2KindAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code' )
    search_fields = ('name', )


class Group2Admin(TreeAdmin):
    list_display = ('id', 'name', 'code', 'kind' ,  'is_active', 'email', 'group' )
    list_filter = ('is_active', 'kind', )
    search_fields = ('name', 'code', 'email')
    form = movenodeform_factory(Group2)
    change_form_template = "groups2/admin/group2_change_form.html"
    actions = ['edit_users_action']

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('<int:pk>/edit_users/', self.edit_users, name='group2_edit_users'),
        ]
        return my_urls + urls

    @admin.action(description='Edit users')
    def edit_users_action(self, request, queryset):
        selected = list(queryset.values_list('pk', flat=True))
        if len(selected) > 1:
            messages.error(request, _('Select only one group'))
            return HttpResponseRedirect(request.path)
                
        return HttpResponseRedirect(reverse('admin:group2_edit_users', args=selected))

    def edit_users(self, request, pk):
        group2 = get_object_or_404(Group2, pk=pk)
        context = dict(
           self.admin_site.each_context(request),
        )

        if request.method == 'POST':
            form = forms.GroupUsersForm(request.POST, instance=group2.group)
            if form.is_valid():
                group = form.instance
                group.user_set.set(form.cleaned_data['users'])
                group.save()
                messages.success(request, _('Users saved'))
                return HttpResponseRedirect(reverse('admin:groups2_group2_change', args=(pk,)))
            context['form'] = form
        else:
            context['form'] = forms.GroupUsersForm(instance=group2.group, )
        
        opts = self.model._meta
        
        context['opts'] = opts
        context['group2'] = group2
        
        return TemplateResponse(request, "groups2/admin/edit_users.html", context)



admin.site.register(Group2Kind, Group2KindAdmin)
admin.site.register(Group2, Group2Admin)