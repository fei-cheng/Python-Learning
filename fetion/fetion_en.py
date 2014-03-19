import urllib
import urllib2
import datetime

class fetion:
    base_url = 'http://quanapi.sinaapp.com/fetion.php'
    # log in
    def log_in(self, sender, passwd):
        self.sender = sender
        self.passwd = passwd
        
    def get_text_content(self, city_list):
        text_content_dict = {}
        today = datetime.date.today()
        yesterday = today + datetime.timedelta(days = -1)
        day = str(today.day)
        year = str(today.year)
        month = str(today.month)
        
        try:
            quip_url = 'http://xue.youdao.com/w?page=1&type=all&position=tinyEnglish'
            quip_content = urllib2.urlopen(quip_url).read()
            first_idx = quip_content.find('<p class="sen">')
            second_idx = quip_content[first_idx:].find('</p>')
            quip = quip_content[first_idx + 15 : first_idx + second_idx]
        except:
            quip = 'In order to be irreplaceable, one must always be different!'
        
        website_head = 'http://www.wunderground.com/history/airport/'
        website_tail = '/' +  datetime.datetime.strftime(yesterday, '%Y/%m/%d') + '/CustomHistory.html?dayend=' + day + '&monthend=' + month + '&yearend=' + year + '&req_city=NA&req_state=NA&req_statename=NA&format=1'
        for city in city_list:
            if text_content_dict.get(city, None) is None:
                weather = ''
                try:
                    city_url = website_head + city + website_tail
                    weather_info = urllib2.urlopen(city_url).read()
                    # extract today's weather information
                    today_idx = weather_info.find(year + '-' + month + '-' + day)
                    today_weather = weather_info[today_idx:].split(',')
                    
                    weather += city + '(' + today_weather[0] + ')\n'
                    weather += 'Weather: ' + today_weather[21] + '\n'
                    weather += 'Temperature: ' + today_weather[3] + '~' + today_weather[1] + 'Celsius\n'
                    weather += 'Wind Speed: ' + today_weather[17] + '(Km/h)\n\n'
                except:
                    weather = 'Sorry! No weather information.'
                text_content_dict[city] = weather + quip
                
        return text_content_dict

    # send text
    def send_text(self, receiver_city_info):
        city_list = [item[1] for item in receiver_city_info]
        
        # get text content(weather & quip)
        text_content_dict = self.get_text_content(city_list)
        
        for item in receiver_city_info:
            receiver = item[0]
            text_content = text_content_dict[item[1]].replace(' ', '%20').replace(':', '%3A').replace('\n', '%0d').replace('-', '%2d')
            smsurl = self.base_url + '?u=' + self.sender + '&p=' + self.passwd + '&to=' + receiver + '&m=' + text_content
            if ((urllib2.urlopen(smsurl).read()).split(',')[0].split(':')[1]) == '0':
                print('Success')

if __name__ == '__main__':
    message = fetion()
    sender  = 'your phone number'
    passwd  = 'your fetion password'
    receiver_city_info = [['13812345678', 'Shanghai'], ['13998765432', 'Beijing']]
    
    message.log_in(sender, passwd)
    message.send_text(receiver_city_info)


