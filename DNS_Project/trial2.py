import dns.message
import dns.rdatatype
import dns.query

def get_records(domain_name: str, record_type: dns.rdatatype.RdataType, dns_addr: str):

    Qry_List = []
    if(record_type == dns.rdatatype.RdataType.ANY):
        Qry_List = [dns.rdatatype.A, dns.rdatatype.AAAA, dns.rdatatype.CNAME, dns.rdatatype.MX, dns.rdatatype.NS,
                    dns.rdatatype.PTR, dns.rdatatype.SRV, dns.rdatatype.SOA, dns.rdatatype.TXT, dns.rdatatype.CAA]
    else:
        Qry_List = [record_type]

    response_list = []

    for qry in Qry_List:
        k = dns.message.make_query(domain_name, qry)
        msg: dns.message.Message = dns.query.tcp(k, where=dns_addr)
        print(msg.answer)
        # msg.find_rrset(msg.answer,domain_name,)
        # print(msg.to_text())
        # continue

        lines = str(msg).split('\n')
        qry_response = []
        flag = False
        for line in lines:
            if( line.count("AUTHORITY") == 1):
                flag = False
                continue
            if(line.count("ANSWER") == 1):
                flag = True
                continue
            if(flag):
                qry_response.append(line)
        # u = qry_response.split(" ")
        response_list.append((qry.name,u))

    return response_list

temp = get_records("iitjammu.ac.in", dns.rdatatype.ANY, "8.8.8.8")
for x in temp:
    print(x)
#
# an_address = "8.8.8.8"
# domain_name = socket.gethostbyaddr(an_address)
# print(domain_name)
