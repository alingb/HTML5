#!/usr/bin/env python

# -*-encoding:utf-8-*-
import urllib, urllib2
import re
from subprocess import Popen, PIPE
import json
import datetime
import shlex
import MySQLdb
import sys
import os


class Collect(object):
    def cpu(self):
        cmd = 'dmidecode -t 4'
        info = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        info = info.stdout.read(); n = 0
        dmi_info = ''
        for i in info.split('\n'):
            if i.startswith('SMBIOS'):
                n += 1
            if n < 2:
                dmi_info += i + "\n"
        if n > 1:
            info = dmi_info
        cpu_info = re.findall(r'\sVersion:(.*CPU.*)', info, re.M)
        cpu_num = len(cpu_info)
        cpu = [i for i in set(cpu_info) if i][0].split('CPU')[1].strip()
        return {"cpu_data": cpu, "cpu_num": cpu_num, "cpu": "%s  (%s)" % (cpu, cpu_num)}


    def mem(self):
        cmd = '/usr/sbin/dmidecode -t 17'
        info = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True);
        info = info.stdout.read()
        n = 0
        dmi_info = ''
        for i in info.split('\n'):
            if i.startswith('SMBIOS'):
                n += 1
            if n < 2:
                dmi_info += i + "\n"
        if n > 1:
            info = dmi_info
        size = re.compile(r'Size:[\s]+([\d]+[\s]+[a-zA-Z]{1,2})', re.M)
        mz = re.compile(r'\t+Speed:\s+([\d]+\s+MHz)', re.M)
        with open('/proc/meminfo') as fd:
            mess = fd.read()
        total = re.compile(r'MemTotal:[\s]+([\d]+)[\s]+[a-zA-Z]{2}', re.M)
        mem_mz = set(mz.findall(info)).pop()
        mem_size = set(size.findall(info)).pop()
        mem_num = len(size.findall(info))
        #        mem_total = total.search(mess)
        #        if mem_total:
        #            mem_total = str(int(mem_total.group(1)) / 1024 / 1024) + 'GB'
        #        else:
        #            mem_total = ''
        return {'mem_size': mem_size, 'mem_mz': mem_mz, 'mem_num': mem_num, 'memory': "%s  (%s)" % (mem_size, mem_num)}


    def raidDisk(self):
        cmd = '/opt/MegaRAID/MegaCli/MegaCli64 -cfgdsply -aall'
        try:
            info = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
            info = info.stdout.read()
            raid = re.search(r'Product Name: (.*)', info)
        except OSError:
            raid = ''
        dic = {}
        diskRaid = self.diskRaid()
        if raid:
            raid = raid.group(1).split()
            raid = raid[0] + ' ' + raid[-1]
            cmd = '/opt/MegaRAID/MegaCli/MegaCli64 -pdlist -aall'
            mess = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
            mess = mess.stdout.read()
            size_gen = re.compile(r'Raw Size:\s+([\d.]+\s[A-Z]{2})', re.M)
            data_gen = re.compile(r'Inquiry Data:\s+(.*)', re.M)
            num_gen = re.compile(r'Slot (Number: [\d]+)', re.M)
            Type = re.compile(r'PD (Type: [A-Z]+)')
            size = size_gen.findall(mess)
            data = data_gen.findall(mess)
            num = num_gen.findall(mess)
            Type = Type.findall(mess)
            data = [i.split() for i in data if i]
            t = 0
            disk_locate = ''
            for i in data:
                disk_locate += '%s    %s    %s    %s %s\n' % (num[t], Type[t], size[t], i[0][8:], i[1])
                t += 1
            argv = []
            for i in data:
                if len(i[0]) < 8:
                    argv.append(i[1])
                else:
                    argv.append(i[0][8:])
            data_argv = []
            size_argv = []
            for i in set(argv):
                data_argv.append(i)
            for i in set(size):
                size_argv.append(i)
            num = len(data_argv)
            for y in data_argv:
                number = 0
                for i in argv:
                    if y == i:
                        number += 1
                dic[y] = number
            disk_num = sum(dic.values())
        else:
            raid = diskRaid['raid']
            disk_locate = ''
            disk_num = 0
        dic.update(diskRaid['disk'])
        disk_num = disk_num + diskRaid['disk_num']
        return {'disk': dic, 'raid': raid, 'disk_num': disk_num, 'disk_locate': disk_locate}

    def diskRaid(self):
        raid = Popen("lspci | grep SAS | awk -F : '{print $3}' | awk -F [ '{print $1}'", stdout=PIPE, stderr=PIPE,
                     shell=True)
        raid = raid.stdout.read().strip()
        cmd = '/usr/bin/lsscsi|grep -v SanDisk | grep -v scsi'
        info = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        info = info.stdout.read()
        disk_name = re.findall(r'/dev/sd.*', info, re.M)
        mess = []
        for i in disk_name:
            cmd = '/usr/sbin/smartctl -i %s' % i
            info = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
            info = info.stdout.readlines()
            for a in info:
                if a.startswith('Device Model'):
                    mess.append(a.split(':')[1].strip())
                elif a.startswith('Product'):
                    mess.append(a.split(':')[1].strip())
        dic = {}
        for d in set(mess):
            if 'Ultra' not in d:
                num = mess.count(d)
                dic[d] = num
        disk_num = sum(dic.values())
        return {'disk': dic, 'raid': raid, 'disk_num': disk_num}

    def raidNum(self):
        raid_num = []
        cmd = '/opt/MegaRAID/MegaCli/MegaCli64 -cfgdsply -a0'
        info = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        info = info.stdout.read()
        if info:
            for i in info.split('\n'):
                if i.startswith('Device Id:'):
                    raid_num.append(i.split(':')[1].strip())
        return raid_num

    def smart(self):
        info = Popen('ls /dev/ | grep ^sd | grep -v [0-9]', stdout=PIPE, stderr=PIPE, shell=True)
        disk_info = info.stdout.read().split()
        disk_parse_num = len(disk_info)
        message = ''
        for i in disk_info:
            smart_info = ''
            data = Popen('smartctl -i /dev/%s ' % i, stdout=PIPE, stderr=PIPE, shell=True)
            data = data.stdout.read()
            info = Popen('smartctl -A /dev/%s ' % i, stdout=PIPE, stderr=PIPE, shell=True)
            info = info.stdout.read().split('\n\n')[1].strip()
            if '/dev/%s' % i not in info:
                for k in info.split('\n'):
                    if k:
                        smart_info += k + '\n'
            else:
                smart_info = ''
            for j in data.split('\n'):
                if j.startswith('Device Model'):
                    message += 'POSITION: %s\nmodel: %s\n' % (i, j.split(':')[1].strip())
                if j.startswith('Serial Number'):
                    message += 'DISK SN: %s\n' % j.split(':')[1].strip()
                if j.startswith('User Capacity'):
                    message += 'DISK SIZE: %s\n' % j.split('[')[1][:-1]
            if message:
                message += '\n%s\n\n' % smart_info.strip()
        raid_num = sorted(self.raidNum())
        if raid_num:
            for i in raid_num:
                smart_info = ''
                data = Popen('smartctl -i -d megaraid,%s /dev/sda ' % i, stdout=PIPE, stderr=PIPE, shell=True)
                data = data.stdout.read().split('\n')
                info = Popen('smartctl -A -d megaraid,%s /dev/sda ' % i, stdout=PIPE, stderr=PIPE, shell=True)
                info = info.stdout.read().split('\n\n')[1].strip()
                if '/dev/' not in info:
                    for k in info.split('\n'):
                        if k:
                            smart_info += k + '\n'
                else:
                    smart_info = ''
                if not smart_info:
                    data = Popen('smartctl -i -d sat+megaraid,%s /dev/sda ' % i, stdout=PIPE, stderr=PIPE, shell=True)
                    data = data.stdout.read().split('\n')
                    info = Popen('smartctl -A -d sat+megaraid,%s /dev/sda ' % i, stdout=PIPE, stderr=PIPE, shell=True)
                    info = info.stdout.read().split('\n\n')[1].strip()
                if '/dev/' not in info:
                    smart_info = info + '\n'
                else:
                    smart_info = ''
                for j in data:
                    if j.startswith('Device Model'):
                        message += 'POSITION: %s\nmodel: %s\n' % (i, j.split(':')[1].strip())
                    if j.startswith('Serial Number'):
                        message += 'DISK SN: %s\n' % j.split(':')[1].strip()
                    if j.startswith('User Capacity'):
                        message += 'DISK SIZE: %s\n' % j.split('[')[1][:-1]
                if message:
                    message += '\n%s\n\n' % smart_info.strip()
        return {'smart_info': message.strip()}

    def mac(self):
        info = Popen(['/sbin/ifconfig'], stdout=PIPE, stderr=PIPE, shell=True)
        info = info.stdout.read()
        mac = re.compile(r'HWaddr\s([\da-fA-Z:]{17})', re.M)
        ip_gen = re.compile(r'inet addr:(192.168.1.\d{1,3})', re.M)
        ip = ip_gen.search(info)
        if ip:
            ip = str(ip.group(1))
        else:
            ip_gen = re.compile(r'inet\s(192.168.1.\d{1,3})', re.M)
            ip = ip_gen.search(info)
            if ip:
                ip = str(ip.group(1))
            else:
                ip = ''
        mess = [i for i in info.split('\n') if
                i and not i.startswith('virbr') and not i.startswith('ib0') and not i.startswith('lo')]
        list = []
        dic = {}
        for i in mess:
            if i[0].strip():
                list.append(i.split()[0])
        for i in list:
            if i.startswith('ib0'):
                list.remove(i)
            if i.startswith('lo'):
                list.remove(i)
            if i.startswith('virbr0'):
                list.remove(i)
        mac_find_info = ''
        for i in info.split('\n\n'):
            if not i.startswith('virbr') and not i.startswith('lo'):
                mac_find_info += i + '\n'
        mac = mac.findall(mac_find_info)
        if not mac:
            mac = re.compile(r'ether\s([\da-fA-Z:]{17})', re.M)
            mac = mac.findall(mac_find_info)
        num = len(list)
        for i in xrange(num):
            dic[list[i]] = mac[i]
        return {'mac': dic, 'mac_addr': str(mac), 'ip': ip}

    @property
    def net(self):
        info = Popen(['/sbin/lspci -v'], stdout=PIPE, stderr=PIPE, shell=True)
        info = info.stdout.read()
        ethe = re.compile(r'Ethernet controller:\s+(.*)', re.M)
        list = []
        dic = {}
        network = ethe.findall(info)
        for i in network:
            i = i.split()[2:-2]
            i = ' '.join(i)
            list.append(i)
        for i in set(list):
            num = 0
            for y in list:
                if i == y:
                    num += 1
            dic[i] = num
        return {'network': dic}

    def sn(self):
        cmd = '/usr/sbin/dmidecode'
        info = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        info = info.stdout.read()
        n = 0
        dmi_info = ''
        for i in info.split('\n'):
            if i.startswith('SMBIOS'):
                n += 1
            if n < 2:
                dmi_info += i + "\n"
        if n > 1:
            info = dmi_info
        sn_info = re.findall(r'Serial Number:\s+(.*)', info, re.M)
        if len(sn_info[:2]) == 2:
            sn = sn_info[0]
            sn_1 = sn_info[1]
        else:
            sn = sn_info[0]
            sn_1 = ''
        return {'sn': str(sn.strip()), 'sn_1': str(sn_1.strip())}

    def time(self):
        time = datetime.datetime.now()
        time = time.strftime('%Y-%m-%d %H:%M')
        return {'time': time}

    def name(self):
        info = Popen(['/usr/sbin/dmidecode'], stdout=PIPE, stderr=PIPE, shell=True)
        info = info.stdout.read()
        bios_info = Popen(['/usr/sbin/dmidecode -t bios'], stdout=PIPE, stderr=PIPE, shell=True)
        bios_info = bios_info.stdout.read()
        n = 0
        dmi_info = ''
        for i in info.split('\n'):
            if i.startswith('SMBIOS'):
                n += 1
            if n < 2:
                dmi_info += i + "\n"
        if n > 1:
            info = dmi_info
        bios_gen = re.compile(r'Version:\s+(.*)', re.M)
        product = re.compile(r'Product Name:\s+(.*)', re.M)
        bios = bios_gen.search(bios_info)
        family_gen = re.compile(r'Family:\s+(.*)', re.M)
        if bios:
            bios = bios.group(1).strip()
        else:
            bios = ''
        nameinfo = product.findall(info)
        if len(nameinfo) == 2:
            name = nameinfo[0]
            name1 = nameinfo[1]
        else:
            name = nameinfo[0]
            name1 = ''
        family = family_gen.search(info)
        if family:
            family = family.group(1)
        else:
            family = ''
        return {'bios': bios, 'name': name.strip(), 'name1': name1.strip(), 'family': family}

    def bmc(self):
        cmd = '/usr/local/bin/ipmitool mc info'
        try:
            info = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
            info = info.stdout.read()
            bmc = re.search(r'Firmware Revision\s+:\s+(.*)', info, re.M)
        except OSError:
            bmc = ''
        if bmc:
            bmc = bmc.group(1)
        else:
            bmc = ''
        return {'bmc': bmc}

    def fru(self):
        cmd = '/usr/local/bin/ipmitool fru'
        cmd1 = '/usr/sbin/dmidecode -t 1'
        cmd2 = '/usr/sbin/dmidecode -t 2'
        info = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        fru = info.stdout.read()
        if not fru:
            info1 = Popen(cmd1, stdout=PIPE, stderr=PIPE, shell=True)
            info2 = Popen(cmd2, stdout=PIPE, stderr=PIPE, shell=True)
            info1 = info1.stdout.readlines()
            info2 = info2.stdout.readlines()
            for i in info1[5:]:
                if i.strip():
                    fru = fru + i
            for i in info2[5:]:
                if i.strip():
                    fru = fru + i
        fru_info = ''
        fru_version = ''
        if fru:
            for mess in fru.split('\n'):
                if mess:
                    if 'Date' not in mess:
                        if len(mess.split(' : ')) == 2:
                            k, v = mess.split(' : ')
                            if v.strip() == 'N/A' or not v.strip():
                                pass
                            else:
                                fru_info += '%s : %s\n' % (k, v)
                    else:
                        fru_info += mess + '\n'
            fru_version = re.search(r'Product Version\s*:\s(.*)', fru_info, re.M)
            if fru_version:
                fru_version = fru_version.group(1).strip()
        return {"fru": fru_info, 'fru_version': fru_version}

    def sel(self):
        cmd = "/usr/local/bin/ipmitool sel list"
        info = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        sel = info.stdout.read()
        return {'sel': sel}

    def hostName(self):
        info = Popen('hostname', stdout=PIPE, stderr=PIPE)
        hostname = info.stdout.read().strip()
        data = Popen('ps aux | grep shutdown | grep -v grep | wc -l', stdout=PIPE, stderr=PIPE, shell=True)
        num = int(data.stdout.read())
        if num == 0:
            power = 'UNSET'
        else:
            try:
                with open('/root/shutdown.time') as fd:
                    msg_info = fd.read().split(',')[0].split('for')[1].split()[1:-1]
                    msg = msg_info[0] + ' ' + msg_info[1]
            except:
                msg = 'SET'
            power = msg
        return {'hostname': hostname, 'power': power}

    @staticmethod
    def bootTime():
        info = Popen('date -d "$(awk -F. \'{print $1}\' /proc/uptime) second ago" +"%Y-%m-%d %H:%M"', stdout=PIPE,
                     stderr=PIPE, shell=True)
        boot_time = info.stdout.read().strip()
        return {'boot_time': boot_time}

    def biosTime(self):
        info = Popen('hwclock -r', stdout=PIPE, stderr=PIPE, shell=True)
        bios_time = info.stdout.read().strip()
        return {'bios_time': bios_time}


