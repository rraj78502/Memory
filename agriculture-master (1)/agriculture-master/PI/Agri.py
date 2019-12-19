from urllib import urlopen
import urllib
import json
import paho.mqtt.client as mqtt
import time
import requests
import RPi.GPIO as IO          
                     
IO.setwarnings(False)          
IO.setmode (IO.BCM)        
IO.setup(19,IO.OUT)  
 
ts=time.time()
ts2=time.time()
humidity=0
temp=0
crop=""
devId=0
start_date=""
curr_date=200
start_crop=0
 
ndvi=[0.0755555556,0.0822588523,0.088962149,0.0956654457,0.1023687424,0.1090720391,0.1157753358,0.1224786325,0.1291819292,0.1358852259,0.1425885226,0.1498778999,0.1572405372,0.1646031746,0.171965812,0.1793284493,0.1866910867,0.1940537241,0.2014163614,0.2087789988,0.2161416361,0.2194871795,0.2216849817,0.2238827839,0.2260805861,0.2282783883,0.2304761905,0.2326739927,0.2348717949,0.2370695971,0.2392673993,0.2438827839,0.2497069597,0.2555311355,0.2613553114,0.2671794872,0.273003663,0.2788278388,0.2846520147,0.2904761905,0.2963003663,0.3046886447,0.3151282051,0.3255677656,0.336007326,0.3464468864,0.3568864469,0.3673260073,0.3777655678,0.3882051282,0.3986446886,0.4092307692,0.42,0.4307692308,0.4415384615,0.4523076923,0.4630769231,0.4738461538,0.4846153846,0.4953846154,0.5061538462,0.5165567766,0.5262271062,0.5358974359,0.5455677656,0.5552380952,0.5649084249,0.5745787546,0.5842490842,0.5939194139,0.6035897436,0.6124786325,0.6186324786,0.6247863248,0.6309401709,0.6370940171,0.6432478632,0.6494017094,0.6555555556,0.6617094017,0.6678632479,0.6737728938,0.6777289377,0.6816849817,0.6856410256,0.6895970696,0.6935531136,0.6975091575,0.7014652015,0.7054212454,0.7093772894,0.7133333333,0.7160805861,0.7188278388,0.7215750916,0.7243223443,0.7270695971,0.7298168498,0.7325641026,0.7353113553,0.7380586081,0.7408058608,0.7415018315,0.7419413919,0.7423809524,0.7428205128,0.7432600733,0.7436996337,0.7441391941,0.7445787546,0.745018315,0.7454578755,0.7443589744,0.7428205128,0.7412820513,0.7397435897,0.7382051282,0.7366666667,0.7351282051,0.7335897436,0.7320512821,0.7305128205,0.726996337,0.7224908425,0.717985348,0.7134798535,0.708974359,0.7044688645,0.69996337,0.6954578755,0.690952381,0.6864468864,0.6805982906,0.6736752137,0.6667521368,0.6598290598,0.6529059829,0.645982906,0.6390598291,0.6321367521,0.6252136752,0.6182905983,0.61004884,0.6001587302,0.5902686203,0.5803785104,0.5704884005,0.5605982906,0.5507081807,0.5408180708,0.5309279609,0.521037851,0.5106715507,0.4993528694,0.488034188,0.4767155067,0.4653968254,0.4540781441,0.4427594628,0.4314407814,0.4201221001,0.4088034188,0.3981196581,0.3896581197,0.3811965812,0.3727350427,0.3642735043,0.3558119658,0.3473504274,0.3388888889,0.3304273504,0.321965812,0.313992674,0.3099267399,0.3058608059,0.3017948718,0.2977289377,0.2936630037,0.2895970696,0.2855311355,0.2814652015,0.2773992674,0.2733333333,0.275970696,0.2786080586,0.2812454212,0.2838827839,0.2865201465,0.2891575092,0.2917948718,0.2944322344,0.2970695971,0.2997069597,0.3064468864,0.3136996337,0.320952381,0.3282051282,0.3354578755,0.3427106227,0.34996337,0.3572161172,0.3644688645,0.3717216117,0.3790598291,0.3864224664,0.3937851038,0.4011477411,0.4085103785,0.4158730159,0.4232356532,0.4305982906,0.437960928,0.4453235653,0.4537118437,0.4626129426,0.4715140415,0.4804151404,0.4893162393,0.4982173382,0.5071184371,0.516019536,0.5249206349,0.5338217338,0.5407081807,0.545982906,0.5512576313,0.5565323565,0.5618070818,0.5670818071,0.5723565324,0.5776312576,0.5829059829,0.5881807082,0.5947252747,0.6028571429,0.610989011,0.6191208791,0.6272527473,0.6353846154,0.6435164835,0.6516483516,0.6597802198,0.6679120879,0.6750915751,0.6803663004,0.6856410256,0.6909157509,0.6961904762,0.7014652015,0.7067399267,0.712014652,0.7172893773,0.7225641026,0.7274725275,0.7310989011,0.7347252747,0.7383516484,0.741978022,0.7456043956,0.7492307692,0.7528571429,0.7564835165,0.7601098901,0.7635286935,0.7652869353,0.767045177,0.7688034188,0.7705616606,0.7723199023,0.7740781441,0.7758363858,0.7775946276,0.7793528694,0.7811111111,0.7813308913,0.7815506716,0.7817704518,0.781990232,0.7822100122,0.7824297924,0.7826495726,0.7828693529,0.7830891331,0.7833089133,0.7827472527,0.7820879121,0.7814285714,0.7807692308,0.7801098901,0.7794505495,0.7787912088,0.7781318681,0.7774725275,0.7768131868,0.7738461538,0.7702197802,0.7665934066,0.762967033,0.7593406593,0.7557142857,0.7520879121,0.7484615385,0.7448351648,0.7412087912,0.7326007326,0.7215018315,0.7104029304,0.6993040293,0.6882051282,0.6771062271,0.666007326,0.6549084249,0.6438095238,0.6327106227,0.6201465201,0.6064102564,0.5926739927,0.5789377289,0.5652014652,0.5514652015,0.5377289377,0.523992674,0.5102564103,0.4965201465,0.4827350427,0.4688888889,0.455042735,0.4411965812,0.4273504274,0.4135042735,0.3996581197,0.3858119658,0.371965812,0.3581196581,0.3465079365,0.3393650794,0.3322222222,0.3250793651,0.3179365079,0.3107936508,0.3036507937,0.2965079365,0.2893650794,0.2822222222,0.2758852259,0.2723687424,0.2688522589,0.2653357753,0.2618192918,0.2583028083,0.2547863248,0.2512698413,0.2477533578,0.2442368742,0.2409157509,0.2391575092,0.2373992674,0.2356410256,0.2338827839,0.2321245421,0.2303663004,0.2286080586,0.2268498168,0.2250915751,0.2233333333
]
 
