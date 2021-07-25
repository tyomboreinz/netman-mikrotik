import routeros_api, re

class MikrotikAPI():

    connection = routeros_api.RouterOsApiPool('192.168.50.1', username='admin', password='tirakat', plaintext_login=True)
    # connection = routeros_api.RouterOsApiPool('192.168.11.1', username='admin', password='mboreinz', plaintext_login=True)
    api = connection.get_api()

    def get_interface_list():
        print("panggil fungsi : get_interface_list")
        interface = MikrotikAPI.api.get_resource('interface/').get()
        iface_brigde = MikrotikAPI.api.get_resource('interface/bridge/').get()
        iface_brigde_port = MikrotikAPI.api.get_resource('interface/bridge/port').get()
        iface_dhcp = MikrotikAPI.api.get_resource('ip/dhcp-server').get()
        iface_list = ()
        
        for data in interface:
            if data['disabled'] == 'false':
                token = 0
                
                for i_dhcp in iface_dhcp:
                    if data['name'] == i_dhcp['interface']:
                        token += 1
                    else:
                        for i_bridge in iface_brigde:
                            if i_dhcp['interface'] == i_bridge['name']:
                                for i_bport in iface_brigde_port:
                                    if data['name'] == i_bport['interface'] and i_dhcp['interface'] == i_bport['bridge']:
                                        token += 1

                if token == 0:
                    ether = (data['name'], data['name'])
                    iface_list += (ether,)

        return iface_list

    def get_dhcp_lease_list():
        list_ipadd = MikrotikAPI.api.get_resource('ip/dhcp-server/lease/').get()
        list_dhcp = []
        for data in list_ipadd:
            list_dhcp.append({key.replace('-','_'): val for key,val in data.items()})

        return list_dhcp

    def add_ip_pool(name, ranges):
        MikrotikAPI.api.get_binary_resource('/').call('ip/pool/add', {'name':name.encode('utf-8'), 'ranges':ranges.encode('utf-8')})
        for data in MikrotikAPI.api.get_resource('ip/pool').get():
            if re.search(name, str(data)):
                id = data['id']
            
        return id

    def add_dhcp_network(ip, gateway, dns, comment):
        MikrotikAPI.api.get_binary_resource('/').call('ip/dhcp-server/network/add', {'address':ip.encode('utf-8'), 'gateway':gateway.encode('utf-8'), 'dns-server':dns.encode('utf-8'), 'comment':comment.encode('utf-8')})
        for data in MikrotikAPI.api.get_resource('ip/dhcp-server/network').get():
            if re.search(ip, str(data)):
                id = data['id']
            
        return id

    def add_dhcp_server(name, interface, address):
        MikrotikAPI.api.get_binary_resource('/').call('ip/dhcp-server/add', {'name':name.encode('utf-8'), 'interface':interface.encode('utf-8'), 'address-pool':address.encode('utf-8'), 'disabled':b'false'})
        for data in MikrotikAPI.api.get_resource('ip/dhcp-server').get():
            if re.search(name, str(data)):
                id = data['id']
    
        return id

    def add_dhcp_static(ip, mac, comment):
        MikrotikAPI.api.get_binary_resource('/').call('ip/dhcp-server/lease/add', {'mac-address':mac.encode('utf-8'), 'address':ip.encode('utf-8'), 'comment':comment.encode('utf-8')})
        for data in MikrotikAPI.api.get_resource('ip/dhcp-server/lease/').get():
            if re.search(mac, str(data)):
                id = data['id']

        return id

    def add_dns_static(name, address):
        MikrotikAPI.api.get_binary_resource('/').call('ip/dns/static/add', {'address':address.encode('utf-8'), 'name':name.encode('utf-8')})
        for data in MikrotikAPI.api.get_resource('ip/dns/static/').get():
            if re.search(name, str(data)):
                id = data['id']

        return id

    def update_ip_pool(id, name, ranges):
        MikrotikAPI.api.get_resource('ip/pool').set(id=id, name=name, ranges=ranges)

    def update_dhcp_network(id, address, gateway, dns, comment):
        MikrotikAPI.api.get_resource('ip/dhcp-server/network').set(id=id, address=address, gateway=gateway, dns_server=dns, comment=comment)

    def update_dhcp_server(id, name, interface, pool):
        MikrotikAPI.api.get_resource('ip/dhcp-server/').set(id=id, name=name, interface=interface, address_pool=pool)

    def update_dns_static(id, name, ip):
        MikrotikAPI.api.get_resource('ip/dns/static/').set(id=id, name=name, address=ip)

    def update_dhcp_static(id, ip, mac, comment):
        MikrotikAPI.api.get_resource('ip/dhcp-server/lease/').set(id=id, address=ip, mac_address=mac, comment=comment)

    def delete_dhcp_server(id_pool, id_network, id_dhcp_server):
        MikrotikAPI.api.get_resource('ip/dhcp-server').remove(id=id_dhcp_server)
        MikrotikAPI.api.get_resource('ip/dhcp-server/network').remove(id=id_network)
        MikrotikAPI.api.get_resource('ip/pool').remove(id=id_pool)

    def delete_dhcp_static(id):
        MikrotikAPI.api.get_resource('ip/dhcp-server/lease/').remove(id=id)

    def delete_dns_static(id):
        MikrotikAPI.api.get_resource('ip/dns/static').remove(id=id)