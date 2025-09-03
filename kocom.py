state = {'floor': floor}
if rs485_floor==floor:
state['state'] = 'off'
                threading.Thread(target=mqttc.publish, args=("kocom/myhome/evarrival/state", json.dumps({'state':'on'}))).start()
                threading.Timer(10, mqttc.publish, args=("kocom/myhome/evarrival/state", json.dumps({'state':'off'}))).start()
else:
state = {'state': 'off'}
            threading.Thread(target=mqttc.publish, args=("kocom/myhome/evarrival/state", json.dumps({'state':'on'}))).start()
            threading.Timer(10, mqttc.publish, args=("kocom/myhome/evarrival/state", json.dumps({'state':'off'}))).start()
logtxt='[MQTT publish|elevator] data[{}]'.format(state)
mqttc.publish("kocom/myhome/elevator/state", json.dumps(state))
# aa5530bc0044000100010300000000000000350d0d
@@ -558,6 +562,8 @@ def discovery():
sub = dev[1]
publish_discovery(dev[0], sub)
publish_discovery('query')
    publish_discovery('evarrival')


#https://www.home-assistant.io/docs/mqtt/discovery/
#<discovery_prefix>/<component>/<object_id>/config
@@ -614,30 +620,50 @@ def publish_discovery(dev, sub=''):
if logtxt != "" and config.get('Log', 'show_mqtt_publish') == 'True':
logging.info(logtxt)
elif dev == 'elevator':
        for i in ['elevator', 'evsensor']: 
            component = 'switch' if i == 'elevator' else 'sensor'
            topic = f'homeassistant/{component}/kocom_wallpad_{i}/config'
            payload = {
                'name': f'Kocom Wallpad {i}',
                'cmd_t': "kocom/myhome/elevator/command",
                'stat_t': "kocom/myhome/elevator/state",
                'val_tpl': "{{ value_json.floor }}",
                'pl_on': 'on',
                'pl_off': 'off',
                'qos': 0,
                'uniq_id': '{}_{}_{}'.format('kocom', 'wallpad', i),
                'device': {
                    'name': '코콤 스마트 월패드',
                    'ids': 'kocom_smart_wallpad',
                    'mf': 'KOCOM',
                    'mdl': '스마트 월패드',
                    'sw': SW_VERSION
                }
        component = 'switch'
        topic = f'homeassistant/{component}/kocom_wallpad_{dev}/config'
        payload = {
            'name': 'Kocom Wallpad Elevator',
            'cmd_t': "kocom/myhome/elevator/command",
            'stat_t': "kocom/myhome/elevator/state",
            'val_tpl': "{{ value_json.floor }}",
            'pl_on': 'on',
            'pl_off': 'off',
            'qos': 0,
            'uniq_id': '{}_{}_{}'.format('kocom', 'wallpad', dev),
            'device': {
                'name': '코콤 스마트 월패드',
                'ids': 'kocom_smart_wallpad',
                'mf': 'KOCOM',
                'mdl': '스마트 월패드',
                'sw': SW_VERSION
}
            logtxt='[MQTT Discovery|{}] data[{}]'.format(i, topic)
            mqttc.publish(topic, json.dumps(payload))
            if logtxt != "" and config.get('Log', 'show_mqtt_publish') == 'True':
                logging.info(logtxt)
        }
        logtxt='[MQTT Discovery|{}] data[{}]'.format(dev, topic)
        mqttc.publish(topic, json.dumps(payload))
        if logtxt != "" and config.get('Log', 'show_mqtt_publish') == 'True':
            logging.info(logtxt)
    elif dev == 'evarrival':
        component = 'sensor'
        topic = f'homeassistant/{component}/kocom_wallpad_{dev}/config'
        payload = {
            'name': 'Kocom Wallpad Evarrival',
            'stat_t': "kocom/myhome/evarrival/state",
            'val_tpl': "{{ value_json.state }}",
            'qos': 0,
            'uniq_id': '{}_{}_{}'.format('kocom', 'wallpad', dev),
            'device': {
                'name': '코콤 스마트 월패드',
                'ids': 'kocom_smart_wallpad',
                'mf': 'KOCOM',
                'mdl': '스마트 월패드',
                'sw': SW_VERSION
            }
        }
        logtxt='[MQTT Discovery|{}] data[{}]'.format(dev, topic)
        mqttc.publish(topic, json.dumps(payload))
        if logtxt != "" and config.get('Log', 'show_mqtt_publish') == 'True':
            logging.info(logtxt)
elif dev == 'light':
for num in range(1, int(config.get('User', 'light_count'))+1):
#ha_topic = 'homeassistant/light/kocom_livingroom_light1/config'
@@ -723,7 +749,7 @@ def poll_state(enforce=False):
poll_timer.cancel()

dev_list = [x.strip() for x in config.get('Device','enabled').split(',')]
    no_polling_list = ['wallpad', 'elevator']
    no_polling_list = ['wallpad', 'elevator', 'evarrival']

#thread health check
for thread_instance in thread_list:
@@ -793,7 +819,7 @@ def read_serial():
not_parsed_buf += buf
buf=''
else:
                        not_parsed_buf += buf[:frame_start]
                        not_parsed_buf += buf[frame_start:]
buf = buf[frame_start:]
except Exception as ex:
logging.error("*** Read error.[{}]".format(ex) )
