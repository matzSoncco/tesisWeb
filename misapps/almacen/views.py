from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.forms import inlineformset_factory
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.db import IntegrityError, models
from datetime import datetime
import json
import logging
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models.Ppe import Ppe
from .models.PpeLoan import PpeLoan
from .models.Equipment import Equipment
from .models.Worker import Worker
from .models.Material import Material
from .models.Loan import Loan
from .models.Tool import Tool
from .models.History import History
<<<<<<< HEAD
from .forms import AdminSignUpForm, PpeForm, MaterialForm, WorkerForm, EquipmentForm, ToolForm, LoanForm, PpeLoanForm, Ppe, ExceptionPpeLoanForm, PpeLoanDetailForm, PpeLoanDetailForm, CreatePpeForm, CreateMaterialForm, CreateToolForm
=======
from .forms import AdminSignUpForm, PpeForm, MaterialForm, WorkerForm, EquipmentForm, ToolForm, LoanForm, PpeLoanForm, Ppe, CreatePpeForm, CreateMaterialForm, CreateEquipentForm, CreateToolForm
>>>>>>> 67c854784d2b52e13464667c66c07171771f41ed

logger = logging.getLogger(__name__)

# Create your views here.
def home(request):
    return render(request, 'home.html')

#DURACIÓN
@login_required
def set_duration(request):
    form = PpeForm()
    return render(request, 'show_duration_table.html', {'form': form})

def cost_summary_view(request):
    epp_items = Ppe.objects.all()
    tool_items = Tool.objects.all()
    equip_items = Equipment.objects.all()
    mat_items = Material.objects.all()

    for item in epp_items:
        item.save()
    for item in tool_items:
        item.save()
    for item in equip_items:
        item.save()
    for item in mat_items:
        item.save()

    all_items = list(epp_items) + list(tool_items) + list(equip_items) + list(mat_items)
    
    final_total_cost = sum(item.totalCost for item in all_items)
    total_ppe_cost = sum(item.totalCost for item in epp_items)
    total_tool_cost = sum(item.totalCost for item in tool_items)
    total_equip_cost = sum(item.totalCost for item in equip_items)
    total_mat_cost = sum(item.totalCost for item in mat_items)

    context = {
        'all_items': all_items,
        'finalTotalCost': final_total_cost,
        'totalPpeCost': total_ppe_cost,
        'totalToolCost': total_tool_cost,
        'totalEquipCost': total_equip_cost,
        'totalMatCost': total_mat_cost
    }

    return render(request, 'total_cost_table.html', context)

@login_required
def show_duration(request):
    query = request.GET.get('q', '')
    if query:
        epp = Ppe.objects.filter(name__icontains=query)
    else:
        epp = Ppe.objects.all()
    return render(request, 'table_duration_ppe.html', {'epp': epp, 'query': query})

@require_POST
def update_ppe_duration(request):
    ppe_id = request.POST.get('ppe_id')
    new_duration = request.POST.get('duration')
    
    ppe = get_object_or_404(Ppe, idPpe=ppe_id)
    ppe.duration = new_duration
    ppe.save()
    
    return JsonResponse({'success': True})

#PPE
@login_required
def PersonalProtectionEquipment(request):
    query = request.GET.get('q', '')
    if query:
        epp = Ppe.objects.filter(name__icontains=query)
    else:
        epp = Ppe.objects.all()
    
    context = {'epp': epp, 'query': query}
    return render(request, 'table_created_ppe.html', context)

def get_ppe_data(request):
    ppe_id = request.GET.get('id')
    ppe = get_object_or_404(Ppe, idPpe=ppe_id)
    data = {
        'guideNumber': ppe.guideNumber,
        'creationDate': ppe.creationDate,
        'name': ppe.name,
        'unitCost': ppe.unitCost,
        'quantity': ppe.quantity,
        'stock': ppe.stock
    }
    return JsonResponse(data)
