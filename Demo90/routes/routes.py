#SF Routes Package - DAnderson 122320

def api():
    # POST request - Sensor Fusion Commands
   
    if request.method == 'POST':
        print('Incoming command from Sensor Fusion client ...')
        sfCommand = request.get_json()
        print(sfCommand)  # parse as JSON
        
        first_char = sfCommand[0] 
        if first_char == 'a':
            chunks = sfCommand.split(',')
            sfCommand = 'annotate'
            
            #Get the annotation data - name, image count, description
            os.environ['annotate_name'] = str(chunks[1])
            os.environ['annotate_images'] = str(chunks[2])
            
            anno_images = str(chunks[2])
            
            os.environ['annotate_description'] = str(chunks[3])
        #kill TensorFlow
        if first_char == 'k':
            os.environ['kill_tensorFlow'] = 'True'
        #Restore Tensor Flow
        if first_char == 'r':
            os.environ['kill_tensorFlow'] = 'False'
            #print('Restore Tensor Flow')
       
        #custom, model
        if first_char == 'c':
            print('Custom Model Changed')
       
        if first_char == 'm':
            print('Model changed')
            
        #Annotate    
        if sfCommand == 'annotate':
            capture_flag =  os.environ['cap_flag'] = 'True'
            print('Capture Flag Command =',capture_flag)
        #Labels    
        elif sfCommand == 'scores_off':
            os.environ['scores_flag'] = sfCommand
            print('Toggle Scores Command =', os.environ['scores_flag'])
        elif sfCommand == 'scores_on':
            os.environ['scores_flag'] = sfCommand
            print('Toggle Scores Command =', os.environ['scores_flag'])
            
        elif sfCommand == 'labels_off':
            os.environ['labels_flag'] = sfCommand
            print('Toggle Labels Command =', os.environ['labels_flag'])
        elif sfCommand == 'labels_on':
            os.environ['labels_flag'] = sfCommand
            print('Toggle Labels Command =', os.environ['labels_flag'])   
        elif sfCommand == 'fps':
            global fps_flag#local scope
           
            if fps_flag == False:#Show/Hide Frames per second
                fps_flag = True
            else:
                fps_flag = False
        elif sfCommand == 'quit':
            os.environ['quit_flag'] = sfCommand
            print('Quit command recieved')
        
        return 'OK', 200

    # GET request
    else:
        print('GET Request from Client');
        #session['cap_flag'] = True
        #print(session.get('capt_flag'))
        os.environ['cap_flag'] = 'True'
        print('Capture Flag Command =', os.environ['cap_flag'])
        
        message = {'Capture':'Capturing Images!'}
        return jsonify(message)  # serialize and use JSON headers
	
	
def login():
	pass
	
def registration():
	pass
	

