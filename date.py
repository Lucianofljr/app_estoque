from flet import *

class controle(UserControl):
    def __init__(self):
        super().__init__()

        self.data_validade = DatePicker(on_change=True)

    def build(self):
         botao = ElevatedButton(icon=icons.CALENDAR_MONTH, on_click=self.data_validade.value)
         texto = Text(f"{self.data_validade.value}")

         linha = Container(Row(
             controls=[texto,botao]
         )
         )
         return Column([
             linha],
             alignment=MainAxisAlignment.CENTER,
             horizontal_alignment=CrossAxisAlignment.CENTER,
         )

    def create_date(self):
        pass
        


def main(page: Page):
    my_date = controle()
    page.controls.append(my_date)
    page.update()

app(target=main) 