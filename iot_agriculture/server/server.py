from iot_agriculture import TcpServer, Header, Responce, SensorData, Config
from iot_agriculture.server import DbConnection, TelegramBot
import logging
from datetime import datetime, timedelta
from twisted.internet import task
from telegram import ParseMode
import os
import yaml

logger = logging.getLogger("Server")


class Server(object):
    def __init__(self, config, *args, **kwargs):
        self.config: Config = config
        self.server = TcpServer(self.config.get("host"),
                                self.config.get("port"),
                                callbacks={"on_connect": self.on_connect,
                                           "on_data": self.on_data,
                                           "on_disconnect": self.on_disconnect})

        self.db = DbConnection(self.config.get("db"))
        self.chat_ids = {'ids': self.config.get("ids")}
        self.heart_beat_time = None
        self.db_data = []
        self.heart_beat_task = task.LoopingCall(self.heart_beat)
        self.heart_beat_interval = int(self.config.get("heart_beat"))
        self.bot = TelegramBot(self.config.get("token"))
        self.set_commands()
        self.count = 0

    def set_commands(self):
        self.bot.add_command([("help", "help function"), ("start", "Start function"),
                              ("status", "Get the realtime sensor value")])

        self.bot.set_command("help", self.bot_help)
        self.bot.set_command("start", self.bot_start)
        self.bot.set_command("status", self.bot_status)

    def bot_help(self, update, context):
        self.chat_ids['ids'].add(update.message.chat.id)

        text = "<b>Help Command</b>           \n\n" \
               "/help: help function            \n" \
               "/start: Start the bot           \n" \
               "/status: Real time sensor value \n"

        context.bot.send_message(
            chat_id=update.message.chat.id,
            text=text,
            parse_mode=ParseMode.HTML)

    def bot_start(self, update, context):
        self.chat_ids['ids'].add(update.message.chat.id)
        text = "<b>Iot based Agriculture</b>"
        context.bot.send_message(
            chat_id=update.message.chat.id,
            text=text,
            parse_mode=ParseMode.HTML)

    def write_yml(self):
        file = open(os.path.join(self.config.base_dir, 'chat_id.yml'), "w+")
        yaml.dump(self.chat_ids, file)
        file.close()

    def bot_status(self, update, context):
        self.chat_ids['ids'].add(update.message.chat.id)

        queue = "SELECT * FROM public.sensor_data order by time DESC limit 1;"

        status = self.db.commit_query(queue)
        if status:
            data = self.db.cursor.fetchall()
            data = SensorData(*data[0])
            text = f"<b>Plant status</b>\n\n" \
                   f"Client id: {data.client_id} \n" \
                   f"Light condition: {data.light}\n" \
                   f"Water: {data.water}\n" \
                   f"temperature: {data.temperature}\n" \
                   f"Humidity: {data.humidity}\n" \
                   f"Last water supplied time: {data.last_water}\n"
        else:
            text = "Some thing went wrong in server"

        context.bot.send_message(
            chat_id=update.message.chat.id,
            text=text,
            parse_mode=ParseMode.HTML)

    def on_connect(self, connection):
        logger.info(f"Connection to raspberrypi")
        self.heart_beat_time = datetime.now()

    def on_data(self, connection, data):
        header = Header.de_json(data)
        data = header.payload

        # handle sensor data
        if header.payload_type == "SensorData":
            resp = Responce(header.uuid)
            resp_header = Header("Responce", resp)
            connection.send_data(resp_header.to_json())
            self.insert_to_db(data)
            if len(self.db_data) > 5:
                remove = []
                for query in self.db_data:
                    status = self.db.commit_query(query)
                    if status:
                        remove.append(query)
                for q in remove:
                    self.db_data.remove(q)

        # handle heartbeat
        elif header.payload_type == "HeartBeat":
            self.heart_beat_time = datetime.now()
            self.count = 0

        # handle logout request
        elif header.payload_type == "Logout":
            self.heart_beat_time = None
            text = "<b>Raspberry pi send logout request</b>\n" \
                   "All the process will we shutting down"
            for ids in self.chat_ids['ids']:
                self.bot.bot.send_message(chat_id=ids,
                                          text=text,
                                          parse_mode=ParseMode.HTML)

    def on_disconnect(self, connection, reason):
        logger.info("Client disconnected")
        logger.info(reason)
        self.heart_beat_time = None
        self.count = 0

    def heart_beat(self):
        now = datetime.now()
        if self.heart_beat_time:
            interval = now - self.heart_beat_time
            if interval > timedelta(seconds=self.heart_beat_interval):
                text = f"<b>Alert !!</b> \n\n" \
                       f"Raspberry pi did not send heart beat for {interval}"
                logger.info(f"Raspberry pi did not send heart beat for {interval}")
                for ids in self.chat_ids['ids']:
                    self.bot.bot.send_message(chat_id=ids,
                                              text=text,
                                              parse_mode=ParseMode.HTML)

                if self.count > 15:
                    self.heart_beat_time = None
                self.count += 1

    def start(self):
        logger.info("Connect to db")
        self.db.connect()
        logger.info("start telegram bot")
        self.bot.clean_updates()
        self.bot.start_polling()
        logger.info("server started")
        self.server.start()
        self.heart_beat_task.start(self.heart_beat_interval)

    def stop(self):
        self.write_yml()
        logger.info("stopping telegram bot")
        self.bot.stop_polling()
        logger.info("server stopped")
        self.heart_beat_task.stop()
        logger.info("+++++++++++++++++++++++++++++++IOT-Agriculture+++++++++++++++++++++++++++++++\n")
        self.server.stop()

    def insert_to_db(self, data):
        status = self.db.commit_query(data.to_db())
        if not status:
            self.db_data.append(data.to_db())
