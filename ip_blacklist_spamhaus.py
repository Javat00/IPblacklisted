import csv
import dns.resolver
import xlsxwriter


def check_ip(csv_file):
    # Lista para almacenar las IPs
    ip_list = []

    # Lee el archivo CSV y agrega las IPs a la lista
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            ip_list.append(row['ip'])

    # Crea un archivo Excel y agrega una hoja de cálculo
    workbook = xlsxwriter.Workbook('ips_spamhaus.xlsx')
    worksheet = workbook.add_worksheet()

    # Agrega encabezados de columna
    worksheet.write(0, 0, 'IP')
    worksheet.write(0, 1, 'Blacklist')

    # Itera sobre la lista de IPs y verifica si están en la lista negra
    row = 1
    for ip in ip_list:
        query = '.'.join(reversed(str(ip).split('.'))) + '.zen.spamhaus.org'
        try:
            answers = dns.resolver.resolve(query, 'A')
            worksheet.write(row, 0, ip)
            worksheet.write(row, 1, 'Si')
        except dns.resolver.NXDOMAIN:
            worksheet.write(row, 0, ip)
            worksheet.write(row, 1, 'No')
        row += 1

    # Cierra el archivo Excel
    workbook.close()


if __name__ == "__main__":
    # Nombre del archivo CSV
    csv_file = 'ips.csv'
    check_ip(csv_file)