@csrf_exempt
def save_all_ppe(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            for ppe_data in data:
                ppe, created = Ppe.objects.update_or_create(
                    name=ppe_data['name'],
                    defaults={
                        'guideNumber': ppe_data['guideNumber'],
                        'creationDate': datetime.strptime(ppe_data['creationDate'], '%Y-%m-%d').date(),
                        'unitCost': float(ppe_data['unitCost']),
                        'quantity': int(ppe_data['quantity']),
                        'stock': int(ppe_data['stock'])
                    }
                )
            return JsonResponse({'status': 'success'})
        except IntegrityError as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'fail', 'message': 'Invalid request method'}, status=400)

@login_required
def total_cost_ppe(request):
    query = request.GET.get('q', '')
    if query:
        epp = Ppe.objects.filter(name__icontains=query)
    else:
        epp = Ppe.objects.all()
    total_cost_final = 0
    for item in epp:
        item.save()
        total_cost_final += item.totalCost
    print(f"Número de PPEs encontrados: {epp.count()}")  # Añade este print
    return render(request, 'total_ppe_cost_table.html', {'epp': epp, 'query': query, 'total_cost_final': total_cost_final})

login_required
def show_added_ppe(request):
    query = request.GET.get('q', '')
    if query:
        epp = Ppe.objects.filter(name__icontains=query)
    else:
        epp = Ppe.objects.all()
    print(f"Número de PPEs encontrados: {epp.count()}")  # Añade este print
    return render(request, 'table_added_ppe.html', {'epp': epp, 'query': query})

@login_required
def create_ppe(request):
    if request.method == 'POST':
        form = CreatePpeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'EPP creado exitosamente.')
            return redirect('create_ppe')
        else:
            print("Form is not valid")
            print(form.errors)
    else:
        form = CreatePpeForm()
    return render(request, 'create_ppe.html', {'form': form})

@login_required
def add_ppe(request):
    if request.method == 'POST':
        form = PpeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('add_ppe')
    else:
        form = PpeForm()
    return render(request, 'add_ppe.html', {'form': form})


@login_required
def delete_ppe(request, id):
    epp = get_object_or_404(Ppe, idPpe=id)
    
    if request.method == 'DELETE':
        epp.delete()
        return redirect('ppe')
    else:
        return render(request, 'delete_ppe.html', {'epp': epp})

@login_required
def modify_ppe(request, id):
    epp = get_object_or_404(Ppe, idPpe=id)
    form = PpeForm(instance=epp)

    if request.method == 'POST':
        form = PpeForm(request.POST, instance=epp)
        if form.is_valid():
            form.instance.status = True
            form.save()
            return redirect('add_ppe')
    else:
        return render(request, 'modify_ppe.html', {'form': form, 'id': id})

@login_required 
def total_ppe_stock(request):
    total_stock = Ppe.objects.aggregate(Sum('stock'))['stock__sum'] or 0
    return JsonResponse({'total_stock': total_stock})

#EQUIMENT
@login_required
def equipment_list(request):
    query = request.GET.get('q')
    if query:
        equipment = Equipment.objects.filter(name__icontains=query)
    else:
        equipment = Equipment.objects.all()
    return render(request, 'equipment_list.html', {'equipment': equipment, 'query': query})

@login_required
def total_cost_equip(request):
    query = request.GET.get('q')
    if query:
        equipment = Equipment.objects.filter(name__icontains=query)
    else:
        equipment = Equipment.objects.all()
    total_cost_final = 0
    for item in equipment:
        item.save()
        total_cost_final += item.totalCost
    return render(request, 'total_equip_cost_table.html', {'equipment': equipment, 'query': query, 'total_cost_final': total_cost_final})

@login_required
def create_equipment(request):
    if request.method == 'POST':
        form = CreateEquipentForm(request.POST)
        if form.is_valid():
            equipment=form.save()
            History.objects.create(
                user=request.user,
                action='create',
                content_type=ContentType.objects.get_for_model(equipment),
                object_id=equipment.idEquipment
            )
            return redirect('equipment_list')
    else:
        form = CreateEquipentForm()
    return render(request, 'create_equipment.html', {'form': form})

