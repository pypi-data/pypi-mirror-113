import os


class WSTypeQualificationException(Exception):
    pass


class ObjectType:
    rectangle = "rectangle"
    polygon = "polygon"


class Point:
    def __init__(self, x: str = None, y: str = None, z: str = None, additional_data: str = None):
        self.x = x
        self.y = y
        self.z = z
        self.additional_data = additional_data


class PointList(list):
    def append(self, temp_object):
        if type(temp_object) is not Point:
            raise WSTypeQualificationException("The type must be Point.")
        super().append(temp_object)


class InferenceResult:
    def __init__(self, id: str, name: str, picture_address: str, point_list: PointList, confidence: str,
                 object_type: ObjectType):
        self.id = id
        self.name = name
        self.picture_address = picture_address
        self.point_list = point_list
        self.confidence = confidence
        self.object_type = object_type


class InferenceResultList(list):
    def append(self, temp_object):
        if type(temp_object) is not InferenceResult:
            raise WSTypeQualificationException("The type must be InferenceResult.")
        super().append(temp_object)


# class PictureAddressList(list):
#     def append(self, temp_object):
#         if type(temp_object) is not str:
#             raise WSTypeQualificationException("The type must be str.")
#         super().append(temp_object)


class MessageData:
    def __init__(self, device_id: str, stream_address: str, video_address: str,
                 inference_result_list: InferenceResultList):
        self.device_id = device_id
        self.stream_address = stream_address
        self.video_address = video_address
        self.inference_result_list = inference_result_list


class MessageType:
    wellsucurity = "wellsucurity"
    unknown = "unknown"
    testing = "testing"


class MessageProducerState:
    def __init__(self, start=True, intermediate=False, end=False, id: str = None, signature: str = None):
        self.start = start
        self.intermediate = intermediate
        self.end = end
        self.id = id
        self.signature = signature


class MessageConsumerState:
    def __init__(self, start=True, intermediate=False, end=False, id: str = None, signature: str = None):
        self.start = start
        self.intermediate = intermediate
        self.end = end
        self.id = id
        self.signature = signature


class MessageConsumerStateList(list):
    def append(self, temp_object):
        if type(temp_object) is not MessageConsumerState:
            raise WSTypeQualificationException("The type must be MessageConsumerState.")
        super().append(temp_object)


class Message:
    def __init__(self, message_id: str = None, start_timestamp: str = None, end_timestamp: str = None,
                 message_producer_state: MessageProducerState = None,
                 message_consumer_state_list: MessageConsumerStateList = None,
                 message_type: str = None,
                 message_data: MessageData = None, additional_data: dict = None):
        self.message_id = message_id
        self.start_timestamp = start_timestamp
        self.end_timestamp = end_timestamp
        self.message_producer_state = message_producer_state
        self.message_consumer_state_list = message_consumer_state_list
        self.message_type = message_type
        self.message_data = message_data
        self.additional_data = additional_data

    # def __repr__(self):
    #     return repr((self.message_id, self.start_timestamp, self.end_timestamp))


class DeviceAndMessage:
    def __init__(self, device_id: str = "", message: Message = None):
        self.device_id = device_id
        self.message = message


class DeviceAndMessageList(list):
    def append(self, temp_object):
        if type(temp_object) is not DeviceAndMessage:
            raise WSTypeQualificationException("The type must be DeviceAndMessage.")
        super().append(temp_object)


