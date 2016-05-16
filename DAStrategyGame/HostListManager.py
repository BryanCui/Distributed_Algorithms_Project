class HostListManager:
    def __init__(self):
        self.host_list_file = open('host_list.txt', 'a')

    def read_host_list(self):
        host_line = self.host_list_file.readline()
        host_list = []
        while host_line:
            host_list.append(host_line)
            host_line = self.host_list_file.readline()
        return host_list

    def write_host_list(self, hosts):
        host_list = self.read_host_list()
        is_existed = False
        for host in hosts:
            for host_line in host_list:
                if host_line == host:
                    is_existed = True
                    break
            if not is_existed:
                self.host_list_file.write(host)