# Define event callbacks
'''def on_publish(client, obj, mid):
    print("mid: " + str(mid))
   
def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))'''
def start():
    global start_crop
    start_crop=1
def calc_date(date):
    if date<30:
        return 0;
    elif date<80:
        return 1;
    elif date<135:
        return 2;
    else:
        return 3;
   
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/humidity")
    client.subscribe("/temp")
    client.subscribe("crop")
    client.subscribe("devId")
    client.subscribe("date")
 
def on_message(client, obj, msg):
    global humidity,temp,crop,start_date,devId
    #print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    if msg.topic == "/humidity":
        humidity=msg.payload
    if msg.topic == "/temp":
        temp=msg.payload
    if msg.topic == "crop":
        crop=msg.payload
    if msg.topic == "date":
        start_date=msg.payload
    if msg.topic == "devId":
        devId=msg.payload
        print(devId)
        start();
 
area=100
url = "https://irrisat-cloud.appspot.com/_ah/api/irrisat/v1/services/forecast/evapotranspiration/30.733315/76.779418"
result = (urllib.urlopen(url).read())
#print result
ans = json.loads(result)
#print ans
kc = {'cotton': (0.45, 0.75,1.15,0.75,0.82), 'maize': (0.40,0.80,1.15,0.70,0.82)}
date = ans['Daily']
mqttc = mqtt.Client()
# Assign event callbacks
#mqttc.on_publish = on_publish
total_water_volume=0
mqttc.on_message = on_message
mqttc.on_connect = on_connect    
mqttc.username_pw_set("dfxukbgb", "lq_IHyYetOBV")
mqttc.connect("m20.cloudmqtt.com", 14917)
curr_date=0;
while(start_crop==0):  
    mqttc.loop()
print "done"
 
while curr_date<180:
    ts3=time.time()
    if ts3-ts2>10:
        index=calc_date(curr_date)
        for i in date:
            present = i['ET0']
            break;
        water_level = kc[crop][index]*present
        water_volume=water_level*area
        IO.output(19,IO.HIGH)
        time.sleep(1.5)
        IO.output(19,IO.LOW)
        ts1=time.time()
       
        if ts1-ts>20:
            url1 = "https://irrisat-cloud.appspot.com/_ah/api/irrisat/v1/services/data/cropgrowth"
            post_fields = {'Start': "2014-01-01T00:00:00",'End': "2014-01-07T00:00:00",'ManagementUnit': {'Geometry':"POLYGON((72.603699 23.431291,72.603980 23.431271,72.603980  23.431271,72.604029 23.431386,72.603718 23.431366))" }}
            r1 = requests.post(url1, json=post_fields).json()
            payload={'temp':temp,'humidity':humidity,'total_water_vol':total_water_volume,'curr_date':curr_date,'ndvi_ideal':ndvi[curr_date],'ndvi_actual':r1['Series']['NDVI'][1],'curr_date_water':water_volume}
            url='http://agriculture12.herokuapp.com/home/resp/'
            print "Humidity: ",humidity
            print "Temperature: ",temp
            print "Current Date: ",curr_date
            print "Ndvi_ideal: ",ndvi[curr_date]
            print "Ndvi_actual: ",r1['Series']['NDVI'][1]
            r=requests.post(url,json.dumps(payload))
            print r
            ts=ts1
        mqttc.publish("/water_level", water_volume)
        total_water_volume+=water_volume
        curr_date=curr_date+1
        ts2=ts3
    mqttc.loop()
   
while(1):
    mqttc.loop()
