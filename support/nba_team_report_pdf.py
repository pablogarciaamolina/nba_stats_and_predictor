from fpdf import FPDF
import pandas as pd
import dataframe_image as dfi

class PDF(FPDF):

    def titles(self, title: str):
        self.set_xy(0.0,0.0)
        self.set_font('Arial', 'B', 20)
        self.set_text_color(220, 50, 50)
        self.cell(w=297.0, h=20.0, align='C', txt=title, border=0)

    def texts(self, text: str):

        xt = text.encode('latin-1', 'ignore')
        text = xt.decode('latin-1')
        self.set_xy(10.0,40.0)    
        self.set_text_color(0, 0, 0)
        self.set_font('Arial', '', 6)
        self.multi_cell(0,10,text)

    def df_in_pdf(self,df: pd.DataFrame, id:str, path: str):
        
        df_to_image(df, id, path)
        image = f"{path}/{id}_table.png"
        self.set_xy(x=0.0, y=400.0)
        self.image(image, type='PNG', w=297.0, h=165, y=30.0)


def df_to_image(df: pd.DataFrame, name, path: str):

    dfi.export(df, f"{path}/{name}_table.png")