import subprocess, random
from django.shortcuts import render, redirect
from django.db.models.functions import Length
from django.contrib.auth.decorators import login_required
from django.conf import settings
from ddi.models import *
from ddi.forms import *
from ddi.mikrotik import MikrotikAPI

@login_required(login_url=settings.LOGIN_URL)
def os_delete(request, id_os):
    os = OS.objects.get(id=id_os)
    os.delete()
    return redirect('/setting')

@login_required(login_url=settings.LOGIN_URL)
def setting(request):
    if request.POST:
        print(request.POST)             ###################
        if '1' in request.POST:
            post_value = request.POST.copy()
            # Router.objects.filter(id=1).update(value=post_value['1'])
            # Router.objects.filter(id=2).update(value=post_value['2'])
            # Router.objects.filter(id=3).update(value=post_value['3'])
        else:
            form = FormOS(request.POST)
            
            if form.is_valid():
                form.save()
        
        return redirect('/setting')
    else:
        form = FormOS()
        # form_router = FormRouter()
        data = {
            'form' : form,
            # 'form_router' : form_router,
            # 'router_config': Router.objects.all(),
            'os_data' : OS.objects.all().order_by('name'),
            'sidebar_domains' : Domain.objects.all().order_by('domain'),
            'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
            }
    return render(request, 'system-setting.html', data)

@login_required(login_url=settings.LOGIN_URL)
def subdomain_delete(request, id_subdomain):
    subdomain = Subdomain.objects.get(id=id_subdomain)
    MikrotikAPI.delete_dns_static(subdomain.id)
    subdomain.delete()
    return redirect('/subdomain/'+str(subdomain.domain_id))

@login_required(login_url=settings.LOGIN_URL)
def subdomain_edit(request, id_subdomain):
    subdomain = Subdomain.objects.get(id=id_subdomain)
    if request.POST:
        post_value = request.POST.copy()
        post_value['domain'] = subdomain.domain
        form = FormSubDomain(post_value, instance=subdomain)
        if form.is_valid():
            domain = Domain.objects.get(domain=form.cleaned_data['domain'])
            form.save()
            MikrotikAPI.update_dns_static(form.cleaned_data['id'], str(form.cleaned_data['subdomain'])+"."+str(form.cleaned_data['domain']), form.cleaned_data['ip'])
            return redirect('/subdomain/' + str(domain.id))
    else:
        form = FormSubDomain(instance=subdomain)
        form.fields['domain'].widget.attrs['disabled'] = True
        data = {
            'form' : form,
            'subdomain' : subdomain,
            'title' : 'Edit Subdomain',
            'sidebar_domains' : Domain.objects.all().order_by('domain'),
            'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
        }
    return render(request, 'item-edit.html', data)

@login_required(login_url=settings.LOGIN_URL)
def subdomain_add(request):
    if request.POST:
        post_value = request.POST.copy()
        domain = Domain.objects.get(id=post_value['domain'])
        subdomain = post_value['subdomain']+"."+domain.domain
        post_value['id'] = MikrotikAPI.add_dns_static(subdomain, post_value['ip'])
        form = FormSubDomain(post_value)

        if form.is_valid():
            domain = Domain.objects.get(domain=form.cleaned_data['domain'])
            form.save()

            return redirect('/subdomain/'+ str(domain.id))
    else:
        form = FormSubDomain()
        data = {
            'form' : form,
            'title' : 'Add Subdomain',
            'sidebar_domains' : Domain.objects.all().order_by('domain'),
            'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
        }
    return render(request, 'item-add.html', data)

@login_required(login_url=settings.LOGIN_URL)
def subdomain_list(request,id_domain):
    subdomains = Subdomain.objects.filter(domain=id_domain)
    data = {
        'id_domain': id_domain,
        'list_subdomains': subdomains,
        'sidebar_domains' : Domain.objects.all().order_by('domain'),
        'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
    }
    return render(request, 'subdomain-list.html', data)

@login_required(login_url=settings.LOGIN_URL)
def domain_delete(request, id_domain):
    domain = Domain.objects.get(id=id_domain)
    subdomain = Subdomain.objects.filter(domain_id=domain.id)
    for sub in subdomain:
        MikrotikAPI.delete_dns_static(sub.id)
    domain.delete()
    return redirect('/domain')

