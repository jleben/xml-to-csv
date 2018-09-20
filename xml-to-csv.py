import xml.etree.ElementTree as ET

def tag(name):
    return '{http://www.tbs-sct.gc.ca/fcsi-rscf}' + name

def real_path(path):
    elems = path.split('/')
    fixed_elems = []
    for e in elems:
        fixed_elems.append(tag(e))
    return '/'.join(fixed_elems)

def get_field(parent, path):
    path = real_path(path)
    values = parent.findall(path)
    return ",".join([v.text for v in values])


def main():
    tree = ET.parse('sites.xml')
    root = tree.getroot()

    sites = root.find(tag('Sites'))

    csv_file = open('sites.csv', 'w')

    fields = [
        ('Name', 'Name'),
        ('Latitude', 'Location/Latitude'),
        ('Longitude', 'Location/Longitude'),
        ('Reporting Org', 'ReportingOrganization'),
        ('Status', 'SiteStatus/Status'),
        ('Status Description', 'SiteStatus/Description'),
        ('Reason For Federal Involvement', 'ReasonForFederalInvolvement'),
        ('Management Strategy', 'ManagementStrategy/ManagementType'),
    ]

    header = ['"' + name + '"' for name, path in fields]
    header.append('"Contaminations"')

    csv_file.write(" ".join(header) + "\n")

    for site in sites:

        values = ['"' + get_field(site, path) + '"' for name, path in fields]

        contaminations = site.findall(real_path('ContaminationDetails/ContaminatedMedia'))
        contamination_texts = []
        for contamination in contaminations:
            agent = contamination.find(tag('Contamination')).text
            medium = contamination.find(tag('Medium')).text
            contamination_texts.append(medium + ": " + agent)

        values.append('"' + "  |  ".join(contamination_texts) + '"')

        csv_file.write(" ".join(values) + "\n")

main()
