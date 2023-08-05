from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from treebeard.mp_tree import MP_Node
from django.contrib.auth.models import Group


class Group2Kind(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'),  )
    code = models.CharField(max_length=64, unique=True, blank=True, null=True, help_text=_('Optional field to add an organization-specific code in addition to the name'))

    class Meta:
        verbose_name = _('Group Kind')
        verbose_name_plural = _('Group Kinds')

    def __str__(self):
        return self.name


class Group2(MP_Node):
    name = models.CharField(max_length=255, verbose_name=_('Name'),  )
    code = models.CharField(max_length=64, unique=True, blank=True, null=True, help_text=_('Optional field to add an organization-specific code in addition to the name'))

    kind = models.ForeignKey('Group2Kind' , verbose_name= _('Kind',), on_delete=models.PROTECT )
    is_active = models.BooleanField(default=True, help_text=_('Unselect this if the Group2 is not active any more'))
    email = models.EmailField(verbose_name= _('Email',), blank=True, null=True, )
    group = models.OneToOneField("auth.Group", editable=False, on_delete=models.CASCADE)
    
    node_order_by = ['name']

    class Meta:
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not hasattr(self, 'group') or self.group is None:
            self.group = Group.objects.create(name=self.name)
        super().save(*args, **kwargs)

