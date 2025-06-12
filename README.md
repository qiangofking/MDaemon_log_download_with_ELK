# MDaemon_log_download_with_ELK(用ELK比划MD日志)
### Describe（嘀咕）
- Through the MDaemon email server API(API Version: 25.0.2), log downloads are implemented and linked to ELK visualization display
- 通过MDaemon邮件服务器API(API Version: 25.0.2)，实现日志下载，联动ELK可视化展示

### Overview（瞅瞅）

![image](https://github.com/user-attachments/assets/3f6fb2e5-0a3b-4583-94f1-d8971c5c2a7a)
![image](https://github.com/user-attachments/assets/7afd2986-4c8c-47a2-8b30-60fbe61dd90e)


### framework（套路）
![image](https://github.com/user-attachments/assets/bbd1d942-779e-4218-bc30-291739ce0a7e)
![image](https://github.com/user-attachments/assets/77a9f8d4-cd2f-4dd2-83e7-a841aa0fd2c2)


### How to use
1. Configure config/config.ini
2. Ensure that the two XML format contents under config are compatible with the currently used MD API interface (e.g. API Version: 25.0.2)
3. Test 4 core modules, file_2json, file_unzip, fileManager in the 'util' folder, as well as the main.py in root path
4. At this point, the deployment of the logdownload section is complete
5. Next, configure ELK (ElasticSearch/Logstash/Kibana), refer to:https://blog.csdn.net/fu_sheng_q/article/details/135215027
6. Key step: Configure the logstash configuration file to enable it to parse the JSON fields of the downloaded logs and formatted them properly. Please refer to the example template for reference
7. After completing everything, you will receive an MD+log_rownload+ELK; Have fun!

### 咋使唤
1. 配置config/config.ini
2. 确保config下的2个xml格式内容与当前使用的MD API接口兼容（例如：API Version: 25.0.2）
3. 测试4个核心模块，“util”文件夹下的file_2json、file_unzip、fileManager，以及根路径的main.py
4. 至此logdownload部分部署完毕
5. 接着配置ELK（ElasticSearch/Logstash/Kibana），参考：https://blog.csdn.net/fu_sheng_q/article/details/135215027
6. 关键步骤：配置logstash的配置文件，使其能够正常解析我们下载日志并格式化后的json的字段，可参考示例模板
7. 都完成后，你会得到一个MD+log_download+ELK

### Tips
1. I just downed a "routing.log", and others followed the same routine; 
2. Alarm? None; There can also be;
3. Disposal? None; There can also be;
4. Equipment linkage? None; There can also be;

### 小声嘀咕
1. 我就载了个routing.log，其他的也这套路；
2. 告警？没有；也可以有;
3. 处置？没有；也可以有;
4. 设备联动？没有；也可以有;
