from flet import *
import sqlite3 as sl 


connect = sl.connect("dados.db", check_same_thread=False)
cursor = connect.cursor()


def table_warehouse():
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS produtos (id INTEGER PRIMARY KEY AUTOINCREMENT,
        lote TEXT,
        produto TEXT,
        validade TEXT,
        quantidade INTEGER)
'''
    )
    connect.commit()


class App(UserControl):
    def __init__(self):
        super().__init__()


        self.warehouse = Column(auto_scroll=True)


        self.create_lote = TextField(label="#lote: ")
        self.value_lote = TextField(label="Quantidade produzida: ", keyboard_type="number")
        self.update_prod = TextField(label="Editar quantidade: ")
        self.shelf_life = DatePicker(open=True, field_label_text="Validade: ")
        self.selected_valid = None
        self.list_prod = Dropdown(options=[
            dropdown.Option("Ghee tradicional 200g"),
            dropdown.Option("Ghee tradicional 300g"),
            dropdown.Option("Ghee tradicional 500g"),
            dropdown.Option("Ghee tradicional refil 300g"),
            dropdown.Option("Ghee sal do himalaia 200g"),
            dropdown.Option("Ghee sal do himalaia 300g"),
            dropdown.Option("Ghee sal do himalaia 500g"),
            dropdown.Option("Ghee sal do himalaia refil 300g"),
            dropdown.Option("Ghee douradíssimo 200g"),
            dropdown.Option("Ghee douradíssimo 300g"),
            dropdown.Option("Ghee douradíssimo 500g"),
            dropdown.Option("Ghee alho 200g"),
            dropdown.Option("Ghee cúrcuma 200g"),
            dropdown.Option("Caldo de legumes 350ml"),
            dropdown.Option("Caldo de legumes 600ml"),
            dropdown.Option("GheeRofa 250g"),          
            ])


    def build(self):
        button_create_lote = ElevatedButton('Inserir Estoque', on_click=self.create_new_lote)

        post_lote = Container(Row(
                controls=[self.create_lote], alignment=MainAxisAlignment.CENTER,
        ))

        post_shelf_life = Container(Row(
                controls=[self.shelf_life], alignment=MainAxisAlignment.CENTER,
        ))
    
        post_prod = Container(Row(
                controls=[self.list_prod], alignment=MainAxisAlignment.CENTER,
        ))
    
        post_quant = Container(Row(
                controls=[self.value_lote], alignment=MainAxisAlignment.CENTER,
        ))

        return Column([
            Text("Atualização do Estoque", size=20, weight="bold"),
            post_lote, post_prod, post_quant, post_shelf_life, button_create_lote
        ], 
        alignment=MainAxisAlignment.SPACE_AROUND,
        horizontal_alignment=CrossAxisAlignment.CENTER,
        )
    
#imprimir a lista do banco de dados em tela.
    def read_list(self):
        cursor.execute("SELECT * FROM produtos")
        connect.commit()

        my_list = cursor.fetchall()

        self.warehouse.controls.clear()

        for prod in my_list:
            id_prod, lote, produto, validade, quantidade = prod
            self.warehouse.controls.append(
                ListTile(
                    title=Text(f"Lote: {lote}"),
                    subtitle=Text(f"Produto: {produto} Validade: {validade} - Quantidade: {quantidade}"),
                    trailing=Row(controls=[
                        IconButton(icon=icons.CREATE_OUTLINED, tooltip="Editar", on_click=lambda e, id=id_prod: self.update_click(id)),
                        IconButton(icon=icons.DELETE_OUTLINED, tooltip="Deletar", on_click=lambda e, id=id_prod: self.delete_click(id)),
                    ])
                )
            )
            self.update()


    def create_new_lote(self, e):
        lote = self.create_lote.value
        produto = self.list_prod.value
        quantidade = self.value_lote.value
        validade = self.shelf_life.value

        if lote and produto and quantidade and validade:
            try:
                quantidade = int(quantidade)
                cursor.execute("INSERT INTO produtos (lote, produto, validade, quantidade) VALUES (?, ?, ?, ?)",
                            (lote, produto, validade, quantidade))
                connect.commit()
            

                self.warehouse.controls.append(Text(f"Novo lote ({lote}): {quantidade} unidades de {produto} (validade: {validade})."))
                self.create_lote.value = ""
                self.value_lote.value = ""
                self.shelf_life.value = None
                self.read_list()
            except ValueError:
                print("Quantidade deve ser um número!")
        else:
            print("preencha todos os campos!")

    def update_click(self, id_prod):
        new_value = self.update_prod.value
        if new_value:
            try:
                new_value = int(new_value)
                cursor.execute("UPDATE produtos SET quantidade = ? WHERE id = ?", (new_value, id_prod))
                connect.commit()
                self.read_list()
            except ValueError:
                print("Informe um valor numérico!")
        else:
            print("Informe um novo valor para editar!")

    def delete_click(self, id_prod):
        cursor.execute("DELETE FROM produtos WHERE id = ?", (id_prod,))
        connect.commit()
        self.read_list()

def main(page:Page):

    my_app = App()
    
    
    page.controls.append(my_app)
    page.update()

app(target=main)