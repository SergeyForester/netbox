import django_filters
from django.db.models import Q

from extras.filters import CustomFieldModelFilterSet, CreatedUpdatedFilterSet
from utilities.filters import BaseFilterSet, NameSlugSearchFilterSet, TagFilter, TreeNodeMultipleChoiceFilter
from .models import Tenant, TenantGroup, Supervisor

__all__ = (
    'TenancyFilterSet',
    'TenantFilterSet',
    'TenantGroupFilterSet',
    'SupervisorFilterSet'
)


class TenantGroupFilterSet(BaseFilterSet, NameSlugSearchFilterSet):
    parent_id = django_filters.ModelMultipleChoiceFilter(
        queryset=TenantGroup.objects.all(),
        label='Tenant group (ID)',
    )
    parent = django_filters.ModelMultipleChoiceFilter(
        field_name='parent__slug',
        queryset=TenantGroup.objects.all(),
        to_field_name='slug',
        label='Tenant group group (slug)',
    )

    class Meta:
        model = TenantGroup
        fields = ['id', 'name', 'slug', 'description']


class TenantFilterSet(BaseFilterSet, CustomFieldModelFilterSet, CreatedUpdatedFilterSet):
    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )
    group_id = TreeNodeMultipleChoiceFilter(
        queryset=TenantGroup.objects.all(),
        field_name='group',
        lookup_expr='in',
        label='Tenant group (ID)',
    )
    group = TreeNodeMultipleChoiceFilter(
        queryset=TenantGroup.objects.all(),
        field_name='group',
        lookup_expr='in',
        to_field_name='slug',
        label='Tenant group (slug)',
    )
    tag = TagFilter()

    class Meta:
        model = Tenant
        fields = ['id', 'name', 'slug']

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(slug__icontains=value) |
            Q(description__icontains=value) |
            Q(comments__icontains=value)
        )


class TenancyFilterSet(django_filters.FilterSet):
    """
    An inheritable FilterSet for models which support Tenant assignment.
    """
    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )

    tenant_group_id = TreeNodeMultipleChoiceFilter(
        queryset=TenantGroup.objects.all(),
        field_name='tenant__group',
        lookup_expr='in',
        label='Tenant Group (ID)',
    )
    tenant_group = TreeNodeMultipleChoiceFilter(
        queryset=TenantGroup.objects.all(),
        field_name='tenant__group',
        to_field_name='slug',
        lookup_expr='in',
        label='Tenant Group (slug)',
    )
    tenant_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Tenant.objects.all(),
        label='Tenant (ID)',
    )
    tenant = django_filters.ModelMultipleChoiceFilter(
        queryset=Tenant.objects.all(),
        field_name='tenant__slug',
        to_field_name='slug',
        label='Tenant (slug)',
    )

    slug = django_filters.TreeNodeMultipleChoiceFilter(
        queryset=Supervisor.objects.all(),
        field_name='slug',
        lookup_expr='in',
        label='Supervisor (Slug)',
    )


class SupervisorFilterSet(django_filters.FilterSet):
    """
    An inheritable FilterSet for models which support Tenant assignment.
    """
    tenant_group_id = TreeNodeMultipleChoiceFilter(
        queryset=TenantGroup.objects.all(),
        field_name='tenant__group',
        lookup_expr='in',
        label='Tenant Group (ID)',
    )
    tenant_group = TreeNodeMultipleChoiceFilter(
        queryset=TenantGroup.objects.all(),
        field_name='tenant__group',
        to_field_name='slug',
        lookup_expr='in',
        label='Tenant Group (slug)',
    )
    tenant_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Tenant.objects.all(),
        label='Tenant (ID)',
    )
    tenant = django_filters.ModelMultipleChoiceFilter(
        queryset=Tenant.objects.all(),
        field_name='tenant__slug',
        to_field_name='slug',
        label='Tenant (slug)',
    )

