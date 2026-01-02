import os
from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from stegtools.embed_watermark import *
from stegtools.tampering_detector import *
from stegtools.utils import *

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'tif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 32 * 1000 * 1000
app.secret_key = 'top-secret-key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload/<selected>', methods=['GET', 'POST'])
def upload(selected):
    # Process images
    if request.method == 'POST':
        cover_file = request.files['coverImage']
        watermark_file = request.files['watermark']
        N = 100
        
        if allowed_file(cover_file.filename) and allowed_file(watermark_file.filename):
            cover_img = filestorage_to_img(cover_file)
            watermark = filestorage_to_img(watermark_file)

            if selected == 'embed-watermark':
                # Embed watermark into image
                embedded_img, kps = embed_watermark(cover_img, watermark, N)

                # Create debug image
                embedded_img_circles = draw_circles(embedded_img, kps, kps)

                # Save images to static folder
                filename = secure_filename('embedded.png')
                img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                cv2.imwrite(img_path, embedded_img)

                filename = secure_filename('embedded_debug.png')
                img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                cv2.imwrite(img_path, embedded_img_circles)

                return render_template('success_embed_watermark.html')
            
            else:
                # Verify image authenticity
                is_authentic, kps, verified_kps = verify_authenticity(cover_img, watermark, N)

                if selected == 'verify-authenticity':
                    return render_template('success_verify_authenticity.html', is_authentic=is_authentic)
                
                elif selected == 'detect-tampering':
                    # Draw circles around the keypoints
                    marked_img = draw_circles(cover_img, kps, verified_kps)
                    confidence = get_error(kps, verified_kps) * 100

                    # Save to static folder
                    filename = secure_filename('marked.png')
                    img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    cv2.imwrite(img_path, marked_img)

                    return render_template('success_detect_tampering.html', is_authentic=is_authentic, confidence=confidence)
        
        else:
            flash('Only png and tif files allowed.', 'warning')
            return redirect(request.url)

    if selected == 'embed-watermark':
        return render_template('upload_embed_watermark.html')
    
    elif selected == 'verify-authenticity':
        return render_template('upload_verify_authenticity.html')
    
    elif selected == 'detect-tampering':
        return render_template('upload_detect_tampering.html')
    
    else:
        return redirect('/')

def allowed_file(filename):
    """
    Checks if a file has a valid file extension.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
