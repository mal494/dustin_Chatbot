import yaml
import streamlit as st
import time
from src import brain, memory
from src.gui import header
from src.tools import filesystem

# 1. Load Config
with open("config/settings.yaml", "r") as f:
    settings = yaml.safe_load(f)
with open("config/personality.yaml", "r") as f:
    persona = yaml.safe_load(f)

# 2. Render Header & Get User Selection
selected_model_key = header.render(settings)
model_config = settings['models'][selected_model_key]

# 3. Initialize/Swap Brain
if "dustin_brain" not in st.session_state or st.session_state.get("model_changed"):
    with st.spinner(f"Loading {model_config['name']}..."):
        st.session_state["dustin_brain"] = brain.DustinBrain(
            model_path=model_config['path'], 
            system_prompt=persona['system_prompt'],
            context_size=model_config['context_size']
        )
        st.session_state["model_changed"] = False
    st.toast(f"Switched to {model_config['name']}!", icon="✅")

# 4. Main Chat Loop
memory.initialize_memory()
dustin = st.session_state["dustin_brain"]

# Display Chat History
for msg in memory.get_messages():
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle Input
if prompt := st.chat_input(f"Chat with {model_config['name']}..."):
    # --- User Turn ---
    with st.chat_message("user"):
        st.markdown(prompt)
    memory.add_message("user", prompt)

    # --- Assistant Turn ---
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        # 1. Generate Initial Response
        stream = dustin.generate_response(memory.get_messages())
        
        for chunk in stream:
            if 'content' in chunk['choices'][0]['delta']:
                content = chunk['choices'][0]['delta']['content']
                full_response += content
                response_placeholder.markdown(full_response + "▌")
        
        response_placeholder.markdown(full_response)
        
        # 2. TOOL CHECKER LOGIC (The "Hands")
        if "ACTION:" in full_response:
            
            lines = full_response.split('\n')
            
            # 1. Find the line that has the Action
            action_line = next((line for line in lines if "ACTION:" in line), None)
            
            if action_line:
                # 2. Extract the Action Name cleanly
                try:
                    raw_action = action_line.split("ACTION:")[1].strip()
                    
                    # Check if "INPUT:" is accidentally on the same line
                    if "INPUT:" in raw_action:
                        parts = raw_action.split("INPUT:")
                        action = parts[0].strip()
                        input_param = parts[1].strip()
                    else:
                        action = raw_action
                        input_param = ""
                        for line in lines:
                            if "INPUT:" in line and "ACTION:" not in line:
                                input_param = line.split("INPUT:", 1)[1].strip()
                                break
                except IndexError:
                    action = None
                    input_param = ""

                if action:
                    # Visual feedback
                    status_container = st.status(f"Dustin is running: {action}...", expanded=True)
                    tool_output = ""
                    
                    # --- Execute Tools ---
                    if action == "list_directory":
                        path = input_param if input_param else "."
                        tool_output = filesystem.list_directory(path)
                        
                    elif action == "read_file":
                        tool_output = filesystem.read_file(input_param)
                        
                    elif action == "create_file":
                        # Splitting filename | content
                        if "|" in input_param:
                            parts = input_param.split("|", 1)
                            fname = parts[0].strip()
                            fcontent = parts[1].strip()
                            tool_output = filesystem.create_file(fname, fcontent)
                        elif " " in input_param:
                            parts = input_param.split(" ", 1)
                            fname = parts[0].strip()
                            fcontent = parts[1].strip()
                            if "." in fname:
                                tool_output = filesystem.create_file(fname, fcontent)
                            else:
                                tool_output = "Error: Could not detect filename. Format: filename | content"
                        else:
                            tool_output = "Error: Input format must be 'filename | content'"
                    
                    elif action == "overwrite_file":
                        # Splitting filename | content
                        if "|" in input_param:
                            parts = input_param.split("|", 1)
                            fname = parts[0].strip()
                            fcontent = parts[1].strip()
                            tool_output = filesystem.overwrite_file(fname, fcontent)
                        elif " " in input_param:
                            parts = input_param.split(" ", 1)
                            fname = parts[0].strip()
                            fcontent = parts[1].strip()
                            if "." in fname:
                                tool_output = filesystem.overwrite_file(fname, fcontent)
                            else:
                                tool_output = "Error: Could not detect filename. Format: filename | content"
                        else:
                            tool_output = "Error: Input format must be 'filename | content'"
                    
                    elif action == "run_script":
                        tool_output = "Error: run_script not implemented"

                    else:
                        tool_output = f"Error: Unknown tool '{action}'"

                    # Display Tool Output
                    status_container.write(tool_output)
                    status_container.update(label="Task Completed", state="complete", expanded=False)

                    # 3. Save Context
                    memory.add_message("assistant", full_response)
                    memory.add_message("system", f"TOOL OUTPUT: {tool_output}")
                    
                    # Force a rerun so the new context is processed immediately
                    st.rerun() 
        
        else:
            # No tool used, just save the text
            memory.add_message("assistant", full_response)