class DiskInfo(object):
    def __init__(self):
        self.disk_info = self.disk()

    def disk(self):
        cmd = '/bin/lsblk -b'
        info = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE)
        info = info.stdout.read()
        return info

    def parse(self, argv):
        disk = re.compile(r'(%s)' % argv, re.M)
        data = disk.findall(self.disk_info)
        return data

    def getDisk(self):
        dic = {}
        dic['disk_4t'] = len(self.parse('4000787030016'))
        dic['disk_2t'] = len(self.parse('2000398934016'))
        dic['disk_1t'] = len(self.parse('1000204886016'))
        dic['ssd_960'] = len(self.parse('960197124096'))
        dic['ssd_240'] = len(self.parse('240057409536'))
        dic['ssd_128'] = len(self.parse('128032974848'))
        dic['ssd_128_1'] = len(self.parse('128035676160'))
        dic['ssd_64'] = len(self.parse('64017212928'))
        dic['ssd_600'] = len(self.parse('600127266816'))
        return dic


class CheckInfo(object):
    def __init__(self, dic, name, family):
        self.dic = dic
        self.name = name
        self.family = family
        self.disk = DiskInfo().getDisk()

    def info(self):
        if self.dic['name'] in self.name or self.dic['family'] in self.family:
            for i in self.name:
                if i == self.dic['name']:
                    return self.check(i)
            for i in self.family:
                if i == self.dic['family']:
                    return self.check(i)
        else:
            ret = []
            if os.path.exists('/var/log/breakin.log'):
                with open('/var/log/breakin.log', 'r') as fd:
                    msg = fd.read()
                    for i in msg.split():
                        if i == 'hpl':
                            ret.append('breakin-hpl')
                        if i == 'fail':
                            ret.append('breakin-fail')
                        if i == 'ecc':
                            ret.append('breakin-ecc')
                        if i == 'failid':
                            if 'No IPMI' not in msg:
                                ret.append('breakin-failid')
                        if i == 'hdhealth':
                            ret.append('breakin-hdhealth')
                        if i == 'mcelog':
                            ret.append('breakin-mcelog')
            if len(ret) == 0:
                return {'status': 'no check data'}
            else:
                return {'status': str(list(set(ret)))}

    def memLocatorInfo(self):
        #        RG_RCD6000_Main = """NODE 1	 DIMM_A0	 16384 MB	 2400 MHz	 1866 MHz
        # NODE 1	 DIMM_A1	 16384 MB	 2400 MHz	 1866 MHz
        # NODE 1	 DIMM_B0	 16384 MB	 2400 MHz	 1866 MHz
        # NODE 1	 DIMM_B1	 No Module Installed	 Unknown	 Unknown
        # NODE 2	 DIMM_C0	 16384 MB	 2400 MHz	 1866 MHz
        # NODE 2	 DIMM_C1	 No Module Installed	 Unknown	 Unknown
        # NODE 2	 DIMM_D0	 16384 MB	 2400 MHz	 1866 MHz
        # NODE 2	 DIMM_D1	 No Module Installed	 Unknown	 Unknown
        # NODE 3	 DIMM_A0	 16384 MB	 2400 MHz	 1866 MHz
        # NODE 3	 DIMM_A1	 16384 MB	 2400 MHz	 1866 MHz
        # NODE 3	 DIMM_B0	 16384 MB	 2400 MHz	 1866 MHz
        # NODE 3	 DIMM_B1	 No Module Installed	 Unknown	 Unknown
        # NODE 4	 DIMM_C0	 16384 MB	 2400 MHz	 1866 MHz
        # NODE 4	 DIMM_C1	 No Module Installed	 Unknown	 Unknown
        # NODE 4	 DIMM_D0	 16384 MB	 2400 MHz	 1866 MHz
        # NODE 4	 DIMM_D1	 No Module Installed	 Unknown	 Unknown"""
        #        RG_RCD6000_Office = """NODE 1	 DIMM_A0	 16384 MB	 2400 MHz	 1866 MHz
        # NODE 1	 DIMM_A1	 16384 MB	 2400 MHz	 1866 MHz
        # NODE 1	 DIMM_B0	 16384 MB	 2400 MHz	 1866 MHz
        # NODE 1	 DIMM_B1	 No Module Installed	 Unknown	 Unknown
        # NODE 2	 DIMM_C0	 16384 MB	 2400 MHz	 1866 MHz
        # NODE 2	 DIMM_C1	 No Module Installed	 Unknown	 Unknown
        # NODE 2	 DIMM_D0	 16384 MB	 2400 MHz	 1866 MHz
        # NODE 2	 DIMM_D1	 No Module Installed	 Unknown	 Unknown
        # NODE 3	 DIMM_A0	 16384 MB	 2400 MHz	 1866 MHz
        # NODE 3	 DIMM_A1	 16384 MB	 2400 MHz	 1866 MHz
        # NODE 3	 DIMM_B0	 16384 MB	 2400 MHz	 1866 MHz
        # NODE 3	 DIMM_B1	 No Module Installed	 Unknown	 Unknown
        # NODE 4	 DIMM_C0	 16384 MB	 2400 MHz	 1866 MHz
        # NODE 4	 DIMM_C1	 No Module Installed	 Unknown	 Unknown
        # NODE 4	 DIMM_D0	 16384 MB	 2400 MHz	 1866 MHz
        # NODE 4	 DIMM_D1	 No Module Installed	 Unknown	 Unknown"""
        #        RG_RCM1000_Edu = """BANK 0	 DIMM_A1	 No Module Installed	 Unknown	 Unknown
        # BANK 1	 DIMM_A2	 No Module Installed	 Unknown	 Unknown
        # BANK 2	 DIMM_B1	 No Module Installed	 Unknown	 Unknown
        # BANK 3	 DIMM_B2	 16384 MB	 2133 MHz	 2133 MHz"""
        #        RG_RCM1000_Office = """BANK 0	 DIMM_A1	 No Module Installed	 Unknown	 Unknown
        # BANK 1	 DIMM_A2	 No Module Installed	 Unknown	 Unknown
        # BANK 2	 DIMM_B1	 No Module Installed	 Unknown	 Unknown
        # BANK 3	 DIMM_B2	 16384 MB	 2133 MHz	 2133 MHz"""
        #        RG_RCP = """BANK 0	 DIMM_A1	 8192 MB	 1600 MHz	 1600 MHz
        # BANK 1	 DIMM_A2	 No Module Installed	 Unknown	 Unknown
        # BANK 2	 DIMM_B1	 No Module Installed	 Unknown	 Unknown
        # BANK 3	 DIMM_B2	 No Module Installed	 Unknown	 Unknown"""
        #        RG_SE04 = """DIMM_A1	 DIMM_A1	 8192 MB	 1600 MHz	 1600 MHz
        # DIMM_A2	 DIMM_A2	 No Module Installed	 Unknown	 Unknown
        # DIMM_B1	 DIMM_B1	 8192 MB	 1600 MHz	 1600 MHz
        # DIMM_B2	 DIMM_B2	 No Module Installed	 Unknown	 Unknown
        # DIMM_C1	 DIMM_C1	 No Module Installed	 Unknown	 Unknown
        # DIMM_C2	 DIMM_C2	 No Module Installed	 Unknown	 Unknown
        # DIMM_D1	 DIMM_D1	 No Module Installed	 Unknown	 Unknown
        # DIMM_D2	 DIMM_D2	 No Module Installed	 Unknown	 Unknown
        # DIMM_E1	 DIMM_E1	 No Module Installed	 Unknown	 Unknown
        # DIMM_E2	 DIMM_E2	 No Module Installed	 Unknown	 Unknown
        # DIMM_F1	 DIMM_F1	 No Module Installed	 Unknown	 Unknown
        # DIMM_F2	 DIMM_F2	 No Module Installed	 Unknown	 Unknown
        # DIMM_G1	 DIMM_G1	 No Module Installed	 Unknown	 Unknown
        # DIMM_G2	 DIMM_G2	 No Module Installed	 Unknown	 Unknown
        # DIMM_H1	 DIMM_H1	 No Module Installed	 Unknown	 Unknown
        # DIMM_H2	 DIMM_H2	 No Module Installed	 Unknown	 Unknown"""
        #        Elog = """BANK 0	 DIMM_A1	 8192 MB	 1600 MHz	 1600 MHz
        # BANK 1	 DIMM_A2	 No Module Installed	 Unknown	 Unknown
        # BANK 2	 DIMM_B1	 No Module Installed	 Unknown	 Unknown
        # BANK 3	 DIMM_B2	 No Module Installed	 Unknown	 Unknown"""
        #        RG_ONC_AIO_E = """NODE 1	 DIMM_A1	 16384 MB	 2400 MHz	 1866 MHz
        # NODE 1	 DIMM_A2	 No Module Installed	 Unknown	 Unknown
        # NODE 1	 DIMM_B1	 16384 MB	 2400 MHz	 1866 MHz
        # NODE 1	 DIMM_B2	 No Module Installed	 Unknown	 Unknown
        # NODE 1	 DIMM_C1	 No Module Installed	 Unknown	 Unknown
        # NODE 1	 DIMM_C2	 No Module Installed	 Unknown	 Unknown
        # NODE 1	 DIMM_D1	 No Module Installed	 Unknown	 Unknown
        # NODE 1	 DIMM_D2	 No Module Installed	 Unknown	 Unknown
        # NODE 2	 DIMM_E1	 No Module Installed	 Unknown	 Unknown
        # NODE 2	 DIMM_E2	 No Module Installed	 Unknown	 Unknown
        # NODE 2	 DIMM_F1	 No Module Installed	 Unknown	 Unknown
        # NODE 2	 DIMM_F2	 No Module Installed	 Unknown	 Unknown
        # NODE 2	 DIMM_G1	 No Module Installed	 Unknown	 Unknown
        # NODE 2	 DIMM_G2	 No Module Installed	 Unknown	 Unknown
        # NODE 2	 DIMM_H1	 No Module Installed	 Unknown	 Unknown
        # NODE 2	 DIMM_H2	 No Module Installed	 Unknown	 Unknown"""
        #        UDS1022_G1 = """_Node0_Channel0_Dimm0	 DIMM_A0	 16384 MB	 2133 MHz	 1600 MHz
        # _Node0_Channel0_Dimm1	 DIMM_A1	 No Module Installed	 Unknown	 Unknown
        # _Node0_Channel0_Dimm2	 DIMM_A2	 No Module Installed	 Unknown	 Unknown
        # _Node0_Channel1_Dimm0	 DIMM_B0	 16384 MB	 2133 MHz	 1600 MHz
        # _Node0_Channel1_Dimm1	 DIMM_B1	 No Module Installed	 Unknown	 Unknown
        # _Node0_Channel1_Dimm2	 DIMM_B2	 No Module Installed	 Unknown	 Unknown
        # _Node0_Channel2_Dimm0	 DIMM_C0	 16384 MB	 2133 MHz	 1600 MHz
        # _Node0_Channel2_Dimm1	 DIMM_C1	 No Module Installed	 Unknown	 Unknown
        # _Node0_Channel2_Dimm2	 DIMM_C2	 No Module Installed	 Unknown	 Unknown
        # _Node0_Channel3_Dimm0	 DIMM_D0	 16384 MB	 2133 MHz	 1600 MHz
        # _Node0_Channel3_Dimm1	 DIMM_D1	 No Module Installed	 Unknown	 Unknown
        # _Node0_Channel3_Dimm2	 DIMM_D2	 No Module Installed	 Unknown	 Unknown
        # _Node1_Channel0_Dimm0	 DIMM_E0	 16384 MB	 2133 MHz	 1600 MHz
        # _Node1_Channel0_Dimm1	 DIMM_E1	 No Module Installed	 Unknown	 Unknown
        # _Node1_Channel0_Dimm2	 DIMM_E2	 No Module Installed	 Unknown	 Unknown
        # _Node1_Channel1_Dimm0	 DIMM_F0	 16384 MB	 2133 MHz	 1600 MHz
        # _Node1_Channel1_Dimm1	 DIMM_F1	 No Module Installed	 Unknown	 Unknown
        # _Node1_Channel1_Dimm2	 DIMM_F2	 No Module Installed	 Unknown	 Unknown
        # _Node1_Channel2_Dimm0	 DIMM_G0	 16384 MB	 2133 MHz	 1600 MHz
        # _Node1_Channel2_Dimm1	 DIMM_G1	 No Module Installed	 Unknown	 Unknown
        # _Node1_Channel2_Dimm2	 DIMM_G2	 No Module Installed	 Unknown	 Unknown
        # _Node1_Channel3_Dimm0	 DIMM_H0	 16384 MB	 2133 MHz	 1600 MHz
        # _Node1_Channel3_Dimm1	 DIMM_H1	 No Module Installed	 Unknown	 Unknown
        # _Node1_Channel3_Dimm2	 DIMM_H2	 No Module Installed	 Unknown	 Unknown"""
        #        XINWEIH_C612_ASERVER_2400 = """NODE 1	 DIMM_A1	 32 GB	 2400 MHz	 2400 MHz
        # NODE 1	 DIMM_A2	 No Module Installed	 Unknown	 Unknown
        # NODE 1	 DIMM_B1	 32 GB	 2400 MHz	 2400 MHz
        # NODE 1	 DIMM_B2	 No Module Installed	 Unknown	 Unknown
        # NODE 2	 DIMM_C1	 No Module Installed	 Unknown	 Unknown
        # NODE 2	 DIMM_C2	 No Module Installed	 Unknown	 Unknown
        # NODE 2	 DIMM_D1	 No Module Installed	 Unknown	 Unknown
        # NODE 2	 DIMM_D2	 No Module Installed	 Unknown	 Unknown
        # NODE 3	 DIMM_E1	 32 GB	 2400 MHz	 2400 MHz
        # NODE 3	 DIMM_E2	 No Module Installed	 Unknown	 Unknown
        # NODE 3	 DIMM_F1	 32 GB	 2400 MHz	 2400 MHz
        # NODE 3	 DIMM_F2	 No Module Installed	 Unknown	 Unknown
        # NODE 4	 DIMM_G1	 No Module Installed	 Unknown	 Unknown
        # NODE 4	 DIMM_G2	 No Module Installed	 Unknown	 Unknown
        # NODE 4	 DIMM_H1	 No Module Installed	 Unknown	 Unknown
        # NODE 4	 DIMM_H2	 No Module Installed	 Unknown	 Unknown"""
        #        XINWEIH_C612_ASERVER_2405 = """NODE 1	 DIMM_A1	 32 GB	 2400 MHz	 2400 MHz
        # NODE 1	 DIMM_A2	 No Module Installed	 Unknown	 Unknown
        # NODE 1	 DIMM_B1	 32 GB	 2400 MHz	 2400 MHz
        # NODE 1	 DIMM_B2	 No Module Installed	 Unknown	 Unknown
        # NODE 2	 DIMM_C1	 No Module Installed	 Unknown	 Unknown
        # NODE 2	 DIMM_C2	 No Module Installed	 Unknown	 Unknown
        # NODE 2	 DIMM_D1	 No Module Installed	 Unknown	 Unknown
        # NODE 2	 DIMM_D2	 No Module Installed	 Unknown	 Unknown
        # NODE 3	 DIMM_E1	 32 GB	 2400 MHz	 2400 MHz
        # NODE 3	 DIMM_E2	 No Module Installed	 Unknown	 Unknown
        # NODE 3	 DIMM_F1	 32 GB	 2400 MHz	 2400 MHz
        # NODE 3	 DIMM_F2	 No Module Installed	 Unknown	 Unknown
        # NODE 4	 DIMM_G1	 No Module Installed	 Unknown	 Unknown
        # NODE 4	 DIMM_G2	 No Module Installed	 Unknown	 Unknown
        # NODE 4	 DIMM_H1	 No Module Installed	 Unknown	 Unknown
        # NODE 4	 DIMM_H2	 No Module Installed	 Unknown	 Unknown"""
        #        XINWEIH_C612_VDS_8050 = """NODE 1	 DIMM_A1	 32 GB	 2400 MHz	 2400 MHz
        # NODE 1	 DIMM_A2	 No Module Installed	 Unknown	 Unknown
        # NODE 1	 DIMM_B1	 32 GB	 2400 MHz	 2400 MHz
        # NODE 1	 DIMM_B2	 No Module Installed	 Unknown	 Unknown
        # NODE 2	 DIMM_C1	 32 GB	 2400 MHz	 2400 MHz
        # NODE 2	 DIMM_C2	 No Module Installed	 Unknown	 Unknown
        # NODE 2	 DIMM_D1	 32 GB	 2400 MHz	 2400 MHz
        # NODE 2	 DIMM_D2	 No Module Installed	 Unknown	 Unknown
        # NODE 3	 DIMM_E1	 32 GB	 2400 MHz	 2400 MHz
        # NODE 3	 DIMM_E2	 No Module Installed	 Unknown	 Unknown
        # NODE 3	 DIMM_F1	 32 GB	 2400 MHz	 2400 MHz
        # NODE 3	 DIMM_F2	 No Module Installed	 Unknown	 Unknown
        # NODE 4	 DIMM_G1	 32 GB	 2400 MHz	 2400 MHz
        # NODE 4	 DIMM_G2	 No Module Installed	 Unknown	 Unknown
        # NODE 4	 DIMM_H1	 32 GB	 2400 MHz	 2400 MHz
        # NODE 4	 DIMM_H2	 No Module Installed	 Unknown	 Unknown"""
        RG_RCD6000_Main = """NODE 1	 DIMM_A0
NODE 1	 DIMM_A1
NODE 1	 DIMM_B0
NODE 2	 DIMM_C0
NODE 2	 DIMM_D0
NODE 3	 DIMM_A0
NODE 3	 DIMM_A1
NODE 3	 DIMM_B0
NODE 4	 DIMM_C0
NODE 4	 DIMM_D0"""
        RG_RCD6000_Office = """NODE 1	 DIMM_A0
NODE 1	 DIMM_A1
NODE 1	 DIMM_B0
NODE 2	 DIMM_C0
NODE 2	 DIMM_D0
NODE 3	 DIMM_A0
NODE 3	 DIMM_A1
NODE 3	 DIMM_B0
NODE 4	 DIMM_C0
NODE 4	 DIMM_D0"""
        RG_RCM1000_Edu = """BANK 3	 DIMM_B2"""
        RG_RCM1000_Office = """BANK 3	 DIMM_B2"""
        RG_RCP = """BANK 0	 DIMM_A1"""
        RG_SE04 = """DIMM_A1	 DIMM_A1
DIMM_B1	 DIMM_B1"""
        Elog = """BANK 0	 DIMM_A1"""
        RG_ONC_AIO_E = """NODE 1	 DIMM_A1
NODE 1	 DIMM_B1"""
        UDS1022_G1 = """_Node0_Channel0_Dimm0	 DIMM_A0
_Node0_Channel1_Dimm0	 DIMM_B0
_Node0_Channel2_Dimm0	 DIMM_C0
_Node0_Channel3_Dimm0	 DIMM_D0
_Node1_Channel0_Dimm0	 DIMM_E0
_Node1_Channel1_Dimm0	 DIMM_F0
_Node1_Channel2_Dimm0	 DIMM_G0
_Node1_Channel3_Dimm0	 DIMM_H0"""
        XINWEIH_C612_ASERVER_2400 = """NODE 1	 DIMM_A1
NODE 1	 DIMM_B1
NODE 3	 DIMM_E1
NODE 3	 DIMM_F1"""
        XINWEIH_C612_ASERVER_2405 = """NODE 1	 DIMM_A1
NODE 1	 DIMM_B1
NODE 3	 DIMM_E1
NODE 3	 DIMM_F1"""
        XINWEIH_C612_VDS_8050 = """NODE 1	 DIMM_A1
NODE 1	 DIMM_B1
NODE 2	 DIMM_C1
NODE 2	 DIMM_D1
NODE 3	 DIMM_E1
NODE 3	 DIMM_F1
NODE 4	 DIMM_G1
NODE 4	 DIMM_H1"""
        RG_iData_Server = """NODE 1		DIMM_A0
NODE 1   DIMM_A1 
NODE 1   DIMM_B0 
NODE 1   DIMM_B1 
NODE 2   DIMM_C0 
NODE 2   DIMM_C1 
NODE 2   DIMM_D0 
NODE 2   DIMM_D1 
NODE 3   DIMM_A0 
NODE 3   DIMM_A1 
NODE 3   DIMM_B0 
NODE 3   DIMM_B1 
NODE 4   DIMM_C0 
NODE 4   DIMM_C1 
NODE 4   DIMM_D0 
NODE 4   DIMM_D1"""
        dic = {'RG-RCD6000-Main': RG_RCD6000_Main, 'RG-RCD6000-Office': RG_RCD6000_Office,
               'RG-RCM1000-Edu': RG_RCM1000_Edu, 'RG-RCM1000-Office': RG_RCM1000_Office, 'RG-RCP': RG_RCP,
               'RG-SE04': RG_SE04, 'Elog': Elog, 'RG-ONC-AIO-E': RG_ONC_AIO_E, 'UDS1022-G1': UDS1022_G1,
               'XINWEIH_C612_ASERVER-2400': XINWEIH_C612_ASERVER_2400,
               'XINWEIH_C612_ASERVER-2405': XINWEIH_C612_ASERVER_2405, 'XINWEIH_C612_VDS-8050': XINWEIH_C612_VDS_8050,
               'RG_iData_Server': RG_iData_Server}
        return dic

    def memLocator(slef):
        info = Popen('/usr/sbin/dmidecode -t 17', stdout=PIPE, stderr=PIPE, shell=True)
        info = info.stdout.read()
        n = 0
        dmi_info = ''
        for i in info.split('\n'):
            if i.startswith('SMBIOS'):
                n += 1
            if n < 2:
                dmi_info += i + "\n"
        if n > 1:
            info = dmi_info
        all_mem = re.findall(r'\t+Size:\s+(.*)', info, re.M)
        locate_mem = re.findall(r'\t+Locator:\s+(.*)', info, re.M)
        lo_mem = re.findall(r'\t+Bank Locator:\s+(.*)', info, re.M)
        mem_speed = re.findall(r'\t+Speed:\s+(.*)', info, re.M)
        mem_conf = re.findall(r'\t+Configured Clock Speed:\s+(.*)', info, re.M)
        count = 0
        mem_locate = ''
        for i in locate_mem:
            if 'No' not in all_mem[count]:
                mem_locate += "%s\t %s\n" % (lo_mem[count], i,)

            #            mem_locate += "%s\t %s\t %s\t %s\t %s\n" %(lo_mem[count], i, all_mem[count],
            #                                                       mem_speed[count], mem_conf[count])
            count += 1
        return mem_locate.strip()

    def check(self, info):
        try:
            con = MySQLdb.connect('192.168.1.57', 'trusme', '6286280300', 'command')
        except:
            return {'status': 'mariadb error'}
        cur = con.cursor()
        cmd = "select * from base where name='%s'" % self.dic['name']
        cur.execute(cmd)
        data = cur.fetchall()
        if data:
            data = data[0]
        else:
            cmd = "select * from base where family='%s'" % self.dic['family']
            cur.execute(cmd)
            data = cur.fetchall()[0]
        cpu = data[1]
        cpu_num = int(data[2])
        memory = data[3]
        memory_num = int(data[4])
        disk_num = data[5]
        ssd_num = data[6]
        bios = data[7]
        bmc = data[8]
        speed = data[10]
        mac_num = len(self.dic['mac_addr'].split(','))
        sel = Collect().sel()['sel'].split()
        cur.close()
        con.close()
        pci_info = Popen('lspci | grep "[01|02|03]:00" | grep -v ^00', stdout=PIPE, stderr=PIPE, shell=True)
        pci_info = pci_info.stdout.read()
        pci_check = '''01:00.0 Ethernet controller: Intel Corporation I350 Gigabit Network Connection (rev 01)
01:00.1 Ethernet controller: Intel Corporation I350 Gigabit Network Connection (rev 01)
01:00.2 Ethernet controller: Intel Corporation I350 Gigabit Network Connection (rev 01)
01:00.3 Ethernet controller: Intel Corporation I350 Gigabit Network Connection (rev 01)
02:00.0 Ethernet controller: Intel Corporation 82599ES 10-Gigabit SFI/SFP+ Network Connection (rev 01)
02:00.1 Ethernet controller: Intel Corporation 82599ES 10-Gigabit SFI/SFP+ Network Connection (rev 01)
03:00.0 Serial Attached SCSI controller: LSI Logic / Symbios Logic SAS3008 PCI-Express Fusion-MPT SAS-3 (rev 02)
'''
        ret = []
        check = self.memLocatorInfo()
        mem_loca = self.memLocator()
        for k, v in check.items():
            if self.dic['name'] == k:
                if v != mem_loca:
                    ret.append('mem locator fail')
                break
            if self.dic['family'] == k:
                if v != mem_loca:
                    ret.append('mem locator fail')
                break
        if os.path.exists('/var/log/breakin.log'):
            with open('/var/log/breakin.log', 'r') as fd:
                msg = fd.read()
                for i in msg.split():
                    if i == 'hpl':
                        ret.append('breakin-hpl')
                    if i == 'fail':
                        ret.append('breakin-fail')
                    if i == 'ecc':
                        ret.append('breakin-ecc')
                    if i == 'failid':
                        if 'No IPMI' not in msg:
                            ret.append('breakin-failid')
                    if i == 'hdhealth':
                        ret.append('breakin-hdhealth')
                    if i == 'mcelog':
                        ret.append('breakin-mcelog')
        if memory:
            if self.dic['mem_size'] != memory or self.dic['mem_num'] != memory_num or self.dic['mem_mz'] != speed:
                ret.append('memory fail')
        if cpu:
            if self.dic['cpu_data'] != cpu or self.dic['cpu_num'] != cpu_num:
                ret.append('cpu fail')
        if bios:
            if self.dic['bios'] != bios:
                ret.append('bios fail')
        if bmc:
            if self.dic['bmc'] != bmc:
                ret.append('bmc fail')
        if sel:
            for i in sel:

                if 'ecc' == i.lower():
                    ret.append('ecc erro')
                if 'temperature' == i.lower():
                    ret.append('temperature erro')
                if 'processor' == i.lower():
                    ret.append('process erro')
                if 'fan' == i.lower():
                    ret.append('fan erro')
                if 'lower' == i.lower():
                    ret.append('lower erro')
                if 'high' == i.lower():
                    ret.append('high erro')
                if 'pcie' == i.lower():
                    ret.append('pcie erro')
        if self.dic['name'] == 'UDS1022-G':
            if self.dic['bios'] == 'S2BA3B10':
                if self.dic['fru_version'] != 'V1.10':
                    ret.append('fru fail')
        if self.dic['name'] == 'UDS1022-G':
            if self.dic['bios'] == 'S2B_3B10.01':
                if self.dic['fru_version'] != 'V1.00':
                    ret.append('fru fail')
        if self.dic['name'] == 'UDS1022-G':
            if self.dic['bios'] == 'S2B_3A22':
                if self.dic['fru_version'] != 'V1.00':
                    ret.append('fru fail')
        if self.dic['name'] == 'RG-RCD6000-Main':
            if self.disk['disk_4t'] != disk_num or self.disk['ssd_960'] != ssd_num:
                ret.append('disk fail')
        elif self.dic['name'] == 'RG-RCD6000-Office':
            if self.disk['disk_1t'] != disk_num or self.disk['ssd_960'] != ssd_num:
                ret.append('disk fail')
        elif self.dic['name'] == 'RG-RCM1000-Smart' or self.dic['name'] == 'RG-RCM1000-Office' or self.dic[
            'name'] == 'RG-RCM1000-Edu':
            if self.disk['disk_4t'] != disk_num or self.disk['ssd_240'] != ssd_num:
                ret.append('disk fail')
        elif self.dic['name'] == 'RG-ONC-AIO-E':
            if self.disk['disk_2t'] != 2:
                ret.append('disk fail')
        elif self.dic['name'] == 'UDS1022-G1':
            if self.disk['disk_4t'] != disk_num or self.disk['ssd_600'] != ssd_num:
                ret.append('disk fail')
        elif self.dic['name'] == 'RG-RCP':
            if self.disk['disk_2t'] != disk_num:
                ret.append('disk fail')
        elif self.dic['name'] == 'Elog':
            if self.disk['disk_2t'] != disk_num:
                ret.append('disk fail')
        elif self.dic['name'] == 'RG-SE04':
            if self.disk['disk_2t'] != disk_num:
                ret.append('disk fail')
        elif self.dic['family'] == 'XINWEIH_C612_VDS-5050':
            if self.disk['ssd_64'] != ssd_num:
                ret.append('disk fail')
        elif self.dic['family'] == 'XINWEIH_C612_VDS-6550':
            if self.disk['ssd_64'] != ssd_num:
                ret.append('disk fail')
        elif self.dic['family'] == 'XINWEIH_C612_ASERVER-2400':
            if self.disk['ssd_128'] != ssd_num:
                ret.append('disk fail')
            if mac_num != 8:
                ret.append('net card erro')
        elif self.dic['family'] == 'XINWEIH_C612_ASERVER-2405':
            if self.disk['ssd_128'] != ssd_num and self.disk['ssd_128_1'] != ssd_num:
                ret.append('disk fail')
            if mac_num != 8:
                ret.append('net card erro')
        elif self.dic['family'] == 'XINWEIH_C612_VDS-G680':
            if self.disk['ssd_128'] != ssd_num:
                ret.append('disk fail')
            if mac_num != 6:
                ret.append('net card erro')
        elif self.dic['family'] == 'XINWEIH_C612_VDS-8050':
            if self.disk['ssd_64'] != ssd_num:
                ret.append('disk fail')
            if mac_num != 8:
                ret.append('net card erro')
            if pci_info != pci_check:
                ret.append('PCI-E fail')
        if len(ret) == 0:
            return {'status': 'pass'}
        else:
            return {'status': str(list(set(ret)))}


