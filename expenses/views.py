from django.db.models import Q
from django.views.generic import UpdateView
from django.views.generic.list import ListView

from .forms import ExpenseSearchForm
from .models import Expense, Category
from .reports import summary_per_category, total_amount_spend, summary_per_month


class ExpenseListView(ListView):
    model = Expense
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list

        form = ExpenseSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get('name', '').strip()
            date_from = form.cleaned_data.get('date_from')
            date_to = form.cleaned_data.get('date_to')
            categories = form.cleaned_data.get('categories')
            order_by = form.cleaned_data.get('order_by')

            filters = Q()

            if name:
                filters &= Q(name__icontains=name)

            if categories:
                filters &= Q(category__in=categories)

            if date_from and date_to:
                filters &= Q(date__gte=date_from, date__lte=date_to)
            elif date_from:
                filters &= Q(date__gte=date_from)
            elif date_to:
                filters &= Q(date__lte=date_to)

            queryset = queryset.filter(filters)

            if order_by:
                queryset = queryset.order_by(order_by)

        query_params = self.request.GET.copy()

        if 'page' in query_params:
            query_params.pop('page')

        search_params = query_params.urlencode()
        return super().get_context_data(
            form=form,
            object_list=queryset,
            summary_per_category=summary_per_category(queryset),
            search_params=search_params,
            current_url=self.request.path,
            total_amount_spend=total_amount_spend(queryset),
            summary_per_month=summary_per_month(queryset),
            **kwargs
        )


class CategoryListView(ListView):
    model = Category
    paginate_by = 5

