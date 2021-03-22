import requests
import json
import PyPDF2

def search_annotation():
    hed = {'Authorization': 'Bearer 6879-uKcO5X5KMfWKiQ4PX_K8c8XthXp3g-JkuMY_eFPOzsw' }
    response = requests.get('https://api.hypothes.is/api/search?limit=200&user=krnlet@hypothes.is', headers=hed)
    response2=response.json()

    ids=[]
    #together=dict()
    list_tog=list()
    list_tog.append({'total':response2['total']})
    for i in range(len(response2['rows'])):
        ids.append(response2['rows'][i]['id'])
        #print(response2['rows'][i]['id'])
        together={'id': response2['rows'][i]['id'],
            'word_tag': response2['rows'][i]['target'][0]['selector'][0]['exact'],
            'text':response2['rows'][i]['text']}
        list_tog.append(together)
    return(ids, list_tog)


def create_annotation(array_exact, prefixes, sufixes, starts, ends):
    
    size=len(array_exact)
    print(len(sufixes))
    for i in range(len(sufixes)):
        value=array_exact[0]
        prefix=prefixes[i]
        sufix=sufixes[i]
        start=starts[i]
        end=ends[i]
        #print(value)
        #print(prefix)
        #print(sufix)
        label={}
        label2={}
        label_array=[]
        label['type']="TextQuoteSelector"
        label['prefix']=prefix
        label['exact']=value
        label['sufix']=sufix
        label_array.append(label)
        label2['type']="TextPositionSelector"
        label2['start']=start
        label2['end']=end
        label_array.append(label2)
        
        #print(i,'--',label_array)
        hed = {'Authorization': 'Bearer 6879-uKcO5X5KMfWKiQ4PX_K8c8XthXp3g-JkuMY_eFPOzsw' }
        data={
            "uri": "http://course.sdu.edu.cn/G2S/eWebEditor/uploadfile/20131018104402214.pdf",
        "user": "acct:krnl@example.org",
        
        "document": {
            "title": "What Is An Ethics Assessment"
        },
        "target": 
            [{
                "source": "http://course.sdu.edu.cn/G2S/eWebEditor/uploadfile/20131018104402214.pdf",
                "selector": 
                    label_array,
            }], 
        "tags": [value+'-'+str(i)],
        "text": "Annotation by Karen."
        }
        #print('-',prefix,'-')
        #print('-',sufix,'-')
        response = requests.post('https://api.hypothes.is/api/annotations', json=data, headers=hed)
        response2=response.json()
        #print(response2)
    return(response2)
        

def delete_annotation(ids):
    trash=list()
    for i in ids:
        print(i)
        id_del=i
        hed = {'Authorization': 'Bearer 6879-uKcO5X5KMfWKiQ4PX_K8c8XthXp3g-JkuMY_eFPOzsw' }
        response = requests.delete('https://api.hypothes.is/api/annotations/'+id_del, headers=hed)
        response2=response.json()
        trash.append(response2)
        print(response2)
    return(trash)

def pdfread(url, words):
    url = 'http://course.sdu.edu.cn/G2S/eWebEditor/uploadfile/'+url
    response = requests.get(url)
    my_raw_data = response.content

    with open("my_pdf.pdf", 'wb') as my_data:
        my_data.write(my_raw_data)

    open_pdf_file = open("my_pdf.pdf", 'rb')
    read_pdf = PyPDF2.PdfFileReader(open_pdf_file)
    
    if read_pdf.isEncrypted:
        read_pdf.decrypt("---")
        print(read_pdf.getPage(0).extractText())

    else:
        np=read_pdf.getNumPages()
        paragraph=[]
        #substring="ethics"
        paragraphtext=str()
        for page in range(np):
            print('-----------------',page)
            text=read_pdf.getPage(page).extractText().replace('\n',' ')
            size=len(text)
            
            posicion = 0
            sufixes=[]
            prefixes=[]
            posiciones = []
            #print(text)
            paragraphtext+=''+text
            paragraph.append(text)
        for substring in words: 
            for i in paragraph:
                if(substring in i):
                    pos=i.index(substring)
                    #print(pos, i[pos:pos+len(substring)])
            #print(len(paragraphtext))
            starts=list()
            ends=list()
            while posicion != -1:
                posicion = paragraphtext.find(substring,posicion)
                if posicion != -1:
                    posiciones.append(posicion)
                    posicion += 1
            print(posiciones)
            sufixes=[]
            prefixes=[]
            for i in posiciones:
                pos=i
                subsub=paragraphtext[pos:pos+len(substring)]
                #print(pos, subsub)
                prefix=paragraphtext[pos-31:pos]
                prefixes.append(prefix)
                #print('Pre: ',prefix)
                #print(substring)
                sufix=paragraphtext[pos+len(substring):pos+len(substring)+31]
                sufixes.append(sufix)
                #print('Suf: ',sufix)
                #print(prefixes)
                #print(sufixes)
                #print(len(prefixes), len(sufixes))
                
                starts.append(pos)
                ends.append(pos+len(substring))
            words=[substring]
            res=create_annotation(words, prefixes, sufixes, starts, ends)
    #print(res)
    
    return(res)

def main(url, words):
    ids=search_annotation()
    delete_annotation(ids[0])
    arrays=pdfread(url, words)
    #array_exact=["ethics"]
    #create_annotation(array_exact, arrays[0], arrays[1])




