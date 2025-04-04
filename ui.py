from dearpygui.dearpygui import *

# Başlangıç değerleri
sensitivity = 1.0
roi_x, roi_y, roi_w, roi_h = 0, 0, 640, 480

def ayarlari_yazdir_callback(sender, app_data, user_data):
    sens = get_value("Hassasiyet")
    x = get_value("ROI X")
    y = get_value("ROI Y")
    w = get_value("ROI W")
    h = get_value("ROI H")
    print(f"Sensitivity: {sens}")
    print(f"ROI: x={x}, y={y}, width={w}, height={h}")

with window(label="El Takibi Ayarları", width=400, height=300):
    add_slider_float(label="Hassasiyet", tag="Hassasiyet", default_value=sensitivity, min_value=0.1, max_value=5.0)
    add_input_int(label="ROI X", tag="ROI X", default_value=roi_x)
    add_input_int(label="ROI Y", tag="ROI Y", default_value=roi_y)
    add_input_int(label="ROI Genişlik", tag="ROI W", default_value=roi_w)
    add_input_int(label="ROI Yükseklik", tag="ROI H", default_value=roi_h)
    add_button(label="Ayarları Yazdır", callback=ayarlari_yazdir_callback)

start_dearpygui()