import json
import urllib
import urllib2

class fetion:
    base_url = 'http://quanapi.sinaapp.com/fetion.php'
    city_code = {'北京' : '101010100',
                 '上海' : '101020100',
                 '杭州' : '101210101',
                 '成都' : '101270101',
                 '安庆' : '101220601'}
    # log in
    def log_in(self, sender, passwd):
        self.sender = sender
        self.passwd = passwd

    def get_quip(self):
        try:
            quip_url = 'http://xue.youdao.com/w?page=1&type=all&position=tinyEnglish'
            quip_content = urllib2.urlopen(quip_url).read()
            first_idx = quip_content.find('<p class="sen">')
            second_idx = quip_content[first_idx:].find('</p>')
            quip = quip_content[first_idx + 15 : first_idx + second_idx]
        except:
            quip = 'In order to be irreplaceable, one must always be different!'
        return quip
        
    def get_weather(self, city_list):
        weather_content_dict = {}
        website_tail = '.html'
        website_head = 'http://www.weather.com.cn/data/sk/'
        
        for city in city_list:
            if weather_content_dict.get(city, None) is None:
                weather = u'---天气预报---' + '\n'
                try:
                    city_url = website_head + self.city_code.get(city, '') + website_tail
                    weather_html = urllib2.urlopen(city_url).read()
                    weather_info = (json.loads(weather_html.decode('utf-8')))['weatherinfo']
                    # extract today's weather information
                    weather += u'城市：' + weather_info['city'] + '\n'
                    weather += u'温度：' + weather_info['temp'] + u'度' + '\n'
                    weather += u'风向：' + weather_info['WD'] + '\n'
                    weather += u'风力：' + weather_info['WS'] + '\n'
                    weather += u'相对湿度：' + weather_info['SD'] + '\n'
                    weather += u'发布时间：' + weather_info['time'] + '\n\n'
                except:
                    weather = u'对不起,无法获取天气信息。'
                weather_content_dict[city] = weather.encode('utf-8')
                
        return weather_content_dict

    # send text
    def send_text(self, receiver_city_info):
        city_list = [item[1] for item in receiver_city_info]
        
        # get text content(weather & quip)
        text_content_dict = self.get_weather(city_list)
        
        for item in receiver_city_info:
            receiver = item[0]
            text_content = text_content_dict[item[1]] + self.get_quip()
            text_content = text_content.replace(' ', '%20').replace(':', '%3A').replace('\n', '%0d').replace('-', '%2d')
            smsurl = self.base_url + '?u=' + self.sender + '&p=' + self.passwd + '&to=' + receiver + '&m=' + text_content
            if ((urllib2.urlopen(smsurl).read()).split(',')[0].split(':')[1]) == '0':
                print('Success')



if __name__ == '__main__':
    message = fetion()
    sender  = 'your phone number'
    passwd  = 'your fetion password'
    receiver_city_info = [['13812345678', '上海'], ['13998765432', '北京']]
    
    message.log_in(sender, passwd)
    message.send_text(receiver_city_info)