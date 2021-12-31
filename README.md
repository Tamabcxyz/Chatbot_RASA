Rasa không hỗ trợ tiếng viêt nên file vi_tokeninzer.py được viết nhằm mục đích sử dụng thư viện Underthesea để tách từ tiếng Việt.
Lưu ý: trước khi đưa nó vào pipline của file config.yml thì phải bỏ nó vào thư mục tokenizers trong thư viện rasa và phải đăng kí trong file registry.py mới có thể sử dụng được. qua từng phiên bản của rasa có thể biến hoặc đường dẫn import sẽ sai cần vào thư viện kiểm tra đường dẫn và cấu hình cho đúng.
Đầu tiên phải tải giọng đọc cho tiếng Việt trên Windows
Cách cài đặt console có thể sử dụng voice để nhận input đầu vào mở regedit.exe (Windows + R, gõ regedit) điều hướng theo đường dẫn Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens.
Chuột phải vào voice muốn set tiếng Việt chọn export (phiên bản Win của tôi là giọng của An phát âm tiếng Việt).
Mở file đã được export ra (có thể sử dụng Notepad++ hoặc bất cứ trình editor nào), thay thế \HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens bằng HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens
Tiếp tục thay thế đường dẫn tiếp theo HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\SPEECH\Voices\Tokens
Save và chạy file vừa edit => Accept the registry modification.
Khởi động lại máy.

de kiem tra voice cua may tinh dung code sau:
import pyttsx3

converter = pyttsx3.init() 
voices = converter.getProperty('voices')  
for voice in voices: 
    # to get the info. about various voices in our PC  
    print("Voice:") 
    print("ID: %s" %voice.id) 
    print("Name: %s" %voice.name) 
    print("Age: %s" %voice.age) 
    print("Gender: %s" %voice.gender) 
    print("Languages Known: %s" %voice.languages) 

de dung voice mat dinh cua may tinh dung code sau: trong do index duoc lay tu code ben tren
import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[index].id) 

để chạy cần mở 2 command line
1. rasa run actions
2. rasa shell

==============================================================================
Rasa does not support Vietnamese, so the file vi_tokeninzer.py was written to use the Underthesea library to extract Vietnamese words.
Note: before putting it in the pipline of the config.yml file, it must be put in the tokenizers folder in the rasa library and must be registered in the registry.py file to be able to use it. Through each version of rasa can be variable or import path will be wrong need to go to the library to check the path and configure it correctly.
First you have to download the voiceover for Vietnamese on Windows
How to install console that can use voice to receive input open regedit.exe (Windows + R, type regedit) navigate to the path Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens.
Right-click the voice you want to set Vietnamese and select export (my Win version is An's voice with Vietnamese pronunciation).
Open the exported file (can use Notepad++ or any other editor), replace \HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens with HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens
Continue to replace the next path HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\SPEECH\Voices\Tokens
Save and run the edited file => Accept the registry modification.
Restart the machine.

To check the voice of the computer using the following code:
import pyttsx3

converter = pyttsx3.init()
voices = converter.getProperty('voices')
for voice in voices:
    # to get the info. about various voices in our PC
    print("Voice:")
    print("ID: %s" %voice.id)
    print("Name: %s" %voice.name)
    print("Age: %s" %voice.age)
    print("Gender: %s" %voice.gender)
    print("Languages ​​Known: %s" %voice.languages)

To use the user's voice command, use the following code: in the index, the code is displayed above
import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[index].id)
Open 2 command line
1. rasa run actions
2. rasa shell