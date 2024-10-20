from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH


def process_text(paragraph, text):
    """Обработка текста и добавление к последнему элементу списка"""
    if 'footnote' in paragraph:
        return f' {text}' if text[0].isalpha() else text
    raise ValueError


def extract_word_data(file_path):
    doc = Document(file_path)
    data = []
    footnote_counter = 1
    footnote_title = ''
    idx = 1
    for block in doc.paragraphs:
        text_len = len(block.text.strip())
        text = ''
        style = ''
        css = ''
        if block.text == '':
            data[-1]['text'] += '<br>'

        for run in block.runs:
            content = run.text.replace('\n', '<br>')
            if run.italic:
                text += f'<i>{content}</i>'
            if run.bold:
                text += f'<b>{content}</b>'
            if run.underline:
                footnote_title = (
                    f'<button data-modal-target="footnote_{footnote_counter}" '
                    f'data-modal-toggle="footnote_{footnote_counter}" type="button"'
                    f'>{content}')
                continue
            if run.font.superscript:
                content = f'{footnote_title}<sup>{footnote_counter}</sup></button>'
                footnote_counter += 1
                text += content
            else:
                text += content

        if block.style.name == 'Subtitle':
            tag = 'img'
            css += 'cover'
            text_len = 0
        elif block.style.name == 'Title':
            tag = 'header'
            css = 'chapter-header dark:chapter-header'
        elif block.style.name == 'Signature':
            tag = 'signature'
        elif block.style.name == 'Heading 1':
            tag = 'h1'
            css = 'chapter-title dark:chapter-title'
        elif block.style.name == 'footnote text':
            tag = 'div'
            css = ('footnote fixed top-0 left-0 right-0 z-50 hidden w-full p-4 '
                   'overflow-x-hidden overflow-y-auto md:inset-0 h-[calc(100%-1rem)] max-h-full')
            text = f'''<div class="relative w-full max-w-md max-h-full">
                <div class="relative bg-white rounded-lg shadow dark:bg-gray-700">
                    <div class="flex items-center justify-between p-4 md:p-5 border-b rounded-t dark:border-gray-600">
                        <button type="button" data-modal-hide="footnote_{idx}" 
                        class="text-gray-400 bg-transparent hover:bg-gray-200 
                        hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto 
                        inline-flex justify-center items-center dark:hover:bg-
                        gray-600 dark:hover:text-white">
                            <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
                                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"/>
                            </svg>
                            <span class="sr-only">Close modal</span>
                        </button>
                    </div>
                    <div class="p-4 md:p-5 space-y-4">
                        <p class="text-base leading-relaxed text-gray-500 dark:text-gray-400">
                        {text}
                        </p>
                    </div>
                </div>
            </div>'''
            idx += 1
        elif block.style.name == 'Body Text':
            tag = 'p'
        else:
            tag = 'i'

        if block.style.paragraph_format.alignment == WD_ALIGN_PARAGRAPH.CENTER:
            style += 'text-align: center;'
        elif block.style.paragraph_format.alignment == WD_ALIGN_PARAGRAPH.RIGHT:
            style += 'text-align: right; '
        elif (block.style.paragraph_format.alignment ==
              WD_ALIGN_PARAGRAPH.JUSTIFY and block.style.name != 'footnote '
                                                                 'text'):
            style += 'text-align: justify;'
        if text:
            data.append(
                {
                    'tag': tag,
                    'css': css,
                    'src': '',
                    'style': style,
                    'text': text,
                    'text_len': text_len,
                }
            )
    return data
