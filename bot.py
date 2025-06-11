import asyncio
import dotenv
from groqhelper import get_kanji_info
import stateload
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import InputFile
from telegram.ext import ApplicationBuilder
from healthcheck import keep_alive

keep_alive()  # Start the health check server
# Load environment variables

TELEGRAM_BOT_TOKEN = dotenv.get_key(".env", "BOT_TOKEN")
TELEGRAM_CHAT_ID = dotenv.get_key(".env", "TELEGRAM_ID")

kanji_groups = [
    ['言', '手', '自', '者', '事', '思', '会', '家', '的', '方', '地', '目', '場', '代', '私', '立', '物', '田', '体', '動'],
    ['社', '知', '理', '同', '心', '発', '作', '新', '世', '度', '明', '力', '意', '用', '主', '通', '文', '屋', '業', '持'],
    ['道', '身', '不', '口', '多', '野', '考', '開', '教', '近', '以', '問', '正', '真', '味', '界', '無', '少', '海', '切'],
    ['重', '集', '員', '公', '画', '死', '安', '親', '強', '使', '朝', '題', '仕', '京', '足', '品', '着', '別', '音', '元'],
    ['特', '風', '夜', '空', '有', '起', '運', '料', '楽', '色', '帰', '歩', '悪', '広', '店', '町', '住', '売', '待', '古'],
    ['始', '終', '計', '院', '送', '族', '映', '買', '病', '早', '質', '台', '室', '可', '建', '転', '医', '止', '字', '工'],
    ['急', '図', '黒', '花', '英', '走', '青', '答', '紙', '歌', '注', '赤', '春', '館', '旅', '験', '写', '去', '研', '飲'],
    ['肉', '服', '銀', '茶', '究', '洋', '兄', '秋', '堂', '週', '習', '試', '夏', '弟', '鳥', '犬', '夕', '魚', '借', '飯'],
    ['駅', '昼', '冬', '姉', '曜', '漢', '牛', '妹', '貸', '勉', '合', '部', '彼', '内', '実', '当', '戦', '性', '対', '関'],
    ['感', '定', '政', '取', '所', '現', '最', '化', '民', '相', '法', '全', '情', '向', '平', '成', '経', '信', '面', '連'],
    ['原', '顔', '機', '次', '数', '美', '回', '表', '声', '報', '要', '変', '神', '記', '和', '引', '治', '決', '太', '込'],
    ['受', '解', '市', '期', '様', '活', '頭', '組', '指', '説', '能', '葉', '流', '然', '初', '在', '調', '笑', '議', '直'],
    ['夫', '選', '権', '利', '制', '続', '石', '進', '伝', '加', '助', '点', '産', '務', '件', '命', '番', '落', '付', '得'],
    ['好', '違', '殺', '置', '返', '論', '際', '歳', '反', '形', '光', '首', '勝', '必', '係', '由', '愛', '都', '放', '確'],
    ['過', '約', '馬', '状', '想', '官', '交', '米', '配', '若', '資', '常', '果', '呼', '共', '残', '判', '役', '他', '術'],
    ['支', '両', '乗', '済', '供', '格', '打', '御', '断', '式', '師', '告', '深', '存', '争', '覚', '側', '飛', '参', '突'],
    ['容', '育', '構', '認', '位', '達', '守', '満', '消', '任', '居', '予', '路', '座', '客', '船', '追', '背', '観', '誰'],
    ['息', '失', '老', '良', '示', '号', '職', '王', '識', '警', '優', '投', '局', '難', '種', '念', '寄', '商', '害', '頼'],
    ['横', '増', '差', '苦', '収', '段', '俺', '渡', '与', '演', '備', '申', '例', '働', '景', '抜', '遠', '絶', '負', '福'],
    ['球', '酒', '君', '察', '望', '婚', '単', '押', '割', '限', '戻', '科', '求', '談', '降', '妻', '岡', '熱', '浮', '等'],
    ['末', '幸', '草', '越', '登', '類', '未', '規', '精', '抱', '労', '処', '退', '費', '非', '喜', '娘', '逃', '探', '犯'],
    ['薬', '園', '疑', '緒', '静', '具', '席', '速', '舞', '宿', '程', '倒', '寝', '宅', '絵', '破', '庭', '婦', '余', '訪'],
    ['冷', '暮', '腹', '危', '許', '似', '険', '財', '遊', '雑', '恐', '値', '暗', '積', '夢', '痛', '富', '刻', '鳴', '欲'],
    ['途', '曲', '耳', '完', '願', '罪', '陽', '亡', '散', '掛', '昨', '怒', '留', '礼', '列', '雪', '払', '給', '敗', '捕'],
    ['忘', '晴', '因', '折', '迎', '悲', '港', '責', '除', '困', '閉', '吸', '髪', '束', '眠', '易', '窓', '祖', '勤', '昔'],
    ['便', '適', '吹', '候', '怖', '辞', '否', '遅', '煙', '徒', '欠', '迷', '洗', '互', '才', '更', '歯', '盗', '慣', '晩'],
    ['箱', '到', '頂', '杯', '皆', '招', '寒', '恥', '疲', '貧', '猫', '誤', '努', '幾', '賛', '偶', '忙', '泳', '靴', '偉']
]

async def send_telegram_message(application):
    # Load the current kanji group index
    kanji_20 = kanji_groups[stateload.load_state()]

    # Get formatted kanji info (adjust your `get_kanji_info` function accordingly)
    table_md = await get_kanji_info(kanji_20)

    # Send the message using Telegram bot
    await application.bot.send_message(
        chat_id=TELEGRAM_CHAT_ID,
        text="Here is your daily kanji info!\n\n" + table_md,
        parse_mode='Markdown'
    )

    stateload.save_state(stateload.load_state() + 1)

async def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_telegram_message, trigger="cron", hour=17, minute=49, args=[application])
    scheduler.start()

    print("Scheduler started. Waiting for jobs...")

    await application.initialize()
    await application.start()
    try:
        while True:
            await asyncio.sleep(3600)
    finally:
        await application.stop()
        await application.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
