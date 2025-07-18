# MDaemon_log_download_with_ELK(用ELK比划MD日志)
### Describe
- Through the MDaemon email server API(API Version: 25.0.2), log downloads are implemented and linked to ELK visualization display
- 通过MDaemon邮件服务器API(API Version: 25.0.2)，实现日志下载，联动ELK可视化展示

### Overview

![image](https://github.com/user-attachments/assets/3f6fb2e5-0a3b-4583-94f1-d8971c5c2a7a)
![image](https://github.com/user-attachments/assets/7afd2986-4c8c-47a2-8b30-60fbe61dd90e)


### framework
![image](https://github.com/user-attachments/assets/bbd1d942-779e-4218-bc30-291739ce0a7e)
![image](https://github.com/user-attachments/assets/77a9f8d4-cd2f-4dd2-83e7-a841aa0fd2c2)


### How to use
1. Configure config/config.ini
2. Ensure that the two XML format contents under config are compatible with the currently used MD API interface (e.g. API Version: 25.0.2)
3. Test 4 core modules, file_2json, file_unzip, fileManager in the 'util' folder, as well as the main.py in root path
4. Most of the libraries used are basic Python libraries. If there are any missing ones, please install them using methods such as "pip install"
5. At this point, the deployment of the logdownload section is complete(By default, it is downloaded every 5 minutes. To do so, it should be placed on line 90 of main. py, in seconds)
6. Next, configure ELK (ElasticSearch/Logstash/Kibana), refer to:https://blog.csdn.net/fu_sheng_q/article/details/135215027
7. Key step: (The monitoring path of the log, line 3; ES address, line 41)Configure the logstash configuration file to enable it to parse the JSON fields of the downloaded logs and formatted them properly. Please refer to the example template for reference
8. After completing everything, you will receive an MD+log_rownload+ELK; Have fun!

### 咋使唤
1. 配置config/config.ini
2. 确保config下的2个xml格式内容与当前使用的MD API接口兼容（例如：API Version: 25.0.2）
3. 测试4个核心模块，“util”文件夹下的file_2json、file_unzip、fileManager，以及根路径的main.py
4. 用的大多是基础python库，如有缺失，自个pip install等安装下
5. 至此logdownload部分部署完毕（默认每5分钟下载一次，要改在main.py的90行，单位为秒）
6. 接着配置ELK（ElasticSearch/Logstash/Kibana），参考：https://blog.csdn.net/fu_sheng_q/article/details/135215027
7. 关键步骤：配置logstash的配置文件（日志的监测路径，第3行；ES的地址，第41行），使其能够正常解析我们下载日志并格式化后的json的字段，可参考示例模板
8. 都完成后，你会得到一个MD+log_download+ELK

### Tips
1. I just downed a "routing.log", and others followed the same routine; 
2. Alarm? None; There can also be;
3. Disposal? None; There can also be;
4. Equipment linkage? None; There can also be;

### Partial Detail Display
```
# 核心功能验证：下载密文routing日志（返当日日志文件id号，下载结果）
python util\fileManager.py
```
![image](https://github.com/user-attachments/assets/40666f52-f06a-45b3-ba9d-013c6dddae0e)


```
# 核心功能验证：密文routing日志转明文
python util\file_2json.py
```
![image](https://github.com/user-attachments/assets/a77072cb-afee-4d21-bf18-428d15e50050)

```
# 核心功能验证：明文routing日志转json
python util\file_2json.py
```
![image](https://github.com/user-attachments/assets/d3d217af-e671-4697-a477-bcf18ca7d614)

```
# 核心功能验证：整体调用
python main.py
```
![image](https://github.com/user-attachments/assets/03a73309-cc34-464b-b5db-29feb190af05)

