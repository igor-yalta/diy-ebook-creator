# Create your forms here.
from django import forms
from django.forms import ModelForm, Select
from models import Project
import djos

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ('title', 'date_created', 'path', 'color_mode', 'auto_mode', 'language1', 'language2', 'language3')
        COLORS = (
                   ('mixed', 'Mixed (i.e. some color or grayscale, some black and white)'),
                   ('color_grayscale', 'Color / Grayscale'),
                   ('black_and_white', 'Black and White only'),
                   )
        AUTO   = (
                  ('manual', 'Manual: Tweak pages with Scantailor prior to creating PDF'),
                  ('auto', 'Auto: Create PDF without tweaking'),
                  )
        LANGS  = (
                    ('Abkhaz', 'Abkhaz'),
                    ('Adyghe', 'Adyghe'),
                    ('Afrikaans', 'Afrikaans'),
                    ('Agul', 'Agul'),
                    ('Albanian', 'Albanian'),
                    ('Altaic', 'Altaic'),
                    ('ArmenianEastern', 'ArmenianEastern'),
                    ('ArmenianGrabar', 'ArmenianGrabar'),
                    ('ArmenianWestern', 'ArmenianWestern'),
                    ('Awar', 'Awar'),
                    ('Aymara', 'Aymara'),
                    ('AzeriCyrillic', 'AzeriCyrillic'),
                    ('AzeriLatin', 'AzeriLatin'),
                    ('Bashkir', 'Bashkir'),
                    ('Basic', 'Basic'),
                    ('Basque', 'Basque'),
                    ('Belarusian', 'Belarusian'),
                    ('Bemba', 'Bemba'),
                    ('Blackfoot', 'Blackfoot'),
                    ('Breton', 'Breton'),
                    ('Bugotu', 'Bugotu'),
                    ('Bulgarian', 'Bulgarian'),
                    ('Buryat', 'Buryat'),
                    ('C++', 'C++'),
                    ('Catalan', 'Catalan'),
                    ('Chamorro', 'Chamorro'),
                    ('Chechen', 'Chechen'),
                    ('Chemistry', 'Chemistry'),
                    ('ChinesePRC', 'ChinesePRC'),
                    ('ChineseTaiwan', 'ChineseTaiwan'),
                    ('Chukcha', 'Chukcha'),
                    ('Chuvash', 'Chuvash'),
                    ('Cobol', 'Cobol'),
                    ('Corsican', 'Corsican'),
                    ('CrimeanTatar', 'CrimeanTatar'),
                    ('Croatian', 'Croatian'),
                    ('Crow', 'Crow'),
                    ('Czech', 'Czech'),
                    ('Danish', 'Danish'),
                    ('Dargwa', 'Dargwa'),
                    ('Digits', 'Digits'),
                    ('Dungan', 'Dungan'),
                    ('Dutch', 'Dutch'),
                    ('DutchBelgian', 'DutchBelgian'),
                    ('English', 'English'),
                    ('EskimoCyrillic', 'EskimoCyrillic'),
                    ('EskimoLatin', 'EskimoLatin'),
                    ('Esperanto', 'Esperanto'),
                    ('Estonian', 'Estonian'),
                    ('Even', 'Even'),
                    ('Evenki', 'Evenki'),
                    ('Faeroese', 'Faeroese'),
                    ('Fijian', 'Fijian'),
                    ('Finnish', 'Finnish'),
                    ('Fortran', 'Fortran'),
                    ('French', 'French'),
                    ('Frisian', 'Frisian'),
                    ('Friulian', 'Friulian'),
                    ('GaelicScottish', 'GaelicScottish'),
                    ('Gagauz', 'Gagauz'),
                    ('Galician', 'Galician'),
                    ('Ganda', 'Ganda'),
                    ('German', 'German'),
                    ('GermanLuxembourg', 'GermanLuxembourg'),
                    ('GermanNewSpelling', 'GermanNewSpelling'),
                    ('Greek', 'Greek'),
                    ('Guarani', 'Guarani'),
                    ('Hani', 'Hani'),
                    ('Hausa', 'Hausa'),
                    ('Hawaiian', 'Hawaiian'),
                    ('Hebrew', 'Hebrew'),
                    ('Hungarian', 'Hungarian'),
                    ('Icelandic', 'Icelandic'),
                    ('Ido', 'Ido'),
                    ('Indonesian', 'Indonesian'),
                    ('Ingush', 'Ingush'),
                    ('Interlingua', 'Interlingua'),
                    ('Irish', 'Irish'),
                    ('Italian', 'Italian'),
                    ('Japanese', 'Japanese'),
                    ('Java', 'Java'),
                    ('Kabardian', 'Kabardian'),
                    ('Kalmyk', 'Kalmyk'),
                    ('KarachayBalkar', 'KarachayBalkar'),
                    ('Karakalpak', 'Karakalpak'),
                    ('Kasub', 'Kasub'),
                    ('Kawa', 'Kawa'),
                    ('Kazakh', 'Kazakh'),
                    ('Khakas', 'Khakas'),
                    ('Khanty', 'Khanty'),
                    ('Kikuyu', 'Kikuyu'),
                    ('Kirgiz', 'Kirgiz'),
                    ('Kongo', 'Kongo'),
                    ('Korean', 'Korean'),
                    ('KoreanHangul', 'KoreanHangul'),
                    ('Koryak', 'Koryak'),
                    ('Kpelle', 'Kpelle'),
                    ('Kumyk', 'Kumyk'),
                    ('Kurdish', 'Kurdish'),
                    ('Lak', 'Lak'),
                    ('Lappish', 'Lappish'),
                    ('Latin', 'Latin'),
                    ('Latvian', 'Latvian'),
                    ('Lezgin', 'Lezgin'),
                    ('Lithuanian', 'Lithuanian'),
                    ('Luba', 'Luba'),
                    ('Macedonian', 'Macedonian'),
                    ('Malagasy', 'Malagasy'),
                    ('Malay', 'Malay'),
                    ('Malinke', 'Malinke'),
                    ('Maltese', 'Maltese'),
                    ('Mansi', 'Mansi'),
                    ('Maori', 'Maori'),
                    ('Mari', 'Mari'),
                    ('Maya', 'Maya'),
                    ('Miao', 'Miao'),
                    ('Minankabaw', 'Minankabaw'),
                    ('Mixed(RussianandEnglish)', 'Mixed(RussianandEnglish)'),
                    ('Mohawk', 'Mohawk'),
                    ('Mongol', 'Mongol'),
                    ('Mordvin', 'Mordvin'),
                    ('Nahuatl', 'Nahuatl'),
                    ('Nenets', 'Nenets'),
                    ('Nivkh', 'Nivkh'),
                    ('Nogay', 'Nogay'),
                    ('Norwegian', 'Norwegian'),
                    ('NorwegianBokmal', 'NorwegianBokmal'),
                    ('NorwegianNynorsk', 'NorwegianNynorsk'),
                    ('Nyanja', 'Nyanja'),
                    ('Occidental', 'Occidental'),
                    ('Ojibway', 'Ojibway'),
                    ('Ossetic', 'Ossetic'),
                    ('Papiamento', 'Papiamento'),
                    ('Pascal', 'Pascal'),
                    ('PidginEnglish', 'PidginEnglish'),
                    ('Polish', 'Polish'),
                    ('PortugueseBrazilian', 'PortugueseBrazilian'),
                    ('PortugueseStandard', 'PortugueseStandard'),
                    ('Provencal', 'Provencal'),
                    ('Quechua', 'Quechua'),
                    ('RhaetoRomanic', 'RhaetoRomanic'),
                    ('Romanian', 'Romanian'),
                    ('RomanianMoldavia', 'RomanianMoldavia'),
                    ('Romany', 'Romany'),
                    ('Ruanda', 'Ruanda'),
                    ('Rundi', 'Rundi'),
                    ('Russian', 'Russian'),
                    ('RussianOldSpelling', 'RussianOldSpelling'),
                    ('Samoan', 'Samoan'),
                    ('Selkup', 'Selkup'),
                    ('SerbianCyrillic', 'SerbianCyrillic'),
                    ('SerbianLatin', 'SerbianLatin'),
                    ('Shona', 'Shona'),
                    ('Sioux', 'Sioux'),
                    ('Slovak', 'Slovak'),
                    ('Slovenian', 'Slovenian'),
                    ('Somali', 'Somali'),
                    ('Sorbian', 'Sorbian'),
                    ('Sotho', 'Sotho'),
                    ('Spanish', 'Spanish'),
                    ('Sunda', 'Sunda'),
                    ('Swahili', 'Swahili'),
                    ('Swazi', 'Swazi'),
                    ('Swedish', 'Swedish'),
                    ('Tabassaran', 'Tabassaran'),
                    ('Tagalog', 'Tagalog'),
                    ('Tahitian', 'Tahitian'),
                    ('Tajik', 'Tajik'),
                    ('Tatar', 'Tatar'),
                    ('Thai', 'Thai'),
                    ('Tinpo', 'Tinpo'),
                    ('Tongan', 'Tongan'),
                    ('Tswana', 'Tswana'),
                    ('Tun', 'Tun'),
                    ('Turkish', 'Turkish'),
                    ('Turkmen', 'Turkmen'),
                    ('Tuvin', 'Tuvin'),
                    ('Udmurt', 'Udmurt'),
                    ('UighurCyrillic', 'UighurCyrillic'),
                    ('UighurLatin', 'UighurLatin'),
                    ('Ukrainian', 'Ukrainian'),
                    ('UzbekCyrillic', 'UzbekCyrillic'),
                    ('UzbekLatin', 'UzbekLatin'),
                    ('Vietnamese', 'Vietnamese'),
                    ('Visayan', 'Visayan'),
                    ('Welsh', 'Welsh'),
                    ('Wolof', 'Wolof'),
                    ('Xhosa', 'Xhosa'),
                    ('Yakut', 'Yakut'),
                    ('Yiddish', 'Yiddish'),
                    ('Zapotec', 'Zapotec'),
                    ('Zulu', 'Zulu'),
                  )
        widgets = {'color_mode': Select(choices=COLORS),
                   'auto_mode' : Select(choices=AUTO),
                   'language1' : Select(choices=LANGS),
                   'language2' : Select(choices=LANGS),
                   'language3' : Select(choices=LANGS),
                   }
        
    def clean_path(self):
        p = self.cleaned_data.get('path', '')
        t = self.cleaned_data.get('title', '')
        valid = djos.create_project_dirs(self.cleaned_data)
        if not valid:
            raise forms.ValidationError("I could not create this path: %s. Please check the path and try different one." % (p))
        return p