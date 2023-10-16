class TaskDataParser:
    def __init__(self, filename):
        self.filename = filename
        self.CAPACITY = 0
        self.N_TASKS = 0
        self.d = []
        self.rr = []
        self.suc = []

    def read_data_from_file(self):
        with open(self.filename, "r") as file:
            lines = file.readlines()

        for line in lines:
            parts = line.split()

            if parts[0] == "CAPACITY":
                self.CAPACITY = int(parts[2].split(";")[0].strip())
            elif parts[0] == "N_TASKS":
                self.N_TASKS = int(parts[2].split(";")[0].strip())
            elif parts[0] == "d":
                self.d = [int(x.replace(',', "")) for x in parts[3:parts.index('];')]]
            elif parts[0] == "rr":
                self.rr = [int(x.replace(',', "")) for x in parts[3:parts.index('];')]]
            else:
                parts = [x for x in parts if x.replace(',', "").isdigit()]
                successors = [int(x.replace(',',"")) for x in parts]
                self.suc.append(successors)

    def print_data(self):
        print("Capacity:", self.CAPACITY)
        print("Number of Tasks:", self.N_TASKS)
        print("Durations:", self.d)
        print("Resource Requirements:", self.rr)
        print("Succession Structure:")
        for i, successors in enumerate(self.suc):
            print(f"Task {i + 1} -> {successors}")

    def get_task_info(self, task_number):
        if 1 <= task_number <= len(self.d):
            duration = self.d[task_number - 1]
            resource_requirement = self.rr[task_number - 1]
            return duration, resource_requirement
        else:
            return None