if __name__ == '__main__':
    c = Collect()
    dic = {}
    dic.update(c.cpu())
    dic.update(c.mem())
    dic.update(c.sn())
    dic.update(c.time())
    dic.update(c.name())
    dic.update(c.bmc())
    dic.update(c.raidDisk())
    dic.update(c.sel())
    dic.update(c.fru())
    dic.update(c.smart())
    dic.update(c.mac())
    dic.update(c.net())
    dic.update(c.hostName())
    dic.update(c.bootTime())
    dic.update(c.biosTime())
    try:
        con = MySQLdb.connect('192.168.1.57', 'trusme', '6286280300', 'command')
        cur = con.cursor()
        cmd = "select * from base"
        cur.execute(cmd)
        data = cur.fetchall()
        name = []
        family = []
        for i in data:
            if i[0]:
                name.append(i[0])
            if i[9]:
                family.append(i[9])
        SN = [c.sn()['sn'], c.sn()['sn_1']]
        cmd = 'select * from web_stat where sn="%s"' % SN
        cur.execute(cmd)
        stress_test = cur.fetchall()
        if stress_test:
            stress_test = stress_test[0][3]
        else:
            cmd = 'select * from web_stat where sn="[\'%s\']"' % c.sn()['sn_1']
            cur.execute(cmd)
            stress_test = cur.fetchall()
            if stress_test:
                stress_test = stress_test[0][3]
            else:
                cmd = 'select * from web_stat where sn="[\'%s\']"' % c.sn()['sn']
                cur.execute(cmd)
                stress_test = cur.fetchall()
                if stress_test:
                    stress_test = stress_test[0][3]
                else:
                    cmd = 'select * from web_stat where sn like "%%%s%%" or sn like "%%%s%%"' % (
                    c.sn()['sn'], c.sn()['sn_1'])
                    cur.execute(cmd)
                    stress_test = cur.fetchall()[0][3]
    except:
        name = [
            'RG-RCD6000-Main',
            'RG-RCD6000-Office',
            'RG-RCM1000-Smart',
            'RG-RCM1000-Office',
            'RG-RCM1000-Edu',
            'RG-ONC-AIO-E',
        ]
        family = [
            'XINWEIH_C612_VDS-5050',
            'XINWEIH_C612_VDS-6550',
            'XINWEIH_C612_ASERVER-2400',
            'XINWEIH_C612_VDS-G680',
            'XINWEIH_C612_VDS-8050',
            'XINWEIH_C612_ASERVER-2405',
        ]
        stress_test = 'system reload'
    cur.close()
    con.close()
    data = CheckInfo(dic, name, family)
    dic.update(data.info())
    dic.update({'stress_test': stress_test})
    sn = dic['sn']
    sn1 = dic['sn_1']
    name = dic['name']
    family = dic['family']
    status = dic['status']
    cpu = dic['cpu']
    memory = dic['memory']
    disk = dic['disk'].items()
    raid = dic['raid']
    network = dic['network'].items()
    bios = dic['bios']
    bmc = dic['bmc']
    fru = dic['fru']
    sel = dic['sel']
    boot_time = dic['boot_time']
    bios_time = dic['bios_time']
    time = dic['time']
    mac = dic['mac'].items()
    pci_info = Popen('lspci | grep "[01|02|03]:00" | grep -v ^00', stdout=PIPE, stderr=PIPE, shell=True)
    pci_info = pci_info.stdout.read()
    disk_info = ''
    network_info = ''
    mac_info = ''
    for k, v in disk:
        disk_info += "%s  (%s)\n\t" % (k, v)
    for k, v in network:
        network_info += "%s  (%s)\n\t" % (k, v)
    for k, v in sorted(mac):
        mac_info += "%s    %s\n\t" % (k, v)
    info = Popen('/usr/bin/lsscsi|egrep -v "SanDisk|enclosu"', stdout=PIPE, stderr=PIPE, shell=True)
    locate_disk = info.stdout.read()
    if not locate_disk:
        try:
            locate_disk = c.raidDisk()['disk_locate']
        except:
            locate_disk = ''
    info = Popen('/usr/sbin/smartctl -i /dev/sda', stdout=PIPE, stderr=PIPE, shell=True)
    info = info.stdout.read()
    if 'Serial Number' not in info:
        info = Popen('/usr/sbin/smartctl -i /dev/sdb', stdout=PIPE, stderr=PIPE, shell=True)
        info = info.stdout.read()
    disk_sn = re.search('Serial Number:\s+(.*)', info, re.M)
    if disk_sn:
        disk_sn = disk_sn.group(1)
    else:
        disk_sn = ''
    info = Popen('/usr/sbin/dmidecode -t 17', stdout=PIPE, stderr=PIPE, shell=True)
    info = info.stdout.read()
    n = 0
    dmi_info = ''
    for i in info.split('\n'):
        if i.startswith('SMBIOS'):
            n += 1
        if n < 2:
            dmi_info += i + "\n"
    if n > 1:
        info = dmi_info
    all_mem = re.findall(r'\t+Size:\s+(.*)', info, re.M)
    locate_mem = re.findall(r'\t+Locator:\s+(.*)', info, re.M)
    lo_mem = re.findall(r'\t+Bank Locator:\s+(.*)', info, re.M)
    mem_speed = re.findall(r'\t+Speed:\s+(.*)', info, re.M)
    mem_conf = re.findall(r'\t+Configured Clock Speed:\s+(.*)', info, re.M)
    mem_man = re.findall(r'\t+Manufacturer:\s+(.*)', info, re.M)
    count = 0
    mem_locate = ''
    for i in locate_mem:
        mem_locate += "%s || %s || %s || %s || %s || %s\n" % (
        lo_mem[count], i, all_mem[count], mem_speed[count], mem_conf[count], mem_man[count])
        count += 1

    message = '''NAME:  %s
FIMILY:  %s
CHECK STAT:
	%s
SN:
	%s
SN1:
	%s
TIME:
	%s
BOOT TIME:
	%s
BIOS TIME:
	%s
CPU:
	%s
MEMORY INFO:
	%s
DISK INFO:
	%s
RAID INFO:
	%s
NETWORK INFO:
	%s
MAC INFO:
	%s
BIOS VERSION:
	%s
BMC VERSION:
	%s
PCIE INFO:
%s
FRU INFO:
%s
LOCATE DISK:
%s
LOCATE MEMORY:
%s
IP:	 %s
POWER: %s
DISK_SN: %s''' % (
        name,
        family,
        status,
        sn,
        sn1,
        time,
        boot_time,
        bios_time,
        cpu,
        memory,
        disk_info.strip(),
        raid,
        network_info.strip(),
        mac_info.strip(),
        bios,
        bmc,
        pci_info,
        fru,
        locate_disk,
        mem_locate,
        dic['ip'],
        dic['power'],
        disk_sn,
    )
    dic.update({'message': message})
    filename = os.path.join('/log', c.sn()['sn'])
    data = json.dumps(dic)
    try:
        urllib2.urlopen('http://192.168.1.57/web/collect/', data)
    finally:
        if not os.path.exists(filename):
            with open(filename, 'wb') as fd:
                fd.write(message)
            cmd = '''/usr/bin/lftp -c "put /log/%s -o ftp://test:test@192.168.1.210/"''' % c.sn()['sn']
            try:
                info = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
                stdout, stderr = info.communicate()
                info.returncode
            except:
                pass
