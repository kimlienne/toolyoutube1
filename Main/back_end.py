import os.path
from pathlib import Path

from utilizes.sentence import SentenceInfo
from utilizes.var_manager import variable_manager as vm


class EngineerUnderground:
    def __init__(self):
        self.main_ui = None
        self.list_sentence = []
        self.current_index = 0
        self.current_sentence = SentenceInfo(0, '', '', '', False, False, 'Not_Done')

    def get_data_local(self):
        folder_path = Path(f'{os.path.dirname(vm.get_svm("file_ans"))}/assignment')
        file_name = f"{vm.get_ivm_value('start_index')}_{vm.get_ivm_value('end_index')}.txt"
        file_path = folder_path/file_name

        if not folder_path.exists():
            folder_path.mkdir(parents=True)

        if not file_path.exists():
            with open(vm.get_svm_value("file_ans"), "r", encoding="utf-8") as f:
                data_ans = f.readlines()
            with open(vm.get_svm_value("file_scp"), "r", encoding="utf-8") as f:
                data_scp = f.readlines()
            if len(data_scp) != len(data_ans):
                return False
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("0\n")
                for index in range(len(data_ans)):
                    if index >= (vm.get_ivm_value("start_index") - 1) and index <= (vm.get_ivm_value("end_index") - 1):
                        f.write(f"{index}\t{data_ans[index].strip()}\t{vm.get_svm_value('file_audio').strip()}\t{data_scp[index].strip()}\tFalse\tFalse\tNot_Done\n")

        with open(file_path, 'r', encoding="utf-8") as f:
            lines = f.readlines()
            index = 0
            for line in lines:
                words = line.split('\t')
                if index == 0:
                    self.current_index = int(words[0].strip())
                else:
                    sentence = SentenceInfo(int(words[0].strip()), words[1].strip(), words[2].strip(), words[3].strip(), words[4].strip(), words[5].strip(), words[6].strip())
                    self.list_sentence.append(sentence)
                index += 1

        self.current_sentence = self.list_sentence[self.current_index]
        vm.set_ivm_value("sum_index", vm.get_ivm_value("end_index") - vm.get_ivm_value("start_index") + 1)
        return True


eu = EngineerUnderground()