import re
from aiohttp import ClientSession
# import sys
# sys.path.append('/var/www/webApp/webApp')

baseUrl = 'https://api.twitter.com/1.1/statuses/show.json'


class AmharicFilter:
    def __init__(self):
        self.sentence = ''
        self.location = ''
        self.country = ''
        self.amharic_letters = ['ሀ', 'ሁ', 'ሂ', 'ሃ', 'ሄ', 'ህ', 'ሆ', 'ሇ', 'ለ', 'ሉ', 'ሊ', 'ላ', 'ሌ', 'ል', 'ሎ', 'ሏ', 'ሐ', 'ሑ', 'ሒ', 'ሓ', 'ሔ', 'ሕ', 'ሖ', 'ሗ', 'መ', 'ሙ', 'ሚ', 'ማ', 'ሜ', 'ም', 'ሞ', 'ሟ', 'ሠ', 'ሡ', 'ሢ', 'ሣ', 'ሤ', 'ሥ', 'ሦ', 'ሧ', 'ረ', 'ሩ', 'ሪ', 'ራ', 'ሬ', 'ር', 'ሮ', 'ሯ', 'ሰ', 'ሱ', 'ሲ', 'ሳ', 'ሴ', 'ስ', 'ሶ', 'ሷ', 'ሸ', 'ሹ', 'ሺ', 'ሻ', 'ሼ', 'ሽ', 'ሾ', 'ሿ', 'ቀ', 'ቁ', 'ቂ', 'ቃ', 'ቄ', 'ቅ', 'ቆ', 'ቇ', 'ቈ', '቉', 'ቊ', 'ቋ', 'ቌ', 'ቍ', '቎', '቏', 'ቐ', 'ቑ', 'ቒ', 'ቓ', 'ቔ', 'ቕ', 'ቖ', '቗', 'ቘ', '቙', 'ቚ', 'ቛ', 'ቜ', 'ቝ', '቞', '቟', 'በ', 'ቡ', 'ቢ', 'ባ', 'ቤ', 'ብ', 'ቦ', 'ቧ', 'ቨ', 'ቩ', 'ቪ', 'ቫ', 'ቬ', 'ቭ', 'ቮ', 'ቯ', 'ተ', 'ቱ', 'ቲ', 'ታ', 'ቴ', 'ት', 'ቶ', 'ቷ', 'ቸ', 'ቹ', 'ቺ', 'ቻ', 'ቼ', 'ች', 'ቾ', 'ቿ', 'ኀ', 'ኁ', 'ኂ', 'ኃ', 'ኄ', 'ኅ', 'ኆ', 'ኇ', 'ኈ', '኉', 'ኊ', 'ኋ', 'ኌ', 'ኍ', '኎', '኏', 'ነ', 'ኑ', 'ኒ', 'ና', 'ኔ', 'ን', 'ኖ', 'ኗ', 'ኘ', 'ኙ', 'ኚ', 'ኛ', 'ኜ', 'ኝ', 'ኞ', 'ኟ', 'አ', 'ኡ', 'ኢ', 'ኣ', 'ኤ', 'እ', 'ኦ', 'ኧ', 'ከ', 'ኩ', 'ኪ', 'ካ', 'ኬ', 'ክ', 'ኮ', 'ኯ', 'ኰ', '኱', 'ኲ', 'ኳ', 'ኴ', 'ኵ', '኶', '኷', 'ኸ', 'ኹ', 'ኺ', 'ኻ', 'ኼ', 'ኽ', 'ኾ', '኿', 'ዀ', '዁', 'ዂ', 'ዃ', 'ዄ', 'ዅ', '዆', '዇',
                                'ወ', ' ዉ', 'ዊ', 'ዋ', 'ዌ', 'ው', 'ዎ', 'ዏ', 'ዐ', 'ዑ', 'ዒ', 'ዓ', 'ዔ', 'ዕ', 'ዖ', '዗', 'ዘ', 'ዙ', 'ዚ', 'ዛ', 'ዜ', 'ዝ', 'ዞ', 'ዟ', 'ዠ', 'ዡ', 'ዢ', 'ዣ', 'ዤ', 'ዥ', 'ዦ', 'ዧ', 'የ', 'ዩ', 'ዪ', 'ያ', 'ዬ', 'ይ', 'ዮ', 'ዯ', 'ደ', 'ዱ', 'ዲ', 'ዳ', 'ዴ', 'ድ', 'ዶ', 'ዷ', 'ዸ', 'ዹ', 'ዺ', 'ዻ', 'ዼ', 'ዽ', 'ዾ', 'ዿ', 'ጀ', 'ጁ', 'ጂ', 'ጃ', 'ጄ', 'ጅ', 'ጆ', 'ጇ', 'ገ', 'ጉ', 'ጊ', 'ጋ', 'ጌ', 'ግ', 'ጎ', 'ጏ', 'ጐ', '጑', 'ጒ', 'ጓ', 'ጔ', 'ጕ', '጖', '጗', 'ጘ', 'ጙ', 'ጚ', 'ጛ', 'ጜ', 'ጝ', 'ጞ', 'ጟ', 'ጠ', 'ጡ', 'ጢ', 'ጣ', 'ጤ', 'ጥ', 'ጦ', 'ጧ', 'ጨ', 'ጩ', 'ጪ', 'ጫ', 'ጬ', ' ጭ', 'ጮ', 'ጯ', 'ጰ', 'ጱ', 'ጲ', 'ጳ', 'ጴ', 'ጵ', 'ጶ', 'ጷ', 'ጸ', 'ጹ', 'ጺ', 'ጻ', 'ጼ', 'ጽ', 'ጾ', 'ጿ', 'ፀ', 'ፁ', 'ፂ', 'ፃ', 'ፄ', 'ፅ', 'ፆ', 'ፇ', 'ፈ', 'ፉ', 'ፊ', 'ፋ', 'ፌ', 'ፍ', 'ፎ', 'ፏ', 'ፐ', 'ፑ', 'ፒ', 'ፓ', 'ፔ', 'ፕ', 'ፖ', 'ፗ', 'ፘ', 'ፙ', 'ፚ', '፛', '፜', '፝', '፞', '፟', '፠', '፡', '።', '፣', '፤', '፥', '፦', '፧', '፨', '፩', '፪', '፫', '፬', '፭', '፮', '፯', '፰', '፱', '፲', '፳', '፴', '፵', '፶', '፷', '፸', '፹', '፺', '፻', '፼', '፽', '፾', '፿', 'ᎀ', 'ᎁ', 'ᎂ', 'ᎃ', 'ᎄ', 'ᎅ', 'ᎆ', 'ᎇ', 'ᎈ', 'ᎉ', 'ᎊ', 'ᎋ', 'ᎌ', 'ᎍ', 'ᎎ', 'ᎏ', '᎐', '።', '፣']

    def setData(self, sentence, country):
        self.sentence = sentence
        self.country = country

    def setLocation(self, location):
        self.location = location

    def getLocation(self):
        return self.location

    def getData(self):
        return {
            "sentence": self.sentence,
            "location": self.location,
            "country": self.country
        }

    def normalize(self):
        norm = self.sentence

        norm = norm.replace("ሃ", "ሀ")
        norm = norm.replace("ሐ", "ሀ")
        norm = norm.replace("ሓ", "ሀ")
        norm = norm.replace("ኅ", "ሀ")
        norm = norm.replace("ኻ", "ሀ")
        norm = norm.replace("ኃ", "ሀ")
        norm = norm.replace("ዅ", "ሁ")
        norm = norm.replace("ሗ", "ኋ")
        norm = norm.replace("ኁ", "ሁ")
        norm = norm.replace("ኂ", "ሂ")
        norm = norm.replace("ኄ", "ሄ")
        norm = norm.replace("ዄ", "ሄ")
        norm = norm.replace("ኅ", "ህ")
        norm = norm.replace("ኆ", "ሆ")
        norm = norm.replace("ሑ", "ሁ")
        norm = norm.replace("ሒ", "ሂ")
        norm = norm.replace("ሔ", "ሄ")
        norm = norm.replace("ሕ", "ህ")
        norm = norm.replace("ሖ", "ሆ")
        norm = norm.replace("ኾ", "ሆ")
        norm = norm.replace("ሠ", "ሰ")
        norm = norm.replace("ሡ", "ሱ")
        norm = norm.replace("ሢ", "ሲ")
        norm = norm.replace("ሣ", "ሳ")
        norm = norm.replace("ሤ", "ሴ")
        norm = norm.replace("ሥ", "ስ")
        norm = norm.replace("ሦ", "ሶ")
        norm = norm.replace("ሼ", "ሸ")
        norm = norm.replace("ቼ", "ቸ")
        norm = norm.replace("ዬ", "የ")
        norm = norm.replace("ዲ", "ድ")
        norm = norm.replace("ጄ", "ጀ")
        norm = norm.replace("ፀ", "ጸ")
        norm = norm.replace("ፁ", "ጹ")
        norm = norm.replace("ፂ", "ጺ")
        norm = norm.replace("ፃ", "ጻ")
        norm = norm.replace("ፄ", "ጼ")
        norm = norm.replace("ፅ", "ጽ")
        norm = norm.replace("ፆ", "ጾ")
        norm = norm.replace("ዉ", "ው")
        norm = norm.replace("ዴ", "ደ")
        norm = norm.replace("ቺ", "ች")
        norm = norm.replace("ዪ", "ይ")
        norm = norm.replace("ጪ", "ጭ")
        norm = norm.replace("ዓ", "አ")
        norm = norm.replace("ዑ", "ኡ")
        norm = norm.replace("ዒ", "ኢ")
        norm = norm.replace("ዐ", "አ")
        norm = norm.replace("ኣ", "አ")
        norm = norm.replace("ዔ", "ኤ")
        norm = norm.replace("ዕ", "እ")
        norm = norm.replace("ዖ", "ኦ")
        norm = norm.replace("ኚ", "ኝ")
        norm = norm.replace("ሺ", "ሽ")

        norm = re.sub('(ሉ[ዋአ])', 'ሏ', norm)
        norm = re.sub('(ሙ[ዋአ])', 'ሟ', norm)
        norm = re.sub('(ቱ[ዋአ])', 'ቷ', norm)
        norm = re.sub('(ሩ[ዋአ])', 'ሯ', norm)
        norm = re.sub('(ሱ[ዋአ])', 'ሷ', norm)
        norm = re.sub('(ሹ[ዋአ])', 'ሿ', norm)
        norm = re.sub('(ቁ[ዋአ])', 'ቋ', norm)
        norm = re.sub('(ቡ[ዋአ])', 'ቧ', norm)
        norm = re.sub('(ቹ[ዋአ])', 'ቿ', norm)
        norm = re.sub('(ሁ[ዋአ])', 'ኋ', norm)
        norm = re.sub('(ኑ[ዋአ])', 'ኗ', norm)
        norm = re.sub('(ኙ[ዋአ])', 'ኟ', norm)
        norm = re.sub('(ኩ[ዋአ])', 'ኳ', norm)
        norm = re.sub('(ዙ[ዋአ])', 'ዟ', norm)
        norm = re.sub('(ጉ[ዋአ])', 'ጓ', norm)
        norm = re.sub('(ደ[ዋአ])', 'ዷ', norm)
        norm = re.sub('(ጡ[ዋአ])', 'ጧ', norm)
        norm = re.sub('(ጩ[ዋአ])', 'ጯ', norm)
        norm = re.sub('(ጹ[ዋአ])', 'ጿ', norm)
        norm = re.sub('(ፉ[ዋአ])', 'ፏ', norm)
        norm = re.sub('[ቊ]', 'ቁ', norm)
        norm = re.sub('[ኵ]', 'ኩ', norm)
        norm = re.sub('\s+', ' ', norm)

        self.sentence = norm
        return norm

    def checkIfAmharic(self):
        # regex to check if sentence contains only amharic letters

        # function to check if sentence contains only amharic letters
        amh_letters = set(self.amharic_letters)

        def checkIfAmharic(s):
            ct = 0
            for letter in s:
                if letter not in self.amharic_letters:
                    ct += 1
            if ct / len(s) > 0.3:
                return False
            return True

        # check = re.compile('[^ሀ-ፚ]+')
        ss = re.sub('[\s+]', '', self.sentence)
        check = checkIfAmharic(ss)

        return check

    async def get_data(self, tweet_id):
        endpoint = f'?id={tweet_id}'

        headers = {"Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAAJ0PXQEAAAAAHBTso%2BOW1k6V5kgGzCfIGLMbUpg%3DvXjswixg0EJ3sgt1uBL78uyeJDfwyAcpXkHjE34aaPsBc07pv6"}
        async with ClientSession() as session:
            async with session.get(f'{baseUrl}{endpoint}', headers=headers) as response:
                return await response.json()
