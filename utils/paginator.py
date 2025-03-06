

from apps.account.models import User
from apps.account.filters import AdminFilter

from django.core.paginator import Paginator

def _create_paginator(request,objects):
    get_copy = request.GET.copy()
    parameters = get_copy.pop('page', True) and get_copy.urlencode()
    paginator = Paginator(objects.qs, 100)    # Show 25 contacts per page.
    page_number = request.GET.get("page",1)
    page_obj = paginator.get_page(page_number)
    context={
        'pagination':page_obj,
        'parameters': parameters,
    }
    return context


# <label for="{{ form.images.id_for_label }}" class="form-label">Imágenes (1 o más)</label>
#               <div class="input-group ">
                
#                 <label class="input-group-text" for="{{form.images.id_for_label}}">
#                   <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class=" bi-image-fill" viewBox="0 0 16 16">
#                     <path d="M.002 3a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2h-12a2 2 0 0 1-2-2zm1 9v1a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V9.5l-3.777-1.947a.5.5 0 0 0-.577.093l-3.71 3.71-2.66-1.772a.5.5 0 0 0-.63.062zm5-6.5a1.5 1.5 0 1 0-3 0 1.5 1.5 0 0 0 3 0"/>
#                   </svg>
#                 </label>
#                 <input type="file" required name="images" accept="image/*" multiple class="form-control" id="{{form.images.id_for_label}}">
#               </div>
#               {% if form.images.errors %}
#               <div class="alert alert-danger mt-2">
#                   {% for error in form.images.errors %}
#                       {{ error }}
#                   {% endfor %}
#                 </div>
#               {% endif %} 