@login_required(login_url=settings.LOGIN_URL)
def domain_edit(request, id_domain):
    domain = Domain.objects.get(id=id_domain)
    if request.POST:
        form = FormDomain(request.POST, instance=domain)
        if form.is_valid():
            form.save()
            return redirect('/domain')
    else:
        form = FormDomain(instance=domain)
        data = {
            'form' : form,
            'title' : 'Edit Domain',
            'sidebar_domains' : Domain.objects.all().order_by('domain'),
            'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
        }
    return render(request, 'item-edit.html', data)

@login_required(login_url=settings.LOGIN_URL)
def domain_add(request):
    if request.POST:
        form = FormDomain(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/domain')
    else:
        form = FormDomain()
        data = {
            'menu_domain_add' : 'class=mm-active',
            'form' : form,
            'title' : 'Add Domain',
            'sidebar_domains' : Domain.objects.all().order_by('domain'),
            'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
        }
    return render(request, 'item-add.html', data)

@login_required(login_url=settings.LOGIN_URL)
def domain_list(request):
    domains = Domain.objects.all().order_by('domain')
    data = {
        'menu_domain_list' : 'class=mm-active',
        'list_domains': domains,
        'sidebar_domains' : domains,
        'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
    }
    return render(request, 'domain-list.html', data)

@login_required(login_url=settings.LOGIN_URL)
def dhcp_lease(request):
    data = {
        'menu_dhcp_lease' : 'class=mm-active',
        'dhcp_lease': MikrotikAPI.get_dhcp_lease_list,
        'sidebar_domains' : Domain.objects.all().order_by('domain'),
        'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
    }
    return render(request, 'dhcp-lease.html', data)

@login_required(login_url=settings.LOGIN_URL)
def dhcp_static_edit(request,id_static):
    dhcp = Dhcp_Static.objects.get(id=id_static)
    if request.POST:
        form = FormDHCP_Static(request.POST, instance=dhcp)
        if form.is_valid():
            MikrotikAPI.update_dhcp_static(form.cleaned_data['id'], form.cleaned_data['ip'], form.cleaned_data['mac'], form.cleaned_data['description'])
            form.save()
            return redirect('/dhcp/static')
    else:
        form = FormDHCP_Static(instance=dhcp)
        data = {
            'form' : form,
            'dhcp' : dhcp,
            'title' : 'Edit Static DHCP',
            'sidebar_domains' : Domain.objects.all().order_by('domain'),
            'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
        }
    return render(request, 'item-edit.html', data)

@login_required(login_url=settings.LOGIN_URL)
def dhcp_static_delete(request, id_static):
    dhcp = Dhcp_Static.objects.get(id=id_static)
    MikrotikAPI.delete_dhcp_static(dhcp.id)
    dhcp.delete()
    return redirect('/dhcp/static')

@login_required(login_url=settings.LOGIN_URL)
def dhcp_static_add(request):
    if request.POST:
        post_value = request.POST.copy()
        post_value['id'] = MikrotikAPI.add_dhcp_static(post_value['ip'], post_value['mac'], post_value['description'])
        form = FormDHCP_Static(post_value)
        
        if form.is_valid():
            form.save()
            return redirect('/dhcp/static')
    else:
        form = FormDHCP_Static()
        data = {
            'form' : form,
            'title' : 'Add DHCP',
            'sidebar_domains' : Domain.objects.all().order_by('domain'),
            'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
        }
    return render(request, 'item-add.html', data)

@login_required(login_url=settings.LOGIN_URL)
def dhcp_static_lease(request):

    dhcp_static = Dhcp_Static.objects.all().order_by(Length('ip').asc(), 'ip')
    data = {
        'menu_dhcp_static' : 'class=mm-active',
        'dhcp_static': dhcp_static,
        'sidebar_domains' : Domain.objects.all().order_by('domain'),
        'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
    }
    return render(request, 'dhcp-static-lease.html', data)

@login_required(login_url=settings.LOGIN_URL)
def dhcp_server_delete(request, id_dhcp_server):
    dhcp_server = Dhcp_Server.objects.get(id=id_dhcp_server)
    MikrotikAPI.delete_dhcp_server(dhcp_server.idm_pool, dhcp_server.idm_network, dhcp_server.idm_dhcp)
    dhcp_server.delete()
    return redirect('/dhcp/server/')

@login_required(login_url=settings.LOGIN_URL)
def dhcp_server_edit(request, id_dhcp_server):
    dhcp_server = Dhcp_Server.objects.get(id=id_dhcp_server)
    if request.POST:
        post_value = request.POST.copy()
        post_value['interface'] = dhcp_server.interface
        form = FormDHCP_Server(post_value, instance=dhcp_server)
        if form.is_valid():
            MikrotikAPI.update_ip_pool(form.cleaned_data['idm_pool'], form.cleaned_data['name'], str(form.cleaned_data['ip_start']+'-'+form.cleaned_data['ip_end']))
            MikrotikAPI.update_dhcp_network(form.cleaned_data['idm_network'], form.cleaned_data['subnet'], form.cleaned_data['gateway'], form.cleaned_data['dns'], form.cleaned_data['name'])
            MikrotikAPI.update_dhcp_server(form.cleaned_data['idm_dhcp'], form.cleaned_data['name'], form.cleaned_data['interface'], form.cleaned_data['name'])
            form.save()
            return redirect('/dhcp/server')
    else:
        form = FormDHCP_Server(instance=dhcp_server)
        form.fields['interface'].widget.attrs['disabled'] = True
        data = {
            'form' : form,
            'title' : 'Edit DHCP Server',
            'sidebar_domains' : Domain.objects.all().order_by('domain'),
            'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
        }
    return render(request, 'item-edit.html', data)

@login_required(login_url=settings.LOGIN_URL)
def dhcp_server_add(request):
    if request.POST:
        post_value = request.POST.copy()
        post_value['idm_pool'] = MikrotikAPI.add_ip_pool(post_value['name'], str(post_value['ip_start']+'-'+post_value['ip_end']))
        post_value['idm_network'] = MikrotikAPI.add_dhcp_network(post_value['subnet'], post_value['gateway'], post_value['dns'], post_value['name'])
        post_value['idm_dhcp'] = MikrotikAPI.add_dhcp_server(post_value['name'], post_value['interface'], post_value['name'])
        form = FormDHCP_Server(post_value)

        if form.is_valid():
            form.save()
            return redirect('/dhcp/server')
    else:
        form = FormDHCP_Server()
        form.fields['interface'] = forms.ChoiceField(choices=MikrotikAPI.get_interface_list)
        form.fields['interface'].widget.attrs['class'] = 'form-control'

        data = {
            'form' : form,
            'title' : 'Add DHCP Server',
            'sidebar_domains' : Domain.objects.all().order_by('domain'),
            'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
        }
    return render(request, 'item-add.html', data)

@login_required(login_url=settings.LOGIN_URL)
def dhcp_server_list(request):
    dhcp_server = Dhcp_Server.objects.all()
    data = {
        'menu_dhcp_server_list' : 'class=mm-active',
        'dhcp_server' : dhcp_server,
        'sidebar_domains' : Domain.objects.all().order_by('domain'),
        'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
    }
    return render(request, 'dhcp-server.html', data)

@login_required(login_url=settings.LOGIN_URL)
def ip_delete(request, id_ip):
    ip = Ip_Address.objects.get(id=id_ip)
    ip.delete()
    return redirect('/network/' + str(ip.subnet_id))

@login_required(login_url=settings.LOGIN_URL)
def ip_edit(request, id_ip):
    ip = Ip_Address.objects.get(id=id_ip)
    if request.POST:
        post_value = request.POST.copy()
        post_value['subnet'] = ip.subnet
        form = FormIpAddress(post_value, instance=ip)
        if form.is_valid():
            form.save()
            subnet = Subnet.objects.get(ip_network=form.cleaned_data['subnet'])
            return redirect('/network/' + str(subnet.id))
    else:
        form = FormIpAddress(instance=ip)
        form.fields['subnet'].widget.attrs['disabled'] = True
        data = {
            'form' : form,
            'ip' : ip,
            'title' : 'Edit IP Address',
            'sidebar_domains' : Domain.objects.all().order_by('domain'),
            'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
        }
    return render(request, 'item-edit.html', data)

@login_required(login_url=settings.LOGIN_URL)
def ip_add(request):
    if request.POST:
        form = FormIpAddress(request.POST)
        if form.is_valid():
            subnet = Subnet.objects.get(ip_network=form.cleaned_data['subnet'])
            form.save()
            return redirect('/network/' + str(subnet.id))
    else:
        form = FormIpAddress()
        data = {
            'form' : form,
            'title' : 'Add IP',
            'sidebar_domains' : Domain.objects.all().order_by('domain'),
            'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
        }
    return render(request, 'item-add.html', data)

@login_required(login_url=settings.LOGIN_URL)
def network_delete(request, id_subnet):
    subnet = Subnet.objects.get(id=id_subnet)
    subnet.delete()
    return redirect('/network/')

@login_required(login_url=settings.LOGIN_URL)
def network_edit(request, id_subnet):
    subnet = Subnet.objects.get(id=id_subnet)
    if request.POST:
        form = FormSubnet(request.POST, instance=subnet)
        if form.is_valid():
            form.save()
            return redirect('/network')
    else:
        form = FormSubnet(instance=subnet)
        data = {
            'form' : form,
            'subnet' : subnet,
            'sidebar_domains' : Domain.objects.all().order_by('domain'),
            'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
            'title' : 'Edit Network',
        }
    return render(request, 'item-edit.html', data)

@login_required(login_url=settings.LOGIN_URL)
def network_detail(request, id_subnet):
    ips = Ip_Address.objects.filter(subnet=id_subnet).order_by(Length('ip_address').asc(), 'ip_address')
    data = {
        'sidebar_domains' : Domain.objects.all().order_by('domain'),
        'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
        'id_subnet' : id_subnet,
        'ips' : ips,
    }
    return render(request, 'network-detail.html', data)

@login_required(login_url=settings.LOGIN_URL)
def network_add(request):
    if request.POST:
        form = FormSubnet(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/network/')
    else:
        form = FormSubnet()
        data = {
            'menu_network_add' : 'class=mm-active',
            'form' : form,
            'sidebar_domains' : Domain.objects.all().order_by('domain'),
            'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
            'title' : 'Add Network',
        }
    return render(request, 'item-add.html', data)

@login_required(login_url=settings.LOGIN_URL)
def network_list(request):
    subnets = Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network')
    data = {
        'menu_network_list' : 'class=mm-active',
        'subnets' : subnets,
        'sidebar_subnets' : subnets,
        'sidebar_domains' : Domain.objects.all().order_by('domain'),
    }
    return render(request, 'network-list.html', data)

@login_required(login_url=settings.LOGIN_URL)
def network_scan(request, id_subnet):
    subnet = Subnet.objects.get(id=id_subnet)
    existing_ip = Ip_Address.objects.filter(subnet=id_subnet)
    x = subprocess.check_output("nmap -sn "+ str(subnet.ip_network) +"/"+ str(subnet.netmask) +""" | grep report | awk '{print $NF}' | sed 's/(//g' | sed 's/)//g' """, shell=True, text=False)
    x_decode = x.decode("utf-8")
    lists_ip = list(filter(None,(x_decode.split("\n"))))

    for ip in lists_ip:
        token = 0
        for address in existing_ip:
            if ip == address.ip_address:
                token += 1

        if token == 0:    
            Ip_Address.objects.create(ip_address=str(ip),subnet_id=id_subnet)
            print("IP : "+ ip +" Addedd Successfully")
        else:
            print("IP : "+ ip +" Already Available")
        
    return redirect('/network/'+ str(id_subnet))

@login_required(login_url=settings.LOGIN_URL)
def home(request):
    os = OS.objects.all().order_by('name')
    total_ip = Ip_Address.objects.all().count()
    total_subnet = Subnet.objects.all().count()
    total_domain = Domain.objects.all().count()
    total_subdomain = Subdomain.objects.all().count()
    total_dhcp_server = Dhcp_Server.objects.all().count()
    total_dhcp_lease = MikrotikAPI.get_count_dhcp_lease()
    color = ['primary', 'success', 'warning', 'danger']
    data_os = []
    for data in os:
        count_data = Ip_Address.objects.filter(os_id=data.id).count()
        if count_data != 0:
            data_os.append({'name' : data.name, 'count' : count_data, 'percentage' : format(count_data / total_ip * 100, ".0f"), 'color' : random.choice(color)})

    data = {
        'total_subnet' : total_subnet,
        'total_dhcp_server' : total_dhcp_server,
        'total_domain' : total_domain,
        'total_ip' : total_ip,
        'total_dhcp_lease' : total_dhcp_lease,
        'total_subdomain' : total_subdomain,
        'data_os' : data_os,
        'menu_dashboard' : 'class=mm-active',
        'sidebar_domains' : Domain.objects.all().order_by('domain'),
        'sidebar_subnets' : Subnet.objects.all().order_by(Length('ip_network').asc(), 'ip_network'),
    }
    return render(request, 'dashboard.html', data)