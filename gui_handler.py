from dearpygui import dearpygui as dpg
from final_model import get_response, save_convo
#from voice_clonner import speak


# Create a callback for sending messages
def send_message(sender, app_data, user_data):
    user_message = dpg.get_value('input_text')
    if user_message.strip() != '':
        # Replace curly apostrophes with straight apostrophes to avoid encoding issues
        user_message = user_message.replace('’', "'").replace('‘', "'")
        dpg.add_text(f'You: {user_message}', parent='chat_window', wrap=750, bullet=True, color=(0, 130, 200))
        response = get_response(user_message)
        #print(response)
        response = response.replace('’', "'").replace('‘', "'")  # Ensure response also handles apostrophes correctly
        dpg.add_text(f'Max: {response}', parent='chat_window', wrap=750, bullet=True, color=(255, 255, 255))
        #speak(response)
        dpg.set_value('input_text', '')

# Create the main window
dpg.create_context()

dpg.create_viewport(title='Chat with Max', width=850, height=750, min_width=850, min_height=750)

with dpg.theme() as global_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (255, 255, 255, 255))
        dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255, 255))
        dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 122, 204))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (0, 162, 255))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (0, 102, 153))
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 10)
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 12, 12)
        dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 1)
        dpg.add_theme_color(dpg.mvThemeCol_Border, (150, 150, 150, 255))
        dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 8, 8)
    with dpg.theme_component(dpg.mvInputText):
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (255, 255, 255))  
        dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0))  

# Add a font registry to increase font size
with dpg.font_registry():
    default_font = dpg.add_font("ARIAL.TTF", 20)

with dpg.window(label='Chat with Max', tag='main_window', width=800, height=700, pos=(25, 25), no_title_bar=False, no_resize=False):
    with dpg.child_window(tag='chat_window', width=780, height=520, border=True):
        dpg.add_text("Chat with Max", wrap=750, color=(0, 130, 200), bullet=False)
    
    with dpg.group(horizontal=True, indent=5, horizontal_spacing=10):
        dpg.add_input_text(tag='input_text', width=580, height=40, hint='Type your message here...', indent=5, callback=None)
        dpg.add_spacer(width=10)
        dpg.add_button(label='Send', callback=send_message, width=120, height=40)

# Apply the global theme and bind the font
dpg.bind_theme(global_theme)
dpg.bind_font(default_font)

# Set up and start the Dear PyGui application
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()

save_convo()