@login_required
def delete_equipment(request, id):
    equipment = get_object_or_404(Equipment, idEquipment=id)
    
    if request.method == 'POST':
        equipment.delete()
        History.objects.create(
            user=request.user,
            action='delete',
            content_type=ContentType.objects.get_for_model(equipment),
            object_id=equipment.pk
        )
        return redirect('equipment_list')
    else:
        return render(request, 'delete_ppe.html', {'equipment': equipment})

@login_required
def modify_equipment(request, id):
    equipment = get_object_or_404(Equipment, idEquipment=id)
    form = EquipmentForm(instance=equipment)

    if request.method == 'POST':
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            form.instance.status = True
            equipment = form.save()
            History.objects.create(
                user=request.user,
                action='update',
                content_type=ContentType.objects.get_for_model(equipment),
                object_id=equipment.pk
            )
            return redirect('equipment_list')
    else:
        return render(request, 'modify_equipment.html', {'form': form})

login_required
def total_equipment_stock(request):
    total_stock = Equipment.objects.aggregate(Sum('stock'))['stock__sum'] or 0
    return JsonResponse({'total_stock': total_stock})

#MATERIAL
@login_required
def material_list(request):
    query = request.GET.get('q')
    if query:
        materials = Material.objects.filter(name__icontains=query)
    else:
        materials = Material.objects.all()
    return render(request, 'material_list.html', {'materials': materials, 'query': query})

@login_required
def create_material(request):
    if request.method == 'POST':
        form = CreateMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save()
            print(f"Material creado: {material.idMaterial}")
            print(f"Datos del POST: {request.POST}")
            messages.success(request, 'Material creado exitosamente.')
            return redirect('create_material')
        else:
            print("Formulario no válido")
            print(form.errors)
    else:
        form = CreateMaterialForm()
    return render(request, 'create_material.html', {'form': form})

@login_required
def total_cost_material(request):
    query = request.GET.get('q')
    if query:
        materials = Material.objects.filter(name__icontains=query)
    else:
        materials = Material.objects.all()
    total_cost_final = 0
    for item in materials:
        item.save()
        total_cost_final += item.totalCost
    return render(request, 'total_mat_cost_table.html', {'materials': materials, 'query': query, 'total_cost_final': total_cost_final})

@login_required
def add_material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('material_list')
    else:
        form = MaterialForm()
    return render(request, 'create_material.html', {'form': form})

@login_required
def delete_material(request, id):
    material = get_object_or_404(Material, idMaterial=id)
    
    if request.method == 'POST':
        material.delete()
        return redirect('material_list')
    else:
        return render(request, 'delete_material.html', {'material': material})

@login_required   
def modify_material(request, id):
    material = get_object_or_404(Material, idMaterial=id)
    form = MaterialForm(instance=material)

    if request.method == 'POST':
        form = MaterialForm(request.POST, instance=material)
        if form.is_valid():
            form.instance.status = True
            form.save()
            return redirect('material_list')
    else:
        return render(request, 'modify_material.html', {'form': form})

@login_required 
def total_material_stock(request):
    total_stock = Material.objects.aggregate(Sum('stock'))['stock__sum'] or 0
    return JsonResponse({'total_stock': total_stock})

#TOOLS
@login_required
def tool_list(request):
    query = request.GET.get('q')
    if query:
        tools = Tool.objects.filter(name__icontains=query)
    else:
        tools = Tool.objects.all()
    return render(request, 'tool_list.html', {'tools': tools, 'query': query})

@login_required
def total_cost_tool(request):
    query = request.GET.get('q', '')
    if query:
        tools = Tool.objects.filter(name__icontains=query)
    else:
        tools = Tool.objects.all()
    total_cost_final = 0
    for item in tools:
        item.save()
        total_cost_final += item.totalCost
    return render(request, 'total_tool_cost_table.html', {'tools': tools, 'query': query, 'total_cost_final': total_cost_final})

@login_required
def create_tool(request):
    if request.method == 'POST':
        form = CreateToolForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
<<<<<<< HEAD
            messages.success(request, 'Herramienta guardada exitosamente.')
=======
            messages.success(request, 'Herramienta creada exitosamente.')
>>>>>>> 67c854784d2b52e13464667c66c07171771f41ed
            return redirect('create_tool')
        else:
            print("Form is not valid")
            print(form.errors)
    else:
        form = CreateToolForm()
    return render(request, 'create_tool.html', {'form': form})

