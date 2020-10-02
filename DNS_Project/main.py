from dns.resolver import dns
name_server = '8.8.8.8'  # Google's DNS server
ADDITIONAL_RDCLASS = 65535
request = dns.message.make_query('google.com', dns.rdatatype.TXT)
request.flags |= dns.flags.RD
#request.flags.RD = True
request.find_rrset(request.additional, dns.name.root, ADDITIONAL_RDCLASS,
                   dns.rdatatype.OPT, create=True, force_unique=True)
response = dns.query.udp(request, name_server)
print(response)
