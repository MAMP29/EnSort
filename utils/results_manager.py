
# Este manager permite un puente entre el sidebar y el excel panel para que puedan compartir información, en especial el apartado de ejecuciones
class ResultsManager:
    def __init__(self):
        self.sidebar = None
        self.exec_panel = None

    def set_sidebar(self, sidebar):
        self.sidebar = sidebar

    def set_exec_panel(self, exec_panel):
        self.exec_panel = exec_panel

    def add_result_button(self, button):
        if self.sidebar:
            self.sidebar.add_results_button(button)