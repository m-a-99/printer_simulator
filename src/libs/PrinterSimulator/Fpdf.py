from fpdf import FPDF
import os

class PDF:
    def __init__(self,isPageFormatCustom,pageFormat,pageWidth,pageHeight,leftMargin,rightMargin,topMargin ,orientation,autoPageBreak,payload):
        self.isPageFormatCustom=isPageFormatCustom
        self.pageFormat=pageFormat
        self.pageWidth=pageWidth
        self.pageHeight=pageHeight
        self.leftMargin=leftMargin
        self.rightMargin=rightMargin
        self.topMargin=topMargin
        self.orientation=orientation
        self.autoPageBreak=autoPageBreak
        self.id=payload["id"]
        self.path=os.path.dirname(__file__)
        # print(payload)
        self.style=""
        if "filepath" in payload["payload"]:
            self.filepath=payload["payload"]["filepath"]
            self.__isfile=True
        else:
            self.__isfile=False
            
        if "font" in payload["payload"]:
            self.font=payload["payload"]['font']
        else :
            self.font="Arial"
            
        if "fontsize" in payload["payload"] :
            self.size=int(str(payload["payload"]["fontsize"]))
        else:
            self.size=12
            
        if "alignment" in payload["payload"]:
            self.alignment= payload["payload"]["alignment"]
        else:
            self.alignment="c"
            
        if "color" in payload["payload"]:
            self.color=payload["payload"]["color"]
        else:
            self.color='#000000'
            
        if "italic" in payload["payload"]:
            self.isItalic=payload["payload"]["italic"]
        else:
            self.isItalic=False
            
        if "bold" in payload["payload"]:
            self.isBold=payload["payload"]["bold"]
        else:
            self.isBold=False
            
        if "underline" in payload["payload"]:
            self.isUnderline=payload["payload"]["underline"]
        else:
            self.isUnderline=False
            
        if "text" in payload["payload"]:
            self.text=payload["payload"]["text"]
        else:
            self.text=""       
            
        if self.isBold:
            self.style+="B"
        if self.isItalic:
            self.style+="I"
        if self.isUnderline:
            self.style+="U" 
    def print(self):
        pdf = FPDF()
        if(self.isPageFormatCustom):
            pdf = FPDF(format=(self.pageWidth,self.pageHeight ),orientation=self.orientation)
        else:
            pdf = FPDF(format=self.pageFormat,orientation=self.orientation)
        pdf.add_page()
        pdf.set_auto_page_break(self.autoPageBreak)
        pdf.set_margins(self.leftMargin,self.topMargin,self.rightMargin)
        pdf.set_font(self.font,style=self.style, size=self.size)
        
        pdf.set_text_color(int(self.color[1:3],base=16), int(self.color[3:5],base=16), int(self.color[5:],base=16))
        pdf.cell(0, 10, txt ="",ln =1, align =self.alignment) 
        if self.__isfile:
            with open(self.filepath) as f:
                for line in f:
                    pdf.cell(0, 10, txt =line,ln =1, align =self.alignment)
        else:
            texts=self.text.split("\n")
            for line in texts:
                pdf.cell(0, 10, txt =line,ln =1, align =self.alignment) 
        pdf.output(os.path.join(self.path,"../../../output/")+str(self.id)+".pdf","F") 
    