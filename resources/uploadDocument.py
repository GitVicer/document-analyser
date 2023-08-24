from flask import jsonify, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
from models import UploadedDocumentModel, KeywordModel, DocumentTypeModel
from schemas import UploadedDocumentSchema
import PyPDF2
from PyPDF2 import PdfReader
import re
#from resources.auth import login_required

blp = Blueprint("UploadedDocument", "UploadedDocument")

# UploadedDocument Endpoint
@blp.route("/uploaded_document/<int:document_id>")
class UploadedDocument(MethodView):

    @blp.response(200, UploadedDocumentSchema)
    def get(self, document_id):
        try:
            uploaded_document = UploadedDocumentModel.query.get_or_404(document_id)
            return uploaded_document

        except SQLAlchemyError:
            abort(500, message="Database error")

    @blp.response(204)
    def delete(self, document_id):
        try:
            uploaded_document = UploadedDocumentModel.query.get_or_404(document_id)
            db.session.delete(uploaded_document)
            db.session.commit()
            return "", 204

        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="Database error")

    @blp.arguments(UploadedDocumentSchema)
    @blp.response(200, UploadedDocumentSchema)
    def put(self, document_data, document_id):
        try:
            uploaded_document = UploadedDocumentModel.query.get(document_id)

            if uploaded_document:
                uploaded_document.filename = document_data["filename"]
                uploaded_document.document_text = document_data["document_text"]
                uploaded_document.document_type_id = document_data["document_type_id"]
            else:
                uploaded_document = UploadedDocumentModel(id=document_id, **document_data)

            db.session.add(uploaded_document)
            db.session.commit()
            return uploaded_document

        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="Database error")


# UploadedDocument List Endpoint
@blp.route("/uploaded_document")
class UploadedDocumentList(MethodView):

    @blp.response(200, UploadedDocumentSchema(many=True))
    def get(self):
        try:
            return UploadedDocumentModel.query.all()

        except SQLAlchemyError:
            abort(500, message="Database error")

    @blp.arguments(UploadedDocumentSchema)
    @blp.response(201, UploadedDocumentSchema)
    def post(self, document_data):
        try:
            uploaded_document = UploadedDocumentModel(**document_data)
            db.session.add(uploaded_document)
            db.session.commit()
            return uploaded_document

        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="Database error")

    @blp.response(204)
    def delete(self):
        try:
            uploaded_documents = UploadedDocumentModel.query.all()
            for uploaded_document in uploaded_documents:
                db.session.delete(uploaded_document)
            db.session.commit()
            return "", 204

        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="Database error")
    

#Route to handle file upload