@login_required
def delete_tool(request, id):
    tools = get_object_or_404(Tool, idTool=id)
    
    if request.method == 'POST':
        tools.delete()
        return redirect('tool_list')
    else:
        return render(request, 'delete_ppe.html', {'tools': tools})

@login_required
def modify_tool(request, id):
    tools = get_object_or_404(Tool, idTool=id)
    form = ToolForm(instance=tools)

    if request.method == 'POST':
        form = ToolForm(request.POST, instance=tools)
        if form.is_valid():
            form.instance.status = True
            form.save()
            return redirect('tool_list')
    else:
        return render(request, 'modify_tool.html', {'form': form})

login_required
def total_tool_stock(request):
    total_stock = Tool.objects.aggregate(Sum('stock'))['stock__sum'] or 0
    return JsonResponse({'total_stock': total_stock})

#WORKER
@login_required
def worker_list(request):
    query = request.GET.get('q', '')
    if query:
        workers = Worker.objects.filter(name__icontains=query) | \
                  Worker.objects.filter(surname__icontains=query) | \
                  Worker.objects.filter(dni__icontains=query) | \
                  Worker.objects.filter(position__icontains=query)
    else:
        workers = Worker.objects.all().order_by('-contractDate')
    return render(request, 'worker_list.html', {'workers': workers, 'query': query})