class WSJsonUtils():
    def __init__(self):
        self.jresult = ""

    def loopKV(self, x):
        print(x)
        print(isinstance(x, list))
        print(type(x))
        if isinstance(x, list):

            self.jresult += '"' + str(x.__class__.__name__) + '"' + ":"
            self.jresult += '['
            for k2 in x:
                self.jresult += '{'
                self.loopKV(k2)
                self.jresult += '}' + ","
            self.jresult += ']' + ","
        elif hasattr(x, "__dict__"):
            print('if hasattr(x, "__dict__")>>>')
            print(x.__dict__)
            bala = x.__dict__
            print(bala)
            print(bala)
            print(x.__dict__)
            for temp in x.__dict__:
                print(temp)
                print(type(temp))
                k1 = x.__getattribute__(temp)
                if isinstance(k1, int) or isinstance(k1, float) or isinstance(k1, str) or isinstance(k1,
                                                                                                     bool) or k1 is None:
                    print(k1)
                    # print(str(temp) + "______" + str(k1) + "______" + str(type(k1)))
                    self.jresult += '"' + str(temp) + '"' + ":" + '"' + str(k1) + '"' + ","
                    pass
                elif isinstance(k1, list):
                    self.jresult += '"' + str(temp) + '"' + ":" + '['
                    for k2 in k1:
                        self.jresult += '{'
                        self.loopKV(k2)
                        self.jresult += '}' + ","
                    self.jresult += ']' + ","
                elif isinstance(k1, set):
                    # print(k1)
                    pass
                elif isinstance(k1, dict):
                    # print(k1)
                    pass
                else:
                    self.jresult += '"' + str(temp) + '"' + ":" + '{'
                    self.loopKV(k1)
                    self.jresult += '}' + ","
        else:
            print('else:')
            # print(x)
            # print(x)
            # print(str(temp) + "______" + str(k1) + "______" + str(type(k1)))
            self.jresult += '"' + str(x) + '"' + ":" + '"' + str(x) + '"' + ","
            pass

    def transfer2json(self, content):
        self.loopKV(content)
        result = "{" + self.jresult + "}"
        import re
        result = re.compile(",}").sub("}", result)
        result = re.compile(",]").sub("]", result)
        return result


"""
v
"""
if __name__ == '__main__':
    path = "/home/wwl/mypython/myworkspace/vialearning/pytorch.demo01-master/vpt"
    import os

    for root, dirs, names in os.walk(path):
        for filename in names:
            #print(root)
            # print(filename)
            tempPath = os.path.join(root,filename)
            print(tempPath)
            print(os.path.exists(tempPath))

if __name__ == '__main2__':
    pointList = PointList(list())
    pointList.append(Point(100, 111))
    pointList.append(Point(200, 211))

    inferenceResult1 = InferenceResult(id="1000001", name="no_vest",
                                       picture_address="http://westwell-lab.com:9090/aaa.jpg", point_list=pointList,
                                       confidence="0.99",
                                       object_type=ObjectType.rectangle)
    inferenceResult2 = InferenceResult(id="1000002", name="no_helmet",
                                       picture_address="http://westwell-lab.com:9090/bbb.jpg", point_list=pointList,
                                       confidence="0.61",
                                       object_type=ObjectType.rectangle)
    inferenceResult3 = InferenceResult(id="1000003", name="pedestrian",
                                       picture_address="http://westwell-lab.com:9090/ccc.jpg", point_list=pointList,
                                       confidence="0.47",
                                       object_type=ObjectType.rectangle)

    inferenceResultList = InferenceResultList(list())
    inferenceResultList.append(inferenceResult1)
    inferenceResultList.append(inferenceResult2)
    inferenceResultList.append(inferenceResult3)

    messageData = MessageData(device_id="camera1", stream_address="rtsp://192.168.110.66",
                              video_address="http://10.66.9.90/via.mp4", inference_result_list=inferenceResultList)

    messageProducerState = MessageProducerState(start=True, intermediate=True, end=False, id="1001000000",
                                                signature="jintaoli")

    messageConsumerState1 = MessageConsumerState(start=True, intermediate=True, end=False, id="2001",
                                                 signature="jianglinzhang")
    messageConsumerState2 = MessageConsumerState(start=True, intermediate=True, end=False, id="2002",
                                                 signature="zhengyu")
    messageConsumerState3 = MessageConsumerState(start=True, intermediate=True, end=False, id="2003",
                                                 signature="jingxianyun")
    messageConsumerStateList = MessageConsumerStateList()
    messageConsumerStateList.append(messageConsumerState1)
    messageConsumerStateList.append(messageConsumerState2)
    messageConsumerStateList.append(messageConsumerState3)

    message = Message(message_id="9854215645555", start_timestamp="123504578", end_timestamp=None,
                      message_producer_state=messageProducerState, message_consumer_state_list=messageConsumerStateList,
                      message_type=MessageType.testing, message_data=messageData,
                      additional_data={"via": "yie", "fly": "fly"})

    deviceAndMessage1 = DeviceAndMessage("camera192.168.110.201", message)
    deviceAndMessage2 = DeviceAndMessage("camera192.168.110.203", message)

    device_and_message_list = DeviceAndMessageList()
    device_and_message_list.append(deviceAndMessage1)
    device_and_message_list.append(deviceAndMessage2)

    wSJsonUtils = WSJsonUtils()
    temp_json = wSJsonUtils.transfer2json(device_and_message_list)
    print(temp_json)
    import json

    json_loads = json.loads(temp_json)
    print(json_loads)