@blp.route('/documentUpload')
class DocumentUpload(MethodView):
    def post(self):
        try:
            # Get the uploaded file from the request
            uploaded_file = request.files['file']
            target_keyword = request.form['word'].lower()
            print(target_keyword)
            
            # Check if the file is a PDF
            if uploaded_file.filename.endswith('.pdf'):
                pdf_reader = PdfReader(uploaded_file)
                num_pages = len(pdf_reader.pages)
                
                page_statistics = []

                for page_number in range(num_pages):
                    pdf_page = pdf_reader.pages[page_number]
                    page_text = pdf_page.extract_text().lower()

                    # Calculate word count, line count, and character count
                    words_list = re.findall(r'\b\w+\b', page_text)
                    print(words_list)
                    word_count = len(words_list)
                    lines_list = page_text.split('\n')
                    line_count = len(lines_list)
                    character_count = len(page_text)

                    # Find the index of the target word

                    substring_positions = []
                    exact_match_positions = []
                    before_words = []
                    after_words = []

                    for index, word in enumerate(words_list, start=1):
                        if word == target_keyword:
                                
                            before_word = words_list[index - 2] if index >= 1 else None
                            after_word = words_list[index] if index < len(words_list) - 1 else None
                            before_words.append(before_word)
                            after_words.append(after_word)
                            
                            exact_match_positions.append(index)

                        if target_keyword in word:
                            if index not in exact_match_positions:
                                substring_positions.append(index)

                                match = re.search(target_keyword, word)
                                before_word = word[:match.start()] if word[:match.start()] != '' else (words_list[index - 2] if index >= 1 else None)
                                after_word = word[match.end():] if word[match.end():] != '' else (words_list[index] if index < len(words_list) - 1 else None)
                                before_words.append(before_word)
                                after_words.append(after_word)

                        if substring_positions == [] and exact_match_positions == []:
                            #for group of strings (don't put less than 3 strings)
                            keyword_parts = target_keyword.split(' ')
                            nested_list = [part.split('-') for part in keyword_parts]
                            target_keyword_list = []
                            for inner_list in nested_list:
                                target_keyword_list.extend(inner_list)
                            target_keyword_initial_word = target_keyword_list[0]
                            target_keyword_length = len(target_keyword_list)

                            # matching the first, second and third word with respective words of wordlist
                            if word == target_keyword_initial_word and target_keyword_list[1] == words_list[index] and target_keyword_list[2] == words_list[index+1]:
                                    
                                before_word = words_list[index - 2] if index >= 1 else None
                                after_word = words_list[index + target_keyword_length - 1] if index < len(words_list) - 1 else None
                                before_words.append(before_word)
                                after_words.append(after_word)
                                
                                exact_match_positions.append(index)

                            # matching the first, second and third word with respective words of wordlist
                            if target_keyword_initial_word in word and target_keyword_list[1] == words_list[index] and target_keyword_list[2] == words_list[index+1]:
                                if index not in exact_match_positions:
                                    substring_positions.append(index)

                                    match = re.search(target_keyword_initial_word, word)
                                    before_word = word[:match.start()] if word[:match.start()] != '' else (words_list[index - 2] if index >= 1 else None)
                                    after_word = word[match.end():] if word[match.end():] != '' else (words_list[index + target_keyword_length - 1] if index < len(words_list) - 1 else None)
                                    before_words.append(before_word)
                                    after_words.append(after_word)

                        #for keywords like 1303.000
                        if substring_positions == [] and exact_match_positions == []:
                            target_keyword_list = target_keyword.split('.')
                            target_keyword_initial_word = target_keyword_list[0]
                            target_keyword_length = len(target_keyword_list)

                            if word == target_keyword_initial_word and target_keyword_list[1] == words_list[index]:
                                before_word = words_list[index - 2] if index >= 1 else None
                                after_word = words_list[index + target_keyword_length - 1] if index < len(words_list) - 1 else None
                                before_words.append(before_word)
                                after_words.append(after_word)
                                
                                exact_match_positions.append(index)

                    word_positions = substring_positions + exact_match_positions

                    # Find position and line number of the target word
                    character_positions = [match.start() + 1 for match in re.finditer(r'{}'.format(target_keyword), page_text)]

                    line_position = [line_number for line_number, line in enumerate(page_text.split('\n'), start=1) if target_keyword in line]


                    page_statistics.append({
                        'text':page_text,
                        'page_number': page_number + 1,
                        'word_count': word_count,
                        'line_count': line_count,
                        'character_count': character_count,
                        'target_keyword_character_positions': character_positions,
                        'target_keyword_line_position': line_position,
                        'target_keyword_location':word_positions,
                        'words_before_keyword': before_words,
                        'words_after_keyword': after_words
                    })

                return page_statistics

                document_type_id = identify_document_type(page_text)
                (identified_keyword, document_type_id)= identify_document_type(page_text)
                print(identified_keyword, document_type_id)
                # Get the original filename of the uploaded file
                original_filename = uploaded_file.filename

                # Include page number in the filename
                filename_with_page = f"{original_filename}_page_{page_number + 1}"
                try:
                    user_document_type = request.json.get('document_type')
                except:
                    user_document_type = None    
                # If no keyword is identified, prompt user for document type
                if identified_keyword and user_document_type is None:
                    return jsonify({"message": "document not identified, enter a keyword along with it"}), 201
                
                if identified_keyword:
                    uploaded_document = UploadedDocumentModel(
                    filename=filename_with_page,
                    document_type_id=document_type_id,
                    identified_keywords= identified_keyword
                    )

                    # Add the uploaded document to the database
                    db.session.add(uploaded_document)
                    db.session.commit()
                    return jsonify({"message": "Document uploaded successfully"}), 201
                
                if user_document_type:
                    # Create a new keyword and document type
                    new_document_type = DocumentTypeModel(document_type=user_document_type)
                    db.session.add(new_document_type)
                    db.session.commit()

                    new_document_type_id = new_document_type.id

                    new_keyword = KeywordModel(keyword=user_document_type, document_type_id=new_document_type_id)
                    db.session.add(new_keyword)
                    db.session.commit()

                    uploaded_document = UploadedDocumentModel(
                    filename=filename_with_page,
                    document_type_id=document_type_id,
                    identified_keywords= identified_keyword
                    )
                    
            
            else:
                return jsonify({'error': 'Uploaded file is not a PDF'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

def extract_text_from_pdf(pdf_file):
    pdf_text = ''
    reader = PyPDF2.PdfReader(pdf_file)
    
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        pdf_text += page.extract_text()
        
    return pdf_text

def identify_document_type(document_content):
    keywords = KeywordModel.query.all()
    for keyword in keywords:
        if keyword.keyword.lower() in document_content.lower():
            return (keyword.keyword, keyword.document_type_id)
    
    return (None,None)  # No matching keyword found



    
    