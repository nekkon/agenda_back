from mongoengine import *
import datetime

class Config(DynamicDocument):
    pass

class Traffic(DynamicDocument):
    created_at = DateTimeField(default=datetime.datetime.now)


from mongoengine import *



class Translation(DynamicDocument):

    _id = StringField(unique=True,primary_key=True)

    @staticmethod
    def get_default_lang():
        return Config.objects.get(config_id='general')['translations']['default_lang']

    @staticmethod
    def get_possible_langs():
        return Config.objects.get(config_id='general')['translations']['languages']


    @staticmethod
    def downloadCSV(csv_url = """https://docs.google.com/spreadsheets/d/1bINGrQDuslpBLjmssYDy1JGDb7A8Wu1_2MX9_RllWLU/export?format=csv&id=1bINGrQDuslpBLjmssYDy1JGDb7A8Wu1_2MX9_RllWLU&gid=0"""):
        import requests
        from io import StringIO
        csv = requests.get(url=csv_url,verify=False)
        csv.encoding = 'utf-8'
        return StringIO(csv.text)

    @staticmethod
    def importFromCSVFile(csvfile):
        import csv
        reader_list = csv.DictReader(csvfile)
        i = 1
        for row in reader_list:

            try:
                entity = Translation()
                for field in row:
                    entity.__setattr__(field,row[field])
                entity.save()
                print('The '+str(i)+' translation inserted')
                i += 1
            except ValidationError:
                print(ValidationError)
                pass

    @staticmethod
    def get_translations(lang):
        translations = Translation.objects.fields(**{
            '_id':1,
            lang:1
        })
        res = {}
        for translation in translations:
            res.update({translation['_id']:translation[lang]})

        return res
