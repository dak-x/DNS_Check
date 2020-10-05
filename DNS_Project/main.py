from dns.resolver import dns
import dns.rdata
import dns.message

name_server = '8.8.8.8'  # Google's DNS server
ADDITIONAL_RDCLASS = 65535
request = dns.message.make_query('iitjammu.ac.in', dns.rdatatype.MX)

request.flags |= dns.flags.RD
#request.flags.RD = True
request.find_rrset(request.additional, dns.name.root, ADDITIONAL_RDCLASS,
                   dns.rdatatype.OPT, create=True, force_unique=True)

response: dns.message.Message = dns.query.udp(request, name_server)

print(response)
