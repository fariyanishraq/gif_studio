import streamlit as st
import os
import base64
import tempfile
from PIL import Image as img
import numpy as np
from moviepy.editor import VideoFileClip as vfc
import moviepy.video.fx.all as vfx

def App():
    #session state#
    if 'clip_width' not in st.session_state:
        st.session_state.clip_width = 0
    if 'clip_height' not in st.session_state:
        st.session_state.clip_height = 0
    if 'clip_duration' not in st.session_state:
        st.session_state.clip_duration = 0
    if 'clip_fps' not in st.session_state:
        st.session_state.clip_fps = 0
    if 'clip_total_frames' not in st.session_state:
        st.session_state.clip_total_frames = 0
    #Frontend
    
    st.set_page_config(
        page_title='GIF Studio',
        page_icon='🎴',
        menu_items={
         'Get Help': 'https://fariyanishraq35@gmail.com',
         'Report a bug': "https://fariyanishraq35@gmail.com",
         'About': "GIF Studio is an opensource web application to convert video clips to gif images. "
        }
    )
    title = st.title("GIF Studio")
    st.info('GIF Studio is an opensource web application to convert video clips to gif images. ')
    #upload section
    upload = st.file_uploader('upload clip', type=['mov','mp4'])
    #conditions
    if upload is not None:
        temp = tempfile.NamedTemporaryFile(delete=False)
        temp.write(upload.read())
        #open file
        clip = vfc(temp.name)
        
        #display output
        st.session_state.clip_duration = clip.duration
        st.session_state.clip_width = clip.w
        st.session_state.clip_height = clip.h
        st.session_state.clip_total_frames = clip.fps * clip.duration
        st.session_state.clip_fps = clip.fps

        #Metrics
        st.subheader('Metrics')
        with st.expander('Show metrics'):
         col1, col2, col3, col4, col5 = st.columns(5)
         col1.metric('Width', st.session_state.clip_width, 'pixels')
         col2.metric('Height', st.session_state.clip_height, 'pexels')
         col3.metric('Duration', st.session_state.clip_duration, 'seconds')
         col4.metric('FPS', st.session_state.clip_fps, '')
         col5.metric('Total Frames', st.session_state.clip_total_frames, 'frames')
        
        #Preview
        st.subheader("Preview")
        with st.expander('show image'):
            selected_frames = st.slider(
                'Preview Time Frame',
                0,
                int(st.session_state.clip_duration),
                int(np.median(st.session_state.clip_duration))
            )
            clip.save_frame('frame.gif', t=selected_frames)
            frame_image = img.open('frame.gif')
            st.image(frame_image, output_format=('Auto'))
        
        #Image Parameter
        st.subheader('Input Parameter')
        selected_resolution_scaling = st.slider(
            'scaling of video resolution',
            0.0, 1.0, 5.0
        )
        selected_speedx = st.slider(
            'Playback speed',
            0.1, 10.0, 5.0
        )
        selected_export_range = st.slider(
            'Duration range to export',
            0,
            int(st.session_state.clip_duration),
            (0, int(st.session_state.clip_duration))
        )
        #print parameter
        st.subheader('Image Parameter')
        with st.expander('Show image parameter'):
            st.write(f'File name: `{upload.name}`')
            st.write(f'Image size: `{frame_image.size}`')
            st.write(f'Video resolution scaling: `{selected_resolution_scaling}`')
            st.write(f'Speed playback: `{selected_speedx}`')
            st.write(f'Export duration: `{selected_export_range}`')
            st.write(f'FPS: `{st.session_state.clip_fps}`')
        #Export animated GIF
        generate_gif = st.button("Generate Animated GIF")
        if generate_gif:
            clip = clip.subclip(
                selected_export_range[0],
                selected_export_range[1],
            ).speedx(selected_speedx)
            frames=[]
            for frame in clip.iter_frames():
                frames.append(np.array(frame))
            image_list =[]
            for frame in frames:
                im = img.fromarray(frame)
                image_list.append(im)
            image_list[0].save(
                'generate_img.gif', 
                format='GIF',
                save_all = True,
                loop = 0,
                append_image = image_list
            )
            clip.write_gif('export.gif', fps=st.session_state.clip_fps)
            ## Download ##
            st.subheader('Download')

            file_ = open('export.gif', 'rb')
            contents = file_.read()
            data_url = base64.b64encode(contents).decode("utf-8")
            file_.close()
            st.markdown(
              f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
              unsafe_allow_html=True,
            )

            fsize = round(os.path.getsize('export.gif')/(1024*1024), 1)
            st.info(f'File size of generated GIF: {fsize} MB')

            fname = upload.name.split('.')[0]
            with open('export.gif', 'rb') as file:
              btn = st.download_button(
              label='Download image',
              data=file,
              file_name=f'{fname}_scaling-{selected_resolution_scaling}_fps-{st.session_state.clip_fps}_speed-{selected_speedx}_duration-{selected_export_range[0]}-{selected_export_range[1]}.gif',
              mime='image/gif'
            )

    else:
        st.info('Developed by Fariyan Ishraq')



        
if __name__ == '__main__':
    App()