import dns.message
from dns.rdatatype import RdataType
import dns.query
from dns.rdataclass import RdataClass
import dns.name
import dns.reversename
import dns.name
import dns.message
import dns.query
import dns.flags
import dns.rdataclass
root_servers = {}

root_servers[1] = '198.41.0.4'
root_servers[2] = '199.9.14.201'
root_servers[3] = '192.33.4.12'
root_servers[4] = '199.7.91.13'
root_servers[5] = '192.203.230.10'
root_servers[6] = '192.5.5.241'
root_servers[7] = '192.112.36.4'
root_servers[8] = '198.97.190.53'
root_servers[9] = '192.36.148.17'
root_servers[10] = '192.58.128.30'
root_servers[11] = '193.0.14.129'
root_servers[12] = '199.7.83.42'
root_servers[13] = '202.12.27.33'

def get_ip_from_rrset(rrset):
    return (((rrset.to_text()).split(' '))[-1])

def RecursiveDNS(domain,rdtype,root_server):
    request = dns.message.make_query(domain, rdtype)
    request.flags ^= dns.flags.RD
    response = dns.query.udp(request, root_server)
    if(len(response.answer) == 0):
        if len(response.additional) > 0:
            for rrset in response.additional:
                next_ip = get_ip_from_rrset(rrset)
                try:
                    return RecursiveDNS(domain,rdtype,next_ip)
                except Exception as e:
                    pass
        else:
            return request
    else:
        return(response)
# Has been directly imported into app.py
def get_records(domain_name: str, record_type, dns_addr: str):
    try:
    # TODO: Add fields names for CNAME , PTR , SRV records
        mapping = {
            "ANY":RdataType.ANY,
            "A":RdataType.A,
            "AAAA":RdataType.AAAA,
            "CNAME":RdataType.CNAME,
            "MX":RdataType.MX,
            "NS":RdataType.NS,
            "PTR":RdataType.PTR,
            "SRV":RdataType.SRV,
            "SOA":RdataType.SOA,
            "TXT":RdataType.TXT,
            "CAA":RdataType.CAA
        }
        record_type = mapping[record_type]
        Table_Header = {
            RdataType.A: ["Type", "Domain Name", "Address", "TTL"],
            RdataType.AAAA: ["Type", "Domain Name", "Address", "TTL"],
            RdataType.CNAME: ["Name","TTL","Content"],
            RdataType.MX: ["Type", "Domain Name", "Pref", "Hostname", "TTL"],
            RdataType.NS: ["Type", "Domain Name", "NS", "TTL"],
            RdataType.PTR: [],
            RdataType.SRV: [],
            RdataType.SOA: ["Type", "Domain Name", "Primary NS", "Responsible Email", "TTL"],
            RdataType.TXT: ["Type", "Domain Name", "Record", "TTL"],
            RdataType.CAA: ["Type", "Domain Name", "Tag", "Value", "TTL"],
        }

        Qry_List = []
        if(record_type == RdataType.ANY):
            Qry_List = [x for x in Table_Header.keys()]
        else:
            Qry_List = [record_type]

        Table_Dict = {}
        domain_name = dns.name.from_text(domain_name)

        for qry in Qry_List:

            msg = dns.message.make_query(domain_name, qry)
            response = dns.query.udp(msg, where=dns_addr)

            record = response.find_rrset(
                response.answer, domain_name, RdataClass.IN, qry, create=True).to_text().split("\n")
            table_content = [Table_Header[qry][:]]

            for line in record:
                [bg, ed] = [4, 5]
                if(qry.name in ["SOA", "MX"]):
                    ed = 6
                elif(qry.name == 'CAA'):
                    bg = 5
                    ed = 7

                x = line.split(" ")
                L = [qry.name, x[0]] + x[bg:ed] + [x[1]]
                table_content.append(L[:])

            Table_Dict[qry.name] = table_content

        return Table_Dict
    except:
        return -2


def get_recordsRecursive(domain_name: str, record_type, dns_addr: str):
    # TODO: Add fields names for CNAME , PTR , SRV records
    try:
        mapping = {
            "ANY":RdataType.ANY,
            "A":RdataType.A,
            "AAAA":RdataType.AAAA,
            "CNAME":RdataType.CNAME,
            "MX":RdataType.MX,
            "NS":RdataType.NS,
            "PTR":RdataType.PTR,
            "SRV":RdataType.SRV,
            "SOA":RdataType.SOA,
            "TXT":RdataType.TXT,
            "CAA":RdataType.CAA
        }
        record_type = mapping[record_type]
        Table_Header = {
            RdataType.A: ["Type", "Domain Name", "Address", "TTL"],
            RdataType.AAAA: ["Type", "Domain Name", "Address", "TTL"],
            RdataType.CNAME: [],
            RdataType.MX: ["Type", "Domain Name", "Pref", "Hostname", "TTL"],
            RdataType.NS: ["Type", "Domain Name", "NS", "TTL"],
            RdataType.PTR: [],
            RdataType.SRV: [],
            RdataType.SOA: ["Type", "Domain Name", "Primary NS", "Responsible Email", "TTL"],
            RdataType.TXT: ["Type", "Domain Name", "Record", "TTL"],
            RdataType.CAA: ["Type", "Domain Name", "Tag", "Value", "TTL"],
        }

        Qry_List = []
        if(record_type == RdataType.ANY):
            Qry_List = [x for x in Table_Header.keys()]
        else:
            Qry_List = [record_type]

        Table_Dict = {}
        domain = domain_name
        domain_name = dns.name.from_text(domain_name)

        for qry in Qry_List:

            response = RecursiveDNS(domain,qry,dns_addr)
            try:
                record = response.find_rrset(
                    response.answer, domain_name, RdataClass.IN, qry, create=True).to_text().split("\n")
            except:
                return -1
            table_content = [Table_Header[qry][:]]

            for line in record:
                [bg, ed] = [4, 5]
                if(qry.name in ["SOA", "MX"]):
                    ed = 6
                elif(qry.name == 'CAA'):
                    bg = 5
                    ed = 7

                x = line.split(" ")
                L = [qry.name, x[0]] + x[bg:ed] + [x[1]]
                table_content.append(L[:])

            Table_Dict[qry.name] = table_content

        return Table_Dict
    except:
        return -2




def get_reversename(addr: str, dns_addr="8.8.8.8"):
    try:
        x = dns.reversename.from_address(addr)
        msg = dns.message.make_query(x, RdataType.ANY)
        response = dns.query.udp(msg, dns_addr)
        record = response.find_rrset(
        response.answer, x, RdataClass.IN, RdataType.PTR).to_text().split(" ")[-1]
        return record
    except:
        return -1
        

# Testing for get_records()
# A = get_records("iitjammu.ac.in", "ANY", "8.8.8.8")
# print(A)
# for x in A:
#     print(x)
#     for line in A[x]:
#         print("        ", line)

# Testing get_reversename()
# print(get_reversename("8.8.8.8"))