@login_required
def create_worker(request):
    if request.method == 'POST':
        form = WorkerForm(request.POST)
        if form.is_valid():
            worker = form.save()
            return JsonResponse({'success': True, 'message': 'Trabajador creado con éxito'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = WorkerForm()
    return render(request, 'create_worker.html', {'form': form})

@login_required
def delete_worker(request, id):
    workers = get_object_or_404(Worker, dni=id)

    if request.method == 'POST':
        workers.delete()
        return redirect('worker_list')
    else:
        return render(request, 'delete_worker.html', {'workers': workers})
    
@login_required
def modify_worker(request, id):
    workers = get_object_or_404(Worker, dni=id)
    form = WorkerForm(instance=workers)

    if request.method == 'POST':
        form = WorkerForm(request.POST, instance=workers)
        if form.is_valid():
            form.save()
            return redirect('worker_list')
    else:
        return render(request, 'modify_worker.html', {'form': form})

#LOAN
@login_required
def loan_list(request):
    query = request.GET.get('q')
    if query:
        loans = Loan.objects.filter(worker__name__icontains=query)
    else:
        loans = Loan.objects.all()
    return render(request, 'loan_list.html', {'loans': loans, 'query': query})

@login_required
def add_loan(request):
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_loan')
    else:
        form = LoanForm()
    return render(request, 'add_loan.html', {'form': form})

@login_required
def delete_loan(request, id):
    loans = get_object_or_404(Loan, idLoan=id)
    
    if request.method == 'POST':
        loans.delete()
        return redirect('loan_list')
    else:
        return render(request, 'delete_loan.html', {'loans': loans})
    
@login_required
def modify_loan(request, id):
    loans = get_object_or_404(Loan, idLoan=id)
    form = LoanForm(instance=loans)

    if request.method == 'POST':
        form = LoanForm(request.POST, instance=loans)
        if form.is_valid():
            form.save()
            return redirect('loan_list')
    else:
        return render(request, 'modify_loan.html', {'form': form})
    
#PPELOAN
@login_required
def ppe_loan_list(request):
    query = request.GET.get('q')
    if query:
        ppe_loans = PpeLoan.objects.filter(worker__name_icontains=query)
    else:
        ppe_loans = PpeLoan.objects.all()
    print(f"Número de préstamos: {ppe_loans.count()}")
    print(f"Préstamos: {list(ppe_loans)}")
    return render(request, 'ppe_loan_list.html', {'ppe_loans': ppe_loans, 'query': query})

@login_required
def add_ppe_loan(request):
    if request.method == 'POST':
        form = PpeLoanForm(request.POST)
        if form.is_valid():
            ppe_loan = form.save(commit=False)
            worker_name = form.cleaned_data['worker']
            try:
                worker = Worker.objects.get(name=worker_name)
                ppe_loan.worker = worker
                ppe_loan.save()
                return redirect('some_success_url')
            except Worker.DoesNotExist:
                form.add_error('worker', 'Trabajador no encontrado')
    else:
        form = PpeLoanForm()
    
    # Obtener todos los objetos Ppe
    ppes = Ppe.objects.all()
    
    context = {
        'form': form,
        'ppes': ppes
    }
    return render(request, 'add_ppe_loan.html', context)

def check_ppe_availability(request):
    if request.method == 'GET':
        ppe_name = request.GET.get('ppe_name')
        try:
            ppe = Ppe.objects.get(name=ppe_name)
            return JsonResponse({'available': ppe.quantity})
        except Ppe.DoesNotExist:
            return JsonResponse({'error': 'EPP no encontrado'}, status=404)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def worker_autocomplete(request):
    if 'term' in request.GET:
        qs = Worker.objects.filter(name__icontains=request.GET.get('term'))
        names = list(qs.values_list('name', flat=True))
        return JsonResponse(names, safe=False)
    return JsonResponse([], safe=False)

def dni_autocomplete(request):
    if 'term' in request.GET:
        qs = Worker.objects.filter(dni__icontains=request.GET.get('term'))
        dnis = list(qs.values_list('dni', flat=True))
        return JsonResponse(dnis, safe=False)
    return JsonResponse([], safe=False)

def worker_details(request):
    if 'worker_name' in request.GET:
        worker = Worker.objects.get(name=request.GET.get('worker_name'))
        return JsonResponse({
            'name': worker.name,
            'dni': worker.dni,
            'position': worker.position
        })
    return JsonResponse({}, status=400)

@csrf_exempt
def confirm_ppe_loan(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        ppe_loans = data.get('ppe_loans', [])
        
        try:
            for loan_data in ppe_loans:
                worker = get_object_or_404(Worker, name=loan_data['worker'])
                ppe = get_object_or_404(Ppe, name=loan_data['name'])
                
                PpeLoan.objects.create(
                    worker=worker,
                    ppe=ppe,
                    loanAmount=loan_data['quantity'],
                    workerPosition=loan_data['workerPosition'],
                    workerDni=loan_data['workerDni'],
                    loanDate=loan_data['loanDate']
                )
                
                # Actualizar la cantidad de EPP disponible
                ppe.quantity -= int(loan_data['quantity'])
                ppe.save()
                
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

def load_given_ppe(request):
    given_ppes = PpeLoan.objects.filter(confirmed=False)
    return render(request, 'partials/given_ppe_table.html', {'given_ppes': given_ppes})

@login_required
def delete_ppe_loan(request, id):
    ppe_loans = get_object_or_404(PpeLoan, idPpeLoan=id)
    
    if request.method == 'POST':
        ppe_loans.delete()
        return redirect('ppe_loan_list')
    else:
        return render(request, 'delete_ppe_loan.html', {'ppe_loans': ppe_loans})
    
@login_required
def modify_ppe_loan(request, id):
    ppe_loans = get_object_or_404(PpeLoan, idPpeLoan=id)

    if request.method == 'POST':
        form = PpeLoanForm(request.POST, request.FILES, instance=ppe_loans)
        if form.is_valid():
            form.instance.status = True
            form.save()
            return redirect('ppe_loan_list')
    else:
        return render(request, 'modify_ppe_loan.html', {'form': form})
    
#historial

def history(request):
    history_records = History.objects.all().order_by('-timestamp')
    return render(request, 'history.html', {'history_records': history_records})
    
#REGISTER
def register_admin(request):
    if request.method == 'POST':
        form = AdminSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = AdminSignUpForm()
    return render(request, 'register_admin.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def user_list(request):
    query = request.GET.get('q', '')
    if query:
        admin = User.objects.filter(admin__name_icontains=query)
    else:
        admin = User.objects.all()
    print(f"Número de usuarios: {admin.count()}")
    return render(request, 'table_user.html', {'admin': admin, 'query': query})

def exit(request):
    logout(request)
    return redirect('home')