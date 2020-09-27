import ntplib
from time import ctime


def get_ntp_offset():
    c = ntplib.NTPClient()
    response = c.request('europe.pool.ntp.org', version=3)
    with open('ntp_data.txt', 'w') as file:
        file.write(
            f'{response.offset},{ctime(response.tx_time)},{ntplib.leap_to_text(response.leap)},{response.root_delay}')


if __name__ == '__main__':
    get_ntp_offset()
