from pyscript import document, fetch 
import asyncio
import json


def update_message(message):
       system_message_element = document.getElementById("system-message")
       system_message_element.innerHTML = message

def update_table(data_list):
            table_body_element = document.getElementById("table-body")

            new_table_html = ""
            for item in data_list[:5]:
                new_table_html += f"""
                <tr>
                    <td>{item.get('name', 'N/A')}</td>
                    <td>{item.get('html_url', 'N/A')}</td>
                    <td>{item.get('description', 'N/A')}</td>
                    <td>{item.get('language', 'N/A')}</td>
                </tr>
                """
            
            table_body_element.innerHTML = new_table_html

def search_item(event):
            search_input_element = document.getElementById("search-input")
            search_user = search_input_element.value.strip()

            if not search_user:
                update_message("Please enter an username to search.")
                return

            update_message(f"Searching for {search_user}...")

             
            async def my_api_call():
                try:
                    response = await fetch(f"http://127.0.0.1:5000/{search_user}")
                    if response.ok:
                        data = await response.json()
                        if data['data']:
                            update_table(data['data'])
                            if not data['message']:
                                update_message("User added")
                            else:
                                update_message("User Updated")  
                        else:
                            update_message("Data Empty")
                    elif response.status == 404:
                        update_message("Not found")
                    else:
                        update_message(f"Server error: {response.status}")
                except Exception as e:
                         update_message(f"Connection error: {e}")
            
            
            asyncio.ensure_future(my_api_call())
            
            search_input_element.value = ""


def initial_load():
    initial_message = "System message: Please enter an username to search."
    initial_data = []
    update_message(initial_message)
    update_table(initial_data)
        
initial_load()