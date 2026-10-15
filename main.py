from tkinter import messagebox

import ttkbootstrap as ttk
import sty

app = ttk.Window(
    title="Calculadora de Planilla", themename="superhero")
app.geometry("1000x1000")
app.resizable(0, 0)

form = ttk.Frame(app, padding=20)
form.pack(fill="both", expand=True)

ttk.Label(form, font=sty.FUENTE_TITULO, text="Calculadora de Planilla").grid(row=0, column=0, sticky="W, E", padx=5, pady=5)
ttk.Label(form, font=sty.FUENTE_ETIQUETA, text="Ingrese los siguientes datos").grid(row=1, column=0, sticky="N", padx=5, pady=5)

#LABELS
nombre=ttk.Label(form, font=sty.FUENTE_ETIQUETA, bootstyle=sty.BOOTSTYLE_ETIQUETA, text="Nombre del empleado: ")
nombre.grid(row=2, column=0, sticky="N", padx=5, pady=5)

pago_bruto=ttk.Label(form, font=sty.FUENTE_ETIQUETA, bootstyle=sty.BOOTSTYLE_ETIQUETA, text="Pago por hora (L): ")
pago_bruto.grid(row=3, column=0, sticky="N", padx=5, pady=5)

horas_trabajadas=ttk.Label(form, font=sty.FUENTE_ETIQUETA, bootstyle=sty.BOOTSTYLE_ETIQUETA, text="Horas trabajadas en el mes: ")
horas_trabajadas.grid(row=4, column=0, sticky="N", padx=5, pady=5)

resultado_label = ttk.Label(form, font=sty.FUENTE_RESULTADO, bootstyle=sty.BOOTSTYLE_EXITO, text="")
resultado_label.grid(row=6, column=0, columnspan=3, sticky="N", padx=5, pady=5)

#ENTRADAS
nombre_entry = ttk.Entry(form, font=sty.FUENTE_ETIQUETA)
nombre_entry.grid(row=2, column=1, sticky="N", padx=5, pady=5)

pago_bruto_entry = ttk.Entry(form, font=sty.FUENTE_ETIQUETA)
pago_bruto_entry.grid(row=3, column=1, sticky="N", padx=5, pady=5)

horas_trabajadas_entry = ttk.Entry(form, font=sty.FUENTE_ETIQUETA)
horas_trabajadas_entry.grid(row=4, column=1, sticky="N", padx=5, pady=5)

#BOTONES
btn_calcular = ttk.Button(form, text="Calcular", bootstyle=sty.BOOTSTYLE_BOTON, command=lambda: calcular_salario(nombre_entry, pago_bruto_entry, horas_trabajadas_entry, resultado_label))
btn_calcular.grid(row=5, column=0, sticky="N", padx=5, pady=5)  

btn_limpiar = ttk.Button(form, text="Limpiar", bootstyle=sty.BOOTSTYLE_BOTON, command=lambda: limpiar_campos(nombre_entry, pago_bruto_entry, horas_trabajadas_entry, resultado_label))
btn_limpiar.grid(row=5, column=1, sticky="N", padx=5, pady=5)

btn_salir = ttk.Button(form, text="Salir", bootstyle=sty.BOOTSTYLE_BOTON, command=app.destroy)
btn_salir.grid(row=5, column=2, sticky="N", padx=5, pady=5)

#Salario bruto = pago por hora × horas trabajadas
#IHSS = 2.5% del salario bruto, con un techo de L11,903.13. Si el salario es mayor al techo, se calcula sobre L11,903.13.
#RAP = 1.5% sobre la parte del salario que exceda L11,903.13. Si no excede, el RAP es L0.00.
#ISR (tabla progresiva mensual, calculado sobre el salario bruto):

def calcular_salario(nombre_entry, pago_bruto_entry, horas_trabajadas_entry, resultado_label):
    try:
        nombre = nombre_entry.get()
        pago_bruto = float(pago_bruto_entry.get())
        horas_trabajadas = float(horas_trabajadas_entry.get())

        #Calcular salario bruto
        salario_bruto = pago_bruto * horas_trabajadas

        #Calcular IHSS
        techo_ihss = 11903.13
        ihss = 0
        if salario_bruto > techo_ihss:
            ihss = techo_ihss * 0.025
        else:
            ihss = salario_bruto * 0.025


        #Calcular RAP
        rap = 0
        if salario_bruto > techo_ihss:
            rap = (salario_bruto - techo_ihss) * 0.015
        else:
            rap = 0


        #Calcular ISR
        isr = 0
        if salario_bruto <= 22360.36:
            isr = 0
        elif salario_bruto >22360.36 or salario_bruto <= 32346.18:
            excedente=salario_bruto-22360.36
            isr = excedente * 0.015
        elif salario_bruto >32346.19 or salario_bruto <= 70805.06:
            excedente=salario_bruto-32346.19
            isr = excedente * 0.20 + 1497.87
        elif salario_bruto >70805.07:
            excedente=salario_bruto-70805.07
            isr = excedente * 0.25 + 9189.65


        salario_neto = salario_bruto - ihss - rap - isr

        resultado = (nombre, salario_bruto, ihss, rap, isr, salario_neto)

        resultado_label.config(text=f"El pago total de {nombre} es: L {salario_neto:.2f}\nSalario Bruto: L {salario_bruto:.2f}\nIHSS: L {ihss:.2f}\nRAP: L {rap:.2f}\nISR: L {isr:.2f}", bootstyle=sty.BOOTSTYLE_EXITO)
        messagebox.showinfo("Resultado", f"El pago neto de {nombre} es: L {salario_neto:.2f}\nSalario Bruto: L {salario_bruto:.2f}\nIHSS: L {ihss:.2f}\nRAP: L {rap:.2f}\nISR: L {isr:.2f}")
    except ValueError:
        resultado_label.config(text="Error\nPor favor, ingrese valores numéricos válidos\npara el pago por hora y las horas trabajadas.\nNo puede dejar campos vacíos.", bootstyle=sty.BOOTSTYLE_ERROR)
        messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos" \
        "\npara el pago por hora y las horas trabajadas." \
        "\nNo puede dejar campos vacíos.")

def limpiar_campos(nombre_entry, pago_bruto_entry, horas_trabajadas_entry, resultado_label):
    nombre_entry.delete(0, "end")
    pago_bruto_entry.delete(0, "end")
    horas_trabajadas_entry.delete(0, "end")
    resultado_label.config(text="", bootstyle=sty.BOOTSTYLE_EXITO)



app.mainloop()