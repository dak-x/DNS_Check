import dns.message
from dns.rdatatype import RdataType
import dns.query
from dns.rdataclass import RdataClass
import dns.name
import dns.reversename

# Has been directly imported into app.py


def get_records(domain_name: str, record_type: RdataType, dns_addr: str):
    # TODO: Add fields names for CNAME , PTR , SRV records
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
    domain_name = dns.name.from_text(domain_name)

    for qry in Qry_List:

        msg = dns.message.make_query(domain_name, qry)
        response = dns.query.tcp(msg, where=dns_addr)

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


def get_reversename(addr: str, dns_addr="8.8.8.8"):
    x = dns.reversename.from_address(addr)
    msg = dns.message.make_query(x, RdataType.ANY)
    response = dns.query.udp(msg, dns_addr)
    record = response.find_rrset(
        response.answer, x, RdataClass.IN, RdataType.PTR).to_text().split(" ")[-1]
    return record

# Testing for get_records()
# A = get_records("iitjammu.ac.in", dns.rdatatype.ANY, "8.8.8.8")
# for x in A:
#     print(x)
#     for line in A[x]:
#         print("        ", line)

# Testing get_reversename()
# print(get_reversename("8.8.8.8"))
